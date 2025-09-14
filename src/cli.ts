// CLI argument parser and help system
import * as path from "path";
import { CLIOptions, VERSION, DESCRIPTION } from "./types";

export class CLIParser {
  private args: string[];

  constructor(args: string[] = process.argv.slice(2)) {
    this.args = args;
  }

  public parse(): CLIOptions {
    const options: CLIOptions = {};

    for (let i = 0; i < this.args.length; i++) {
      const arg = this.args[i];

      switch (arg) {
        case "--help":
        case "-h":
          options.help = true;
          break;

        case "--version":
        case "-v":
          options.version = true;
          break;

        case "--md-only":
        case "--markdown-only":
          options.markdownOnly = true;
          break;

        case "--include-hidden":
          options.includeHidden = true;
          break;

        case "--legacy":
          options.legacyMode = true;
          break;

        case "--verbose":
          options.verbose = true;
          break;

        case "--quiet":
        case "-q":
          options.quiet = true;
          break;

        case "--max-depth":
          const depthValue = this.args[++i];
          if (depthValue && !isNaN(Number(depthValue))) {
            options.maxDepth = Number(depthValue);
          } else {
            throw new Error("--max-depth requires a numeric value");
          }
          break;

        case "--output":
        case "-o":
          const outputValue = this.args[++i];
          if (outputValue) {
            options.outputPath = outputValue;
          } else {
            throw new Error("--output requires a file path");
          }
          break;

        case "--format":
        case "-f":
          const formatValue = this.args[++i];
          if (formatValue === "json" || formatValue === "text") {
            options.outputFormat = formatValue;
          } else {
            throw new Error('--format must be "json" or "text"');
          }
          break;

        default:
          // If it doesn't start with --, treat as input path
          if (!arg.startsWith("--") && !arg.startsWith("-")) {
            if (!options.inputPath) {
              options.inputPath = arg;
            } else {
              throw new Error(`Unexpected argument: ${arg}`);
            }
          } else {
            throw new Error(`Unknown option: ${arg}`);
          }
          break;
      }
    }

    return options;
  }

  public static showHelp(): void {
    console.log(`${DESCRIPTION}

Usage: generate-metadata [options] [input-directory]

Options:
  -h, --help              Show this help message
  -v, --version           Show version information
  
  File Filtering:
  --md-only, --markdown-only    Include only markdown files (.md, .markdown, etc.)
  --include-hidden              Include hidden files and directories
  
  Hierarchy Options:
  --max-depth <number>          Maximum directory depth to scan (default: unlimited)
  --legacy                      Use legacy 3-level hierarchy structure
  
  Output Options:
  -o, --output <path>          Output file path (default: meta.json)
  -f, --format <json|text>     Output format (default: json)
  --verbose                    Show detailed output and error messages
  -q, --quiet                  Suppress hierarchy display
  
Arguments:
  input-directory               Directory to scan (default: ./knowledges)

Examples:
  generate-metadata                                    # Scan ./knowledges with default options
  generate-metadata --md-only --max-depth 3          # Only markdown files, max 3 levels
  generate-metadata --legacy ./docs                   # Use legacy mode on ./docs directory
  generate-metadata --format text --quiet             # Text output, no hierarchy display
  generate-metadata --output metadata.json --verbose  # Custom output file with verbose logging

Backward Compatibility:
  - Default behavior maintains compatibility with existing meta.json format
  - Use --legacy flag to enforce the original 3-level hierarchy limit
  - File counting includes all file types unless --md-only is specified`);
  }

  public static showVersion(): void {
    console.log(`${VERSION}`);
  }

  public static validateOptions(options: CLIOptions): void {
    // Validate conflicting options
    if (options.verbose && options.quiet) {
      throw new Error("Cannot use both --verbose and --quiet options");
    }

    // Validate max depth
    if (options.maxDepth !== undefined) {
      if (options.maxDepth < 1) {
        throw new Error("--max-depth must be at least 1");
      }
      if (options.maxDepth > 50) {
        throw new Error("--max-depth cannot exceed 50 (reasonable limit)");
      }
    }

    // Validate output path
    if (options.outputPath) {
      const dir = path.dirname(options.outputPath);
      if (dir !== "." && dir !== "" && !require("fs").existsSync(dir)) {
        throw new Error(`Output directory does not exist: ${dir}`);
      }
    }

    // Validate input path
    if (options.inputPath && !require("fs").existsSync(options.inputPath)) {
      throw new Error(`Input directory does not exist: ${options.inputPath}`);
    }
  }
}

export function parseArgs(args?: string[]): CLIOptions {
  const parser = new CLIParser(args);
  return parser.parse();
}

export function showHelp(): void {
  CLIParser.showHelp();
}

export function showVersion(): void {
  CLIParser.showVersion();
}
