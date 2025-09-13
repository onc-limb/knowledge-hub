# Feature Specification: knowledges ディレクトリメタデータ生成機能

**Feature Branch**: `001-knowledges-markdown`  
**Created**: 2025 年 9 月 14 日  
**Status**: Draft  
**Input**: User description: "knowledges 配下に存在する markdown ファイルをスキャンして、メタデータを取得する機能"

## Execution Flow (main)

```
1. Parse user description from Input
   → 要求: knowledgesディレクトリ配下のMarkdownファイルをスキャンし、メタデータを生成する
2. Extract key concepts from description
   → Actors: システム, Users (知識ベース利用者)
   → Actions: スキャン, メタデータ生成, 統計計算
   → Data: Markdownファイル, ディレクトリ構造, メタデータ
   → Constraints: 特定のJSONフォーマット要求
3. No unclear aspects identified
4. Fill User Scenarios & Testing section
   → Clear user flow: ファイル変更検知 → メタデータ更新 → 統計確認
5. Generate Functional Requirements
   → All requirements are testable and specific
6. Identify Key Entities
   → Category, SubCategory, File metadata structures
7. Run Review Checklist
   → No [NEEDS CLARIFICATION] markers
   → No implementation details included
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines

- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

---

## User Scenarios & Testing

### Primary User Story

知識ベース管理者として、knowledges ディレクトリ配下の Markdown ファイルの統計情報を自動的に把握し、各カテゴリの充実度を数値で確認できるようにしたい。ファイルが追加・削除・移動された際に、メタデータが自動的に更新され、常に最新の状態を維持できる。

### Acceptance Scenarios

1. **Given** knowledges ディレクトリに新しい Markdown ファイルが追加される, **When** メタデータ生成処理が実行される, **Then** meta.json が更新され、該当カテゴリのポイントが増加し、ファイル名リストに追加される
2. **Given** 既存の Markdown ファイルが削除される, **When** メタデータ生成処理が実行される, **Then** meta.json が更新され、該当カテゴリのポイントが減少し、ファイル名リストから削除される
3. **Given** 新しいサブディレクトリと Markdown ファイルが作成される, **When** メタデータ生成処理が実行される, **Then** meta.json に新しいサブカテゴリエントリが追加される
4. **Given** カテゴリ配下に直接 Markdown ファイルとサブカテゴリが混在している, **When** メタデータ生成処理が実行される, **Then** カテゴリのポイントが直下のファイル数とサブカテゴリのポイント合計になる
5. **Given** 深い階層（10 層以上）のディレクトリ構造が存在する, **When** メタデータ生成処理が実行される, **Then** 無制限の深度でネストしたサブカテゴリ構造がメタデータに正しく反映される

### Edge Cases

- 空のディレクトリが存在する場合は？ → メタデータに含めない
- ファイル名に特殊文字（日本語、スペース）が含まれる場合は？ → そのままファイル名として記録
- ディレクトリの深度が深い場合は？ → 再帰的にサブカテゴリを作成し、無制限の深度まで対応する（パフォーマンス上の合理的な制限は実装時に考慮）

## Requirements

### Functional Requirements

- **FR-001**: システムは knowledges ディレクトリ配下をスキャンし、全ての Markdown ファイル（.md 拡張子）を検出しなければならない
- **FR-002**: システムはディレクトリ名をカテゴリとして、その直下のディレクトリ名をサブカテゴリとして再帰的に認識しなければならない
- **FR-003**: システムは各カテゴリ・サブカテゴリ配下の Markdown ファイル数をポイントとして計算しなければならない
- **FR-004**: システムはカテゴリのポイントを、直下の Markdown ファイル数とサブカテゴリのポイント合計として算出しなければならない
- **FR-005**: システムは各ディレクトリ配下の Markdown ファイル名を配列として記録しなければならない
- **FR-006**: システムは生成したメタデータを/knowledges/meta.json ファイルに保存しなければならない
- **FR-007**: システムは既存の meta.json が存在する場合、完全に置き換えなければならない
- **FR-008**: 生成される JSON は既存の形式（categories 配列、category/point/subCategories/names 構造）と互換性を保たなければならない
- **FR-009**: システムは任意の深度のディレクトリ階層に対応し、無制限にネストしたサブカテゴリ構造を再帰的に生成しなければならない

### Key Entities

- **Category**: knowledges 直下のディレクトリを表す。名前、ポイント（ファイル数統計）、サブカテゴリ配列、ファイル名配列を持つ
- **SubCategory**: カテゴリ配下のディレクトリを表す。名前、ポイント（配下の Markdown ファイル数）、ファイル名配列、さらに深い階層のサブカテゴリ配列を再帰的に持つ。階層数に制限はない
- **MetadataFile**: /knowledges/meta.json。全カテゴリとサブカテゴリの階層的な統計情報を格納する JSON ファイル

---

## Review & Acceptance Checklist

### Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
