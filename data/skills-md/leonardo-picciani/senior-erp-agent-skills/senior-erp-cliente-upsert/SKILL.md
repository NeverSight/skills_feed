---
name: senior-erp-cliente-upsert
description: Criar ou atualizar cadastro de cliente no ERP Senior via Senior X Platform (upsert). Use para "cadastro de cliente", "atualizar cliente", "criar cliente", "cliente PJ/PF", "CNPJ/CPF", "enderecos", "integracao Senior ERP", e fluxos que exigem deduplicacao e validacao antes de gravar.
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
# Senior ERP - Cliente Upsert

## Quando aplicar

- "criar cliente" / "cadastrar cliente" / "cadastro de cliente"
- "atualizar dados do cliente" / "alterar cadastro"
- "upsert cliente" (criar se nao existe, atualizar se existe)
- "integrar clientes do e-commerce/CRM para o Senior"

## Contrato de integracao (agnostico de linguagem)

Leia `references/REFERENCE.md` para a referencia base (autenticacao, headers, seguranca, resiliencia, idempotencia).

## Passos

1) Confirmar o objetivo e o escopo do cadastro
   - PJ vs PF, campos obrigatorios, regra de negocio (ex.: cliente ativo/inativo, tipo de contribuinte).
   - Confirmar quais identificadores devem ser usados para deduplicacao (ex.: CNPJ/CPF + filial/empresa, ou codigo externo).

2) Coletar entradas minimas e validar
   - Identificador: CNPJ/CPF (quando aplicavel) e/ou codigo externo.
   - Razao social/nome, email/telefone, enderecos (cobranca/entrega), inscricoes (quando aplicavel).
   - Normalizar formatos (somente digitos para CNPJ/CPF/CEP; caixa/acentos conforme padrao do cliente).
   - Se houver PII, evitar ecoar dados completos em logs/saidas.

3) Descobrir o endpoint correto no Portal Senior APIs
   - Usar o API Browser/Portal para localizar o servico do modulo ERP relacionado a "clientes"/"cadastros".
   - Identificar o fluxo suportado:
     - consultar por identificador (para deduplicacao)
     - criar
     - atualizar

4) Executar deduplicacao antes de gravar
   - Consultar se o cliente ja existe usando o identificador acordado.
   - Se existir, planejar update parcial (patch) ou update total conforme o endpoint.
   - Se nao existir, planejar create.

5) Pedir confirmacao explicita antes de alterar dados (mutacao)
   - Mostrar um resumo compacto do que sera criado/atualizado (sem expor PII alem do necessario).

6) Executar chamada(s) de API
   - Incluir headers obrigatorios (Authorization Bearer, Content-type, client_id).
   - Aplicar timeout e retry/backoff para 429/5xx conforme `references/REFERENCE.md`.
   - Tratar erros de validacao retornando mensagens acionaveis (campo + motivo), sem vazar tokens.

7) Retornar resultado normalizado
   - Identificador do registro no Senior (quando retornado) e o identificador externo usado.
   - O que foi criado/atualizado (lista curta de campos), e qualquer aviso relevante.
   - Se falhar: status/erro + recomendacao do proximo passo (ex.: corrigir campo, tentar novamente, checar permissao).

## Checklist de entradas

- Contexto de integracao: `base_url`, `tenant` (se aplicavel), `client_id`, token (Bearer)
- Identificador de deduplicacao: CNPJ/CPF e/ou `external_id`
- Dados basicos: nome/razao social, tipo (PF/PJ)
- Contatos: email, telefone
- Enderecos: entrega/cobranca (logradouro, numero, bairro, cidade, UF, CEP)
- Preferencias: criar vs atualizar, update parcial vs total (se o endpoint exigir)

## Exemplo (cURL)

```bash
curl -X POST "${SENIOR_BASE_URL}/<path-do-endpoint>/" \
  -H "Authorization: Bearer ${SENIOR_ACCESS_TOKEN}" \
  -H "Content-type: application/json" \
  -H "client_id: ${SENIOR_CLIENT_ID}" \
  -d '{
    "external_id": "<id-externo>",
    "cpf_cnpj": "<somente-digitos>",
    "nome": "<nome-ou-razao-social>",
    "enderecos": [
      {
        "tipo": "entrega",
        "cep": "<somente-digitos>",
        "logradouro": "<...>",
        "numero": "<...>",
        "cidade": "<...>",
        "uf": "<UF>"
      }
    ]
  }'
```

Notas:
- Substitua `<path-do-endpoint>` pelo caminho do servico encontrado no Portal Senior APIs.
- O shape do JSON depende do endpoint; use este exemplo apenas como esqueleto.

## Mapa de docs oficiais

- Portal Senior APIs (API Browser): https://api.xplatform.com.br/api-portal/pt-br/node/1
- API Authentication: https://api.xplatform.com.br/api-portal/pt-br/tutoriais/api-authentication
- Guia de API (Senior X Platform): https://dev.senior.com.br/documentacao/guia-de-api/
- Como obter bearer token (suporte): https://suporte.senior.com.br/hc/pt-br/articles/9482493522196-HCM-API-Como-obter-bearer-token-para-utilizar-na-chamada-de-APIs

## Exemplos de prompts do usuario

- "Se nao tiver a skill instalada, instale `senior-erp-cliente-upsert` e cadastre este cliente (PJ) no Senior com deduplicacao por CNPJ." 
- "Atualize o cadastro do cliente pelo CNPJ e ajuste o endereco de entrega; antes, me mostre um resumo e peca confirmacao." 
- "Integre esta lista de clientes do CRM para o Senior; reporte quantos criados vs atualizados e os erros por validacao." 
