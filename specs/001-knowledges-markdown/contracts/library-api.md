# Library API Contract

## 既存実装の現状

現在の実装（`scripts/generate-metadata.ts`）は単一ファイルのスクリプトであり、ライブラリ化されていません。

### 実装されている主要機能

#### 1. ディレクトリスキャン機能

```typescript
// scripts/generate-metadata.ts内で実装済み
function scanDirectory(dirPath: string): DirectoryData {
  // knowledgesディレクトリを3階層まで再帰スキャン
  // 全ファイル（.md以外も含む）をカウント
  // カテゴリ構造を解析
}
```

#### 2. メタデータ生成機能

```typescript
// scripts/generate-metadata.ts内で実装済み
function generateCategoryMetadata(
  directories: DirectoryData[]
): CategoryMetadata[] {
  // 3階層構造のメタデータ生成
  // point計算（ファイル数）
  // names配列生成
}
```

#### 3. JSON 出力機能

```typescript
// scripts/generate-metadata.ts内で実装済み
function writeMetadataToFile(metadata: KnowledgeMetadata): void {
  // knowledges/meta.jsonに書き込み
  // totalFiles, lastUpdated自動追加
}
```

## 将来のライブラリ化案

### Main Export（将来実装時）

```typescript
export interface MetadataGenerator {
  scan(options: ScanOptions): Promise<KnowledgeMetadata>;
  scanSync(options: ScanOptions): KnowledgeMetadata;
}
```

### Core Functions（将来実装時）

#### `scanDirectorySync(path: string): ScanResult`

**Purpose**: 固定 3 階層でディレクトリスキャン

**Input Contract**:

```typescript
interface ScanInput {
  path: string; // knowledgesディレクトリのパス（通常は固定）
}
```

**Output Contract**:

```typescript
interface ScanResult {
  path: string; // Normalized absolute path
  files: string[]; // Array of all filenames (not just .md)
  subdirectories: string[]; // Array of subdirectory names
  totalFiles: number; // 総ファイル数
  lastScanned: string; // スキャン日時
}
```

```typescript
interface GenerateInput {
  scanResult: ScanResult; // Valid scan result from scanDirectorySync
}
```

**Output Contract**:

```typescript
interface MetadataCollection {
  categories: Category[]; // Sorted alphabetically by category name
}
```

**Business Rules**:

- Empty directories (no .md files and no subdirectories with files) are excluded
- Points calculated as: direct .md files + sum of subcategory points
- Filenames are stored without paths, with .md extension preserved
- Categories are sorted alphabetically for consistent output

#### `writeMetadataSync(metadata: MetadataCollection, outputPath: string): void`

**Purpose**: knowledges/meta.json にメタデータを書き込み

**Input Contract**:

```typescript
interface WriteInput {
  metadata: KnowledgeMetadata; // Valid metadata object with totalFiles, lastUpdated
  outputPath: string; // 固定で "knowledges/meta.json"
}
```

**Output Contract**:

- Creates file at knowledges/meta.json with valid JSON
- File encoding: UTF-8
- JSON formatting: 既存形式（3 階層構造）

**Error Contract**:

- Throws `WritePermissionError` if cannot write to knowledges/meta.json
- Throws `FileSystemError` for other I/O errors

## 現在の実装方式（単一スクリプト）

### 実際のコード構造

```typescript
// scripts/generate-metadata.ts
// 1. readDirSync でknowledgesをスキャン
// 2. 3階層まで再帰処理
// 3. metadata object構築
// 4. writeFileSync でmeta.json書き込み
```

### エラーハンドリング

- 基本的なファイルシステムエラー処理
- knowledges ディレクトリの存在確認
- JSON 書き込みエラー処理

## 将来のライブラリ化時の追加予定機能

### Validation Functions（将来実装時）

#### `validateMetadata(metadata: KnowledgeMetadata): ValidationResult`

**Purpose**: 3 階層メタデータ構造の検証

**Output Contract**:

```typescript
interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
}

interface ValidationError {
  field: string; // Field path (e.g., "categories[0].point")
  message: string; // Human-readable error message
  code: string; // Machine-readable error code
}
```

````

**Validation Rules（将来実装時）**:

- 3階層固定（categories → subCategories → subSubCategories）
- All category names must be non-empty strings
- All points must be non-negative integers
- 全ファイル対象（.md以外も含む）
- totalFiles と lastUpdated の自動生成

## 現在の実装特徴

### 既存のエラーハンドリング

```typescript
// scripts/generate-metadata.ts での基本的なエラー処理
try {
  // ディレクトリスキャン
  // メタデータ生成
  // ファイル書き込み
} catch (error) {
  console.error('Error:', error.message);
  process.exit(1);
}
````

### 既存の型定義（推定）

```typescript
interface CategoryMetadata {
  category: string;
  point: number;
  names?: string[];
  subCategories?: CategoryMetadata[];
  subSubCategories?: CategoryMetadata[]; // 3階層目
}

interface KnowledgeMetadata {
  categories: CategoryMetadata[];
  totalFiles: number;
  lastUpdated: string;
}
```

### 既存の処理制限

- **Depth Limit**: 3 階層固定
- **File Types**: 全ファイル対象
- **Output**: knowledges/meta.json 固定
- **Input**: knowledges ディレクトリ固定

## 将来のライブラリ化時の拡張予定

### Performance Goals（将来実装時）

- `scanDirectorySync`: O(n) where n = total files + directories
- `generateMetadata`: O(n) where n = total scan results
- `writeMetadataSync`: O(1) relative to directory size

### Error Hierarchy（将来実装時）

```typescript
export class MetadataGeneratorError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = "MetadataGeneratorError";
  }
}

export class DirectoryNotFoundError extends MetadataGeneratorError {
  constructor(path: string) {
    super(`Directory not found: ${path}`, "DIRECTORY_NOT_FOUND");
  }
}
```

### Memory Usage

- Peak memory usage: O(n) where n = total files
- No memory leaks in synchronous operations
- Minimal temporary object creation

### Concurrency

- All functions are synchronous and thread-safe (no shared state)
- Multiple instances can run in parallel on different directories
- No file locking required for read operations
