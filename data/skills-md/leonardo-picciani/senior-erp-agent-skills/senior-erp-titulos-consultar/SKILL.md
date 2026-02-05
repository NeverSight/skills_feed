---
name: senior-erp-titulos-consultar
description: Consultar titulos financeiros (contas a receber/pagar) no ERP Senior via Senior X Platform. Use para "titulos", "contas a receber", "contas a pagar", "boletos", "baixar/consultar status", "extrato financeiro", "inadimplencia", e integracoes de conciliacao.
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
# Senior ERP - Titulos (Consultar)

## Quando aplicar

- "consultar titulos" / "contas a receber" / "contas a pagar"
- "status de boleto" / "titulo em aberto" / "titulo baixado"
- "extrato financeiro" / "conciliacao" / "inadimplencia"
- "buscar titulos por cliente" / "por periodo" / "por nosso numero"

## Contrato de integracao (agnostico de linguagem)

Leia `references/REFERENCE.md` para a referencia base (autenticacao, headers, seguranca, resiliencia).

## Passos

1) Confirmar o recorte do job
   - Receber vs pagar.
   - Filtros: cliente/fornecedor, periodo, situacao (aberto/baixado/vencido), filial/empresa.
   - Campos desejados: valor, vencimento, pagamentos, documento (nosso numero/linha digitavel quando aplicavel).

2) Descobrir endpoint(s) no Portal Senior APIs
   - Localizar servicos do modulo ERP/financeiro para consulta de titulos.
   - Identificar suporte a filtros e paginacao.

3) Executar consulta com paginacao segura
   - Definir limite por pagina e iterar ate completar (ou ate limite acordado).
   - Aplicar timeout e retry/backoff para 429/5xx.

4) Normalizar e retornar
   - Retornar lista compacta com:
     - identificadores do titulo
     - parte (cliente/fornecedor) quando aplicavel
     - valor, vencimento, situacao/status
     - datas relevantes (emissao/baixa) quando existirem
   - Agregar totals (ex.: soma em aberto, soma vencida) quando fizer sentido.

5) Cuidados de dados
   - Titulos podem conter dados financeiros sensiveis; evitar vazar em logs.
   - Se for exportar, mascarar quando solicitado (ex.: documento).

## Checklist de entradas

- Contexto de integracao: `base_url`, `tenant` (se aplicavel), `client_id`, token (Bearer)
- Tipo: receber vs pagar
- Filtros: periodo, parte (cliente/fornecedor), situacao/status
- Paginacao: limite por pagina, maximo de paginas (quando necessário)

## Exemplo (cURL)

```bash
curl -X GET "${SENIOR_BASE_URL}/<path-do-endpoint>?tipo=receber&data_ini=<YYYY-MM-DD>&data_fim=<YYYY-MM-DD>&status=aberto&limit=100&page=1" \
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

- "Se nao tiver a skill instalada, instale `senior-erp-titulos-consultar` e liste titulos em aberto por cliente no periodo." 
- "Traga os titulos vencidos dos ultimos 30 dias e some o total em atraso." 
- "Reconcilie: compare estes pagamentos do banco com os titulos no Senior e destaque divergencias." 
