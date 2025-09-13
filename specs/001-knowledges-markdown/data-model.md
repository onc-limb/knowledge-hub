# Data Model: knowledges ディレクトリメタデータ生成機能

## エンティティ設計

### Category (カテゴリ)

knowledges 直下のディレクトリを表現するエンティティ。

**フィールド**:

```typescript
interface Category {
  category: string; // ディレクトリ名
  point: number; // 直下のファイル数 + サブカテゴリのポイント合計
  names?: string[]; // 直下のMarkdownファイル名配列 (optional)
  subCategories?: SubCategory[]; // サブカテゴリ配列 (optional)
}
```

**バリデーションルール**:

- `category`: 空文字列不可、ファイルシステム有効名
- `point`: 0 以上の整数、計算値（手動設定不可）
- `names`: .md 拡張子のファイル名のみ含む
- `subCategories`: 再帰的な階層構造をサポート

**計算ルール**:

```
point = names.length + sum(subCategories.map(sub => sub.point))
```

### SubCategory (サブカテゴリ)

カテゴリ配下のディレクトリを表現するエンティティ。Category と同じ構造を持つ再帰的構造。

**フィールド**:

```typescript
interface SubCategory {
  category: string; // サブディレクトリ名
  point: number; // 配下のファイル数 + さらに深いサブカテゴリのポイント合計
  names?: string[]; // 配下のMarkdownファイル名配列 (optional)
  subCategories?: SubCategory[]; // さらに深い階層のサブカテゴリ (optional)
}
```

**バリデーションルール**:

- Category と同じルールを適用
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
