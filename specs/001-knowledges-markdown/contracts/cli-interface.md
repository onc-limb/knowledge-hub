# CLI Interface Contract

## Command Specification

### Basic Usage

```bash
node scripts/generate-metadata.ts [options] [directory]
```

### Arguments

- `directory` (optional): Path to knowledges directory (default: "./knowledges")

### Options

- `--help`, `-h`: Show help message
- `--version`, `-v`: Show version information
- `--format <format>`: Output format (json|pretty) (default: "pretty")
- `--output <file>`: Output file path (default: "knowledges/meta.json")
- `--dry-run`: Show what would be generated without writing files
- `--verbose`: Enable verbose logging

## Input Contract

### Directory Structure Requirements

```
<target-directory>/
├── category1/
│   ├── file1.md
│   ├── file2.md
│   └── subcategory1/
│       └── file3.md
└── category2/
    └── file4.md
```

### File Requirements

- **File Extensions**: Only `.md` files are processed
- **File Names**: UTF-8 encoded, OS filesystem-compatible names
- **Directory Names**: Valid filesystem directory names, UTF-8 support

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
    }
  },
  "required": ["categories"],
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
            "type": "string",
            "pattern": "\\.md$"
          }
        },
        "subCategories": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Category"
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
- **Stdout**: Progress messages (if --verbose)
- **File Output**: Valid JSON written to specified output file

### Error Response

- **Exit Code**: Non-zero
- **Stderr**: Error message with context
- **File Output**: No file written or partial file cleaned up

## Example Interactions

### Successful Execution

```bash
$ node scripts/generate-metadata.ts --verbose
Scanning directory: knowledges
Found category: ai (2 files, 1 subcategory)
Found category: aws (0 files, 2 subcategories)
Found category: go (1 file, 0 subcategories)
Generated metadata for 3 categories
Written to: knowledges/meta.json
```

### Error Cases

```bash
# Directory not found
$ node scripts/generate-metadata.ts ./nonexistent
Error: Directory not found: ./nonexistent

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
