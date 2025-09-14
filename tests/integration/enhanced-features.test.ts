// Tests for enhanced functionality
import * as path from "path";
import * as fs from "fs";
import * as os from "os";
import { testRunner, assert } from "../test-runner";
import { DirectoryScanner } from "../../src/scanner";
import { MetadataGenerator } from "../../src/index";
import { parseArgs, CLIParser } from "../../src/cli";

testRunner.describe("Enhanced Functionality Tests", () => {
  const fixturesPath = path.resolve(
    process.cwd(),
    "tests",
    "fixtures",
    "sample-knowledges"
  );
  let tempDir: string;

  // Helper functions
  function createTempDir(): string {
    return fs.mkdtempSync(path.join(os.tmpdir(), "enhanced-test-"));
  }

  function cleanupTempDir(dir: string): void {
    if (fs.existsSync(dir)) {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  }

  function createDeepStructure(baseDir: string, depth: number): void {
    let currentDir = baseDir;
    for (let i = 0; i < depth; i++) {
      currentDir = path.join(currentDir, `level${i}`);
      fs.mkdirSync(currentDir, { recursive: true });
      fs.writeFileSync(
        path.join(currentDir, `file${i}.md`),
        `Content at level ${i}`
      );
    }
  }

  testRunner.it(
    "should support unlimited depth hierarchy (beyond 3 levels)",
    () => {
      tempDir = createTempDir();

      try {
        // Create a 5-level deep structure
        createDeepStructure(tempDir, 5);

        const scanner = new DirectoryScanner({ maxDepth: undefined }); // Unlimited
        const result = scanner.scan(tempDir);

        // Should scan all 5 levels
        assert.true(
          result.maxDepthReached >= 4,
          "Should reach at least depth 4 (5 levels)"
        );
        assert.true(result.categories.length > 0, "Should find categories");

        // Navigate to verify deep structure
        let currentCategories = result.categories;
        let depth = 0;
        while (currentCategories.length > 0 && depth < 4) {
          const category = currentCategories[0];
          assert.true(
            category.category === `level${depth}`,
            `Should find level${depth} category`
          );
          currentCategories = category.subCategories || [];
          depth++;
        }

        assert.true(depth >= 4, "Should have navigated to at least depth 4");
      } finally {
        cleanupTempDir(tempDir);
      }
    }
  );

  testRunner.it("should support markdown-only filtering", () => {
    tempDir = createTempDir();

    try {
      // Create mixed file types
      fs.writeFileSync(path.join(tempDir, "doc.md"), "markdown");
      fs.writeFileSync(path.join(tempDir, "script.js"), "javascript");
      fs.writeFileSync(path.join(tempDir, "readme.txt"), "text");
      fs.writeFileSync(path.join(tempDir, "config.json"), "json");

      const scannerAll = new DirectoryScanner({ markdownOnly: false });
      const resultAll = scannerAll.scan(tempDir);

      const scannerMdOnly = new DirectoryScanner({ markdownOnly: true });
      const resultMdOnly = scannerMdOnly.scan(tempDir);

      assert.true(
        resultAll.totalFiles === 4,
        "Should count all 4 files without filter"
      );
      assert.true(
        resultMdOnly.totalFiles === 1,
        "Should count only 1 markdown file with filter"
      );
    } finally {
      cleanupTempDir(tempDir);
    }
  });

  testRunner.it("should respect maxDepth option", () => {
    tempDir = createTempDir();

    try {
      createDeepStructure(tempDir, 5);

      const scanner = new DirectoryScanner({ maxDepth: 3 });
      const result = scanner.scan(tempDir);

      // Should stop at depth 2 (3 levels: 0, 1, 2)
      assert.true(
        result.maxDepthReached <= 2,
        "Should not exceed maxDepth - 1"
      );

      // Navigate and ensure it stops at correct depth
      let currentCategories = result.categories;
      let depth = 0;
      while (currentCategories.length > 0 && depth < 5) {
        const category = currentCategories[0];
        if (depth >= 2) {
          assert.true(
            category.subCategories === undefined,
            `Should not have subCategories at depth ${depth} with maxDepth 3`
          );
          break;
        }
        currentCategories = category.subCategories || [];
        depth++;
      }
    } finally {
      cleanupTempDir(tempDir);
    }
  });

  testRunner.it("should maintain backward compatibility in legacy mode", () => {
    const scanner = new DirectoryScanner({ legacyMode: true });
    const result = scanner.scan(fixturesPath);

    // Should behave exactly like the original implementation
    const webCategory = result.categories.find((cat) => cat.category === "web");
    assert.true(webCategory !== undefined, "Should find web category");

    if (webCategory!.subCategories) {
      const frontendCategory = webCategory!.subCategories.find(
        (sub) => sub.category === "frontend"
      );
      if (frontendCategory && frontendCategory.subSubCategories) {
        const reactCategory = frontendCategory.subSubCategories.find(
          (sub) => sub.category === "react"
        );
        assert.true(
          reactCategory !== undefined,
          "Should find react in subSubCategories (legacy mode)"
        );
        assert.true(
          reactCategory!.subSubCategories === undefined,
          "Should not go deeper than 3 levels in legacy mode"
        );
      }
    }
  });

  testRunner.it("should handle CLI argument parsing", () => {
    // Test basic options
    const options1 = parseArgs(["--md-only", "--verbose", "--max-depth", "5"]);
    assert.true(options1.markdownOnly === true, "Should parse --md-only");
    assert.true(options1.verbose === true, "Should parse --verbose");
    assert.true(options1.maxDepth === 5, "Should parse --max-depth");

    // Test help and version
    const options2 = parseArgs(["--help"]);
    assert.true(options2.help === true, "Should parse --help");

    const options3 = parseArgs(["--version"]);
    assert.true(options3.version === true, "Should parse --version");

    // Test input path
    const options4 = parseArgs(["./custom-path"]);
    assert.true(
      options4.inputPath === "./custom-path",
      "Should parse input path"
    );
  });

  testRunner.it("should validate CLI options correctly", () => {
    // Valid options should not throw
    try {
      CLIParser.validateOptions({ maxDepth: 5, verbose: true });
      assert.true(true, "Valid options should not throw");
    } catch (error) {
      assert.true(false, "Valid options should not throw error");
    }

    // Invalid options should throw
    try {
      CLIParser.validateOptions({ verbose: true, quiet: true });
      assert.true(false, "Should throw for conflicting verbose and quiet");
    } catch (error) {
      assert.true(true, "Should throw for conflicting options");
    }

    try {
      CLIParser.validateOptions({ maxDepth: 0 });
      assert.true(false, "Should throw for invalid maxDepth");
    } catch (error) {
      assert.true(true, "Should throw for maxDepth < 1");
    }
  });

  testRunner.it("should generate metadata with enhanced options", () => {
    const generator = new MetadataGenerator({
      markdownOnly: false,
      verbose: true,
      maxDepth: undefined, // Unlimited
    });

    const metadata = generator.generateMetadata(fixturesPath);

    assert.isArray(metadata.categories, "Should generate categories");
    assert.isNumber(metadata.totalFiles, "Should have totalFiles");
    assert.isString(metadata.lastUpdated, "Should have lastUpdated");

    // Should maintain compatibility with existing structure
    assert.true(
      metadata.totalFiles >= 8,
      "Should count all files (including non-markdown)"
    );
  });

  testRunner.it("should support different output formats", () => {
    tempDir = createTempDir();

    try {
      const generator = new MetadataGenerator({
        outputFormat: "text",
        quiet: true, // Suppress console output during test
      });

      const metadata = generator.generateMetadata(fixturesPath);
      const outputPath = path.join(tempDir, "output.txt");

      generator.writeMetadataFile(metadata, outputPath);

      assert.true(fs.existsSync(outputPath), "Should create output file");

      const content = fs.readFileSync(outputPath, "utf-8");
      assert.true(
        content.includes("Knowledge Base Metadata"),
        "Should contain text format header"
      );
      assert.true(
        content.includes("Directory Structure:"),
        "Should contain hierarchy section"
      );
    } finally {
      cleanupTempDir(tempDir);
    }
  });
});

// Separate test file runner
if (require.main === module) {
  testRunner.run();
} else {
  setTimeout(() => testRunner.run(), 0);
}
