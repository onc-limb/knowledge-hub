// Enhanced type definitions for metadata generator
export interface CategoryMetadata {
  category: string;
  point: number;
  names?: string[];
  subCategories?: CategoryMetadata[];
  // Legacy support for 3-level hierarchy
  subSubCategories?: CategoryMetadata[];
}

export interface KnowledgeMetadata {
  categories: CategoryMetadata[];
  totalFiles: number;
  lastUpdated: string;
}

export interface GeneratorOptions {
  // Filter options
  markdownOnly?: boolean; // --md-only: Include only .md files
  includeHidden?: boolean; // Include hidden files/directories

  // Hierarchy options
  maxDepth?: number; // Maximum depth (undefined = unlimited)
  legacyMode?: boolean; // --legacy: Use 3-level hierarchy limit

  // Output options
  outputFormat?: "json" | "text"; // Output format
  verbose?: boolean; // --verbose: Show detailed output
  quiet?: boolean; // --quiet: Suppress hierarchy display

  // File options
  outputPath?: string; // Custom output path
  excludeMetaFile?: boolean; // Exclude meta.json from file counts
}

export interface CLIOptions extends GeneratorOptions {
  help?: boolean; // --help
  version?: boolean; // --version
  inputPath?: string; // Input directory path
}

export interface ScanResult {
  categories: CategoryMetadata[];
  totalFiles: number;
  scannedDirectories: number;
  maxDepthReached: number;
}

export interface FileFilter {
  (filename: string): boolean;
}

export const DEFAULT_OPTIONS: Required<GeneratorOptions> = {
  markdownOnly: false,
  includeHidden: false,
  maxDepth: undefined as any, // Unlimited depth by default
  legacyMode: false,
  outputFormat: "json",
  verbose: false,
  quiet: false,
  outputPath: "meta.json",
  excludeMetaFile: true,
};

// File extension patterns
export const MARKDOWN_EXTENSIONS = [
  ".md",
  ".markdown",
  ".mdown",
  ".mkdn",
  ".mkd",
];

// Version information
export const VERSION = "2.0.0";
export const DESCRIPTION =
  "Enhanced knowledge base metadata generator with unlimited hierarchy support";
