---
name: uniprot-database
description: Query and retrieve protein sequences, annotations, and functional data from UniProt. Supports text search, ID mapping between databases, batch downloads, and access to Swiss-Prot (reviewed) and TrEMBL (predicted) entries.
---

# UniProt Database

UniProt serves as the authoritative resource for protein sequence data and functional annotations. This skill enables programmatic access to search proteins by various criteria, retrieve FASTA sequences, translate identifiers between biological databases, and query both manually curated (Swiss-Prot) and computationally predicted (TrEMBL) protein records.

## Use Cases

- Retrieve protein sequences in FASTA format for downstream analysis
- Query proteins by name, gene symbol, organism, or functional terms
- Convert identifiers between UniProt, Ensembl, RefSeq, PDB, and 100+ databases
- Access functional annotations including GO terms, domains, and pathways
- Download curated datasets for machine learning or comparative studies
- Build protein datasets filtered by organism, size, or annotation quality

## Installation

No package installation required - UniProt provides a REST API accessed via HTTP requests:

```python
import requests

# Test connectivity
resp = requests.get("https://rest.uniprot.org/uniprotkb/P53_HUMAN.json")
print(resp.json()["primaryAccession"])  # Q9NZC2 or similar
```

## Searching the Database

### Basic Text Search

Find proteins by keywords, names, or descriptions:

```python
import requests

endpoint = "https://rest.uniprot.org/uniprotkb/search"
params = {
    "query": "hemoglobin AND organism_id:9606 AND reviewed:true",
    "format": "json",
    "size": 10
}

resp = requests.get(endpoint, params=params)
results = resp.json()

for entry in results["results"]:
    acc = entry["primaryAccession"]
    name = entry["proteinDescription"]["recommendedName"]["fullName"]["value"]
    print(f"{acc}: {name}")
```

### Query Syntax

UniProt uses a powerful query language with field prefixes and boolean operators:

```
# Boolean combinations
hemoglobin AND organism_id:9606
(kinase OR phosphatase) AND reviewed:true
receptor NOT bacteria

# Field-specific queries
gene:TP53
accession:P00533
organism_name:"Homo sapiens"

# Numeric ranges
length:[100 TO 500]
mass:[20000 TO 50000]

# Wildcards
gene:IL*
protein_name:transport*

# Existence checks
cc_function:*          # has function annotation
xref:pdb               # has PDB structure
ft_signal:*            # has signal peptide
```

### Common Filters

| Filter | Description |
|--------|-------------|
| `reviewed:true` | Swiss-Prot entries only (manually curated) |
| `organism_id:9606` | Human proteins (NCBI taxonomy ID) |
| `organism_id:10090` | Mouse proteins |
| `length:[100 TO 500]` | Sequence length range |
| `xref:pdb` | Has experimental structure |
| `cc_disease:*` | Has disease association |

## Fetching Individual Entries

Access specific proteins using their accession numbers:

```python
import requests

acc = "P53_HUMAN"  # or "P04637"
url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
resp = requests.get(url)
print(resp.text)
```

### Supported Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| FASTA | `.fasta` | Sequence analysis, alignments |
| JSON | `.json` | Parsing in code |
| TSV | `.tsv` | Spreadsheets, data frames |
| XML | `.xml` | Structured data exchange |
| TXT | `.txt` | Human-readable flat file |

### Custom Fields (TSV)

Request only the fields you need to minimize bandwidth:

```python
import requests

params = {
    "query": "gene:TP53 AND reviewed:true",
    "format": "tsv",
    "fields": "accession,gene_names,organism_name,length,sequence,cc_function"
}

resp = requests.get("https://rest.uniprot.org/uniprotkb/search", params=params)
print(resp.text)
```

Common field sets:

```
# Minimal identification
accession,id,protein_name,gene_names,organism_name

# Sequence analysis
accession,sequence,length,mass,xref_pdb,xref_alphafolddb

# Functional profiling
accession,protein_name,cc_function,cc_catalytic_activity,go,cc_pathway

# Clinical applications
accession,gene_names,cc_disease,xref_omim,ft_variant
```

See `references/api-reference.md` for the complete field catalog.

## Identifier Mapping

Translate identifiers between database systems:

```python
import requests
import time

def map_identifiers(ids, source_db, target_db):
    """Map identifiers from one database to another."""
    # Submit mapping job
    submit_resp = requests.post(
        "https://rest.uniprot.org/idmapping/run",
        data={
            "from": source_db,
            "to": target_db,
            "ids": ",".join(ids)
        }
    )
    job_id = submit_resp.json()["jobId"]

    # Poll until complete
    status_url = f"https://rest.uniprot.org/idmapping/status/{job_id}"
    while True:
        status_resp = requests.get(status_url)
        status_data = status_resp.json()
        if "results" in status_data or "failedIds" in status_data:
            break
        time.sleep(2)

    # Fetch results
    results_resp = requests.get(
        f"https://rest.uniprot.org/idmapping/results/{job_id}"
    )
    return results_resp.json()

# Examples
# UniProt to PDB
mapping = map_identifiers(["P04637", "P00533"], "UniProtKB_AC-ID", "PDB")

# Gene symbols to UniProt
mapping = map_identifiers(["TP53", "EGFR"], "Gene_Name", "UniProtKB")

# UniProt to Ensembl
mapping = map_identifiers(["P00533"], "UniProtKB_AC-ID", "Ensembl")
```

### Common Database Pairs

| From | To | Use Case |
|------|-----|----------|
| `UniProtKB_AC-ID` | `PDB` | Find structures |
| `UniProtKB_AC-ID` | `Ensembl` | Link to genomics |
| `Gene_Name` | `UniProtKB` | Gene symbol lookup |
| `RefSeq_Protein` | `UniProtKB` | NCBI to UniProt |
| `UniProtKB_AC-ID` | `GO` | Get GO annotations |
| `UniProtKB_AC-ID` | `ChEMBL` | Drug target info |

See `references/api-reference.md` for all 200+ supported databases.

**Constraints:**
- Maximum 100,000 identifiers per request
- Results persist for 7 days

## Streaming Large Datasets

For complete proteomes or large result sets, use streaming to bypass pagination:

```python
import requests

params = {
    "query": "organism_id:9606 AND reviewed:true",
    "format": "fasta"
}

resp = requests.get(
    "https://rest.uniprot.org/uniprotkb/stream",
    params=params,
    stream=True
)

with open("human_proteome.fasta", "wb") as f:
    for chunk in resp.iter_content(chunk_size=8192):
        f.write(chunk)
```

## Batch Operations

### Rate-Limited Client

Respect server resources when processing many requests:

```python
import requests
import time

class UniProtClient:
    BASE = "https://rest.uniprot.org"

    def __init__(self, delay=0.5):
        self.delay = delay
        self.last_call = 0

    def _throttle(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_call = time.time()

    def get_proteins(self, accessions, batch_size=100):
        """Fetch metadata for multiple accessions."""
        results = []

        for i in range(0, len(accessions), batch_size):
            batch = accessions[i:i+batch_size]
            query = " OR ".join(f"accession:{a}" for a in batch)

            self._throttle()
            resp = requests.get(
                f"{self.BASE}/uniprotkb/search",
                params={"query": query, "format": "json", "size": batch_size}
            )

            if resp.ok:
                results.extend(resp.json().get("results", []))

        return results

# Usage
client = UniProtClient(delay=0.3)
proteins = client.get_proteins(["P04637", "P00533", "Q07817", "P38398"])
```

### Paginated Retrieval

For queries with many results:

```python
import requests

def fetch_all(query, fields=None, max_results=None):
    """Retrieve all results with automatic pagination."""
    url = "https://rest.uniprot.org/uniprotkb/search"
    collected = []

    params = {
        "query": query,
        "format": "json",
        "size": 500
    }
    if fields:
        params["fields"] = ",".join(fields)

    while url:
        resp = requests.get(url, params=params if "rest.uniprot.org" in url else None)
        data = resp.json()
        collected.extend(data["results"])

        if max_results and len(collected) >= max_results:
            return collected[:max_results]

        url = resp.links.get("next", {}).get("url")
        params = None  # Next URL contains all params

    return collected

# Example: all human phosphatases
entries = fetch_all(
    "protein_name:phosphatase AND organism_id:9606 AND reviewed:true",
    fields=["accession", "gene_names", "protein_name"]
)
```

## Working with Results

### Parse JSON Response

```python
import requests

resp = requests.get(
    "https://rest.uniprot.org/uniprotkb/search",
    params={
        "query": "gene:BRCA1 AND reviewed:true",
        "format": "json",
        "size": 1
    }
)

entry = resp.json()["results"][0]

# Extract common fields
accession = entry["primaryAccession"]
gene_name = entry["genes"][0]["geneName"]["value"]
organism = entry["organism"]["scientificName"]
sequence = entry["sequence"]["value"]
length = entry["sequence"]["length"]

# Function annotation
if "comments" in entry:
    for comment in entry["comments"]:
        if comment["commentType"] == "FUNCTION":
            print(f"Function: {comment['texts'][0]['value']}")
```

### Build a Protein Dataset

```python
import requests
import csv

def build_dataset(query, output_path, fields):
    """Export search results to CSV."""
    resp = requests.get(
        "https://rest.uniprot.org/uniprotkb/stream",
        params={
            "query": query,
            "format": "tsv",
            "fields": ",".join(fields)
        }
    )

    with open(output_path, "w") as f:
        f.write(resp.text)

# Create dataset of human kinases
build_dataset(
    query="family:kinase AND organism_id:9606 AND reviewed:true",
    output_path="human_kinases.tsv",
    fields=["accession", "gene_names", "protein_name", "length", "sequence"]
)
```

## Key Terminology

**Swiss-Prot vs TrEMBL**: Swiss-Prot entries (`reviewed:true`) are manually curated by experts. TrEMBL entries (`reviewed:false`) are computationally predicted. Always prefer Swiss-Prot for high-confidence data.

**Accession Number**: Stable identifier for a protein entry (e.g., P04637). Entry names like "P53_HUMAN" may change.

**Entity Types**: UniProt covers UniProtKB (proteins), UniRef (clustered sequences), UniParc (archive), and Proteomes (complete sets).

**Annotation Score**: Quality indicator from 1 (basic) to 5 (comprehensive). Higher scores indicate more complete annotations.

## Best Practices

| Recommendation | Rationale |
|----------------|-----------|
| Add `reviewed:true` to queries | Swiss-Prot entries are manually curated |
| Request minimal fields | Reduces transfer size and response time |
| Use streaming for large sets | Avoids pagination complexity |
| Implement rate limiting | Respects server resources (0.3-0.5s delay) |
| Cache repeated queries | Minimizes redundant API calls |
| Handle errors gracefully | Network issues, rate limits, missing entries |

## References

See `references/api-reference.md` for:
- Complete field listing for query customization
- All searchable attributes and operators
- Database pairs for identifier translation
- Working code examples in curl, R, and JavaScript
- Rate limiting and error handling strategies

## External Documentation

- REST API: https://www.uniprot.org/help/api
- Query Fields: https://www.uniprot.org/help/query-fields
- ID Mapping: https://www.uniprot.org/help/id_mapping
- Programmatic Access: https://www.uniprot.org/help/programmatic_access
