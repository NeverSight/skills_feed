---
name: openapi-specification-v3.2
description: OpenAPI Specification 3.2 — write and interpret OpenAPI descriptions (OAD), paths, operations, parameters, request/response, schema (JSON Schema 2020-12), security, and extensions. Use when authoring or validating OpenAPI 3.2 documents.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.2.0.md, scripts located at https://github.com/antfu/skills
---

# OpenAPI Specification 3.2

Agent-oriented reference for the OpenAPI Specification 3.2.0. Use when editing, generating, or validating OpenAPI descriptions (OAD).

## When to Use

- Authoring or updating OpenAPI 3.2 YAML/JSON documents
- Resolving `$ref`, `$self`, and relative URIs in multi-document OADs
- Describing paths, operations, parameters (query/path/header/cookie/querystring), request body, and responses
- Using Schema Objects (JSON Schema Draft 2020-12 dialect), components, and references
- Configuring security schemes (apiKey, http, mutualTLS, oauth2, openIdConnect) and requirements
- Working with media types, encoding (form, multipart), and examples (dataValue/serializedValue/externalValue)

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| OpenAPI Object | Root object, openapi, $self, info, servers, paths, webhooks, components, security, tags | [core-openapi-object](references/core-openapi-object.md) |
| Format & Structure | JSON/YAML, case sensitivity, rich text, OAD structure, parsing, base URI | [core-format-and-structure](references/core-format-and-structure.md) |
| Fixed & Patterned Fields | Fixed vs patterned fields, paths keys, components keys, extensions (x-) | [core-fixed-patterned-fields](references/core-fixed-patterned-fields.md) |
| Info & Metadata | Info, Contact, License objects | [core-info-metadata](references/core-info-metadata.md) |
| Server | Server Object, Server Variable, URL templating | [core-server](references/core-server.md) |
| Paths & Operations | Paths Object, Path Item, Operation Object, additionalOperations, query | [paths-and-operations](references/paths-and-operations.md) |
| Path Templating | Path templating, path parameters, matching, ABNF | [core-path-templating](references/core-path-templating.md) |
| Parameters | Parameter Object, in (path/query/header/cookie/querystring), style, schema vs content | [parameters](references/parameters.md) |
| Request Body & Media Type | Request Body, Media Type Object, sequential media types, itemSchema | [request-body-and-media-type](references/request-body-and-media-type.md) |
| Encoding Object | Encoding by name/position, contentType, style, explode, form, multipart | [core-encoding-object](references/core-encoding-object.md) |
| Media Types | Content keys, media type ranges, OpenAPI Media Type Registry | [core-media-types](references/core-media-types.md) |
| Responses | Responses Object, Response Object, headers, content, links | [responses](references/responses.md) |
| HTTP Status Codes | Response keys, default, 1XX–5XX range with X | [core-http-status-codes](references/core-http-status-codes.md) |
| Schema & Components | Schema Object (JSON Schema 2020-12), Components, $ref resolution | [schema-and-components](references/schema-and-components.md) |
| Schema JSON Schema Keywords | JSON Schema 2020-12 keywords and OAS extensions in Schema | [schema-json-schema-keywords](references/schema-json-schema-keywords.md) |
| Schema Composition & Polymorphism | allOf, oneOf, anyOf, discriminator | [schema-composition-polymorphism](references/schema-composition-polymorphism.md) |
| Data Types & Formats | JSON Schema types, format keyword, OAS dialect | [core-data-types-and-formats](references/core-data-types-and-formats.md) |
| Discriminator & XML | Discriminator Object, XML Object (nodeType, name, namespace) | [core-discriminator-and-xml](references/core-discriminator-and-xml.md) |
| Components Reuse | Reusing parameters, responses, schemas via $ref | [components-reuse](references/components-reuse.md) |
| Reference Object | $ref, summary/description override, resolution rules | [core-reference-object](references/core-reference-object.md) |
| Header Object | Response/multipart headers, style simple, Set-Cookie, Link | [core-header-object](references/core-header-object.md) |
| Example Object | dataValue, serializedValue, value, externalValue, Working with Examples | [core-example-object](references/core-example-object.md) |
| Tag & External Docs | Tag Object, External Documentation Object, parent, kind | [core-tags-and-external-docs](references/core-tags-and-external-docs.md) |
| Link Object | operationRef, operationId, parameters, requestBody | [core-link-object](references/core-link-object.md) |
| Runtime Expressions | $request, $response, $url, $method, ABNF, Link/Callback usage | [core-runtime-expressions](references/core-runtime-expressions.md) |
| Security | Security Scheme, OAuth Flows, Security Requirement Object | [security](references/security.md) |
| Security Scheme Types | apiKey, http (basic/bearer), mutualTLS, oauth2, openIdConnect | [security-scheme-types](references/security-scheme-types.md) |
| Security Requirement Object | OR/AND semantics, {} optional, [] clear, scopes | [security-requirement-object](references/security-requirement-object.md) |
| OAuth2 Flows | OAuth Flows Object, OAuth Flow Object, authorizationCode, deviceAuthorization | [security-oauth2-flows](references/security-oauth2-flows.md) |
| Callbacks & Webhooks | Callback Object, webhooks | [callbacks-and-webhooks](references/callbacks-and-webhooks.md) |
| Extensions | Specification extensions (x-), extension registries | [advanced-extensions](references/advanced-extensions.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Spec Authoring | operationId, tags, $self, components reuse, responses, security | [best-practices-spec-authoring](references/best-practices-spec-authoring.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Base URI & Resolution | $self, retrieval URI, reference resolution, parsing guidance | [advanced-base-uri-and-resolution](references/advanced-base-uri-and-resolution.md) |
| Security Filtering | Empty Paths/Path Item, Security Considerations | [advanced-security-filtering](references/advanced-security-filtering.md) |

## Key Points

- OAS 3.2 root uses `openapi: 3.2.0`; at least one of `components`, `paths`, or `webhooks` MUST be present.
- `$self` provides the document's base URI for reference resolution; use it in multi-document OADs.
- Schema Object is a superset of JSON Schema Draft 2020-12; empty schema = `true`, none = `false`.
- Parameter: use either `schema`+`style` or `content` (one Media Type); `in: "querystring"` requires `content`.
- Security at root is OR (one of the Security Requirement Objects); per-operation overrides; `{}` = optional.

<!--
Source: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.2.0.md
-->
