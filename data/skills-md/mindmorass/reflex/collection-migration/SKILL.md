---
name: collection-migration
description: Migrate and sync vector database collections across environments
---


# Collection Migration Skill

> Safely move, rename, merge, and manage RAG collections.

## Overview

As projects evolve, you may need to:
- Rename collections (project renamed)
- Merge collections (consolidating knowledge)
- Split collections (grew too large)
- Archive collections (project ended)
- Clone collections (forking a project)

This skill provides safe procedures for each operation.

## Prerequisites

```bash
pip install qdrant-client
```

## Safety Principles

1. **Always backup first** - Export before any destructive operation
2. **Verify after migration** - Run validation checks
3. **Preserve metadata** - Don't lose document provenance
4. **Atomic operations** - Complete fully or rollback


## Operation 1: Export Collection

**Use case**: Backup or transfer to another environment

```python
#!/usr/bin/env python3
"""Export a collection to JSON."""

import json
from datetime import datetime
from qdrant_client import QdrantClient

def export_collection(
    collection_name: str,
    output_path: str = None,
    qdrant_url: str = "http://localhost:6333"
) -> str:
    """
    Export collection to JSON file.

    Args:
        collection_name: Name of collection to export
        output_path: Output file path (default: {collection}_{timestamp}.json)
        qdrant_url: Qdrant server URL

    Returns:
        Path to exported file
    """
    client = QdrantClient(url=qdrant_url)

    # Get all points
    results = client.scroll(
        collection_name=collection_name,
        limit=100000,
        with_payload=True,
        with_vectors=True
    )

    points = results[0]

    # Build export data
    export_data = {
        "collection_name": collection_name,
        "exported_at": datetime.now().isoformat(),
        "document_count": len(points),
        "documents": [
            {
                "id": str(p.id),
                "content": p.payload.get("content", ""),
                "metadata": {k: v for k, v in p.payload.items() if k != "content"},
                "vector": p.vector
            }
            for p in points
        ]
    }

    # Write to file
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{collection_name}_{timestamp}.json"

    with open(output_path, "w") as f:
        json.dump(export_data, f, indent=2)

    print(f"✅ Exported {len(points)} documents to {output_path}")
    return output_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python export_collection.py <collection_name> [output_path]")
        sys.exit(1)

    collection = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    export_collection(collection, output)
```


## Operation 2: Import Collection

**Use case**: Restore from backup or import shared collection

```python
#!/usr/bin/env python3
"""Import a collection from JSON export."""

import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

def import_collection(
    input_path: str,
    new_name: str = None,
    qdrant_url: str = "http://localhost:6333",
    skip_vectors: bool = False
) -> str:
    """
    Import collection from JSON file.

    Args:
        input_path: Path to exported JSON file
        new_name: New collection name (default: use original name)
        qdrant_url: Qdrant server URL
        skip_vectors: If True, regenerate embeddings instead of using exported ones

    Returns:
        Name of imported collection
    """
    with open(input_path) as f:
        data = json.load(f)

    collection_name = new_name or data["collection_name"]
    client = QdrantClient(url=qdrant_url)

    # Check if collection exists
    existing = [c.name for c in client.get_collections().collections]
    if collection_name in existing:
        raise ValueError(f"Collection '{collection_name}' already exists. Use different name or delete first.")

    # Determine vector size from first document
    if data["documents"] and data["documents"][0].get("vector"):
        vector_size = len(data["documents"][0]["vector"])
    else:
        vector_size = 384  # Default for all-MiniLM-L6-v2

    # Create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

    # Prepare points
    points = []
    for doc in data["documents"]:
        if skip_vectors or not doc.get("vector"):
            continue  # Would need to regenerate embeddings

        payload = doc["metadata"] or {}
        payload["content"] = doc["content"]
        payload["imported_from"] = data["collection_name"]
        payload["imported_at"] = data["exported_at"]

        points.append(PointStruct(
            id=hash(doc["id"]) % (2**63),
            vector=doc["vector"],
            payload=payload
        ))

    # Batch insert
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(collection_name=collection_name, points=batch)

    print(f"✅ Imported {len(points)} documents into '{collection_name}'")
    return collection_name


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python import_collection.py <input_path> [new_name]")
        sys.exit(1)

    input_path = sys.argv[1]
    new_name = sys.argv[2] if len(sys.argv) > 2 else None
    import_collection(input_path, new_name)
```


## Operation 3: Rename Collection

**Use case**: Project renamed, need to update collection name

```python
def rename_collection(
    old_name: str,
    new_name: str,
    qdrant_url: str = "http://localhost:6333"
):
    """
    Rename a collection (export + import + delete).
    """
    # Export first (backup)
    export_path = export_collection(old_name, qdrant_url=qdrant_url)

    # Import with new name
    import_collection(export_path, new_name=new_name, qdrant_url=qdrant_url)

    # Delete old collection
    client = QdrantClient(url=qdrant_url)
    client.delete_collection(old_name)

    print(f"✅ Renamed '{old_name}' to '{new_name}'")
```


## Operation 4: Merge Collections

**Use case**: Consolidating multiple projects, combining research

```python
def merge_collections(
    source_collections: list,
    target_collection: str,
    qdrant_url: str = "http://localhost:6333",
    deduplicate: bool = True
):
    """
    Merge multiple collections into one.

    Args:
        source_collections: List of collection names to merge
        target_collection: Name for merged collection
        deduplicate: If True, skip duplicate content
    """
    client = QdrantClient(url=qdrant_url)

    # Determine vector size from first source
    first_coll = client.get_collection(source_collections[0])
    vector_size = first_coll.config.params.vectors.size

    # Create or get target collection
    existing = [c.name for c in client.get_collections().collections]
    if target_collection not in existing:
        from qdrant_client.models import Distance, VectorParams
        client.create_collection(
            collection_name=target_collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    seen_hashes = set()
    total_added = 0
    total_skipped = 0

    for source_name in source_collections:
        print(f"Merging '{source_name}'...")

        results = client.scroll(
            collection_name=source_name,
            limit=100000,
            with_payload=True,
            with_vectors=True
        )

        points = results[0]

        for p in points:
            content = p.payload.get("content", "")

            # Deduplication
            if deduplicate:
                content_hash = hash(content)
                if content_hash in seen_hashes:
                    total_skipped += 1
                    continue
                seen_hashes.add(content_hash)

            # Track source in payload
            payload = p.payload.copy()
            payload["merged_from"] = source_name

            client.upsert(
                collection_name=target_collection,
                points=[PointStruct(
                    id=hash(f"{source_name}_{p.id}") % (2**63),
                    vector=p.vector,
                    payload=payload
                )]
            )
            total_added += 1

    print(f"✅ Merged {total_added} documents into '{target_collection}'")
    if deduplicate:
        print(f"   Skipped {total_skipped} duplicates")
```


## Operation 5: Archive Collection

**Use case**: Project ended, keep data but mark as inactive

```python
from pathlib import Path

def archive_collection(
    collection_name: str,
    qdrant_url: str = "http://localhost:6333"
):
    """
    Archive a collection (export + delete with marker file).
    """
    # Export
    export_path = export_collection(collection_name, qdrant_url=qdrant_url)

    # Move to archives
    archive_dir = Path("archives")
    archive_dir.mkdir(exist_ok=True)

    archive_path = archive_dir / Path(export_path).name
    Path(export_path).rename(archive_path)

    # Delete from database
    client = QdrantClient(url=qdrant_url)
    client.delete_collection(collection_name)

    # Create marker file
    from datetime import datetime
    marker_path = archive_dir / f"{collection_name}.archived"
    with open(marker_path, "w") as f:
        f.write(f"Archived: {datetime.now().isoformat()}\n")
        f.write(f"Export: {archive_path}\n")

    print(f"✅ Archived '{collection_name}' to {archive_path}")


def restore_archive(
    collection_name: str,
    qdrant_url: str = "http://localhost:6333"
):
    """Restore an archived collection."""
    archive_dir = Path("archives")

    # Find the export file
    exports = list(archive_dir.glob(f"{collection_name}_*.json"))
    if not exports:
        raise FileNotFoundError(f"No archive found for '{collection_name}'")

    # Use most recent
    export_path = sorted(exports)[-1]

    # Import
    import_collection(str(export_path), new_name=collection_name, qdrant_url=qdrant_url)

    # Remove marker
    marker = archive_dir / f"{collection_name}.archived"
    if marker.exists():
        marker.unlink()

    print(f"✅ Restored '{collection_name}' from archive")
```

## Refinement Notes

> Add notes as you use these migration tools.

- [ ] Export/import tested
- [ ] Merge with deduplication verified
- [ ] Archive/restore workflow complete
