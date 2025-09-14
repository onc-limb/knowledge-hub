// Integration tests for unlimited depth hierarchy (current behavior verification)
import * as path from "path";
import * as fs from "fs";
import { testRunner, assert } from "../test-runner";
import {
  generateMetadataForPath,
  scanDirectory,
  countFilesRecursively,
  CategoryMetadata,
} from "../metadata-functions";

testRunner.describe(
  "Integration Tests - Current Hierarchy and File Processing",
  () => {
    const fixturesPath = path.resolve(
      process.cwd(),
      "tests",
      "fixtures",
      "sample-knowledges"
    );

    testRunner.it("should properly scan 3-level hierarchy structure", () => {
      const categories = scanDirectory(fixturesPath, 0);

      // Root level: ai, web
      assert.true(
        categories.length >= 2,
        "Should have at least 2 root categories"
      );

      const webCategory = categories.find((cat) => cat.category === "web");
      assert.true(webCategory !== undefined, "Should find web category");

      // Level 1: web has frontend
      assert.isArray(
        webCategory!.subCategories,
        "Web should have subCategories"
      );
      assert.true(
        webCategory!.subCategories!.length >= 1,
        "Web should have at least 1 subcategory"
      );

      const frontendCategory = webCategory!.subCategories!.find(
        (sub) => sub.category === "frontend"
      );
      assert.true(
        frontendCategory !== undefined,
        "Should find frontend subcategory"
      );

      // Level 2: frontend has react
      assert.isArray(
        frontendCategory!.subSubCategories,
        "Frontend should have subSubCategories"
      );
      assert.true(
        frontendCategory!.subSubCategories!.length >= 1,
        "Frontend should have at least 1 sub-subcategory"
      );

      const reactCategory = frontendCategory!.subSubCategories!.find(
        (sub) => sub.category === "react"
      );
      assert.true(
        reactCategory !== undefined,
        "Should find react sub-subcategory"
      );

      // Level 3: react does not go deeper (current implementation limit)
      assert.true(
        reactCategory!.subSubCategories === undefined,
        "React should not have further levels"
      );
    });

    testRunner.it(
      "should count all files recursively including non-markdown",
      () => {
        const totalFiles = countFilesRecursively(fixturesPath);

        // Expected files:
        // - config.js (root)
        // - README.md (root)
        // - ai/overview.md
        // - ai/machine-learning/basics.md
        // - ai/machine-learning/advanced.md
        // - web/overview.md
        // - web/frontend/basics.md
        // - web/frontend/react/hooks.md
        // Total: 8 files

        assert.equal(totalFiles, 8, "Should count all 8 files recursively");
      }
    );

    testRunner.it("should exclude meta.json from total file count", () => {
      // Create a meta.json file in the fixtures
      const metaPath = path.join(fixturesPath, "meta.json");
      const tempMetadata = { test: true };
      fs.writeFileSync(metaPath, JSON.stringify(tempMetadata));

      try {
        const metadata = generateMetadataForPath(fixturesPath);

        // Should exclude meta.json from count
        const rawCount = countFilesRecursively(fixturesPath);
        assert.equal(
          metadata.totalFiles,
          rawCount - 1,
          "Should exclude meta.json from totalFiles count"
        );
      } finally {
        // Clean up
        if (fs.existsSync(metaPath)) {
          fs.unlinkSync(metaPath);
        }
      }
    });

    testRunner.it(
      "should handle directory structure with mixed file types",
      () => {
        const metadata = generateMetadataForPath(fixturesPath);

        // Should process both .md and .js files
        assert.true(
          metadata.totalFiles >= 8,
          "Should include both markdown and other file types"
        );

        // Verify specific file types are included in names
        let foundJsFile = false;
        let foundMdFile = false;

        function checkNamesRecursively(categories: CategoryMetadata[]): void {
          for (const category of categories) {
            if (category.names) {
              for (const name of category.names) {
                if (name.endsWith(".js")) foundJsFile = true;
                if (name.endsWith(".md")) foundMdFile = true;
              }
            }
            if (category.subCategories) {
              checkNamesRecursively(category.subCategories);
            }
            if (category.subSubCategories) {
              checkNamesRecursively(category.subSubCategories);
            }
          }
        }

        checkNamesRecursively(metadata.categories);

        assert.true(foundMdFile, "Should find at least one .md file in names");
        // Note: config.js is in root, so it won't appear in category names,
        // but it should be counted in totalFiles
      }
    );

    testRunner.it(
      "should calculate correct point values for each hierarchy level",
      () => {
        const metadata = generateMetadataForPath(fixturesPath);

        const webCategory = metadata.categories.find(
          (cat) => cat.category === "web"
        );
        assert.true(webCategory !== undefined, "Should find web category");

        // Web category point should include all files in web subtree
        // web/overview.md + web/frontend/basics.md + web/frontend/react/hooks.md = 3
        assert.equal(
          webCategory!.point,
          3,
          "Web category should have 3 total files"
        );

        const frontendCategory = webCategory!.subCategories!.find(
          (sub) => sub.category === "frontend"
        );
        assert.true(
          frontendCategory !== undefined,
          "Should find frontend subcategory"
        );

        // Frontend point should include its files + react files
        // web/frontend/basics.md + web/frontend/react/hooks.md = 2
        assert.equal(
          frontendCategory!.point,
          2,
          "Frontend subcategory should have 2 total files"
        );

        const reactCategory = frontendCategory!.subSubCategories!.find(
          (sub) => sub.category === "react"
        );
        assert.true(
          reactCategory !== undefined,
          "Should find react sub-subcategory"
        );

        // React point should only include its own files
        // web/frontend/react/hooks.md = 1
        assert.equal(
          reactCategory!.point,
          1,
          "React sub-subcategory should have 1 file"
        );
      }
    );

    testRunner.it(
      "should maintain consistency between metadata structure and file system",
      () => {
        const metadata = generateMetadataForPath(fixturesPath);

        // Total files should match sum of all individual file counts
        let calculatedTotal = 0;

        // Count files in root (non-category files)
        const items = fs.readdirSync(fixturesPath, { withFileTypes: true });
        const rootFiles = items.filter(
          (item) =>
            item.isFile() &&
            !item.name.startsWith(".") &&
            item.name !== "meta.json"
        );
        calculatedTotal += rootFiles.length;

        // Count files in categories
        for (const category of metadata.categories) {
          calculatedTotal += category.point;
        }

        assert.equal(
          metadata.totalFiles,
          calculatedTotal,
          "Total files should match sum of root files and category files"
        );
      }
    );
  }
);

// Separate test file runner
if (require.main === module) {
  testRunner.run();
} else {
  // When imported, still execute the tests
  setTimeout(() => testRunner.run(), 0);
}
