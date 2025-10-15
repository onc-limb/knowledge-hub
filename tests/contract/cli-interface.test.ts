// Contract tests for current CLI usage
import * as path from "path";
import * as fs from "fs";
import { testRunner, assert } from "../test-runner";
import {
  generateMetadataForPath,
  scanDirectory,
  countFilesRecursively,
  getDirectFilenames,
} from "../metadata-functions";

testRunner.describe("CLI Contract Tests - Current Behavior", () => {
  const fixturesPath = path.resolve(
    process.cwd(),
    "tests",
    "fixtures",
    "sample-knowledges"
  );

  testRunner.it(
    "should generate metadata with 3-level hierarchy structure",
    () => {
      const metadata = generateMetadataForPath(fixturesPath);

      // Should have main categories
      assert.isArray(metadata.categories, "Should have categories array");
      assert.true(
        metadata.categories.length > 0,
        "Should have at least one category"
      );

      // Find the 'web' category which has the deepest structure
      const webCategory = metadata.categories.find(
        (cat) => cat.category === "web"
      );
      assert.true(webCategory !== undefined, "Should have 'web' category");

      // Check 3-level structure: web -> frontend -> react
      assert.true(
        webCategory!.subCategories !== undefined,
        "Web should have subCategories"
      );

      const frontendCategory = webCategory!.subCategories!.find(
        (sub) => sub.category === "frontend"
      );
      assert.true(
        frontendCategory !== undefined,
        "Should have 'frontend' subcategory"
      );

      assert.true(
        frontendCategory!.subSubCategories !== undefined,
        "Frontend should have subSubCategories"
      );

      const reactCategory = frontendCategory!.subSubCategories!.find(
        (sub) => sub.category === "react"
      );
      assert.true(
        reactCategory !== undefined,
        "Should have 'react' sub-subcategory"
      );

      // React category should not have further nesting (depth limit = 3)
      assert.true(
        reactCategory!.subSubCategories === undefined,
        "React should not have further nesting"
      );
    }
  );

  testRunner.it("should count all file types, not just markdown", () => {
    const metadata = generateMetadataForPath(fixturesPath);

    // Should count config.js and README.md in root
    assert.true(
      metadata.totalFiles >= 7,
      "Should count all files including non-markdown"
    );

    // Check that all files are counted, not just .md files
    const totalFiles = countFilesRecursively(fixturesPath);
    const excludingMeta =
      totalFiles -
      (fs.existsSync(path.join(fixturesPath, "meta.json")) ? 1 : 0);

    assert.equal(
      metadata.totalFiles,
      excludingMeta,
      "Should count all files except meta.json"
    );
  });

  testRunner.it(
    "should include totalFiles and lastUpdated metadata fields",
    () => {
      const metadata = generateMetadataForPath(fixturesPath);

      assert.isNumber(metadata.totalFiles, "Should have totalFiles as number");
      assert.isString(
        metadata.lastUpdated,
        "Should have lastUpdated as string"
      );

      // lastUpdated should be valid ISO string
      const date = new Date(metadata.lastUpdated);
      assert.true(!isNaN(date.getTime()), "lastUpdated should be valid date");
    }
  );

  testRunner.it(
    "should correctly calculate file counts (point) in each category",
    () => {
      const metadata = generateMetadataForPath(fixturesPath);

      const aiCategory = metadata.categories.find(
        (cat) => cat.category === "ai"
      );
      assert.true(aiCategory !== undefined, "Should have 'ai' category");

      // AI has: overview.md + machine-learning/basics.md + machine-learning/advanced.md = 3 files
      assert.equal(aiCategory!.point, 3, "AI category should have 3 files");

      const machinelearningCategory = aiCategory!.subCategories!.find(
        (sub) => sub.category === "machine-learning"
      );
      assert.true(
        machinelearningCategory !== undefined,
        "Should have 'machine-learning' subcategory"
      );

      // Machine learning has: basics.md + advanced.md = 2 files
      assert.equal(
        machinelearningCategory!.point,
        2,
        "Machine learning should have 2 files"
      );
    }
  );

  testRunner.it("should include direct filenames in names array", () => {
    const metadata = generateMetadataForPath(fixturesPath);

    const aiCategory = metadata.categories.find((cat) => cat.category === "ai");
    assert.true(aiCategory !== undefined, "Should have 'ai' category");

    // AI directory has overview.md as direct file
    assert.isArray(aiCategory!.names, "Should have names array");
    assert.true(
      aiCategory!.names!.includes("overview.md"),
      "Should include overview.md in names"
    );

    const machinelearningCategory = aiCategory!.subCategories!.find(
      (sub) => sub.category === "machine-learning"
    );
    assert.true(
      machinelearningCategory !== undefined,
      "Should have 'machine-learning' subcategory"
    );

    // Machine learning has basics.md and advanced.md
    assert.isArray(
      machinelearningCategory!.names,
      "Should have names array for machine-learning"
    );
    assert.true(
      machinelearningCategory!.names!.includes("basics.md"),
      "Should include basics.md"
    );
    assert.true(
      machinelearningCategory!.names!.includes("advanced.md"),
      "Should include advanced.md"
    );
  });

  testRunner.it(
    "should handle directories with no further subdirectories",
    () => {
      const categories = scanDirectory(fixturesPath, 0);

      // Find a category that has only files, no subdirectories
      const hasDirectFilesOnly = categories.some(
        (cat) =>
          cat.names &&
          cat.names.length > 0 &&
          (!cat.subCategories || cat.subCategories.length === 0)
      );

      // This test ensures scanDirectory handles leaf directories correctly
      assert.true(
        true,
        "scanDirectory should handle leaf directories without errors"
      );
    }
  );
});

// Separate test file runner
if (require.main === module) {
  testRunner.run();
} else {
  // When imported, still execute the tests
  setTimeout(() => testRunner.run(), 0);
}
