---
name: openapi-specification-v2
description: OpenAPI (Swagger) 2.0 specification for describing REST APIs. Use when writing, validating, or interpreting Swagger 2.0 specs, generating clients/docs, or working with path/operation/parameter/response/schema/security definitions.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/OAI/OpenAPI-Specification, scripts located at https://github.com/antfu/skills
---

OpenAPI Specification 2.0 (formerly Swagger 2.0) defines a JSON/YAML format for describing RESTful APIs: paths, operations, parameters, responses, schemas, and security. Use this skill when creating or editing Swagger 2.0 specs, validating structure, or generating code/documentation from them.

> The skill is based on OpenAPI Specification 2.0, generated at 2026-01-30.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Format and Structure | Document format, file structure, data types | [core-format-and-structure](references/core-format-and-structure.md) |
| Fixed and Patterned Fields | Fixed vs patterned field names in the schema | [core-fixed-patterned-fields](references/core-fixed-patterned-fields.md) |
| Swagger Object | Root document, required/optional fields, extensions | [core-swagger-object](references/core-swagger-object.md) |
| Info and Metadata | Info, Contact, License objects | [core-info-metadata](references/core-info-metadata.md) |
| Tags and External Docs | Tag Object, External Documentation Object | [core-tags-and-external-docs](references/core-tags-and-external-docs.md) |
| Reference Object | $ref, JSON Pointer, same-document and external file references | [core-reference-object](references/core-reference-object.md) |
| Data Types and Formats | Primitives, format table, validation, file type | [core-data-types-and-formats](references/core-data-types-and-formats.md) |
| MIME Types | consumes/produces, RFC 6838, examples | [core-mime-types](references/core-mime-types.md) |
| HTTP Status Codes | Response keys, default response, IANA/RFC 7231 | [core-http-status-codes](references/core-http-status-codes.md) |
| Path Templating | Curly braces, path parameters, name matching | [core-path-templating](references/core-path-templating.md) |
| Header Object | Response header definition (type, format, items, validation) | [core-header-object](references/core-header-object.md) |
| Headers Object | Container for response headers (name → Header Object) | [core-headers-object](references/core-headers-object.md) |
| Items Object | Non-body array items (parameters, headers) | [core-items-object](references/core-items-object.md) |
| Example Object | Response examples by MIME type | [core-example-object](references/core-example-object.md) |

## Paths and Operations

| Topic | Description | Reference |
|-------|-------------|-----------|
| Paths and Operations | Paths Object, Path Item, Operation Object | [paths-and-operations](references/paths-and-operations.md) |
| Path Item $ref | External path definition, conflict behavior | [path-item-ref](references/path-item-ref.md) |

## Parameters and Responses

| Topic | Description | Reference |
|-------|-------------|-----------|
| Parameters | Parameter locations (path, query, header, body, formData) | [parameters](references/parameters.md) |
| collectionFormat | csv, ssv, tsv, pipes, multi and where they apply | [parameters-collection-format](references/parameters-collection-format.md) |
| Parameters Definitions (Reuse) | Root-level parameters, reuse via $ref | [parameters-definitions-reuse](references/parameters-definitions-reuse.md) |
| Responses | Responses Object, Response Object | [responses](references/responses.md) |
| Responses Definitions (Reuse) | Root-level responses, reuse via $ref | [responses-definitions-reuse](references/responses-definitions-reuse.md) |

## Schemas and Definitions

| Topic | Description | Reference |
|-------|-------------|-----------|
| Schema and Definitions | Schema Object, Definitions, composition, polymorphism | [schema-and-definitions](references/schema-and-definitions.md) |
| Schema JSON Schema Keywords | JSON Schema Draft 4 subset and Swagger-specific fields | [schema-json-schema-keywords](references/schema-json-schema-keywords.md) |

## Security

| Topic | Description | Reference |
|-------|-------------|-----------|
| Security | Security Definitions, Security Scheme | [security](references/security.md) |
| Security Requirement Object | Applying security at root/operation, OR/AND logic | [security-requirement-object](references/security-requirement-object.md) |
| Scopes Object | OAuth2 scope name → description | [security-scopes-object](references/security-scopes-object.md) |
| Basic and API Key | basic and apiKey Security Scheme | [security-basic-apikey](references/security-basic-apikey.md) |
| OAuth2 Flows | implicit, password, application, accessCode and required URLs | [security-oauth2-flows](references/security-oauth2-flows.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Spec Authoring | operationId, tags, responses, parameters, definitions, security | [best-practices-spec-authoring](references/best-practices-spec-authoring.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Vendor Extensions | x- prefix, value types, where allowed | [advanced-vendor-extensions](references/advanced-vendor-extensions.md) |
| Security Filtering | Empty Paths, empty Path Item for access control | [advanced-security-filtering](references/advanced-security-filtering.md) |
| Extensions and XML | XML Object for schema properties | [advanced-extensions-and-xml](references/advanced-extensions-and-xml.md) |
