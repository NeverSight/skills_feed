---
name: afp-product-builder
description: Build valid AFP products by composing on-chain PredictionProductV1, extended metadata DAG, and API-backed resolution rules. Use when creating or validating AFP product JSON for Forecastathon, selecting public data sources, or preparing IPFS pinning and registration.
compatibility: Requires Python 3.12+, afp-sdk, internet access, and an IPFS pinning endpoint (Filebase or IPFS node).
metadata:
  author: autonity
  version: "0.1.0"
---

# AFP Product Builder

Use this skill to produce a complete, valid product specification for the
Forecastathon competition, including extended metadata that can be pinned to
IPFS as a DAG-CBOR encoded DAG.

## Inputs to gather first

- Network: bakerloo or mainnet.
- Builder address (Forecastathon-registered).
- Product type: time series (scalar) or event (binary or ternary).
- Data source: public API URL and fields to extract.
- Start time and earliest FSP submission time (UTC ISO 8601).
- Min and max price band (unleveraged products only).
- Symbol and description.

## Forecastathon constraints (must enforce)

- Required contract addresses:
  - Bakerloo: oracleAddress `0x72EeD9f7286292f119089F56e3068a3A931FCD49`,
    collateralAsset `0xDEfAaC81a079533Bf2fb004c613cc2870cF0A5b5`.
  - Mainnet: oracleAddress `0x06CaDDDf6CC08048596aE051c8ce644725219C73`,
    collateralAsset `0xAE2C6c29F6403fDf5A31e74CC8bFd1D75a3CcB8d`.
- Builder must be a registered Forecastathon participant.
- startTime must be at least two full working days after PR submission.
- Products are unleveraged and must define minPrice and maxPrice.
- Extended metadata must be pinned on IPFS and conform to standard schemas.
- API source must be valid and freely accessible.

## Build the on-chain product (PredictionProductV1)

Use camelCase field names inside `product`:

- product.base.metadata.builder (EVM checksum address)
- product.base.metadata.symbol (A-Z0-9, 1-16 chars)
- product.base.metadata.description
- product.base.oracleSpec.oracleAddress (required per network)
- product.base.oracleSpec.fsvDecimals, fspAlpha, fspBeta, fsvCalldata
- product.base.collateralAsset (required per network)
- product.base.startTime (UTC ISO 8601, Z)
- product.base.pointValue
- product.base.priceDecimals
- product.base.extendedMetadata (CID, filled after pinning)
- product.expirySpec.earliestFSPSubmissionTime (UTC ISO 8601, Z)
- product.expirySpec.tradeoutInterval
- product.minPrice < product.maxPrice

## Build extended metadata (snake_case)

Extended metadata fields are `outcome_space`, `outcome_point`, `oracle_config`,
and `oracle_fallback`. These are pinned on IPFS and referenced by CID.

### Outcome space and point

Time series (scalar):

- outcome_space: OutcomeSpaceTimeSeries
  - fsp_type: "scalar"
  - description
  - base_case.condition and base_case.fsp_resolution
  - edge_cases (optional)
  - units, source_name, source_uri
  - frequency: daily, weekly, fortnightly, semimonthly, monthly, quarterly, yearly
  - history_api_spec (optional for backing data)
- outcome_point: OutcomePointTimeSeries
  - fsp_type: "scalar"
  - observation.reference_date and observation.release_date (YYYY-MM-DD)

Event (binary or ternary):

- outcome_space: OutcomeSpace
  - fsp_type: "binary" or "ternary"
  - description
  - base_case.condition and base_case.fsp_resolution
  - edge_cases (optional)
- outcome_point: OutcomePointEvent
  - fsp_type: "binary" or "ternary"
  - outcome (specific candidate or yes/no outcome)

Template variables in conditions must resolve against outcome_point fields.
Example: `{outcome}` for events, `{observation.release_date}` for time series.

### Oracle config

Manual resolution:

- oracle_config: OracleConfig
  - description
  - project_url (optional)

API-backed resolution:

- oracle_config: OracleConfigPrototype1
  - description
  - project_url (optional)
  - evaluation_api_spec: ApiSpecJSONPath
    - spec_variant: "product-fsv"
    - url, date_path, value_path
    - date_format_type: iso_8601 | unix_timestamp | custom
    - timestamp_scale if unix timestamps are ms
    - auth_param_location: none | query | header
    - auth_param_name / auth_param_prefix if needed

For time series, `history_api_spec` (OutcomeSpaceTimeSeries) should use
`spec_variant: "underlying-history"` when you include it.

### Oracle fallback

- oracle_fallback.fallback_time must be at least 7 days after
  earliestFSPSubmissionTime.
- oracle_fallback.fallback_fsp must be within [minPrice, maxPrice].

## API spec guidance

- Use JSONPath strings that select parallel arrays for dates and values.
- Prefer APIs that return ISO 8601 dates or UNIX timestamps to avoid custom
  parsing.
- Verify the URL is reachable (HEAD request succeeds).
- Prefer no-auth or free-access endpoints for Forecastathon.
- See references/api-sources.md for vetted examples.

## IPFS pinning (DAG-CBOR required)

Extended metadata must be pinned as a DAG-CBOR DAG, not a single JSON blob.
The AFP SDK handles this automatically by encoding and pinning each component
and the root DAG:

```python
import afp

app = afp.AFP(
    rpc_url=AUTONITY_RPC_URL,
    authenticator=afp.PrivateKeyAuthenticator(PRIVATE_KEY),
    ipfs_api_url=IPFS_API_URL,
    ipfs_api_key=IPFS_API_KEY,
)
product_api = app.Product()

spec = product_api.validate(product_dict)
pinned = product_api.pin(spec)  # builds and pins DAG-CBOR
```

If you build the DAG manually, ensure you store it as dag-cbor (e.g.,
`ipfs dag put` default store codec) and include schema CIDs for each component.

## Validation and output

1) Use `Product.validate` or `Product.validate_json` to enforce schemas.
2) Ensure business rules and Forecastathon constraints pass.
3) Use `Product.dump_json` for canonical JSON output.

```python
import afp

product_api = afp.AFP(...).Product()
spec = product_api.validate(product_dict)
pinned = product_api.pin(spec)
product_json = product_api.dump_json(pinned)
```

## Deliverables

- Complete product JSON with `extendedMetadata` CID filled in.
- Clear explanation of outcome_space resolution and data source.
- Validation checklist confirmation (see references/validation-checklist.md).

## References

- Public API options and JSONPath examples: references/api-sources.md
- Validation checklist and constraints: references/validation-checklist.md
