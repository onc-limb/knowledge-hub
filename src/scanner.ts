// Enhanced directory scanner with unlimited depth support
import * as fs from "fs";
import * as path from "path";
import {
  CategoryMetadata,
  GeneratorOptions,
  ScanResult,
  FileFilter,
  MARKDOWN_EXTENSIONS,
  DEFAULT_OPTIONS,
} from "./types";

export class DirectoryScanner {
  private options: Required<GeneratorOptions>;
  private fileFilter: FileFilter;
  private scannedDirectories: number = 0;
  private maxDepthReached: number = 0;

  constructor(options: GeneratorOptions = {}) {
    this.options = { ...DEFAULT_OPTIONS, ...options };
    this.fileFilter = this.createFileFilter();
  }

  private createFileFilter(): FileFilter {
    if (this.options.markdownOnly) {
      return (filename: string): boolean => {
        return MARKDOWN_EXTENSIONS.some((ext) =>
          filename.toLowerCase().endsWith(ext)
        );
      };
    }
    return () => true; // Accept all files
  }

  private shouldIncludeFile(filename: string): boolean {
    // Skip hidden files unless includeHidden is true
    if (!this.options.includeHidden && filename.startsWith(".")) {
      return false;
    }

    // Skip meta.json if excludeMetaFile is true
    if (this.options.excludeMetaFile && filename === "meta.json") {
      return false;
    }

    return this.fileFilter(filename);
  }

  private shouldIncludeDirectory(dirname: string): boolean {
    // Skip hidden directories unless includeHidden is true
    if (!this.options.includeHidden && dirname.startsWith(".")) {
      return false;
    }
    return true;
  }

  public scanDirectory(dirPath: string, depth: number = 0): CategoryMetadata[] {
    const categories: CategoryMetadata[] = [];
    this.scannedDirectories++;
    this.maxDepthReached = Math.max(this.maxDepthReached, depth);

    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      // Find subdirectories
      const subdirs = items.filter(
        (item) => item.isDirectory() && this.shouldIncludeDirectory(item.name)
      );

      // For each subdirectory, create a category
      for (const subdir of subdirs) {
        const subdirPath = path.join(dirPath, subdir.name);
        const directFiles = this.getDirectFilenames(subdirPath);

        const categoryData: CategoryMetadata = {
          category: subdir.name,
          point: 0, // Will be calculated later
        };

        // Add filenames if there are any direct files
        if (directFiles.length > 0) {
          categoryData.names = directFiles;
        }

        // Check depth limits
        const shouldScanDeeper = this.shouldScanDeeper(depth);

        if (shouldScanDeeper) {
          // Unlimited depth mode or within legacy limits
          const subCategories = this.scanDirectory(subdirPath, depth + 1);
          if (subCategories.length > 0) {
            if (this.options.legacyMode && depth === 1) {
              // Legacy mode: use subSubCategories at depth 1
              categoryData.subSubCategories = subCategories;
            } else {
              // Standard mode: always use subCategories
              categoryData.subCategories = subCategories;
            }
          }
        }

        // Count files in this directory and all subdirectories
        categoryData.point = this.countFilesRecursively(subdirPath);
        categories.push(categoryData);
      }
    } catch (error) {
      if (this.options.verbose) {
        console.error(`Error scanning directory ${dirPath}:`, error);
      }
    }

    return categories;
  }

  private shouldScanDeeper(currentDepth: number): boolean {
    // Check maximum depth limit
    if (
      this.options.maxDepth !== undefined &&
      currentDepth >= this.options.maxDepth - 1
    ) {
      return false;
    }

    // Legacy mode: limit to 3 levels (depth 0, 1, 2)
    if (this.options.legacyMode && currentDepth >= 2) {
      return false;
    }

    return true;
  }

  public getDirectFilenames(dirPath: string): string[] {
    const filenames: string[] = [];

    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const item of items) {
        if (item.isFile() && this.shouldIncludeFile(item.name)) {
          filenames.push(item.name);
        }
      }
    } catch (error) {
      if (this.options.verbose) {
        console.error(`Error reading filenames in ${dirPath}:`, error);
      }
    }

    return filenames;
  }

  public countFilesRecursively(dirPath: string): number {
    let count = 0;

    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const item of items) {
        if (item.isFile() && this.shouldIncludeFile(item.name)) {
          count++;
        } else if (
          item.isDirectory() &&
          this.shouldIncludeDirectory(item.name)
        ) {
          count += this.countFilesRecursively(path.join(dirPath, item.name));
        }
      }
    } catch (error) {
      if (this.options.verbose) {
        console.error(`Error counting files in ${dirPath}:`, error);
      }
    }

    return count;
  }

  public scan(knowledgesPath: string): ScanResult {
    if (!fs.existsSync(knowledgesPath)) {
      throw new Error(`Directory not found: ${knowledgesPath}`);
    }

    // Reset counters
    this.scannedDirectories = 0;
    this.maxDepthReached = 0;

    // Scan the directory structure
    const categories = this.scanDirectory(knowledgesPath, 0);
    const totalFiles = this.countFilesRecursively(knowledgesPath);

    return {
      categories,
      totalFiles,
      scannedDirectories: this.scannedDirectories,
      maxDepthReached: this.maxDepthReached,
    };
  }

  public getOptions(): Required<GeneratorOptions> {
    return { ...this.options };
  }
}

// Backward compatibility functions
export function scanDirectory(
  dirPath: string,
  depth: number = 0
): CategoryMetadata[] {
  const scanner = new DirectoryScanner({ legacyMode: true });
  return scanner.scanDirectory(dirPath, depth);
}

export function getDirectFilenames(dirPath: string): string[] {
  const scanner = new DirectoryScanner();
  return scanner.getDirectFilenames(dirPath);
}

export function countFilesRecursively(dirPath: string): number {
  const scanner = new DirectoryScanner();
  return scanner.countFilesRecursively(dirPath);
}
