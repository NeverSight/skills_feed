---
name: n8n-prd-generator
description: Generate structured PRD documents for n8n automation workflows. Use when planning n8n workflows, creating automation requirements, starting a new n8n project, or preparing workflow specifications before building.
---

# n8n Automation PRD Generator

Generate structured, MCP-ready PRD documents for n8n automation workflows. Captures all requirements needed to build the workflow with Claude Code + n8n-mcp.

---

## Activation

When the user wants to plan or specify an n8n automation workflow, activate this skill. The output is a PRD markdown file saved to the project directory.

---

## Process: Structured Requirements Gathering

Follow these phases strictly. Do NOT skip phases or rush to the PRD.

### Phase 1: Initial Understanding

Ask the user to describe the automation they need. Accept any format:
- Free-text description
- Bullet points
- Meeting notes
- Voice transcript

After receiving the input, summarize what you understood in 2-3 sentences and confirm with the user before proceeding.

### Phase 2: Clarifying Questions (MANDATORY)

Ask targeted questions across these dimensions. Use the AskUserQuestion tool with grouped questions (max 4 per round). Run multiple rounds if needed.

**Round 1 - Trigger & Schedule:**
- What starts the workflow? (Webhook, Schedule, Manual, Event-based)
- How often should it run? (Real-time, hourly, daily, weekly)
- What timezone/business hours apply?

**Round 2 - Data Flow & Services:**
- Which external services/APIs are involved? (Name them specifically)
- What data comes in? (Structure, format, volume)
- What data goes out? (Where, format, who receives it)
- Are there data transformations needed? (Mapping, filtering, enrichment)

**Round 3 - Error Handling & Edge Cases:**
- What happens if an API is down or returns errors?
- What if incoming data is incomplete or malformed?
- Should there be notifications on failure? (Email, Slack, etc.)
- What are known edge cases? (Empty data, duplicates, rate limits)

**Round 4 - Credentials & Environment:**
- Which services are already connected in n8n? (Existing credentials)
- Are there API keys that need to be set up first?
- Any environment-specific considerations? (Staging vs Production)

Skip questions that were already answered in the initial description. Ask follow-up questions if answers reveal new complexity.

### Phase 3: PRD Generation

After all questions are answered, generate the PRD using the template below. Save it as a markdown file in the project directory:

**File naming convention:** `prd-[short-name].md`
**Example:** `prd-youtube-video-ideas.md`, `prd-linkedin-lead-capture.md`

---

## PRD Template

```markdown
# PRD: [Workflow Name]

**Status:** Draft
**Erstellt:** [Datum]
**Autor:** [Name]

---

## 1. Ziel & Kontext

**Was soll automatisiert werden?**
[1-3 Saetze die das Ziel beschreiben]

**Warum wird diese Automatisierung gebraucht?**
[Business-Kontext, Zeitersparnis, aktueller manueller Prozess]

**Wer nutzt das Ergebnis?**
[Zielgruppe/Empfaenger des Outputs]

---

## 2. Trigger & Zeitplan

| Eigenschaft | Wert |
|---|---|
| Trigger-Typ | [Webhook / Schedule / Manual / Event] |
| Zeitplan | [z.B. Jeden Montag 9:00 / Echtzeit / Bei Bedarf] |
| Zeitzone | [z.B. Europe/Berlin] |
| Erwartetes Volumen | [z.B. 10-50 Ausfuehrungen pro Tag] |

---

## 3. Datenfluss

### Input
- **Quelle:** [Service/API/Webhook]
- **Format:** [JSON / Form Data / CSV / etc.]
- **Beispiel-Payload:**
```json
{
  "beispiel": "daten"
}
```

### Verarbeitung
1. [Schritt 1: Was passiert mit den Daten]
2. [Schritt 2: Transformation/Anreicherung]
3. [Schritt n: ...]

### Output
- **Ziel:** [Service/API/E-Mail/Sheet]
- **Format:** [Beschreibung des Outputs]
- **Empfaenger:** [Wer bekommt das Ergebnis]

---

## 4. Beteiligte Services & Credentials

| Service | Zweck | Credential-Typ | Status |
|---|---|---|---|
| [z.B. YouTube] | [Videos abrufen] | [OAuth2] | [Vorhanden / Fehlt] |
| [z.B. Anthropic] | [AI-Verarbeitung] | [API Key] | [Vorhanden / Fehlt] |
| [z.B. Gmail] | [E-Mail senden] | [OAuth2] | [Vorhanden / Fehlt] |

---

## 5. Workflow-Architektur

### Node-Uebersicht (empfohlen)

| # | Node-Name | Node-Typ | Funktion |
|---|---|---|---|
| 1 | [Name] | [n8n-nodes-base.xyz] | [Was macht der Node] |
| 2 | [Name] | [n8n-nodes-base.xyz] | [Was macht der Node] |
| ... | ... | ... | ... |

### Datenfluss-Diagramm

```
[Trigger] -> [Node 2] -> [Node 3] -> ... -> [Output]
                              |
                              v
                        [Error Branch]
```

### Aggregation & Batching
- [Muessen Daten aggregiert werden bevor sie verarbeitet werden?]
- [Gibt es Batch-Verarbeitung?]
- [Wie viele Items werden erwartet pro Durchlauf?]

---

## 6. Error Handling & Edge Cases

### Fehlerbehandlung

| Fehlertyp | Reaktion |
|---|---|
| API nicht erreichbar | [z.B. Retry 3x, dann Benachrichtigung] |
| Leere Daten | [z.B. Info-Mail senden, Workflow beenden] |
| Rate Limit erreicht | [z.B. Warten und erneut versuchen] |
| Ungueltige Eingabe | [z.B. Validierung, Fehlermeldung] |

### Bekannte Edge Cases
- [Edge Case 1: Beschreibung + gewuenschtes Verhalten]
- [Edge Case 2: Beschreibung + gewuenschtes Verhalten]

### Benachrichtigung bei Fehler
- **Kanal:** [E-Mail / Slack / etc.]
- **Empfaenger:** [Wer wird benachrichtigt]
- **Inhalt:** [Was soll in der Fehlermeldung stehen]

---

## 7. n8n-spezifische Hinweise

### Datenstruktur-Warnungen
- [z.B. YouTube getAll gibt id als Objekt zurueck: $json.id.videoId statt $json.id]
- [z.B. Webhook-Daten liegen unter $json.body, nicht $json]

### Expression-Einschraenkungen
- Kein Optional Chaining (?.) in n8n Expressions - nur in Code Nodes
- Expressions muessen mit = Prefix beginnen wenn sie dynamisch sind

### Aggregation
- [Muessen Items vor AI/E-Mail-Nodes aggregiert werden?]
- [Code Node mit "Run Once for All Items" fuer Aggregation nutzen]

### Error Handling Pattern
- `onError: "continueRegularOutput"` statt deprecated `continueOnFail: true`
- IF-Node fuer Edge Cases (z.B. keine Daten vorhanden)

---

## 8. Akzeptanzkriterien

- [ ] [Kriterium 1: Was muss funktionieren]
- [ ] [Kriterium 2: Was muss funktionieren]
- [ ] [Kriterium 3: Was muss funktionieren]
- [ ] Error Handling getestet (leere Daten, API-Fehler)
- [ ] Workflow-Validierung ohne Errors (Warnings akzeptabel)
- [ ] E2E-Test mit echten Daten erfolgreich

---

## 9. Offene Fragen

- [Frage 1: Was noch geklaert werden muss]
- [Frage 2: Was noch geklaert werden muss]
```

---

## Guidelines for the Agent

### DO:
- Ask ALL clarifying questions before generating the PRD
- Use the n8n-mcp `search_nodes` tool to validate node suggestions
- Include specific n8n node types in the architecture section
- Flag known n8n pitfalls (data structure, expressions, aggregation)
- Save the PRD as a file in the project directory
- Number the workflow steps clearly

### DON'T:
- Skip the clarifying questions phase
- Assume services or credentials - always ask
- Generate vague requirements ("handle errors somehow")
- Include implementation details like exact expressions or code
- Create the workflow - this PRD is INPUT for the build phase

### Quality Checklist (verify before delivering):
- [ ] Every service has a credential status (Vorhanden/Fehlt)
- [ ] Error handling is specified for each external API call
- [ ] Aggregation needs are explicitly stated
- [ ] Data flow is clear: what comes in, what goes out
- [ ] At least 3 acceptance criteria are defined
- [ ] Known n8n pitfalls are documented in Section 7

---

## Integration with Other Skills

### Build Phase (after PRD is approved):
Once the user approves the PRD, they can use the n8n-mcp tools to build:
1. `search_nodes` - Find the right nodes
2. `get_node` - Check node configuration
3. `n8n_create_workflow` - Build the workflow
4. `n8n_validate_workflow` - Validate
5. `n8n_autofix_workflow` - Auto-fix issues
6. `n8n_executions` - Debug runs

### Related Skills:
- **n8n-workflow-patterns** - Architectural patterns for the workflow design
- **n8n-node-configuration** - Detailed node setup guidance
- **n8n-expression-syntax** - Expression rules for n8n
- **n8n-validation-expert** - Validation and debugging
