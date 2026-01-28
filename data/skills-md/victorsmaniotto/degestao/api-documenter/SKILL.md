---
name: api-documenter
description: Geração de documentação de APIs no padrão OpenAPI/Swagger a partir de código PHP/Laravel. Usar para documentar endpoints, gerar specs OpenAPI 3.0, criar documentação interativa, documentar autenticação, schemas de request/response, e integrar com ferramentas como Swagger UI, Redoc, ou Stoplight.
---

# API Documenter

Skill para documentação de APIs RESTful no padrão OpenAPI 3.0.

## Estrutura OpenAPI

```yaml
openapi: 3.0.3
info:
  title: Nome da API
  description: Descrição detalhada
  version: 1.0.0
  contact:
    name: Equipe de Desenvolvimento
    email: dev@empresa.com

servers:
  - url: https://api.empresa.com/v1
    description: Produção
  - url: https://staging-api.empresa.com/v1
    description: Staging
  - url: http://localhost:8000/api/v1
    description: Local

tags:
  - name: Contratos
    description: Gerenciamento de contratos
  - name: Clientes
    description: Gerenciamento de clientes

paths:
  # Endpoints aqui

components:
  # Schemas, Security, etc.
```

## Documentando Endpoints

### CRUD Completo

```yaml
paths:
  /contracts:
    get:
      tags:
        - Contratos
      summary: Listar contratos
      description: Retorna lista paginada de contratos com filtros opcionais
      operationId: listContracts
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/PerPageParam'
        - name: status
          in: query
          description: Filtrar por status
          schema:
            type: string
            enum: [pending, active, completed, cancelled]
        - name: client_id
          in: query
          description: Filtrar por cliente
          schema:
            type: integer
        - name: date_from
          in: query
          description: Data inicial (YYYY-MM-DD)
          schema:
            type: string
            format: date
        - name: date_to
          in: query
          description: Data final (YYYY-MM-DD)
          schema:
            type: string
            format: date
      responses:
        '200':
          description: Lista de contratos
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ContractPaginatedResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      tags:
        - Contratos
      summary: Criar contrato
      description: Cria um novo contrato no sistema
      operationId: createContract
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateContractRequest'
            example:
              client_id: 1
              event_date: "2024-06-15"
              value: 5000.00
              notes: "Evento corporativo"
      responses:
        '201':
          description: Contrato criado com sucesso
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ContractResponse'
        '422':
          $ref: '#/components/responses/ValidationError'

  /contracts/{id}:
    get:
      tags:
        - Contratos
      summary: Obter contrato
      operationId: getContract
      parameters:
        - $ref: '#/components/parameters/ContractId'
      responses:
        '200':
          description: Detalhes do contrato
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ContractResponse'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      tags:
        - Contratos
      summary: Atualizar contrato
      operationId: updateContract
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/ContractId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateContractRequest'
      responses:
        '200':
          description: Contrato atualizado
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ContractResponse'
        '404':
          $ref: '#/components/responses/NotFound'
        '422':
          $ref: '#/components/responses/ValidationError'

    delete:
      tags:
        - Contratos
      summary: Excluir contrato
      operationId: deleteContract
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/ContractId'
      responses:
        '204':
          description: Contrato excluído com sucesso
        '404':
          $ref: '#/components/responses/NotFound'
```

## Components (Schemas)

```yaml
components:
  schemas:
    # Request Schemas
    CreateContractRequest:
      type: object
      required:
        - client_id
        - event_date
        - value
      properties:
        client_id:
          type: integer
          description: ID do cliente
          example: 1
        event_date:
          type: string
          format: date
          description: Data do evento
          example: "2024-06-15"
        value:
          type: number
          format: float
          minimum: 0.01
          description: Valor do contrato
          example: 5000.00
        status:
          type: string
          enum: [pending, active]
          default: pending
        notes:
          type: string
          maxLength: 1000
          description: Observações
          nullable: true

    UpdateContractRequest:
      type: object
      properties:
        event_date:
          type: string
          format: date
        value:
          type: number
          format: float
          minimum: 0.01
        status:
          type: string
          enum: [pending, active, completed, cancelled]
        notes:
          type: string
          nullable: true

    # Response Schemas
    Contract:
      type: object
      properties:
        id:
          type: integer
          example: 1
        client_id:
          type: integer
          example: 1
        event_date:
          type: string
          format: date
          example: "2024-06-15"
        event_date_formatted:
          type: string
          example: "15/06/2024"
        value:
          type: number
          format: float
          example: 5000.00
        value_formatted:
          type: string
          example: "R$ 5.000,00"
        status:
          type: string
          enum: [pending, active, completed, cancelled]
        status_label:
          type: string
          example: "Pendente"
        notes:
          type: string
          nullable: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
        client:
          $ref: '#/components/schemas/Client'

    ContractResponse:
      type: object
      properties:
        data:
          $ref: '#/components/schemas/Contract'

    ContractPaginatedResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Contract'
        meta:
          $ref: '#/components/schemas/PaginationMeta'
        links:
          $ref: '#/components/schemas/PaginationLinks'

    # Pagination
    PaginationMeta:
      type: object
      properties:
        current_page:
          type: integer
        from:
          type: integer
        last_page:
          type: integer
        per_page:
          type: integer
        to:
          type: integer
        total:
          type: integer

    PaginationLinks:
      type: object
      properties:
        first:
          type: string
          format: uri
        last:
          type: string
          format: uri
        prev:
          type: string
          format: uri
          nullable: true
        next:
          type: string
          format: uri
          nullable: true

    # Error Schemas
    ValidationError:
      type: object
      properties:
        message:
          type: string
          example: "The given data was invalid."
        errors:
          type: object
          additionalProperties:
            type: array
            items:
              type: string
          example:
            client_id: ["O campo cliente é obrigatório."]
            value: ["O valor deve ser maior que zero."]

  # Parameters
  parameters:
    ContractId:
      name: id
      in: path
      required: true
      description: ID do contrato
      schema:
        type: integer

    PageParam:
      name: page
      in: query
      description: Número da página
      schema:
        type: integer
        default: 1
        minimum: 1

    PerPageParam:
      name: per_page
      in: query
      description: Itens por página
      schema:
        type: integer
        default: 15
        minimum: 1
        maximum: 100

  # Responses
  responses:
    Unauthorized:
      description: Não autenticado
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                example: "Unauthenticated."

    NotFound:
      description: Recurso não encontrado
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                example: "Contrato não encontrado."

    ValidationError:
      description: Erro de validação
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ValidationError'

  # Security
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: Token JWT obtido via login

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
```

## Integração Laravel com Annotations

```php
/**
 * @OA\Get(
 *     path="/api/contracts",
 *     tags={"Contratos"},
 *     summary="Listar contratos",
 *     @OA\Parameter(ref="#/components/parameters/PageParam"),
 *     @OA\Response(
 *         response=200,
 *         description="Lista de contratos",
 *         @OA\JsonContent(ref="#/components/schemas/ContractPaginatedResponse")
 *     )
 * )
 */
public function index()
{
    // ...
}
```

## Exportação

```bash
# Gerar spec com l5-swagger
php artisan l5-swagger:generate

# Validar spec
npx @stoplight/spectral-cli lint openapi.yaml

# Gerar cliente
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./sdk
```
