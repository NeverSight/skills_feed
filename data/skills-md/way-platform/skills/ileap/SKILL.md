---
name: ileap
description: >-
  iLEAP technical specs for exchanging logistics emissions data
  (ISO 14083 / GLEC Framework) via the PACT protocol. Use when
  implementing iLEAP APIs, data models (ShipmentFootprint, TCE, TOC,
  HOC, TAD), PACT DataModelExtensions, or conformance testing.
  Language-agnostic.
---

# iLEAP Technical Specifications

iLEAP extends the PACT Data Exchange Protocol with logistics emissions
data types conforming to ISO 14083 and the GLEC Framework v3.1.

- **Spec**: https://sine-fdn.github.io/ileap-extension/
- **Demo API**: https://api.ileap.sine.dev

## Implementation Order

1. **PACT base**: Authentication (OpenID discovery + OAuth2 Client
   Credentials), `GET /2/footprints`, `GET /2/footprints/{id}`,
   `POST /2/events`. See `references/pact-implementation-guide.md`.
2. **iLEAP extensions**: Embed ShipmentFootprint, TOC, HOC as
   `DataModelExtension`s in ProductFootprints.
3. **TAD endpoint**: `GET /2/ileap/tad` with filtering and pagination.
4. **Conformance**: Run ACT against your server.

## Architecture Overview

### Roles

| Role | Description |
|---|---|
| Transport Service User | Purchases transport (e.g., shipper) |
| Transport Service Organizer | Provides transport, subcontracts operations (e.g., LSP) |
| Transport Operator | Carries out transport (e.g., carrier) |

### Key invariant

All numeric values are `Decimal` -- JSON strings matching
`^-?\d+(\.\d+)?$`. Never use JSON numbers for iLEAP numeric fields.

## Data Transactions

| DT | Data type | Provider | Consumer | Endpoint |
|---|---|---|---|---|
| DT#1 | ShipmentFootprint (TCEs) | Operator/Organizer | Service User | `GET /2/footprints` |
| DT#2 | TOC or HOC | Operator/Organizer | Organizer/User | `GET /2/footprints` |
| DT#3 | TAD | Operator | Organizer/User | `GET /2/ileap/tad` |

- **DT#1**: TCE-level emissions for a single shipment, wrapped in a ShipmentFootprint
- **DT#2**: Emission intensity data at TOC (transport) or HOC (hub) cluster level
- **DT#3**: Raw activity data (distance, mass, energy) for parties that cannot yet calculate emissions

## Data Model Quick Reference

### ShipmentFootprint

| Property | Type | Req | Description |
|---|---|---|---|
| `mass` | Decimal | M | Freight mass in kg |
| `volume` | Decimal | O | Freight volume in CBM |
| `shipmentId` | String | M | Shipment identifier |
| `tces` | TCE[] | M | Non-empty array of TCEs |

### TCE (Transport Chain Element)

| Property | Type | Req | Description |
|---|---|---|---|
| `tceId` | String | M | Unique TCE id |
| `prevTceIds` | String[] | O | IDs of preceding TCEs (ordering) |
| `tocId` | String | M* | TOC id (*one of tocId/hocId required) |
| `hocId` | String | M* | HOC id (*one of tocId/hocId required) |
| `shipmentId` | String | M | Shipment id |
| `mass` | Decimal | M | Freight mass in kg |
| `distance` | GLECDistance | M | Origin-destination distance |
| `transportActivity` | Decimal | M | Transport activity in tkm |
| `co2eWTW` | Decimal | M | WTW GHG emissions in kgCO2e |
| `co2eTTW` | Decimal | M | TTW GHG emissions in kgCO2e |

### TOC (Transport Operation Category)

| Property | Type | Req | Description |
|---|---|---|---|
| `tocId` | String | M | Unique TOC id |
| `mode` | TransportMode | M | Transport mode |
| `energyCarriers` | EnergyCarrier[] | M | Energy carriers (shares must sum to 1) |
| `co2eIntensityWTW` | Decimal | M | WTW intensity per transportActivityUnit |
| `co2eIntensityTTW` | Decimal | M | TTW intensity per transportActivityUnit |
| `transportActivityUnit` | String | M | `"tkm"` or `"TEUkm"` |

### HOC (Hub Operation Category)

| Property | Type | Req | Description |
|---|---|---|---|
| `hocId` | String | M | Unique HOC id |
| `hubType` | HubType | M | Hub type |
| `energyCarriers` | EnergyCarrier[] | M | Energy carriers (shares must sum to 1) |
| `co2eIntensityWTW` | Decimal | M | WTW intensity per hubActivityUnit |
| `co2eIntensityTTW` | Decimal | M | TTW intensity per hubActivityUnit |
| `hubActivityUnit` | String | M | `"tonnes"` or `"TEU"` |

### TAD (Transport Activity Data)

| Property | Type | Req | Description |
|---|---|---|---|
| `activityId` | String | M | Unique activity id |
| `consignmentIds` | String[] | M | Consignment identifiers |
| `distance` | GLECDistance | M | Origin-destination distance |
| `origin` | Location | M | Origin location |
| `destination` | Location | M | Destination location |
| `departureAt` | DateTime | M | ISO 8601 UTC departure |
| `arrivalAt` | DateTime | M | ISO 8601 UTC arrival |
| `mode` | TransportMode | M | Transport mode |

### Enum values

- **TransportMode**: `Road`, `Rail`, `Air`, `Sea`, `InlandWaterway`
- **HubType**: `Transshipment`, `StorageAndTransshipment`, `Warehouse`, `LiquidBulkTerminal`, `MaritimeContainerTerminal`
- **EnergyCarrierType**: `Diesel`, `HVO`, `Petrol`, `CNG`, `LNG`, `LPG`, `HFO`, `MGO`, `Aviation fuel`, `Hydrogen`, `Methanol`, `Electric`
- **PackagingOrTrEqType**: `Box`, `Pallet`, `Container-TEU`, `Container-FEU`, `Container`
- **Feedstock**: `Fossil`, `Natural gas`, `Grid`, `Renewable electricity`, `Cooking oil`

### JSON schemas

Located at `references/ileap-data-model/schemas/`:
- `shipment-footprint.json`, `toc.json`, `hoc.json`, `tad.json`
- `pcf-shipment-footprint.json`, `pcf-toc.json`, `pcf-hoc.json`, `pcf-tad.json`

## PACT Integration Rules

These are the most error-prone mappings when embedding iLEAP data into
PACT ProductFootprints.

### Common rules (all iLEAP types)

- `productCategoryCpc`: MUST always be `"83117"`
- `packagingEmissionsIncluded`: MUST be `false`
- `biogenicCarbonContent`: SHOULD be `"0"`
- `extensions[].specVersion`: MUST be `"2.0.0"`
- One iLEAP extension per ProductFootprint (cannot mix SF + TOC etc.)

### Per-type mapping

| Field | ShipmentFootprint | TOC | HOC |
|---|---|---|---|
| `productIds` | `urn:...:shipment:{shipmentId}` | `urn:...:toc:{tocId}` | `urn:...:hoc:{hocId}` |
| `declaredUnit` | `"ton kilometer"` | `"ton kilometer"` | `"kilogram"` |
| `unitaryProductAmount` | `sum(tces[].transportActivity)` | `"1"` | `"1000"` |
| `pCfExcludingBiogenic` | `sum(tces[].co2eWTW)` | `co2eIntensityWTW` | `co2eIntensityWTW` |
| `dataSchema` URL | `.../shipment-footprint.json` | `.../toc.json` | `.../hoc.json` |

### productIds URN format

```
urn:pathfinder:product:customcode:vendor-assigned:{type}:{id}
urn:pathfinder:product:customcode:buyer-assigned:{type}:{id}
```

Where `{type}` is `shipment`, `toc`, or `hoc`.

### dataSchema URLs

| Type | URL |
|---|---|
| ShipmentFootprint | `https://api.ileap.sine.dev/shipment-footprint.json` |
| TOC | `https://api.ileap.sine.dev/toc.json` |
| HOC | `https://api.ileap.sine.dev/hoc.json` |

See `references/pact-integration-examples.md` for complete annotated
JSON examples of each type.

## HTTP API

### Authentication

1. Discover token endpoint: `GET /.well-known/openid-configuration`
2. Obtain token: `POST /auth/token` with Basic Auth + `grant_type=client_credentials`
3. Use token: `Authorization: Bearer {token}` on all API calls

See `references/pact-implementation-guide.md` for the full auth
contract including request/response formats.

### PACT endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/2/footprints` | List ProductFootprints (with iLEAP extensions) |
| `GET` | `/2/footprints/{id}` | Get single ProductFootprint |
| `POST` | `/2/events` | Async event notifications |

Supports `$filter` query parameter (OData v4 subset) and `limit`
pagination with `Link` header.

### iLEAP endpoint

```
GET /2/ileap/tad?[filter params]&limit={n}
```

- **Filtering**: query parameters as key-value pairs (e.g., `?mode=Road`)
- **Pagination**: `limit` param + `Link: <url>; rel="next"` header
- **Response**: `{ "data": [TAD, ...] }`

### Error codes

| Code | HTTP Status | Description |
|---|---|---|
| `AccessDenied` | 403 | Invalid or missing token |
| `TokenExpired` | 401 | Expired access token |
| `BadRequest` | 400 | Malformed request |
| `NoSuchFootprint` | 404 | Footprint ID not found |
| `NotImplemented` | 400 | Unsupported filter or feature |

See `references/known-issues.md` for error code gotchas (e.g.,
`NotImplemented` is HTTP 400 not 501).

## Conformance Testing & ACT

### Conformance levels

1. **Emissions Data Conformance**: DT#1 + DT#2 (ShipmentFootprint, TOC, HOC via `/2/footprints`)
2. **Activity Data Conformance**: DT#3 (TAD via `/2/ileap/tad`)

### Test cases

| TC | Description | Endpoint | Expected |
|---|---|---|---|
| TC001 | Get ProductFootprint with ShipmentFootprint | `GET /2/footprints` | 200 + valid SF extension |
| TC002 | Get ProductFootprint with TOC | `GET /2/footprints` | 200 + valid TOC extension |
| TC003 | Get ProductFootprint with HOC | `GET /2/footprints` | 200 + valid HOC extension |
| TC004 | Get all TransportActivityData | `GET /2/ileap/tad` | 200 + valid TAD list |
| TC005 | Get filtered TAD | `GET /2/ileap/tad?mode=Road` | 200 + filtered results |
| TC006 | Get limited TAD | `GET /2/ileap/tad?limit=1` | 200 + max 1 result |
| TC007 | TAD with invalid token | `GET /2/ileap/tad` | 403 AccessDenied |
| TC008 | TAD with expired token | `GET /2/ileap/tad` | 401 TokenExpired |

> **TC008 note**: TC008 requires the server to issue short-lived tokens
> so ACT can wait for expiry. Most test servers skip this by issuing
> long-lived tokens — TC008 will then time out or fail.

### ACT (Automated Conformance Testing)

- **Web UI**: https://act.sine.dev
- **CLI**: `references/act/act.sh` -- downloads and runs binary for current architecture (arm64/x86_64)

```sh
# Run against demo API
curl -sSf https://raw.githubusercontent.com/sine-fdn/act/main/act.sh |\
  bash -s -- test -b "https://api.ileap.sine.dev" -u "hello" -p "pathfinder"
```

```sh
# Run against your own API
curl -sSf https://raw.githubusercontent.com/sine-fdn/act/main/act.sh |\
  bash -s -- test -b "<your-url>" -u "<user>" -p "<password>"
```

**GitHub Actions integration**:
```yaml
act_test:
  name: ACT Test
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - name: Run ACT
      run: |
        set -o pipefail
        curl -sSf https://raw.githubusercontent.com/sine-fdn/act/main/act.sh |\
        bash -s -- test \
        -b "${{ secrets.API_URL }}" \
        -u "${{ secrets.ACT_USER }}" \
        -p "${{ secrets.ACT_PASSWORD }}"
```

**Important ACT constraints**:
- PACT tests require a publicly reachable server — ACT delegates PACT
  tests to an external service that must reach the API over the internet
- No iLEAP-only flag — ACT always runs both PACT and iLEAP test suites
- PACT TC8 and TC18 are known failures even on the SINE reference API
  (`api.ileap.sine.dev`)

See `references/act/README.md` for full CLI options and coverage details.

## Certification

### SFC Certification Scheme extension for iLEAP Tool Providers

- **Eligibility**: must be SFC Certified + implemented DT#1 and DT#2
- **Testing**: ACT runs both PACT tests and iLEAP-specific tests
- **Mandatory**: DT#1 and DT#2 tests must pass
- **Optional**: DT#3 tests (recommended)
- **Remediation**: up to 3 attempts at 2-week intervals
- **Validity**: matches SFC Certification validity period

See `references/pilot-certification.md` for full certification process details.

## Verification with SINE Demo API

The SINE Foundation hosts a public iLEAP-conformant server for testing.

### Base URL

https://api.ileap.sine.dev

### Credentials

| client_id | client_secret | Scope |
|---|---|---|
| `hello` | `pathfinder` | Global access to all data |
| `transport_service_user` | `ileap` | ShipmentFootprints + TAD |
| `transport_service_organizer` | `ileap` | TOCs + HOCs + TAD |

### Step-by-step verification

```sh
# 1. Discover OpenID configuration
curl -s https://api.ileap.sine.dev/.well-known/openid-configuration | jq .

# 2. Obtain access token
TOKEN=$(curl -s -X POST https://api.ileap.sine.dev/auth/token \
  -u "hello:pathfinder" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" | jq -r .access_token)

# 3. List all footprints
curl -s https://api.ileap.sine.dev/2/footprints \
  -H "Authorization: Bearer $TOKEN" | jq .

# 4. Get a specific footprint by ID
curl -s https://api.ileap.sine.dev/2/footprints/91715e5e-fd0b-4d1c-8fab-76290c46e6ed \
  -H "Authorization: Bearer $TOKEN" | jq .

# 5. List transport activity data
curl -s https://api.ileap.sine.dev/2/ileap/tad \
  -H "Authorization: Bearer $TOKEN" | jq .

# 6. Filter TAD by transport mode
curl -s "https://api.ileap.sine.dev/2/ileap/tad?mode=Road" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

## Navigating the Specs

### iLEAP spec

The normative iLEAP spec is at `references/ileap-extension/specs/index.bs`
(Bikeshed format, 3291 lines).

| Section | Topic | Lines |
|---|---|---|
| `#introduction` | Overview, PACT interop | 23-120 |
| `#definitions` | ISO14083 and auxiliary terms | 125-237 |
| `#business-cases` | Business cases 1-3 | 239-312 |
| `#txns` | Data transactions DT#1-DT#3 | 315-387 |
| `#data-model` | Data types (SF, TCE, TOC, HOC, TAD) | 624-1507 |
| `#dt-utility-section` | GLECDistance, Location, enums | 1510-1897 |
| `#http-rest-api` | TAD endpoint, filtering, pagination | 1899-2050 |
| `#pcf-mapping` | PACT integration rules | 2052-2597 |
| `#conformance` | Conformance levels | 2600-2730 |
| `#appendix-b` | Example JSON (SF, TOC, HOC) | 2807-3049 |
| `#appendix-c` | Conformance test cases TC001-TC008 | 3050-3244 |

### PACT spec

The PACT v2.1.0 spec is at `references/pact-spec-v2/index.bs`
(Bikeshed format, 2520 lines).

| Section | Topic | Lines |
|---|---|---|
| `#intro` | Introduction, scope | 16-70 |
| `#terminology` | Term definitions | 73-121 |
| `#data-model` | Data model overview | 138-161 |
| `#dt-pf` | ProductFootprint properties | 163-334 |
| `#dt-carbonfootprint` | CarbonFootprint properties | 337-646 |
| `#dt-datamodelextension` | DataModelExtension | 827-852 |
| `#dt-declaredunit` | DeclaredUnit enum | 1089-1121 |
| `#api-auth` | Authentication flow | 1539-1564 |
| `#api-action-auth` | Action Authenticate | 1591-1703 |
| `#api-action-list` | Action ListFootprints | 1706-1861 |
| `#api-action-get` | Action GetFootprint | 1863-1922 |
| `#api-action-events` | Action Events | 1925-2134 |
| `#api-error-responses` | Error codes table | 2135-2277 |

### Grep patterns

```sh
# iLEAP: find a data type definition
grep -n '<dfn element>' references/ileap-extension/specs/index.bs

# iLEAP: find all required properties for a type
grep -n -A2 '<td>M$' references/ileap-extension/specs/index.bs

# iLEAP: find PACT mapping rules
grep -n 'MUST be set to\|MUST equal\|MUST contain' references/ileap-extension/specs/index.bs

# PACT: find property definitions
grep -n '<dfn>' references/pact-spec-v2/index.bs | head -40

# PACT: find all mandatory properties
grep -n '<td>M$' references/pact-spec-v2/index.bs

# PACT: find error codes
grep -n 'dfn>.*Denied\|dfn>.*Request\|dfn>.*Expired' references/pact-spec-v2/index.bs
```

## Reference Files

| File | Purpose |
|---|---|
| `references/ileap-extension/specs/index.bs` | Normative iLEAP spec (Bikeshed source) |
| `references/pact-spec-v2/index.bs` | PACT v2.1.0 spec (Bikeshed source) |
| `references/pact-implementation-guide.md` | PACT implementation steps (auth, endpoints, data model) |
| `references/known-issues.md` | Implementation gotchas and workarounds |
| `references/demo-api-guide.md` | iLEAP server implementation patterns |
| `references/openapi.json` | OpenAPI contract (non-normative) |
| `references/ileap-data-model/schemas/*.json` | JSON schemas for all iLEAP data types |
| `references/pact-data-model/schema/data-model-schema.json` | PACT base data model schema |
| `references/pact-integration-examples.md` | Annotated PACT integration JSON examples |
| `references/demo-api/` | SINE Foundation demo server source (Rust/Rocket) |
| `references/act/README.md` | ACT CLI usage, test coverage |
| `references/act/act.sh` | ACT runner script (detects arch, downloads binary) |
| `references/pilot-certification.md` | SFC certification process for iLEAP |
| `references/whitepaper-v1.md` | Strategic context only (not useful for implementation) |
