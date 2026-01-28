---
name: gioia-analysis
description: |
  Systematisk analys av intervjutranskript enligt Gioia-metodiken.

  [VAD] Analyserar kvalitativa intervjutranskript genom 1st-order kodning
  (informantspråk), 2nd-order tematisering (forskarkonceptualisering) och
  aggregerade dimensioner. Producerar standardiserad dokumentation med
  indexerade, export-ready citat.

  [NÄR] Use when: gioia, intervjuanalys, transkriptanalys, kvalitativ analys,
  kodning, tematisk analys, grounded theory, 1st-order, 2nd-order

  [SPRÅK] Svenska (primärt), engelska vid behov

  [KÄLLA] Gioia, D.A., Corley, K.G. & Hamilton, A.L. (2013). Seeking
  Qualitative Rigor in Inductive Research. Organizational Research Methods.

tier: 2
allowed-tools: Read, Write, Glob, Grep
output_directory: <OUTPUT_DIRECTORY>
output_naming: "YYYY-MM-DD_gioia_[intervju-id].md"
---

# Gioia Intervjuanalys

**Roll:** Kvalitativ forskningsanalytiker
**Metod:** Gioia-metodiken för induktiv konceptutveckling
**Output:** Standardiserad analysdokumentation med indexerade citat

## Aktiveras vid

- Analys av intervjutranskript
- Kvalitativ kodning/tematisering
- Gioia-metodik
- Induktiv teoriutveckling
- Systematisk citatextraktion

## Grundprinciper (från Gioia et al., 2013)

### Epistemologiska antaganden

1. **Social konstruktion**: Organisatorisk verklighet är socialt konstruerad
2. **Kunskapsbärande agenter**: Informanter vet vad de gör och kan förklara det
3. **Dubbel adequacy**: Analys ska vara adekvat både på informantens nivå OCH teoretisk nivå

### Analysens tre nivåer

```
┌─────────────────────────────────────────────────────────────────────┐
│  1ST-ORDER KONCEPT          │  Informantens egna termer och uttryck │
│  (Informant-centriska)      │  "Direkt från transkriptet"           │
├─────────────────────────────┼───────────────────────────────────────┤
│  2ND-ORDER TEMAN            │  Forskarens teoretiska tolkning       │
│  (Forskar-centriska)        │  "Vad betyder detta konceptuellt?"    │
├─────────────────────────────┼───────────────────────────────────────┤
│  AGGREGERADE DIMENSIONER    │  Övergripande teoretiska kategorier   │
│  (Teoretiska)               │  "Vilken större helhet tillhör detta?"│
└─────────────────────────────┴───────────────────────────────────────┘
```

## Analysprocess

### Steg 1: Transkriptparsning

Identifiera fråga-svar-segment oavsett format:
- Q:/A: eller I:/R: format
- Intervjuare/Informant med namn
- Tidsstämplar med talarbyten
- Numrerade frågor
- Tematiska block (vid fri dialog)

### Steg 2: Segment-för-segment-kodning

För varje segment:

1. **Sammanfatta svaret** (behåll nyanser)
2. **Extrahera nyckelcitat** med:
   - Unikt ID (C01, C02, etc.)
   - Exakt ordval bevarad
   - Tillräcklig kontext
3. **1st-order kodning**: Använd informantens språk
4. **Preliminär 2nd-order tolkning**: Teoretisk reflektion

### Steg 3: Tematisk syntes

- Gruppera 1st-order koder till 2nd-order teman
- Identifiera aggregerade dimensioner
- Bygg datastruktur

### Steg 4: Dokumentation

Generera standardiserad output med:
- Komplett segment-analys
- Datastruktur (visuell)
- Citatregister (indexerat)
- Export-ready citat

## Citathantering

### Citatformat

```markdown
> "Exakt citat från informanten med tillräcklig kontext för att
> förstå innebörden."
>
> — **[C01]** | Segment 3 | Tema: X, Y | Rad 45-47
```

### Citatregister-struktur

Varje citat indexeras med:
- **ID**: Unikt referensnummer (C01, C02...)
- **Segment**: Var i intervjun
- **1st-order kod**: Informantterm
- **2nd-order tema**: Forskarkonceptualisering
- **Dimension**: Aggregerad kategori
- **Källposition**: Rad/tidsstämpel i original

## Output

### Filplacering
```
<OUTPUT_DIRECTORY>
```

### Namnkonvention
```
YYYY-MM-DD_gioia_[intervju-id].md
```

Exempel:
- `2026-01-05_gioia_INT01.md`
- `2026-01-05_gioia_mellanchef-org-a.md`

### Metadata-huvud (YAML frontmatter)
```yaml
---
type: gioia-analysis
source: [originalfilnamn]
informant: [id/pseudonym]
date_analyzed: YYYY-MM-DD
project: [projektnamn]
status: draft
tags: [gioia, intervjuanalys, kvalitativ]
quote_count: [antal citat]
dimensions: [lista på aggregerade dimensioner]
---
```

## Kvalitetskriterier

### Från Gioia et al. (2013)

- [ ] 1st-order termer bevarar informantens språk
- [ ] 2nd-order teman är teoretiskt meningsfulla
- [ ] Tydlig koppling data → koncept → teori
- [ ] Citat stödjer tolkningar transparent
- [ ] Datastruktur visualiserar analysens logik

### Citatspecifikt

- [ ] Varje citat har unikt ID
- [ ] Kontext bevarad (fråga som föranledde svaret)
- [ ] Tillräckligt långa för att stå självständigt
- [ ] Taggade för sökning/återanvändning

## Workflow

Se: `workflows/analyze-transcript.md`

## Mallar

Se: `templates/analysis-output.md`

## Referens

Se: `reference/transcript-formats.md` för olika transkriptformat

---

🎯 COMPLETED: [SKILL:gioia-analysis] [interview transcript analyzed]
🗣️ CUSTOM COMPLETED: [SKILL:gioia-analysis] [Analysis complete]
