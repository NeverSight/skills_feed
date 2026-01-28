---
name: requirements-spec-kit
description: Spec Kit を使って要件定義や仕様作成（仕様策定・仕様書作成・仕様設計を含む）を新規作成または既存仕様へ追記し、spec.md/plan.md/tasks.mdまで生成・更新する。要件定義、要件追加/変更、TDD前提の要件整理、仕様の明文化、Spec Kitのspecify/clarify/plan/tasksフロー実行が求められるときに使用。
---

# Requirements Spec Kit

## Overview

Spec Kit のリポジトリ内テンプレートとスクリプトを使い、要件定義を作成・更新して spec.md → plan.md → tasks.md を完成させる。新規作成か既存追記かを判断し、対象 SPEC を確定してから作業する。

## 決定フロー: 新規作成 or 既存追記

- ユーザー入力で即決する: SPEC-ID、spec.md パス、または「追記/既存」指示があれば追記する。
- 迷う場合は既存 SPEC を検索する: `rg -n "# 機能仕様:" specs/SPEC-*/spec.md` と主要キーワードで一致確認する。
- 一致が1件なら追記する。複数一致なら候補（SPEC-IDとタイトル）を提示して選択を求める。
- 一致が無ければ新規作成する。
- 追記時は対象 SPEC の worktree/feature ブランチで作業する（`.specify/scripts/bash/check-prerequisites.sh` は最新 SPEC を選ぶため）。

## ワークフロー（specify → clarify → plan → tasks）

### 1) specify

- `.specify/templates/commands/specify.md` を読み、記載のスクリプトを1回実行する。
- `.specify/templates/spec-template.md` を用いて spec.md を日本語で埋める。
- 新規作成時はスクリプト出力の `WORKTREE_PATH` に移動して以降の作業を行う。
- 既存追記時は該当セクションのみ更新し、見出し順・FR番号などの連番を維持する。
- TDD/テスト要求がある場合は、要件または成功基準に「自動テストが必須」である旨を明記する。

### 2) clarify

- `.specify/templates/commands/clarify.md` に従う。
- 質問は最大5つに抑え、推奨回答を提示する。
- 回答は spec.md の該当セクションへ即時反映する。

### 3) plan

- `.specify/templates/commands/plan.md` に従う。
- `.specify/memory/constitution.md` を参照し、ゲート評価を満たす。
- 出力（plan.md / research.md / data-model.md / quickstart.md / contracts/）を生成する。

### 4) tasks

- `.specify/templates/commands/tasks.md` に従う。
- TDD/テスト要求がある場合はテストタスクを必ず含める。
- tasks.md のチェックリスト形式（ID/Story/ファイルパス）を厳守する。

## 出力の報告

- 生成/更新した spec.md、plan.md、tasks.md のパスを報告する。
- 未解決の明確化が残る場合は、ユーザー回答を得てから次へ進む。
