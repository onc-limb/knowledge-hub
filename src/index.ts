// Enhanced metadata generator with unlimited hierarchy support
import * as fs from "fs";
import * as path from "path";
import {
  KnowledgeMetadata,
  CategoryMetadata,
  GeneratorOptions,
  CLIOptions,
  DEFAULT_OPTIONS,
} from "./types";
import { DirectoryScanner } from "./scanner";

export class MetadataGenerator {
  private options: Required<GeneratorOptions>;
  private scanner: DirectoryScanner;

  constructor(options: GeneratorOptions = {}) {
    this.options = { ...DEFAULT_OPTIONS, ...options };
    this.scanner = new DirectoryScanner(this.options);
  }

  public generateMetadata(inputPath: string): KnowledgeMetadata {
    if (!fs.existsSync(inputPath)) {
      throw new Error(`Input directory not found: ${inputPath}`);
    }

    const scanResult = this.scanner.scan(inputPath);

    const metadata: KnowledgeMetadata = {
      categories: scanResult.categories,
      totalFiles: scanResult.totalFiles,
      lastUpdated: new Date().toISOString(),
    };

    // Show statistics if verbose
    if (this.options.verbose) {
      console.log(`Scan completed:`);
      console.log(`  - Directories scanned: ${scanResult.scannedDirectories}`);
      console.log(
        `  - Maximum depth reached: ${scanResult.maxDepthReached + 1}`
      );
      console.log(`  - Total files found: ${scanResult.totalFiles}`);
      console.log(`  - Categories found: ${scanResult.categories.length}`);
    }

    return metadata;
  }

  public writeMetadataFile(
    metadata: KnowledgeMetadata,
    outputPath?: string
  ): void {
    const finalOutputPath = outputPath || this.options.outputPath;

    if (this.options.outputFormat === "text") {
      this.writeTextFormat(metadata, finalOutputPath);
    } else {
      this.writeJsonFormat(metadata, finalOutputPath);
    }

    if (!this.options.quiet) {
      console.log(`Metadata generated successfully at ${finalOutputPath}`);
      console.log(`Total files: ${metadata.totalFiles}`);
      console.log(`Categories: ${metadata.categories.length}`);
    }
  }

  private writeJsonFormat(
    metadata: KnowledgeMetadata,
    outputPath: string
  ): void {
    fs.writeFileSync(outputPath, JSON.stringify(metadata, null, 2));
  }

  private writeTextFormat(
    metadata: KnowledgeMetadata,
    outputPath: string
  ): void {
    const lines: string[] = [];
    lines.push(`Knowledge Base Metadata`);
    lines.push(`Generated: ${metadata.lastUpdated}`);
    lines.push(`Total Files: ${metadata.totalFiles}`);
    lines.push(`Categories: ${metadata.categories.length}`);
    lines.push("");

    lines.push("Directory Structure:");
    this.appendHierarchyText(metadata.categories, lines, "");

    fs.writeFileSync(outputPath, lines.join("\n"));
  }

  private appendHierarchyText(
    categories: CategoryMetadata[],
    lines: string[],
    prefix: string
  ): void {
    categories.forEach((category, index) => {
      const isLast = index === categories.length - 1;
      const connector = isLast ? "└──" : "├──";
      const filesInfo = category.names ? ` [${category.names.join(", ")}]` : "";

      lines.push(
        `${prefix}${connector} ${category.category} (${category.point} files)${filesInfo}`
      );

      const nextPrefix = prefix + (isLast ? "    " : "│   ");

      // Handle both legacy subSubCategories and modern subCategories
      const subCategories = category.subCategories || category.subSubCategories;
      if (subCategories && subCategories.length > 0) {
        this.appendHierarchyText(subCategories, lines, nextPrefix);
      }
    });
  }

  public displayHierarchy(categories: CategoryMetadata[]): void {
    if (this.options.quiet) return;

    console.log("\nHierarchy structure:");
    this.displayHierarchyRecursive(categories, "", 0);
  }

  private displayHierarchyRecursive(
    categories: CategoryMetadata[],
    prefix: string,
    depth: number
  ): void {
    categories.forEach((category, index) => {
      const isLast = index === categories.length - 1;
      const connector = isLast ? "└──" : "├──";
      const filesInfo = category.names ? ` [${category.names.join(", ")}]` : "";

      console.log(
        `${prefix}${connector} ${category.category} (${category.point} files)${filesInfo}`
      );

      const nextPrefix = prefix + (isLast ? "    " : "│   ");

      // Handle both legacy subSubCategories and modern subCategories
      const subCategories = category.subCategories || category.subSubCategories;
      if (subCategories && subCategories.length > 0) {
        this.displayHierarchyRecursive(subCategories, nextPrefix, depth + 1);
      }
    });
  }

  public getOptions(): Required<GeneratorOptions> {
    return { ...this.options };
  }
}

// Main function for CLI usage
export function generateMetadataForPath(
  knowledgesPath: string,
  options: GeneratorOptions = {}
): KnowledgeMetadata {
  const generator = new MetadataGenerator(options);
  return generator.generateMetadata(knowledgesPath);
}

// Enhanced CLI function
export function runCLI(cliOptions: CLIOptions): void {
  // Convert CLI options to generator options
  const generatorOptions: GeneratorOptions = {
    markdownOnly: cliOptions.markdownOnly,
    includeHidden: cliOptions.includeHidden,
    maxDepth: cliOptions.maxDepth,
    legacyMode: cliOptions.legacyMode,
    outputFormat: cliOptions.outputFormat,
    verbose: cliOptions.verbose,
    quiet: cliOptions.quiet,
    outputPath: cliOptions.outputPath,
  };

  const inputPath =
    cliOptions.inputPath || path.join(process.cwd(), "knowledges");
  const generator = new MetadataGenerator(generatorOptions);

  try {
    const metadata = generator.generateMetadata(inputPath);
    const outputPath =
      cliOptions.outputPath || path.join(inputPath, "meta.json");

    generator.writeMetadataFile(metadata, outputPath);
    generator.displayHierarchy(metadata.categories);
  } catch (error) {
    console.error("Error generating metadata:", (error as Error).message);
    process.exit(1);
  }
}

// Backward compatibility: Legacy function that maintains exact original behavior
export function generateMetadata(): void {
  const knowledgesPath = path.join(__dirname, "..", "knowledges");
  const generator = new MetadataGenerator({ legacyMode: true });

  try {
    const metadata = generator.generateMetadata(knowledgesPath);
    const outputPath = path.join(knowledgesPath, "meta.json");

    generator.writeMetadataFile(metadata, outputPath);
    generator.displayHierarchy(metadata.categories);
  } catch (error) {
    console.error("Error:", (error as Error).message);
  }
}
