# Data Model: knowledges ディレクトリメタデータ生成機能（既存実装ベース）

## 既存実装の構造

### CategoryMetadata (既存のインターフェース)

knowledges 配下のディレクトリを表現するエンティティ。既に実装済み。

**フィールド**:

```typescript
interface CategoryMetadata {
  category: string; // ディレクトリ名
  point: number; // 再帰的にカウントされた全ファイル数
  names?: string[]; // 直下のファイル名配列 (optional)
  subCategories?: CategoryMetadata[]; // サブカテゴリ配列 (optional)
  subSubCategories?: CategoryMetadata[]; // サブサブカテゴリ配列 (optional) - 既存実装
}
```

**既存の特徴**:

- `point`: 再帰的にカウントされた全ファイル数（.md ファイル限定ではない）
- `names`: 直下のファイル名（拡張子制限なし）
- **3 レベル階層**: `subSubCategories` まで対応済み
- **固定深度**: 現在は 3 レベルまでの制限あり

### KnowledgeMetadata (既存のルートエンティティ)

全体のメタデータ構造を表現するエンティティ。

**フィールド**:

```typescript
interface KnowledgeMetadata {
  categories: CategoryMetadata[]; // カテゴリ配列
  totalFiles: number; // 全ファイル数（meta.jsonを除く）
  lastUpdated: string; // 最終更新日時（ISO文字列）
}
```

**既存の特徴**:

- `totalFiles`: meta.json 以外の全ファイル数
- `lastUpdated`: 生成時のタイムスタンプ
- 再帰の深度制限なし（実装上は合理的な制限を設ける場合あり）

### MetadataCollection (メタデータコレクション)

全体のメタデータ構造を表現するルートエンティティ。

**フィールド**:

```typescript
interface MetadataCollection {
  categories: Category[]; // カテゴリ配列
}
```

**バリデーションルール**:

- `categories`: 重複する category 名不可
- ソート順: アルファベット順（安定した出力のため）

## データフロー

### 入力データ

```
knowledges/
├── ai/
│   └── 機械学習/
│       ├── LightningCLIとは.md
│       └── Lightningのモジュール.md
├── aws/
│   ├── ec2/
│   └── s3/
├── go.md
└── scrum.md
```

### 中間データ構造

スキャン処理中の一時的なデータ構造:

```typescript
interface ScanResult {
  directoryPath: string;
  markdownFiles: string[];
  subdirectories: string[];
  scanResults: ScanResult[]; // 再帰的な構造
}
```

### 出力データ

```json
{
  "categories": [
    {
      "category": "ai",
      "point": 2,
      "subCategories": [
        {
          "category": "機械学習",
          "point": 2,
          "names": ["LightningCLIとは.md", "Lightningのモジュール.md"]
        }
      ]
    },
    {
      "category": "aws",
      "point": 0,
      "subCategories": [
        {
          "category": "ec2",
          "point": 0
        },
        {
          "category": "s3",
          "point": 0
        }
      ]
    }
  ]
}
```

## 状態遷移

### スキャンプロセス状態

```
Initial → Scanning → Processing → Complete
   ↓         ↓          ↓         ↓
 Start    Read Dir   Calculate   Write JSON
           ↓         Points        ↓
        Recurse      ↓           Success
                  Validate
```

### エラー状態

```
Any State → Error State
    ↓
  Log Error
    ↓
  Cleanup
    ↓
  Exit with code
```

## 制約・不変条件

### ビジネスルール

1. **階層整合性**: 親カテゴリのポイント = 直下ファイル数 + 全サブカテゴリポイント合計
2. **ファイル一意性**: 同一ディレクトリ内でのファイル名重複なし
3. **拡張子制限**: .md 拡張子のファイルのみ対象
4. **空ディレクトリ除外**: Markdown ファイルもサブカテゴリも存在しないディレクトリは出力に含めない

### 技術制約

1. **ファイルシステム制約**: OS 固有のファイル名制限に準拠
2. **JSON 制約**: 有効な JSON 形式、循環参照なし
3. **パフォーマンス制約**: メモリ使用量はファイル数に線形比例
4. **エンコーディング**: UTF-8 での日本語ファイル名サポート

## 型定義

```typescript
// Core types
export interface Category {
  category: string;
  point: number;
  names?: string[];
  subCategories?: SubCategory[];
}

export interface SubCategory extends Category {
  // SubCategoryはCategoryと同じ構造（再帰的）
}

export interface MetadataCollection {
  categories: Category[];
}

// Utility types
export interface ScanOptions {
  baseDirectory: string;
  includeEmptyDirectories?: boolean;
  fileExtensions?: string[];
}

export interface ScanResult {
  path: string;
  files: string[];
  subdirectories: ScanResult[];
}
```
