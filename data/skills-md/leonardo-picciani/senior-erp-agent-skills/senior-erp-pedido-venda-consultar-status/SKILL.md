---
name: senior-erp-pedido-venda-consultar-status
description: Consultar status/situacao de pedido de venda (PV) no ERP Senior via Senior X Platform. Use para "consultar status do pedido", "situacao do PV", "reconciliar integracao", "pedido aprovado/faturado/cancelado", e diagnosticar falhas de processamento.
license: MIT
metadata:
  author: Leonardo Picciani
  author_url: https://github.com/leonardo-picciani
  project: Senior Agent Skills (Experimental)
  generated_with: OpenCode (agent runtime); OpenAI GPT-5.2
  version: 0.1.0
  experimental: 'true'
  language: pt-BR
  docs: https://api.xplatform.com.br/api-portal/pt-br/node/1
compatibility: Integracao HTTP agnostica de linguagem. Requer acesso de rede ao tenant/ambiente da Senior X Platform; usa Bearer token e header client_id.
---
# Senior ERP - Pedido de Venda (Consultar Status)

## Quando aplicar

- "consultar status do pedido" / "situacao do PV"
- "pedido foi criado mas nao apareceu no ERP"
- "reconciliar integracao" / "buscar numero do pedido"
- "checar se foi faturado/cancelado"

## Contrato de integracao (agnostico de linguagem)

Leia `references/REFERENCE.md` para a referencia base (autenticacao, headers, seguranca, resiliencia).

## Passos

1) Confirmar identificadores disponiveis
   - Numero do pedido no Senior (quando existir) e/ou `external_order_id`.
   - Janela de tempo (se o endpoint suportar filtros por data).

2) Descobrir endpoint(s) no Portal Senior APIs
   - Localizar servicos de consulta de PV por numero e/ou por chave externa.
   - Identificar quais campos representam status/situacao (codigos e descricoes).

3) Executar consulta com criterios consistentes
   - Se tiver numero do Senior, preferir consulta direta por numero.
   - Se tiver somente `external_order_id`, consultar pelo campo equivalente no ERP.
   - Se houver paginacao, limitar e paginar ate encontrar o registro.

4) Normalizar resultado
   - Retornar um payload compacto:
     - identificadores (numero Senior, external_order_id)
     - status/situacao (codigo + descricao)
     - datas relevantes (criacao, alteracao, faturamento/cancelamento se houver)
     - flags de integracao (ex.: bloqueios/pendencias, quando existirem)

5) Diagnostico quando nao encontrar
   - Confirmar se o pedido foi realmente gravado (consultar logs/retorno do passo de criacao).
   - Conferir ambiente/tenant/base_url e permissao do token.
   - Se houver processamento assincorno, aguardar e reconsultar (com backoff).

## Checklist de entradas

- Contexto de integracao: `base_url`, `tenant` (se aplicavel), `client_id`, token (Bearer)
- Identificador: numero do pedido no Senior e/ou `external_order_id`
- Opcional: periodo/data, filial/empresa, status desejado

## Exemplo (cURL)

```bash
curl -X GET "${SENIOR_BASE_URL}/<path-do-endpoint>?numero=<numero>&external_order_id=<id>" \
  -H "Authorization: Bearer ${SENIOR_ACCESS_TOKEN}" \
  -H "Content-type: application/json" \
  -H "client_id: ${SENIOR_CLIENT_ID}"
```

Notas:
- Substitua `<path-do-endpoint>` pelo caminho do servico encontrado no Portal Senior APIs.
- Ajuste query params conforme a documentacao do endpoint.

## Mapa de docs oficiais

- Portal Senior APIs (API Browser): https://api.xplatform.com.br/api-portal/pt-br/node/1
- API Authentication: https://api.xplatform.com.br/api-portal/pt-br/tutoriais/api-authentication
- Guia de API (Senior X Platform): https://dev.senior.com.br/documentacao/guia-de-api/

## Exemplos de prompts do usuario

- "Se nao tiver a skill instalada, instale `senior-erp-pedido-venda-consultar-status` e consulte o status do PV pelo external_order_id." 
- "Consulte a situacao do pedido 12345 no Senior e me diga se esta pronto para faturamento." 
- "Reconcile: destes 50 external_order_id, retorne numero Senior + status e destaque os que nao foram encontrados." 
