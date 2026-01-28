---
name: legal-impressum
description: Austrian Impressum (legal notice) requirements for all company types. Covers ECG, UGB, GewO, MedienG, and Offenlegungspflicht for public media.
version: 1.0.0
triggers:
  - impressum
  - legal notice
  - imprint
  - austria
  - österreich
  - ECG
  - mediengesetz
  - offenlegung
  - gesellschaftsform
---

# Austrian Impressum Requirements

> **Jurisdiction:** Austria (Österreich)
> 
> **Related Skills:**
> - [SKILL-GERMANY.md](./SKILL-GERMANY.md) - German requirements
> - [SKILL-EU.md](./SKILL-EU.md) - EU-wide requirements
> - [SKILL-WORLD.md](./SKILL-WORLD.md) - International requirements

This skill provides comprehensive guidance on Austrian Impressum (legal notice) requirements for websites and electronic media, covering all company types (Gesellschaftsformen).

---

## 1. Legal Framework Overview

| Law | German Name | Scope | Penalty |
|-----|-------------|-------|---------|
| § 5 ECG | E-Commerce-Gesetz | All commercial websites | Up to €3,000 |
| § 14 UGB | Unternehmensgesetzbuch | Firmenbuch-registered companies | Varies |
| § 63 GewO | Gewerbeordnung | Non-Firmenbuch trade businesses | Varies |
| § 24 MedienG | Mediengesetz (Impressum) | Media works | Up to €20,000 |
| § 25 MedienG | Mediengesetz (Offenlegung) | Periodical media / public websites | Up to €20,000 |
| Art. 13-14 DSGVO | Datenschutz-Grundverordnung | Privacy notice | Up to €20M or 4% |
| § 4 DLG | Dienstleistungsgesetz | Service providers | Varies |
| ODR-VO | Online Dispute Resolution | B2C online sales | Required link |

---

## 2. Quick Reference by Gesellschaftsform

| Company Type | Firmenbuch | Required Fields | Special Notes |
|--------------|------------|-----------------|---------------|
| Einzelunternehmen (not registered) | No | Name, address, trade, chamber | § 63 GewO applies |
| Einzelunternehmen e.U. | Yes | Firm name, FB-Nr, court, address | § 14 UGB applies |
| OG (Offene Gesellschaft) | Yes | Firm, FB-Nr, court, all partners | Partners' names required |
| KG (Kommanditgesellschaft) | Yes | Firm, FB-Nr, court, Komplementäre | Kommanditisten optional |
| GmbH | Yes | Firm, FB-Nr, court, capital, directors | Stammkapital required |
| GmbH & Co KG | Yes | Both entities' details | Dual disclosure |
| AG (Aktiengesellschaft) | Yes | Firm, FB-Nr, court, capital, Vorstand | Grundkapital required |
| SE (Europäische Gesellschaft) | Yes | Firm, FB-Nr, court, capital, board | EU company form |
| GesBR | No | All partners' names, addresses | Civil law partnership |
| Genossenschaft | Yes | Firm, FB-Nr, court, Vorstand | Cooperative |
| Verein | ZVR | Name, ZVR-Zahl, address, Vorstand | Association register |

---

## 3. Required Fields by Law

### 3.1 E-Commerce-Gesetz (§ 5 ECG)

Applies to **all commercial websites**:

| Field | Description | Required |
|-------|-------------|----------|
| Name/Firma | Full legal name or company name | ✓ |
| Geographic address | Physical address (no P.O. Box) | ✓ |
| Email | Contact email address | ✓ |
| Phone | Contact phone (if available) | Optional but recommended |
| Firmenbuch number | FN XXXXXX + court (if applicable) | ✓ if registered |
| Aufsichtsbehörde | Supervisory authority (if regulated) | ✓ if applicable |
| Kammer/Berufsverband | Chamber membership (trade businesses) | ✓ if applicable |
| Berufsrecht | Professional regulations, access link | ✓ if regulated profession |
| UID-Nummer | VAT ID (if VAT registered) | ✓ if applicable |
| Unternehmensgegenstand | Business purpose | ✓ |

### 3.2 Unternehmensgesetzbuch (§ 14 UGB)

Additional requirements for **Firmenbuch-registered companies** on all business letters, including websites:

| Field | Description |
|-------|-------------|
| Firma | Exact registered company name |
| Rechtsform | Legal form (GmbH, AG, OG, KG, etc.) |
| Sitz | Registered seat (city) |
| Firmenbuchnummer | FN number with registration court |
| Firmenbuchgericht | Court where registered (e.g., "LG Wien") |
| Kapital | Share capital for GmbH/AG (optional but common) |
| Liquidation | "in Liquidation" if applicable |

### 3.3 Gewerbeordnung (§ 63 GewO)

For **trade businesses NOT in Firmenbuch**:

| Field | Description |
|-------|-------------|
| Name | Full name of owner |
| Standort | Business location |
| Gewerbe | Trade/business type |
| Behörde | Issuing authority (Bezirkshauptmannschaft) |
| Kammer | WKO membership (Bundesland) |

---

## 4. All Gesellschaftsformen - Detailed Templates

### 4.1 Einzelunternehmen (Not Firmenbuch-registered)

```
IMPRESSUM

Max Mustermann
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@mustermann.at

Gewerbe: Handel mit Waren aller Art
Gewerbebehörde: Magistrat der Stadt Wien

Mitglied der WKO Wien
Berufsrecht: Gewerbeordnung 1994 (www.ris.bka.gv.at)

UID-Nr.: ATU12345678
```

### 4.2 Einzelunternehmen e.U. (Firmenbuch-registered)

```
IMPRESSUM

Max Mustermann e.U.
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@mustermann.at

Firmenbuchnummer: FN 123456a
Firmenbuchgericht: Handelsgericht Wien
Sitz: Wien

Unternehmensgegenstand: Handel mit Waren aller Art

Mitglied der WKO Wien
Berufsrecht: Gewerbeordnung 1994 (www.ris.bka.gv.at)

UID-Nr.: ATU12345678
```

### 4.3 Offene Gesellschaft (OG)

```
IMPRESSUM

Mustermann & Partner OG
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@mustermann-partner.at

Firmenbuchnummer: FN 123456g
Firmenbuchgericht: Handelsgericht Wien
Sitz: Wien

Gesellschafter:
- Max Mustermann
- Maria Musterfrau

Unternehmensgegenstand: Unternehmensberatung

Mitglied der WKO Wien
UID-Nr.: ATU12345678
```

### 4.4 Kommanditgesellschaft (KG)

```
IMPRESSUM

Mustermann KG
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@mustermann-kg.at

Firmenbuchnummer: FN 123456k
Firmenbuchgericht: Handelsgericht Wien
Sitz: Wien

Komplementär(e):
- Max Mustermann (unbeschränkt haftend)

Unternehmensgegenstand: Handel mit Waren aller Art

Mitglied der WKO Wien
UID-Nr.: ATU12345678
```

### 4.5 GmbH (Gesellschaft mit beschränkter Haftung)

```
IMPRESSUM

Muster GmbH
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@muster-gmbh.at

Firmenbuchnummer: FN 123456z
Firmenbuchgericht: Handelsgericht Wien
Sitz: Wien
Stammkapital: EUR 35.000,–

Geschäftsführer: Max Mustermann

Unternehmensgegenstand: IT-Dienstleistungen

Mitglied der WKO Wien
UID-Nr.: ATU12345678
```

### 4.6 GmbH & Co KG

```
IMPRESSUM

Muster GmbH & Co KG
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@muster-kg.at

Firmenbuchnummer: FN 123456d
Firmenbuchgericht: Handelsgericht Wien
Sitz: Wien

Komplementärin: Muster Verwaltungs GmbH
  Firmenbuchnummer: FN 654321z
  Firmenbuchgericht: Handelsgericht Wien
  Geschäftsführer: Max Mustermann

Unternehmensgegenstand: Handel und Dienstleistungen

Mitglied der WKO Wien
UID-Nr.: ATU12345678
```

### 4.7 Aktiengesellschaft (AG)

```
IMPRESSUM

Muster AG
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@muster-ag.at

Firmenbuchnummer: FN 123456m
Firmenbuchgericht: Handelsgericht Wien
Sitz: Wien
Grundkapital: EUR 70.000,–

Vorstand: Mag. Max Mustermann (Vorsitzender)
Aufsichtsratsvorsitzender: Dr. Klaus Beispiel

Unternehmensgegenstand: Holding und Beteiligungen

Mitglied der WKO Wien
UID-Nr.: ATU12345678
```

### 4.8 Europäische Gesellschaft (SE)

```
IMPRESSUM

Muster SE
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@muster-se.eu

Firmenbuchnummer: FN 123456s
Firmenbuchgericht: Handelsgericht Wien
Sitz: Wien
Grundkapital: EUR 120.000,–

Vorstand: Max Mustermann (CEO)

Unternehmensgegenstand: Europäische Handelsgesellschaft

UID-Nr.: ATU12345678
```

### 4.9 Gesellschaft bürgerlichen Rechts (GesBR)

```
IMPRESSUM

Mustermann & Partner GesBR
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@mustermann-partner.at

Gesellschafter:
- Max Mustermann, Musterstraße 1, 1010 Wien
- Maria Musterfrau, Beispielgasse 2, 1020 Wien

Unternehmensgegenstand: Beratungsdienstleistungen

UID-Nr.: ATU12345678
```

### 4.10 Genossenschaft (eGen/SCE)

```
IMPRESSUM

Muster Genossenschaft eGen
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@muster-gen.at

Firmenbuchnummer: FN 123456v
Firmenbuchgericht: Handelsgericht Wien
Sitz: Wien

Vorstand:
- Max Mustermann (Obmann)
- Maria Musterfrau (Obmann-Stellvertreterin)

Unternehmensgegenstand: Förderung der Mitglieder

Mitglied des ÖGV
UID-Nr.: ATU12345678
```

### 4.11 Verein

```
IMPRESSUM

Musterverein
Musterstraße 1
1010 Wien
Österreich

Tel.: +43 1 234 5678
E-Mail: office@musterverein.at

ZVR-Zahl: 123456789

Vorstand:
- Max Mustermann (Obmann)
- Maria Musterfrau (Schriftführerin)
- Klaus Beispiel (Kassier)

Vereinszweck: Förderung von Kunst und Kultur
```

---

## 5. Öffentliches Medium - Full Offenlegungspflicht

### 5.1 "Kleine" vs "Große" Website

| Type | Definition | Disclosure Level |
|------|------------|------------------|
| **Kleine Website** | Self-presentation only, no public opinion influence | Simplified (name, address, purpose) |
| **Große Website** | Content influences public opinion | Full Offenlegungspflicht |

### 5.2 When is a Website "Groß"?

A website is considered a "große Website" (public medium) if it:

- Contains editorial/journalistic content
- Publishes news, opinions, or commentary
- Hosts a blog with public interest topics
- Provides information beyond pure self-presentation
- Is capable of influencing public opinion

**Examples:**
- News portals
- Political blogs
- Industry news sites
- Commentary/opinion platforms

### 5.3 Full Offenlegungspflicht Requirements (§ 25 MedienG)

For periodical electronic media and "große" websites:

| Requirement | Description |
|-------------|-------------|
| **Medieninhaber** | Name/firm of media owner |
| **Sitz/Wohnort** | Registered seat or residence |
| **Unternehmensgegenstand** | Business purpose |
| **Vertretungsbefugte Organe** | Authorized representatives (directors, board) |
| **Aufsichtsrat** | Supervisory board members (if applicable) |
| **Eigentumsverhältnisse** | Complete ownership structure |
| **Beteiligungen** | All shareholdings (direct and indirect) |
| **Stille Beteiligungen** | Silent partnerships |
| **Treuhandverhältnisse** | Trust relationships |
| **Stifter/Begünstigte** | Foundation founders and beneficiaries |
| **Grundlegende Richtung** | Editorial direction statement |

### 5.4 Grundlegende Richtung (Editorial Direction)

Required statement describing the fundamental editorial direction:

```
GRUNDLEGENDE RICHTUNG

[Beispiel für ein Unternehmensblog:]
Diese Website dient der Information über Produkte und Dienstleistungen
der Muster GmbH sowie der Berichterstattung über Branchenentwicklungen
im Bereich IT und Digitalisierung. Die redaktionelle Verantwortung liegt
bei der Geschäftsführung.

[Beispiel für Nachrichtenportal:]
Unabhängiges Nachrichtenportal mit Fokus auf Wirtschaft, Technologie
und Politik. Überparteilich und der journalistischen Objektivität
verpflichtet.
```

### 5.5 Complete Offenlegung Template

```
OFFENLEGUNG gemäß § 25 Mediengesetz

MEDIENINHABER UND HERAUSGEBER:
Muster GmbH
Musterstraße 1
1010 Wien

Firmenbuchnummer: FN 123456z
Firmenbuchgericht: Handelsgericht Wien

UNTERNEHMENSGEGENSTAND:
IT-Dienstleistungen und Softwareentwicklung

GESCHÄFTSFÜHRUNG:
Mag. Max Mustermann

GESELLSCHAFTER UND EIGENTUMSVERHÄLTNISSE:
- Max Mustermann (60%)
- Maria Musterfrau (40%)

Es bestehen keine stillen Beteiligungen oder Treuhandverhältnisse.

GRUNDLEGENDE RICHTUNG:
Informationsportal über IT-Trends und digitale Transformation.
Unabhängige Berichterstattung über Technologie-Themen mit Fokus
auf den österreichischen Markt.

KONTAKT:
E-Mail: redaktion@muster-gmbh.at
Tel.: +43 1 234 5678
```

---

## 6. Additional Required Notices

### 6.1 Privacy Notice (DSGVO)

Link to separate Datenschutzerklärung required with:
- Controller identity
- DPO contact (if applicable)
- Processing purposes
- Legal basis
- Data categories
- Recipients
- Retention periods
- Data subject rights
- Complaint right (Datenschutzbehörde)

### 6.2 Cookie Notice (TKG 2021)

Required consent mechanism for non-essential cookies.

### 6.3 ODR Link (for B2C)

Required for businesses selling to consumers online:

```
Online-Streitbeilegung gemäß Art. 14 Abs. 1 ODR-VO:
Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung 
(OS) bereit: https://ec.europa.eu/consumers/odr/
```

---

## 7. Compliance Checklist

### Basic Website (All Commercial Sites)

- [ ] Company name/owner name
- [ ] Physical address
- [ ] Email address
- [ ] Phone number (recommended)
- [ ] Firmenbuch number + court (if registered)
- [ ] Business purpose
- [ ] VAT ID (if applicable)
- [ ] Chamber membership (if trade)
- [ ] Professional regulations link (if regulated)
- [ ] Privacy notice link
- [ ] Cookie consent (if applicable)
- [ ] ODR link (if B2C online sales)

### Public Media Website (Offenlegungspflicht)

All basic requirements PLUS:
- [ ] Complete ownership structure
- [ ] All direct/indirect shareholdings
- [ ] Silent partnerships
- [ ] Trust relationships
- [ ] Foundation details (if applicable)
- [ ] Grundlegende Richtung statement
- [ ] Herausgeber (publisher) name

---

## 8. Penalties

| Violation | Maximum Penalty |
|-----------|-----------------|
| Missing/incomplete Impressum (ECG) | €3,000 |
| Missing/incomplete Impressum (MedienG) | €20,000 |
| Missing Offenlegung (MedienG) | €20,000 |
| DSGVO violations | Up to €20M or 4% of global turnover |

---

## 9. Resources

- **WKO Impressum Generator**: https://www.wko.at/service/wirtschaftsrecht-gewerberecht/ecg-service
- **WKO Impressum Guide**: https://www.wko.at/internetrecht/website-impressum
- **USP Impressumspflicht**: https://www.usp.gv.at/
- **RIS (Legal texts)**: https://www.ris.bka.gv.at/

---

## Credits & Attribution

This skill is part of the webconsulting.at skills collection.

Sources: WKO, USP.gv.at, Austrian Federal Legal Information System (RIS)
