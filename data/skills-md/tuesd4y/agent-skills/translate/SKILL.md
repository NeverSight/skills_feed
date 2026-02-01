---
name: translate
description: Translate new entries in XLF files. Finds state="new" in changed messages.{LANG}.xlf files, shows context, proposes translations for review.
---

# Translation Skill

Translate new entries in XLF translation files by finding `state="new"` targets, locating source context, and proposing translations for review.

## Workflow

### Step 1: Find Changed Translation Files

Run these commands to find changed translation files:
```bash
git diff --name-only | grep -E 'messages\.[a-z]{2}\.xlf$'
git diff --cached --name-only | grep -E 'messages\.[a-z]{2}\.xlf$'
```

Combine results and deduplicate. If no changed translation files found, inform the user.

### Step 2: Extract New Translations

For each changed `.xlf` file:
1. Read the file content
2. Parse to find all `<trans-unit>` elements
3. Filter for those containing `<target state="new">`
4. Extract for each:
   - `id` attribute (translation ID)
   - `<source>` content (English text)
   - `<target>` content (current translation, may be empty or placeholder)
   - Any placeholder elements (`<x .../>`)

### Step 3: Find Source Context

For each translation ID, search for its usage in the codebase:

**TypeScript files** (`$localize` strings):
```bash
grep -r "@@{ID}:" --include="*.ts" apps/ libs/
```

**HTML files** (`i18n` attributes):
```bash
grep -r "@@{ID}\"" --include="*.html" apps/ libs/
```

Read the surrounding code (5-10 lines) to understand context.

### Step 4: Generate & Review Translations

For each `state="new"` entry, present to the user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Translation ID: {id}
File: {xlf_file_path}
Target Language: {language_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source (English):
  {source_text}

Context:
  {file_path}:{line_number}
  {code_snippet}

Proposed Translation:
  {proposed_translation}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Wait for user confirmation** before proceeding. Options:
- Accept the proposed translation
- Provide an alternative translation
- Skip this entry

### Step 5: Apply Approved Translations

For approved translations, update the XLF file:
1. Replace the `<target>` element content with the approved translation
2. Change `state="new"` to `state="ai"`

**Before:**
```xml
<trans-unit id="myTranslationId" datatype="html">
  <source>English text</source>
  <target state="new">Old or empty translation</target>
</trans-unit>
```

**After:**
```xml
<trans-unit id="myTranslationId" datatype="html">
  <source>English text</source>
  <target state="ai">Translated text</target>
</trans-unit>
```

## Language Detection

Identify the target language from the filename pattern:

| Filename Pattern | Language | Native Name |
|-----------------|----------|-------------|
| `messages.de.xlf` | German | Deutsch |
| `messages.fr.xlf` | French | Francais |
| `messages.es.xlf` | Spanish | Espanol |
| `messages.hu.xlf` | Hungarian | Magyar |

## Placeholder Handling

**Critical**: Preserve all XML placeholder elements exactly as they appear in the source. These include:

| Element | Purpose | Example |
|---------|---------|---------|
| `<x id="INTERPOLATION" equiv-text="{{...}}"/>` | Angular interpolations | `{{count}}` |
| `<x id="INTERPOLATION_n"/>` | Multiple interpolations | Second, third interpolation |
| `<x id="PH" equiv-text="..."/>` | Named placeholders | ICU expressions |
| `<x id="PH_n"/>` | Multiple placeholders | Additional placeholders |
| `<x id="LINE_BREAK" ctype="lb"/>` | Line breaks | `<br>` |
| `<x id="START_TAG_SPAN"/>` | Opening HTML tags | `<span>` |
| `<x id="CLOSE_TAG_SPAN"/>` | Closing HTML tags | `</span>` |
| `<x id="START_BOLD_TEXT"/>` | Bold text start | `<b>` |
| `<x id="CLOSE_BOLD_TEXT"/>` | Bold text end | `</b>` |

**Example with placeholders:**
```xml
<source>Hello <x id="INTERPOLATION" equiv-text="{{name}}"/>, you have <x id="INTERPOLATION_1" equiv-text="{{count}}"/> messages.</source>
<target state="ai">Hallo <x id="INTERPOLATION" equiv-text="{{name}}"/>, Sie haben <x id="INTERPOLATION_1" equiv-text="{{count}}"/> Nachrichten.</target>
```

## Translation Guidelines

1. **Match existing tone**: Review other translations in the file to maintain consistent style
2. **Preserve placeholders**: Copy placeholder elements exactly, only translate surrounding text
3. **Consider context**: Use the code context to understand how the text is used
4. **Domain terminology**: Use standard terms for:
   - Mobility/transport: commute, emissions, CO2, modal split
   - UI elements: buttons, labels, tooltips
   - Business terms: audit, score, analysis
5. **Formal vs informal**: German typically uses formal "Sie" form in business software

## Common Translation Patterns

### German (de)
- "Save" → "Speichern"
- "Cancel" → "Abbrechen"
- "Loading..." → "Wird geladen..."
- "Error" → "Fehler"
- "Success" → "Erfolgreich"

### French (fr)
- "Save" → "Enregistrer"
- "Cancel" → "Annuler"
- "Loading..." → "Chargement..."
- "Error" → "Erreur"
- "Success" → "Succes"

### Spanish (es)
- "Save" → "Guardar"
- "Cancel" → "Cancelar"
- "Loading..." → "Cargando..."
- "Error" → "Error"
- "Success" → "Exito"

### Hungarian (hu)
- "Save" → "Mentes"
- "Cancel" → "Megse"
- "Loading..." → "Betoltes..."
- "Error" → "Hiba"
- "Success" → "Sikeres"

## Batch Processing

When multiple entries need translation:
1. Group by file for efficiency
2. Show a summary of how many entries need translation per file
3. Process entries one at a time, waiting for approval
4. After all entries are reviewed, show summary of changes made

## Error Handling

- If no changed translation files found: Inform user and suggest running `git status`
- If no `state="new"` entries found: Inform user that all translations are up to date
- If context not found: Still propose translation based on source text alone, note missing context
- If file parse error: Report the error and skip the problematic file