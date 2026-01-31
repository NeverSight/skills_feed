---
name: github-harvester
description: Extract and process data from GitHub repositories
---


# GitHub Harvester Skill

> Extract and ingest content from GitHub repositories into RAG.

## Overview

GitHub repositories contain valuable documentation, code examples, and discussions. This skill covers:
- README and documentation extraction
- Code example mining
- Issue and discussion harvesting
- Wiki content extraction
- Release notes and changelogs

## Prerequisites

```bash
# GitHub CLI (recommended)
brew install gh  # macOS
# or: https://cli.github.com/

# Python libraries
pip install PyGithub httpx
```

## Authentication

```bash
# Authenticate with GitHub CLI
gh auth login

# Or set token for API access
export GITHUB_TOKEN="ghp_..."
```

## Extraction Methods

### Method 1: GitHub CLI (Recommended)

Best for quick extraction and authenticated access.

```bash
#!/bin/bash
# Extract repo content using gh CLI

REPO="$1"  # owner/repo format

# Clone with depth 1 for content only
gh repo clone "$REPO" -- --depth 1

# Get repo info
gh repo view "$REPO" --json name,description,readme

# Get issues
gh issue list --repo "$REPO" --limit 100 --json title,body,comments

# Get discussions (if enabled)
gh api "repos/$REPO/discussions" --paginate

# Get releases
gh release list --repo "$REPO" --limit 20
```

### Method 2: PyGithub API

Better for programmatic access and complex queries.

```python
#!/usr/bin/env python3
"""GitHub content extraction using PyGithub."""

from github import Github
from typing import Dict, List, Optional
import base64
import os

class GitHubExtractor:
    """Extract content from GitHub repositories."""

    def __init__(self, token: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.github = Github(self.token) if self.token else Github()

    def get_repo(self, repo_name: str):
        """Get repository object."""
        return self.github.get_repo(repo_name)

    def get_readme(self, repo_name: str) -> Dict:
        """Extract README content."""
        repo = self.get_repo(repo_name)

        try:
            readme = repo.get_readme()
            content = base64.b64decode(readme.content).decode('utf-8')

            return {
                "content": content,
                "path": readme.path,
                "size": readme.size,
                "url": readme.html_url
            }
        except Exception as e:
            return {"error": str(e)}

    def get_docs(self, repo_name: str) -> List[Dict]:
        """Extract documentation files."""
        repo = self.get_repo(repo_name)
        docs = []

        # Common doc locations
        doc_paths = ['docs', 'doc', 'documentation', '.github']

        for path in doc_paths:
            try:
                contents = repo.get_contents(path)
                docs.extend(self._extract_dir(repo, contents))
            except Exception:
                continue

        # Also get root markdown files
        try:
            root_contents = repo.get_contents("")
            for item in root_contents:
                if item.type == "file" and item.name.endswith('.md'):
                    content = base64.b64decode(item.content).decode('utf-8')
                    docs.append({
                        "path": item.path,
                        "content": content,
                        "url": item.html_url
                    })
        except Exception:
            pass

        return docs

    def _extract_dir(self, repo, contents) -> List[Dict]:
        """Recursively extract directory contents."""
        docs = []

        if not isinstance(contents, list):
            contents = [contents]

        for item in contents:
            if item.type == "dir":
                sub_contents = repo.get_contents(item.path)
                docs.extend(self._extract_dir(repo, sub_contents))
            elif item.type == "file":
                if item.name.endswith(('.md', '.rst', '.txt')):
                    try:
                        content = base64.b64decode(item.content).decode('utf-8')
                        docs.append({
                            "path": item.path,
                            "content": content,
                            "url": item.html_url
                        })
                    except Exception:
                        pass

        return docs

    def get_code_examples(
        self,
        repo_name: str,
        patterns: List[str] = None
    ) -> List[Dict]:
        """Extract code examples from repository."""
        repo = self.get_repo(repo_name)
        examples = []

        if patterns is None:
            patterns = ['examples', 'samples', 'demo', 'tutorials']

        for pattern in patterns:
            try:
                contents = repo.get_contents(pattern)
                examples.extend(self._extract_code(repo, contents))
            except Exception:
                continue

        return examples

    def _extract_code(self, repo, contents) -> List[Dict]:
        """Extract code files."""
        code = []
        code_extensions = ['.py', '.js', '.ts', '.go', '.rs', '.java', '.rb']

        if not isinstance(contents, list):
            contents = [contents]

        for item in contents:
            if item.type == "dir":
                sub = repo.get_contents(item.path)
                code.extend(self._extract_code(repo, sub))
            elif item.type == "file":
                if any(item.name.endswith(ext) for ext in code_extensions):
                    try:
                        content = base64.b64decode(item.content).decode('utf-8')
                        code.append({
                            "path": item.path,
                            "content": content,
                            "language": self._detect_language(item.name),
                            "url": item.html_url
                        })
                    except Exception:
                        pass

        return code

    def _detect_language(self, filename: str) -> str:
        """Detect programming language from filename."""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.rb': 'ruby',
            '.sh': 'bash',
        }
        for ext, lang in ext_map.items():
            if filename.endswith(ext):
                return lang
        return 'unknown'

    def get_issues(
        self,
        repo_name: str,
        state: str = "all",
        limit: int = 100
    ) -> List[Dict]:
        """Extract issues with comments."""
        repo = self.get_repo(repo_name)
        issues = []

        for issue in repo.get_issues(state=state)[:limit]:
            issue_data = {
                "number": issue.number,
                "title": issue.title,
                "body": issue.body or "",
                "state": issue.state,
                "labels": [l.name for l in issue.labels],
                "created_at": issue.created_at.isoformat(),
                "url": issue.html_url,
                "comments": []
            }

            # Get comments
            for comment in issue.get_comments():
                issue_data["comments"].append({
                    "body": comment.body,
                    "author": comment.user.login,
                    "created_at": comment.created_at.isoformat()
                })

            issues.append(issue_data)

        return issues

    def get_discussions(self, repo_name: str, limit: int = 50) -> List[Dict]:
        """Extract discussions using GraphQL API."""
        # Note: Requires GraphQL query, simplified version here
        query = """
        query($owner: String!, $name: String!, $first: Int!) {
          repository(owner: $owner, name: $name) {
            discussions(first: $first) {
              nodes {
                title
                body
                url
                category { name }
                comments(first: 10) {
                  nodes { body }
                }
              }
            }
          }
        }
        """

        owner, name = repo_name.split('/')

        # Would need to execute GraphQL query
        # Simplified: return empty for now
        return []

    def get_releases(self, repo_name: str, limit: int = 20) -> List[Dict]:
        """Extract release information."""
        repo = self.get_repo(repo_name)
        releases = []

        for release in repo.get_releases()[:limit]:
            releases.append({
                "tag": release.tag_name,
                "name": release.title,
                "body": release.body or "",
                "published_at": release.published_at.isoformat() if release.published_at else None,
                "url": release.html_url,
                "prerelease": release.prerelease
            })

        return releases

    def get_repo_metadata(self, repo_name: str) -> Dict:
        """Get repository metadata."""
        repo = self.get_repo(repo_name)

        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "topics": repo.get_topics(),
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "url": repo.html_url,
            "homepage": repo.homepage
        }
```

## Chunking Strategies

### README Chunking

```python
def chunk_readme(content: str) -> List[Dict]:
    """Chunk README by sections."""
    import re

    sections = []
    current_section = {"heading": "Overview", "content": "", "level": 1}

    for line in content.split('
'):
        heading_match = re.match(r'^(#{1,3})\s+(.+)$', line)

        if heading_match:
            # Save current section
            if current_section["content"].strip():
                sections.append(current_section)

            level = len(heading_match.group(1))
            heading = heading_match.group(2)
            current_section = {"heading": heading, "content": "", "level": level}
        else:
            current_section["content"] += line + "
"

    # Don't forget last section
    if current_section["content"].strip():
        sections.append(current_section)

    return sections
```

### Code Example Chunking

```python
def chunk_code_file(content: str, language: str) -> List[Dict]:
    """Chunk code file by functions/classes."""
    import ast

    if language != 'python':
        # For non-Python, chunk by size
        return [{"content": content, "type": "file"}]

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return [{"content": content, "type": "file"}]

    chunks = []

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            source = ast.get_source_segment(content, node)
            if source:
                chunks.append({
                    "content": source,
                    "type": "function",
                    "name": node.name,
                    "docstring": ast.get_docstring(node)
                })

        elif isinstance(node, ast.ClassDef):
            source = ast.get_source_segment(content, node)
            if source:
                chunks.append({
                    "content": source,
                    "type": "class",
                    "name": node.name,
                    "docstring": ast.get_docstring(node)
                })

    return chunks if chunks else [{"content": content, "type": "file"}]
```

### Issue/Discussion Chunking

```python
def chunk_issue(issue: Dict) -> List[Dict]:
    """Chunk issue with comments."""
    chunks = []

    # Issue body as main chunk
    chunks.append({
        "content": f"# {issue['title']}

{issue['body']}",
        "type": "issue",
        "issue_number": issue["number"]
    })

    # Significant comments as separate chunks
    for i, comment in enumerate(issue.get("comments", [])):
        if len(comment["body"]) > 200:  # Only substantial comments
            chunks.append({
                "content": comment["body"],
                "type": "comment",
                "issue_number": issue["number"],
                "comment_index": i
            })

    return chunks
```

## Full Harvesting Pipeline

```python
#!/usr/bin/env python3
"""Complete GitHub harvesting pipeline."""

from datetime import datetime
from typing import Dict, List
import hashlib

async def harvest_github_repo(
    repo_name: str,
    collection: str,
    include_readme: bool = True,
    include_docs: bool = True,
    include_examples: bool = True,
    include_issues: bool = False,
    include_releases: bool = True,
    max_issues: int = 50
) -> Dict:
    """
    Harvest a GitHub repository into RAG.

    Args:
        repo_name: Repository in owner/repo format
        collection: Target RAG collection
        include_*: What content to harvest
        max_issues: Maximum issues to harvest
    """
    extractor = GitHubExtractor()

    # Get repo metadata
    repo_meta = extractor.get_repo_metadata(repo_name)

    base_metadata = {
        "source_type": "github",
        "repo": repo_name,
        "repo_description": repo_meta.get("description"),
        "repo_language": repo_meta.get("language"),
        "repo_topics": repo_meta.get("topics", []),
        "harvested_at": datetime.now().isoformat()
    }

    stats = {
        "readme": 0,
        "docs": 0,
        "examples": 0,
        "issues": 0,
        "releases": 0
    }

    # Harvest README
    if include_readme:
        readme = extractor.get_readme(repo_name)
        if "content" in readme:
            sections = chunk_readme(readme["content"])

            for i, section in enumerate(sections):
                metadata = {
                    **base_metadata,
                    "content_type": "readme",
                    "section": section["heading"],
                    "section_level": section["level"],
                    "chunk_index": i,
                    "source_url": readme["url"]
                }

                await ingest(
                    content=section["content"],
                    collection=collection,
                    metadata=metadata,
                    doc_id=f"gh_{repo_name.replace('/', '_')}_readme_{i}"
                )
                stats["readme"] += 1

    # Harvest docs
    if include_docs:
        docs = extractor.get_docs(repo_name)

        for doc in docs:
            metadata = {
                **base_metadata,
                "content_type": "documentation",
                "file_path": doc["path"],
                "source_url": doc["url"]
            }

            await ingest(
                content=doc["content"],
                collection=collection,
                metadata=metadata,
                doc_id=f"gh_{repo_name.replace('/', '_')}_doc_{hashlib.md5(doc['path'].encode()).hexdigest()[:8]}"
            )
            stats["docs"] += 1

    # Harvest code examples
    if include_examples:
        examples = extractor.get_code_examples(repo_name)

        for example in examples:
            chunks = chunk_code_file(example["content"], example["language"])

            for i, chunk in enumerate(chunks):
                metadata = {
                    **base_metadata,
                    "content_type": "code_example",
                    "file_path": example["path"],
                    "language": example["language"],
                    "code_type": chunk.get("type", "file"),
                    "code_name": chunk.get("name", ""),
                    "source_url": example["url"]
                }

                await ingest(
                    content=chunk["content"],
                    collection=collection,
                    metadata=metadata,
                    doc_id=f"gh_{repo_name.replace('/', '_')}_code_{hashlib.md5(example['path'].encode()).hexdigest()[:8]}_{i}"
                )
                stats["examples"] += 1

    # Harvest issues
    if include_issues:
        issues = extractor.get_issues(repo_name, limit=max_issues)

        for issue in issues:
            chunks = chunk_issue(issue)

            for chunk in chunks:
                metadata = {
                    **base_metadata,
                    "content_type": chunk["type"],
                    "issue_number": issue["number"],
                    "issue_title": issue["title"],
                    "issue_state": issue["state"],
                    "issue_labels": issue["labels"],
                    "source_url": issue["url"]
                }

                await ingest(
                    content=chunk["content"],
                    collection=collection,
                    metadata=metadata,
                    doc_id=f"gh_{repo_name.replace('/', '_')}_issue_{issue['number']}_{chunk.get('comment_index', 0)}"
                )
                stats["issues"] += 1

    # Harvest releases
    if include_releases:
        releases = extractor.get_releases(repo_name)

        for release in releases:
            if release["body"]:  # Only if has release notes
                metadata = {
                    **base_metadata,
                    "content_type": "release",
                    "release_tag": release["tag"],
                    "release_name": release["name"],
                    "published_at": release["published_at"],
                    "source_url": release["url"]
                }

                await ingest(
                    content=f"# {release['name']}

{release['body']}",
                    collection=collection,
                    metadata=metadata,
                    doc_id=f"gh_{repo_name.replace('/', '_')}_release_{release['tag']}"
                )
                stats["releases"] += 1

    return {
        "status": "success",
        "repo": repo_name,
        "collection": collection,
        "harvested": stats,
        "total": sum(stats.values())
    }
```

## Metadata Schema

```yaml
# GitHub content metadata
source_type: github
repo: owner/repo
repo_description: "Repository description"
repo_language: Python
repo_topics: [topic1, topic2]
content_type: readme|documentation|code_example|issue|release
file_path: docs/guide.md (for docs/code)
language: python (for code)
code_type: function|class|file
code_name: function_name
issue_number: 123
issue_title: "Issue title"
issue_state: open|closed
issue_labels: [bug, help wanted]
release_tag: v1.0.0
source_url: https://github.com/...
harvested_at: "2024-01-01T12:00:00Z"
```

## Usage Examples

```python
# Full repository harvest
result = await harvest_github_repo(
    repo_name="anthropics/anthropic-sdk-python",
    collection="anthropic_sdk",
    include_readme=True,
    include_docs=True,
    include_examples=True,
    include_issues=False,
    include_releases=True
)

# Issues focus
result = await harvest_github_repo(
    repo_name="langchain-ai/langchain",
    collection="langchain_issues",
    include_readme=False,
    include_docs=False,
    include_issues=True,
    max_issues=200
)

# Code examples only
result = await harvest_github_repo(
    repo_name="fastapi/fastapi",
    collection="fastapi_examples",
    include_readme=True,
    include_docs=False,
    include_examples=True
)
```

## CLI Usage

```bash
# Using gh CLI for quick extraction
gh repo clone owner/repo -- --depth 1
gh repo view owner/repo --json readme -q .readme.content

# Get issues as JSON
gh issue list --repo owner/repo --json title,body,comments --limit 50
```

## Refinement Notes

> Track improvements as you use this skill.

- [ ] README extraction tested
- [ ] Documentation crawling working
- [ ] Code example chunking optimized
- [ ] Issue extraction with comments
- [ ] Rate limiting handled
- [ ] Authentication working
