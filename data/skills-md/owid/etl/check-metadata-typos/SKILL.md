---
name: check-metadata-typos
description: Check .meta.yml and snapshot .dvc files for spelling typos using codespell. Use when user mentions typos, spelling errors, metadata quality, or wants to check metadata files for mistakes.
---

# Check Metadata Typos

Check metadata files for spelling typos using comprehensive spell checking.

## Scope Options

Ask the user which scope they want to check:

1. **Current step only** - Ask the user to specify the step path (e.g., `etl/steps/data/garden/energy/2025-06-27/electricity_mix`)
2. **All ETL metadata** - Check all active `.meta.yml` files in `etl/steps/data/{garden,meadow,grapher}/` (automatically excludes ~3,570 archived steps)
3. **Snapshot metadata** - Check all snapshot `.dvc` files in `snapshots/` (~7,915 files)
4. **All metadata** - Check both ETL steps and snapshot metadata files

**Note:** Archived steps and snapshots (defined in `dag/archive/*.yml`) are automatically excluded from checking as they are no longer actively maintained.

---

## Implementation Strategy

### 0. Check codespell installation

**IMPORTANT:** Check if codespell is installed before attempting to use it. Since codespell is now a dev dependency in the project, it should already be installed, but verify first to avoid reinstalling unnecessarily.

```bash
# Check if codespell is installed
if ! .venv/bin/codespell --version &> /dev/null; then
    echo "codespell not found, installing..."
    uv add --dev codespell
else
    echo "codespell is already installed"
fi
```

If codespell is not installed and `uv add --dev codespell` fails, explain to the user how to install it manually.

### 1. Exclude archived steps and snapshots

**IMPORTANT:** Do not check archived steps and snapshots as they are no longer in use.

Archived steps and snapshots are defined in `dag/archive/*.yml` files:
- ~3,570 deprecated steps (garden, meadow, grapher)
- ~736 deprecated snapshots

To exclude them, extract their paths and create a list of active files:

```bash
# Extract archived step paths to a file
for step_type in garden meadow grapher; do
  grep -h "data://${step_type}/" dag/archive/*.yml 2>/dev/null | \
    grep -o "data://${step_type}/[^:]*" | \
    sed 's|data://|etl/steps/data/|' | \
    sed 's|$|.meta.yml|'
done > /tmp/archived_files.txt

# Extract archived snapshots
grep -rh "snapshot://" dag/archive/*.yml 2>/dev/null | \
  grep -o "snapshot://[^:]*" | \
  sed 's|snapshot://|snapshots/|' | \
  sed 's|$|.dvc|' | \
  sort -u >> /tmp/archived_files.txt

# Create list of all metadata files
find etl/steps/data/garden -name "*.meta.yml" > /tmp/all_meta_files.txt
find etl/steps/data/meadow -name "*.meta.yml" >> /tmp/all_meta_files.txt
find etl/steps/data/grapher -name "*.meta.yml" >> /tmp/all_meta_files.txt
find snapshots -name "*.dvc" >> /tmp/all_meta_files.txt

# Filter out archived files
grep -vFf /tmp/archived_files.txt /tmp/all_meta_files.txt > /tmp/active_meta_files.txt

echo "Total files to check: $(wc -l < /tmp/active_meta_files.txt)"
```

### 2. Run codespell with ignore list and exclusions

Use the existing `.codespell-ignore.txt` file to filter out domain-specific terms:

**For option 1 (current step only):**

1. Ask the user to provide the step path (e.g., `etl/steps/data/garden/energy/2025-06-27/electricity_mix`)
2. Construct the full path to the metadata file: `<step_path>/*.meta.yml`
3. Run codespell on that specific path:

```bash
# For specific step (option 1)
STEP_PATH="<user_provided_path>"  # e.g., etl/steps/data/garden/energy/2025-06-27/electricity_mix
.venv/bin/codespell "${STEP_PATH}"/*.meta.yml \
  --ignore-words=.codespell-ignore.txt
```

**For option 2 (all ETL metadata - garden, meadow, grapher):**

```bash
# For all ETL step metadata (option 2)
find etl/steps/data/garden -name "*.meta.yml" > /tmp/all_step_files.txt
find etl/steps/data/meadow -name "*.meta.yml" >> /tmp/all_step_files.txt
find etl/steps/data/grapher -name "*.meta.yml" >> /tmp/all_step_files.txt
grep -vFf /tmp/archived_files.txt /tmp/all_step_files.txt > /tmp/active_step_files.txt

cat /tmp/active_step_files.txt | xargs .venv/bin/codespell \
  --ignore-words=.codespell-ignore.txt
```

Note: Excluding archived steps reduces the scope by ~3,570 files and focuses on actively maintained metadata.

**For option 3 (snapshot metadata):**

```bash
# For all snapshot metadata (option 3)
find snapshots -name "*.dvc" > /tmp/all_snapshot_files.txt
grep -vFf /tmp/archived_files.txt /tmp/all_snapshot_files.txt > /tmp/active_snapshot_files.txt

cat /tmp/active_snapshot_files.txt | xargs .venv/bin/codespell \
  --ignore-words=.codespell-ignore.txt
```

Note: Snapshot `.dvc` files contain metadata in the `meta.source.description` and `meta.source.published_by` fields. ~736 archived snapshots are excluded.

**For option 4 (all metadata):**

```bash
# For all metadata - ETL and snapshots (option 4)
# Use the active_meta_files.txt created in step 1
cat /tmp/active_meta_files.txt | xargs .venv/bin/codespell \
  --ignore-words=.codespell-ignore.txt
```

### 3. Parse and present results

Extract typos from codespell output and present them in a structured format:

- Group by typo type (e.g., all instances of "seperate" → "separate")
- Show file paths (as clickable links when possible)
- Show line numbers
- Show suggested corrections

**Example output format:**

```
Found 15 typos across 8 files:

Most common:
- "inmigrant" → "immigrant" (5 occurrences in 2 files)
- "seperate" → "separate" (3 occurrences in 1 file)
- "accomodation" → "accommodation" (2 occurrences in 1 file)

Detailed list:
[file.meta.yml:123] inmigrant → immigrant
[file.meta.yml:456] seperate → separate
...
```

### 4. Offer to fix typos

After presenting results, ask the user:

- **Fix all automatically?** - Apply all suggested fixes
- **Review each typo?** - Go through typos one by one for confirmation
- **Cancel** - Exit without making changes

### 5. Apply fixes (if user confirms)

For automatic fixes:

```bash
# Use sed or Python script to replace typos in files
# Example: sed -i '' 's/seperate/separate/g' file.meta.yml
```

For reviewed fixes, confirm each change before applying.

### 6. Verify fixes

After applying fixes, re-run codespell to verify all typos were corrected:

```bash
.venv/bin/codespell <path> --ignore-words=.codespell-ignore.txt
```

Should return 0 results.

### 7. Clean up

**IMPORTANT:** Delete any temporary files created during the check:

```bash
rm -f /tmp/archived_files.txt /tmp/all_meta_files.txt /tmp/active_meta_files.txt \
      /tmp/all_step_files.txt /tmp/active_step_files.txt \
      /tmp/all_snapshot_files.txt /tmp/active_snapshot_files.txt \
      /tmp/codespell_output.txt

The only persistent files should be:

- The `.codespell-ignore.txt` whitelist (if it doesn't exist, create it)
- Modified `.meta.yml` files (if fixes were applied)

**Do NOT create new persistent files in the repo like:**

- ❌ `TYPO_CHECK_REPORT.md`
- ❌ `scripts/analyze_typos.py`
- ❌ `scripts/advanced_spell_checker.py`

All analysis logic should be embedded in this command execution, not saved as separate files.

---

## Error Handling

- Check if codespell is installed first (see step 0). If not installed and `uv add --dev codespell` fails, explain to the user how to install it manually with `uv sync` or check their Python environment
- If no `.meta.yml` or `.dvc` files are found in the specified scope, inform the user
- If codespell finds no typos, congratulate the user on clean metadata!
- If file modification fails, report which files couldn't be updated

---

## Notes

- Always use American English spelling (e.g., "combating" not "combatting")
- Technical field names (like variable names with underscores) are typically safe to ignore
- **Acronyms in ALL CAPS should be ignored** - they are almost always legitimate acronyms (e.g., TE, INE, DIEA)
- **URLs and domain names should be ignored** - codespell may flag parts of URLs (e.g., "ine.es", "corona.fo") but these are correct
- When in doubt about a flagged word, ask the user before fixing
