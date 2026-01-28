---
name: azure-env-builder
description: "⚠️ Alpha (開発中) - エンタープライズ Azure 環境構築スキル。AVM 活用、VM アプリ初期化、App Service/AKS/Container Apps へのアプリデプロイ、サービス間設定連携、CI/CD 生成をサポート。Hub-Spoke, AKS, AI Foundry 等の複合アーキテクチャに対応。Bicep MCP と Microsoft Learn Docs MCP で最新スキーマを取得。"
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# Azure Environment Builder

エンタープライズ向け Azure 環境を効率的に構築するスキル。

## When to use

- エンタープライズ向け Azure 環境の新規構築や再構成
- AVM モジュールを活用した Bicep 設計・実装
- Hub-Spoke/AKS/AI Foundry など複合アーキテクチャの設計

## 🎯 機能一覧

| カテゴリ          | 機能                                                       |
| ----------------- | ---------------------------------------------------------- |
| 🏗️ アーキテクチャ | Hub-Spoke, Web+DB, AKS, AI Foundry, Proxy VM パターン      |
| 📦 AVM モジュール | 200+ Azure Verified Modules カタログ                       |
| 🖥️ VM 初期化      | Squid, Nginx, Docker, IIS 等のアプリ組み込みスクリプト     |
| � アプリデプロイ  | App Service, AKS (Helm/kubectl), Container Apps デプロイ   |
| �🔗 設定連携      | SQL/Storage/Redis 接続文字列、Managed Identity RBAC 自動化 |
| 🚀 CI/CD          | GitHub Actions / Azure Pipelines テンプレート              |
| 🔒 セキュリティ   | Private Endpoint, Firewall, NSG 自動構成                   |

## ワークフロー概要

```
1. ヒアリング (基本情報 + アーキテクチャパターン選択)
      ↓
2. MCP ツールで最新 AVM/スキーマ取得
      ↓
3. 環境フォルダ生成 (scripts/scaffold_environment.ps1)
      ↓
4. Bicep 実装 (AVM モジュール + VM 初期化スクリプト)
      ↓
5. CI/CD パイプライン生成 (GitHub Actions or Azure Pipelines)
      ↓
6. 検証 (what-if) → デプロイ → 結果記録
```

## 必須: MCP ツールの使用

**Bicep コード生成前に必ず実行すること。**

```
# 1. ベストプラクティス取得
mcp_bicep_experim_get_bicep_best_practices

# 2. AVM (Azure Verified Modules) カタログ確認
mcp_bicep_experim_list_avm_metadata

# 3. リソーススキーマ確認
mcp_bicep_experim_list_az_resource_types_for_provider(providerNamespace: "Microsoft.Network")
mcp_bicep_experim_get_az_resource_type_schema(azResourceType: "Microsoft.Storage/storageAccounts", apiVersion: "2023-05-01")

# 4. 公式ドキュメント/サンプル検索
microsoft_docs_search(query: "Private Endpoint Bicep")
microsoft_code_sample_search(query: "cloud-init CustomScriptExtension", language: "bicep")
```

## Step 1: ヒアリング

### 基本情報 (必須)

| 項目               | 確認内容                                  |
| ------------------ | ----------------------------------------- |
| サブスクリプション | ID またはログイン状態 (`az account show`) |
| 環境名             | dev / staging / prod など                 |
| リージョン         | japaneast / japanwest など                |
| デプロイ方式       | Azure CLI / Bicep                         |
| スコープ           | ResourceGroup / Subscription              |

### アーキテクチャパターン選択

→ **[references/architecture-patterns.md](references/architecture-patterns.md)** から選択

| パターン                  | 用途                              |
| ------------------------- | --------------------------------- |
| 🏢 Hub-Spoke Landing Zone | 大規模エンタープライズ、複数環境  |
| 🌐 Web + Database         | 一般的な Web アプリ (App Service) |
| ☸️ AKS Kubernetes         | コンテナ化されたマイクロサービス  |
| 🤖 AI Foundry             | AI/ML ワークロード                |
| 🔒 Proxy VM (Squid 等)    | 閉域ネットワーク、送信制御        |

### VM アプリ初期化要件

→ **[references/vm-app-scripts.md](references/vm-app-scripts.md)** 参照

| アプリ              | 対応 OS | 初期化方式                         |
| ------------------- | ------- | ---------------------------------- |
| 🦑 Squid Proxy      | Linux   | cloud-init + CustomScriptExtension |
| 🌐 Nginx Reverse    | Linux   | cloud-init                         |
| 🐳 Docker + Compose | Linux   | cloud-init                         |
| 🪟 IIS              | Windows | CustomScriptExtension (PowerShell) |

### サービス間設定連携

→ **[references/service-config-templates.md](references/service-config-templates.md)** 参照

| 連携パターン       | 設定内容                                  |
| ------------------ | ----------------------------------------- |
| App → SQL Database | 接続文字列自動生成、Managed Identity RBAC |
| App → Storage      | AccountKey または RBAC、SAS トークン      |
| App → Redis Cache  | 接続文字列、アクセスキー                  |
| App → Key Vault    | Managed Identity、シークレット参照        |
| Private Endpoint   | DNS Zone Link、NIC 自動構成               |

→ 詳細なヒアリング項目: [references/hearing-checklist.md](references/hearing-checklist.md)

## Step 2: 環境フォルダ生成

```powershell
pwsh scripts/scaffold_environment.ps1 -Environment <env> -Location <region> -DeploymentMode Bicep -DeploymentScope <scope>
```

生成物:

- `env/<env>/bicep/main.bicep`
- `env/<env>/bicep/parameters/<env>.json`
- `env/<env>/README.md`

## Step 3: Bicep 実装 (AVM 活用)

### AVM モジュール参照

→ **[references/avm-modules.md](references/avm-modules.md)** で最新バージョン確認

```bicep
// AVM モジュール使用例 (VNet)
module vnet 'br/public:avm/res/network/virtual-network:0.7.1' = {
  name: 'vnetDeployment'
  params: {
    name: 'vnet-${environment}-${location}'
    addressPrefixes: ['10.0.0.0/16']
    subnets: [
      { name: 'snet-web', addressPrefix: '10.0.1.0/24' }
      { name: 'snet-db', addressPrefix: '10.0.2.0/24' }
    ]
  }
}
```

### VM アプリ初期化 (Squid 例)

```bicep
// Squid Proxy VM with cloud-init
module squidVm 'br/public:avm/res/compute/virtual-machine:0.13.0' = {
  name: 'squidVmDeployment'
  params: {
    name: 'vm-squid-${environment}'
    vmSize: 'Standard_B2s'
    osType: 'Linux'
    imageReference: {
      publisher: 'Canonical'
      offer: '0001-com-ubuntu-server-jammy'
      sku: '22_04-lts-gen2'
      version: 'latest'
    }
    // cloud-init でアプリ初期化
    customData: loadFileAsBase64('../scripts/cloud-init-squid.yaml')
  }
}
```

→ 詳細: [references/vm-app-scripts.md](references/vm-app-scripts.md)

## Step 4: CI/CD パイプライン生成

→ **[references/cicd-templates/](references/cicd-templates/)** 参照

### GitHub Actions

```yaml
# .github/workflows/deploy-azure.yml
name: Deploy Azure Environment
on:
  push:
    branches: [main]
    paths: ["env/**/*.bicep"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - run: |
          az deployment group create \
            --resource-group ${{ vars.RESOURCE_GROUP }} \
            --template-file env/prod/bicep/main.bicep
```

## Step 5: 検証 & デプロイ

```powershell
# 検証 (what-if)
az deployment group what-if --resource-group <rg> --template-file main.bicep --parameters @parameters/<env>.json

# デプロイ
az deployment group create --resource-group <rg> --template-file main.bicep --parameters @parameters/<env>.json
```

## Step 6: 結果出力

デプロイ完了後、以下を必ず出力：

```markdown
## 🎉 デプロイ完了

| リソース        | 名前          | 状態     | 備考                  |
| --------------- | ------------- | -------- | --------------------- |
| ✅ VNet         | vnet-prod-jpe | 作成済み | Hub-Spoke             |
| ✅ Squid VM     | vm-squid-prod | 作成済み | Squid 3128 リッスン中 |
| ✅ App Service  | app-web-prod  | 作成済み | MI で SQL 接続        |
| ✅ SQL Database | sql-db-prod   | 作成済み | PE 経由アクセスのみ   |

### サービス間接続設定

| 接続元      | 接続先       | 認証方式           |
| ----------- | ------------ | ------------------ |
| App Service | SQL Database | Managed Identity   |
| App Service | Storage      | RBAC (Blob Reader) |

### Azure Portal リンク

- [リソースグループ](https://portal.azure.com/#@/resource/subscriptions/{subId}/resourceGroups/{rg}/overview)
```

## 📚 参照ファイル

### コア

| ファイル                                                                 | 用途                   |
| ------------------------------------------------------------------------ | ---------------------- |
| [references/hearing-checklist.md](references/hearing-checklist.md)       | 詳細ヒアリング項目     |
| [references/environment-template.md](references/environment-template.md) | 環境定義テンプレート   |
| [references/resource-patterns.md](references/resource-patterns.md)       | リソース別構成パターン |
| [references/review-checklist.md](references/review-checklist.md)         | レビュー確認事項       |

### 新機能

| ファイル                                                                         | 用途                                      |
| -------------------------------------------------------------------------------- | ----------------------------------------- |
| [references/architecture-patterns.md](references/architecture-patterns.md)       | Hub-Spoke, AKS, AI 等のアーキテクチャ     |
| [references/avm-modules.md](references/avm-modules.md)                           | AVM モジュールカタログ (200+)             |
| [references/vm-app-scripts.md](references/vm-app-scripts.md)                     | Squid/Nginx/Docker 等 VM 初期化スクリプト |
| [references/app-deploy-patterns.md](references/app-deploy-patterns.md)           | App Service/AKS/Container Apps デプロイ   |
| [references/service-config-templates.md](references/service-config-templates.md) | サービス間設定連携パターン                |
| [references/cicd-templates/](references/cicd-templates/)                         | GitHub Actions / Azure Pipelines          |

### スクリプト

| ファイル                         | 用途             |
| -------------------------------- | ---------------- |
| scripts/scaffold_environment.ps1 | 環境フォルダ生成 |
| scripts/validate_bicep.ps1       | Bicep 検証       |
| scripts/preview_cli.ps1          | CLI プレビュー   |
