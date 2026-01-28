---
name: terraform-aws-annotated-reference
description: 単一のTerraform AWSリソースに対する全プロパティ解説付きリファレンステンプレートを生成する。ユーザーがリソース名（例：aws_s3_bucket, aws_lambda_function）を指定すると、Providerスキーマに基づいた正確な属性一覧とAWS公式ドキュメントに基づく解説を含むテンプレートを出力する。「aws_xxxのテンプレートを作成して」「aws_xxxの全プロパティを教えて」などのリクエストで使用。
---

# Terraform AWS Annotated Reference

単一AWSリソースの全プロパティに詳細解説付きのリファレンステンプレートを生成する。

## 前提条件

以下のMCP serverが必須。利用不可の場合は警告・設定方法を表示し作業を終了する。

**必須MCP server:**
- `awslabs.terraform-mcp-server` - AWSプロバイダードキュメント・実装例の検索
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

## 重要な原則

**スキーマが信頼の源泉（Source of Truth）**

`terraform providers schema -json` から取得したスキーマを正とする。MCPサーバーのドキュメントはスキーマに含まれない補足情報（説明文、設定可能な値の詳細等）の取得に使用する。

**Web検索の禁止**

インターネット検索は使用しない。情報取得はMCPサーバーのみを使用する。

## ワークフロー

### 1. 入力の確認

ユーザーから以下を取得:
- **リソース名** (必須): `aws_cloudwatch_log_group` など
- **AWS Providerバージョン** (任意): 指定がなければ最新バージョンを使用
- **出力先ディレクトリ** (任意): 指定がなければ `${プロジェクトルート}/.local/terraform-aws-annotated-reference` を使用

**入力例:**

自然言語での指定:
```
aws_s3_bucketのテンプレートを作成して
aws_lambda_functionのテンプレートを ./terraform/refs に出力して
aws_iam_role（v5.80.0）のリファレンスを ./docs/terraform に作成して
```

引数形式での指定:
```
/terraform-aws-annotated-reference aws_s3_bucket
/terraform-aws-annotated-reference aws_lambda_function --output ./terraform/refs
/terraform-aws-annotated-reference aws_iam_role --version 5.80.0 --output ./docs/terraform
```

バージョン未指定時はTerraform Registry APIから最新バージョンを取得:
```bash
curl -s "https://registry.terraform.io/v1/providers/hashicorp/aws" | jq -r '.version'
```

### 2. スキーマの存在確認と取得

`${出力先ディレクトリ}/${provider_version}/schema.json` が既に存在するか確認:

```bash
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_ROOT}/.local/terraform-aws-annotated-reference}"
SCHEMA_FILE="${OUTPUT_DIR}/${provider_version}/schema.json"
if [[ -f "$SCHEMA_FILE" ]]; then
  echo "スキーマファイルが存在します。スキップします。"
else
  echo "スキーマを取得します..."
  # 以下のステップ2a, 2bを実行
fi
```

#### 2a. スキーマ取得用Terraform設定の作成（スキーマが存在しない場合のみ）

`${出力先ディレクトリ}/${provider_version}/` ディレクトリにプロバイダー設定を作成:

```hcl
# ${出力先ディレクトリ}/${provider_version}/providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "{provider_version}"
    }
  }
}
```

#### 2b. プロバイダースキーマの取得（スキーマが存在しない場合のみ）

```bash
cd ${OUTPUT_DIR}/${provider_version}
terraform init
terraform providers schema -json > schema.json
```

### 3. スキーマからリソース情報を抽出

スキーマJSONから対象リソースの情報を抽出:

```bash
jq '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["{リソース名}"]' schema.json
```

抽出対象:
- `.block.attributes` - 通常の属性
- `.block.block_types` - ネストブロック（vpc_config等）

### 4. 属性の分類

スキーマの各属性を以下のルールで分類:

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

### 5. ドキュメント情報の取得

`aws-knowledge-mcp-server`を使用して補足情報を取得:
- `aws___search_documentation` でAWS公式ドキュメントを検索
- `aws___read_documentation` で詳細情報を取得

### 6. テンプレート生成

[references/template_example.md](references/template_example.md) のフォーマットに従いテンプレートを生成。

**必須要件:**
- スキーマから取得した入力可能な全属性を記載
- ネストブロック（block_types）も漏れなく記載
- 各プロパティにコメントで解説を記載
- AWS公式ドキュメントのURLは実在するもののみ記載
- 推測や誤った情報は絶対に記載しない

**ファイルヘッダー:**
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

### 7. 抜け漏れ検証

スキーマの属性一覧と生成したテンプレートを照合:

```bash
# スキーマの入力可能属性一覧
jq -r '.provider_schemas["registry.terraform.io/hashicorp/aws"].resource_schemas["{リソース名}"].block.attributes | to_entries[] | select(.value.optional == true) | .key' schema.json | sort

# テンプレートに含まれる属性一覧
grep -E "^\s{2}[a-z_]+ =" {リソース名}.tf | sed 's/=.*//' | tr -d ' ' | sort
```

両者を比較し、差分がないことを確認。

### 8. ファイル出力

出力先: `${出力先ディレクトリ}/${provider_version}/${リソース名}.tf`

例（デフォルト）: `./.local/terraform-aws-annotated-reference/6.28.0/aws_cloudwatch_log_group.tf`
例（カスタム）: `./terraform/references/6.28.0/aws_cloudwatch_log_group.tf`

## 品質要件

1. **正確性**: スキーマを信頼の源泉とし、MCPサーバーは補足情報として使用
2. **網羅性**: スキーマの全入力可能属性（attributes + block_types）を記載
3. **検証可能性**: 記載するURLは全て実在するものであること
4. **除外の明確性**: computed only属性はAttributes Referenceセクションに記載
