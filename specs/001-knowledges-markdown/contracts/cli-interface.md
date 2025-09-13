# CLI Interface Contract

## Command Specification

### Basic Usage

```bash
npx tsx scripts/generate-metadata.ts
```

### Arguments

- なし（固定で knowledges ディレクトリをスキャン）

### Options

- 現在の実装ではオプション引数なし（シンプルな単一機能）
- 将来追加予定: `--help`, `--version`, `--output` など

## Input Contract

### Directory Structure Requirements

```
knowledges/
├── category1/              # レベル1: カテゴリ
│   ├── file1.md
│   ├── file2.md
│   └── subcategory1/       # レベル2: サブカテゴリ
│       ├── file3.md
│       └── subsubcategory1/ # レベル3: サブサブカテゴリ
│           └── file4.md
└── category2/
    └── file5.md
```

### File Requirements

- **File Extensions**: 全ファイル対象（.md ファイル以外も含む）
- **File Names**: UTF-8 encoded, OS filesystem-compatible names
- **Directory Names**: Valid filesystem directory names, UTF-8 support
- **Depth Limit**: 3 階層まで（categories → subCategories → subSubCategories）

### Access Requirements

- Read access to target directory and all subdirectories
- Write access to output file location
- Sufficient disk space for output file

## Output Contract

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "categories": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/Category"
      }
    },
    "totalFiles": {
      "type": "integer",
      "minimum": 0
    },
    "lastUpdated": {
      "type": "string",
      "format": "date-time"
    }
  },
  "required": ["categories", "totalFiles", "lastUpdated"],
  "definitions": {
    "Category": {
      "type": "object",
      "properties": {
        "category": {
          "type": "string",
          "minLength": 1
        },
        "point": {
          "type": "integer",
          "minimum": 0
        },
        "names": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "subCategories": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/SubCategory"
          }
        }
      },
      "required": ["category", "point"]
    },
    "SubCategory": {
      "type": "object",
      "properties": {
        "category": {
          "type": "string",
          "minLength": 1
        },
        "point": {
          "type": "integer",
          "minimum": 0
        },
        "names": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "subSubCategories": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/SubSubCategory"
          }
        }
      },
      "required": ["category", "point"]
    },
    "SubSubCategory": {
      "type": "object",
      "properties": {
        "category": {
          "type": "string",
          "minLength": 1
        },
        "point": {
          "type": "integer",
          "minimum": 0
        },
        "names": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "required": ["category", "point"]
    }
  }
}
```

### Success Response

- **Exit Code**: 0
- **Stdout**: 実行完了メッセージ
- **File Output**: Valid JSON written to knowledges/meta.json

### Error Response

- **Exit Code**: Non-zero
- **Stderr**: Error message with context
- **File Output**: No file written or partial file cleaned up

## Example Interactions

### Successful Execution

```bash
$ npx tsx scripts/generate-metadata.ts
Metadata generated successfully.
Written to: knowledges/meta.json
```

### Error Cases

```bash
# TypeScript実行エラー
$ npx tsx scripts/generate-metadata.ts
Error: Cannot find module 'tsx'
# 解決: npm install -g tsx

# knowledges ディレクトリが見つからない
$ npx tsx scripts/generate-metadata.ts
Error: knowledges directory not found

# Permission denied
$ node scripts/generate-metadata.ts /root/protected
Error: Permission denied accessing directory: /root/protected

# Invalid output location
$ node scripts/generate-metadata.ts --output /readonly/meta.json
Error: Cannot write to output file: /readonly/meta.json
```

### Dry Run

```bash
$ node scripts/generate-metadata.ts --dry-run
Would scan directory: knowledges
Would generate metadata for:
  - ai (2 points)
  - aws (0 points)
  - go (1 point)
Would write to: knowledges/meta.json
No files were modified.
```

## Backward Compatibility

### Output Format

- Must maintain exact JSON structure of existing meta.json
- Field names must remain unchanged: `categories`, `category`, `point`, `names`, `subCategories`
- Field types must remain unchanged
- Category ordering may change (alphabetical) but content must be identical

### CLI Interface

- New options may be added
- Existing behavior for no arguments must remain unchanged
- Default output location must remain `knowledges/meta.json`

## Performance Contract

### Time Complexity

- **Expectation**: O(n) where n = total number of files + directories
- **Timeout**: Should complete within 5 seconds for up to 1000 files
- **Memory**: Should not exceed 100MB for typical usage

### Error Recovery

- Partial failures in subdirectories should not prevent processing of other directories
- Invalid or unreadable files should be logged and skipped
- Temporary file system issues should be retried once
