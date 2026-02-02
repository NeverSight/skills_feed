---
name: senior-erp-estoque-consultar-disponibilidade
description: Consultar disponibilidade/saldo de estoque no ERP Senior via Senior X Platform. Use para "consultar estoque", "disponibilidade", "saldo", "estoque por deposito", "estoque reservado", "validar antes de vender", e integracoes de catalogo/checkout.
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
# Senior ERP - Estoque (Consultar Disponibilidade)

## Quando aplicar

- "consultar estoque" / "saldo" / "disponivel"
- "estoque por deposito/CD" / "estoque reservado"
- "validar disponibilidade antes de criar pedido"
- "sincronizar catalogo" / "atualizar vitrine"

## Contrato de integracao (agnostico de linguagem)

Leia `references/REFERENCE.md` para a referencia base (autenticacao, headers, seguranca, resiliencia).

## Passos

1) Confirmar definicao de "disponivel"
   - Saldo fisico vs disponivel (saldo - reservas - bloqueios).
   - Se deve considerar deposito especifico, filial/empresa, lote/validade.

2) Coletar entradas
   - Lista de itens (SKU/codigo) e quantidades desejadas.
   - Escopo: deposito/CD, filial/empresa.
   - Nivel de detalhe: apenas disponivel, ou tambem saldo/reservado.

3) Descobrir endpoint(s) no Portal Senior APIs
   - Localizar servicos do modulo ERP para consulta de estoque.
   - Identificar suporte a consulta em lote (bulk) vs item a item.
   - Identificar parametros de deposito/filial e campos retornados.

4) Executar consulta
   - Preferir consultas em lote quando disponivel.
   - Implementar paginacao/particionamento para listas grandes (ex.: batches de 50/100 SKUs).
   - Aplicar timeout e retry/backoff para 429/5xx.

5) Normalizar saida
   - Para cada SKU: `saldo`, `reservado`, `disponivel` (quando houver), `deposito`.
   - Sinalizar itens nao encontrados e ambiguidades (SKU duplicado, unidade divergente).

## Checklist de entradas

- Contexto de integracao: `base_url`, `tenant` (se aplicavel), `client_id`, token (Bearer)
- Itens: lista de SKUs/codigos
- Quantidades (se precisar validar disponibilidade para venda)
- Escopo: deposito/CD, filial/empresa

## Exemplo (cURL)

```bash
curl -X POST "${SENIOR_BASE_URL}/<path-do-endpoint>/" \
  -H "Authorization: Bearer ${SENIOR_ACCESS_TOKEN}" \
  -H "Content-type: application/json" \
  -H "client_id: ${SENIOR_CLIENT_ID}" \
  -d '{
    "deposito": "<codigo>",
    "itens": ["SKU1", "SKU2"]
  }'
```

Notas:
- Substitua `<path-do-endpoint>` pelo caminho do servico encontrado no Portal Senior APIs.

## Mapa de docs oficiais

- Portal Senior APIs (API Browser): https://api.xplatform.com.br/api-portal/pt-br/node/1
- API Authentication: https://api.xplatform.com.br/api-portal/pt-br/tutoriais/api-authentication
- Guia de API (Senior X Platform): https://dev.senior.com.br/documentacao/guia-de-api/

## Exemplos de prompts do usuario

- "Se nao tiver a skill instalada, instale `senior-erp-estoque-consultar-disponibilidade` e valide disponibilidade destes 20 SKUs no deposito X." 
- "Antes de criar o pedido, consulte o estoque e bloqueie a criacao se algum item estiver indisponivel." 
- "Sincronize estoque para o e-commerce: retorne disponivel por SKU e destaque itens nao encontrados." 
