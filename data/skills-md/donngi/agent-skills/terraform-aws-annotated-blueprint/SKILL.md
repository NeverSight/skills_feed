---
name: terraform-aws-annotated-blueprint
description: 全プロパティに詳細な解説が付いたTerraform AWSテンプレートを作成する。ユーザーが「/terraform-annotated-aws-blueprint」コマンドで構築したいインフラの概要を入力すると、Terraform Providerスキーマに基づいた正確な属性一覧と、AWS公式ドキュメントに基づく解説を含むテンプレートを生成する。
---

# Terraform AWS Annotated Blueprint

要求された構成のTerraformテンプレートを全プロパティに詳細な解説付きで生成するスキル。

## 前提条件

以下のMCP serverが必須。利用不可の場合は警告・利用しているAI Agentごとの設定方法を表示し作業を終了する。

**必須MCP server:**
- `awslabs.terraform-mcp-server` - AWSプロバイダードキュメント検索・AWS Well-Architectedガイダンス・セキュリティスキャン
- `aws-knowledge-mcp-server` - AWS公式ドキュメント参照用

**MCP server設定例:**
```json
{
  "aws-knowledge-mcp-server": {
    "command": "uvx",
    "args": ["fastmcp", "run", "https://knowledge-mcp.global.api.aws"]
  },
  "awslabs.terraform-mcp-server": {
    "command": "uvx",
    "args": ["awslabs.terraform-mcp-server@latest"],
    "env": {
      "FASTMCP_LOG_LEVEL": "ERROR"
    }
  }
}
```

**MCP serverの役割・使い所**
- `awslabs.terraform-mcp-server`:
  - AWSプロバイダードキュメント・実装例の検索
  - AWS Well-Architectedガイダンスの参照（設計判断に活用）
  - Checkovによるセキュリティスキャン（生成後の検証）
- `aws-knowledge-mcp-server` - AWS公式ドキュメント参照

## 重要な原則

**スキーマが信頼の源泉（Source of Truth）**

`terraform providers schema -json` から取得したスキーマを正とする。MCPサーバーのドキュメントはスキーマに含まれない補足情報（説明文、設定可能な値の詳細等）の取得に使用する。

**Web検索の禁止**

インターネット検索は使用しない。情報取得はMCPサーバーのみを使用する。

## ワークフロー

### 1. 入力の理解

ユーザーから `/terraform-aws-annotated-blueprint {概要}` 形式で入力を受け取り、作成したいTerraformテンプレートの要件を把握する。

### 2. 作業計画の作成

チェックボックス付きの計画書を `{プロジェクトルート}/.local/terraform-aws-annotated-blueprint/${provider_version}/` に出力する。

**計画書の必須内容:**
- スキーマ取得（キャッシュがなければ実行）
- 構築が必要なリソース一覧の生成
- 各リソースの全プロパティをカテゴリ別にannotation付きで記載
- 抜け漏れ検証
- awslabs.terraform-mcp-serverを用いたCheckovによるセキュリティスキャン および 指摘事項の修正

**質問タグのルール:**
独自の判断はせず、意思決定が必要な際は必ずユーザーに質問をする。

判断が必要な箇所は、作業計画書内に `[🤔Question]` タグで質問を追加し、`[✅Answer]` タグで回答フィールドを作成する。
1つのタグにつき質問は1つ。複数の質問はタグを分割する。

```markdown
[🤔Question] ここに質問を記載

[✅Answer]
```

### 3. 計画書の更新

ユーザーからの回答を踏まえて計画書を更新する。質問と回答のペアは削除しない。

### 4. 作業実行

ユーザーから承認を得てから作業を開始する。計画書のチェックボックスを更新しながら進める。

## スキーマ取得方法

`${プロジェクトルート}/.local/terraform-aws-annotated-blueprint/${provider_version}/schema.json` が既に存在するか確認:

```bash
SCHEMA_FILE="${PROJECT_ROOT}/.local/terraform-aws-annotated-blueprint/${provider_version}/schema.json"
if [[ -f "$SCHEMA_FILE" ]]; then
  echo "スキーマファイルが存在します。スキップします。"
else
  echo "スキーマを取得します..."
  # 以下の手順を実行
fi
```

**スキーマが存在しない場合:**

1. プロバイダー設定を作成:
```hcl
# ${プロジェクトルート}/.local/terraform-aws-annotated-blueprint/${provider_version}/providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "{provider_version}"
    }
  }
}
```

2. スキーマを取得:
```bash
cd ${プロジェクトルート}/.local/terraform-aws-annotated-blueprint/${provider_version}
terraform init
terraform providers schema -json > schema.json
```

**スキーマからリソース情報を抽出:**
```bash
jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["{リソース名}"]' schema.json
```

## テンプレート生成ルール

### 必須要件

- スキーマから取得した入力可能な全属性を記載
- ネストブロック（block_types）も漏れなく記載
- 各プロパティにコメントで解説を記載
- AWS公式ドキュメントのURLは実在するもののみ記載
- 推測や誤った情報は絶対に記載しない
- 利用しないプロパティも削除せずにコメントとして残す

### ファイルヘッダー

```hcl
#---------------------------------------------------------------
# {リソース表示名}
#---------------------------------------------------------------
#
# {どのようなAWSリソースをプロビジョニングするかの説明}
#
# AWS公式ドキュメント:
#   - {ドキュメント名}: {URL}
#
# Terraform Registry:
#   - {URL}
#
# Provider Version: {version}
# Generated: {YYYY-MM-DD}
# NOTE: 本テンプレートは生成時点の情報に基づきAIが生成しています。
#       情報が古くなっている可能性、誤りを含む可能性があるため、
#       正確な最新仕様は公式ドキュメントを参照してください。
#
#---------------------------------------------------------------
```

### 属性の分類

**テンプレートに含める属性（入力可能）:**
- `optional: true` を持つ属性
- `required: true` を持つ属性

**テンプレートから除外する属性（computed only）:**
- `computed: true` かつ `optional` がない属性
- 例: `arn`, `id`, `tags_all`

**分類確認コマンド:**
```bash
# 入力可能な属性一覧
jq -r '.block.attributes | to_entries[] | select(.value.optional == true) | .key' <<< "$SCHEMA"

# computed only属性一覧
jq -r '.block.attributes | to_entries[] | select(.value.computed == true and .value.optional != true) | .key' <<< "$SCHEMA"
```

### フォーマット

テンプレートの詳細なフォーマットは [references/template_example.md](references/template_example.md) を参照。

### 抜け漏れ検証

各リソースのテンプレート生成後、スキーマの属性一覧と照合:

```bash
# スキーマの入力可能属性一覧
jq -r '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["{リソース名}"].block.attributes | to_entries[] | select(.value.optional == true) | .key' schema.json | sort

# テンプレートに含まれる属性一覧
grep -E "^\s{2}[a-z_]+ =" {リソース名}.tf | sed 's/=.*//' | tr -d ' ' | sort
```

両者を比較し、差分がないことを確認。

## ファイル分割ルール

以下の内容は別ファイルに分割する：

- **variables.tf**: 入力変数（variable）
- **locals.tf**: ローカル変数（locals）
- **data.tf**: データソース（data）
- **versions.tf**: Terraformバージョン制約とrequired_providers（terraformブロック）
- **providers.tf**: プロバイダー設定（providerブロック）

## ファイル生成単位

基本は1リソースにつき1ファイル。ただし以下は1ファイルにまとめる：

- IAM role定義（aws_iam_role, aws_iam_policy, aws_iam_role_policy_attachment）
- Security groupとそのegress/ingress rule
- Route tableとそのルール
- Target groupとそのattachment（aws_lb_target_group, aws_lb_target_group_attachment）

**ファイル命名規則:**
- ファイル名に `aws` は含めない
- 単一リソース: `lambda.tf`
- 複数の同一リソース: `lambda_parser.tf`, `lambda_archiver.tf`

## 依存関係の扱い

- リソース参照による暗黙的な依存関係を活用する
- 明示的な`depends_on`は、暗黙的な依存関係では表現できない場合にのみ使用
- 不要な`depends_on`はコードの可読性を下げるため避ける

## その他ルール

- IAM policyの定義はdata resourceを使わず、リソースに直接jsonencodeしたポリシーを記載する

## Provider最新バージョン取得

version指定がない場合は以下でTerraform Registry APIから最新バージョンを取得：

```bash
curl -s "https://registry.terraform.io/v1/providers/hashicorp/aws" | jq -r '.version'
```
