# Library API Contract

## Metadata Generator Library

### Main Export

```typescript
export interface MetadataGenerator {
  scan(options: ScanOptions): Promise<MetadataCollection>;
  scanSync(options: ScanOptions): MetadataCollection;
}
```

### Core Functions

#### `scanDirectorySync(path: string): ScanResult`

**Purpose**: Synchronously scan a directory and return file/subdirectory information

**Input Contract**:

```typescript
interface ScanInput {
  path: string; // Absolute or relative path to directory
}
```

**Output Contract**:

```typescript
interface ScanResult {
  path: string; // Normalized absolute path
  files: string[]; // Array of .md filenames (not full paths)
  subdirectories: string[]; // Array of subdirectory names
  scanResults: ScanResult[]; // Recursive results for subdirectories
}
```

**Error Contract**:

- Throws `DirectoryNotFoundError` if path doesn't exist
- Throws `PermissionError` if read access denied
- Throws `InvalidPathError` if path is not a directory

#### `generateMetadata(scanResult: ScanResult): MetadataCollection`

**Purpose**: Transform scan results into metadata collection

**Input Contract**:

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

**Purpose**: Write metadata to JSON file

**Input Contract**:

```typescript
interface WriteInput {
  metadata: MetadataCollection; // Valid metadata object
  outputPath: string; // File path for output
}
```

**Output Contract**:

- Creates file at specified path with valid JSON
- File encoding: UTF-8
- JSON formatting: Compact (no pretty-printing in library function)

**Error Contract**:

- Throws `WritePermissionError` if cannot write to output path
- Throws `InvalidMetadataError` if metadata fails validation
- Throws `FileSystemError` for other I/O errors

### Validation Functions

#### `validateMetadata(metadata: MetadataCollection): ValidationResult`

**Purpose**: Validate metadata structure and business rules

**Input Contract**:

```typescript
interface MetadataCollection {
  categories: Category[];
}
```

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

**Validation Rules**:

- All category names must be non-empty strings
- All points must be non-negative integers
- All points must equal sum of direct files + subcategory points
- No duplicate category names at same level
- All names arrays must contain only .md files
- Maximum nesting depth: 10 levels (practical limit)

### Utility Functions

#### `calculatePoints(category: Category): number`

**Purpose**: Calculate total points for a category

**Input Contract**:

```typescript
interface Category {
  names?: string[];
  subCategories?: SubCategory[];
}
```

**Output Contract**:

- Returns non-negative integer
- Formula: (names?.length || 0) + sum(subCategories.map(calculatePoints))

#### `isMarkdownFile(filename: string): boolean`

**Purpose**: Check if filename has .md extension

**Input Contract**:

```typescript
interface Input {
  filename: string; // Just filename, not full path
}
```

**Output Contract**:

- Returns true if filename ends with `.md` (case-insensitive)
- Returns false otherwise

## Error Hierarchy

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

export class PermissionError extends MetadataGeneratorError {
  constructor(path: string, operation: string) {
    super(`Permission denied: ${operation} ${path}`, "PERMISSION_DENIED");
  }
}

export class ValidationError extends MetadataGeneratorError {
  constructor(message: string) {
    super(`Validation failed: ${message}`, "VALIDATION_FAILED");
  }
}
```

## Type Definitions

```typescript
export interface ScanOptions {
  baseDirectory: string;
  includeEmptyDirectories?: boolean; // default: false
  maxDepth?: number; // default: 10
  fileExtensions?: string[]; // default: ['.md']
}

export interface Category {
  category: string;
  point: number;
  names?: string[];
  subCategories?: SubCategory[];
}

export interface SubCategory extends Category {}

export interface MetadataCollection {
  categories: Category[];
}
```

## Performance Guarantees

### Time Complexity

- `scanDirectorySync`: O(n) where n = total files + directories
- `generateMetadata`: O(n) where n = total scan results
- `writeMetadataSync`: O(1) relative to directory size
- `validateMetadata`: O(n) where n = total categories

### Memory Usage

- Peak memory usage: O(n) where n = total files
- No memory leaks in synchronous operations
- Minimal temporary object creation

### Concurrency

- All functions are synchronous and thread-safe (no shared state)
- Multiple instances can run in parallel on different directories
- No file locking required for read operations
