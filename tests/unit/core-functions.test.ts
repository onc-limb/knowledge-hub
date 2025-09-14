// Unit tests for existing functionality
import * as path from "path";
import * as fs from "fs";
import * as os from "os";
import { testRunner, assert } from "../test-runner";
import {
  scanDirectory,
  getDirectFilenames,
  countFilesRecursively,
  CategoryMetadata,
} from "../metadata-functions";

testRunner.describe("Unit Tests - Core Functions", () => {
  const fixturesPath = path.resolve(
    process.cwd(),
    "tests",
    "fixtures",
    "sample-knowledges"
  );
  let tempDir: string;

  // Helper to create temporary directory
  function createTempDir(): string {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "metadata-test-"));
    return tmpDir;
  }

  // Helper to clean up temporary directory
  function cleanupTempDir(dir: string): void {
    if (fs.existsSync(dir)) {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  }

  testRunner.it("scanDirectory should handle empty directory", () => {
    tempDir = createTempDir();

    try {
      const result = scanDirectory(tempDir, 0);
      assert.isArray(result, "Should return array");
      assert.equal(
        result.length,
        0,
        "Should return empty array for empty directory"
      );
    } finally {
      cleanupTempDir(tempDir);
    }
  });

  testRunner.it("scanDirectory should ignore hidden directories", () => {
    tempDir = createTempDir();

    try {
      // Create hidden directory
      const hiddenDir = path.join(tempDir, ".hidden");
      fs.mkdirSync(hiddenDir);
      fs.writeFileSync(path.join(hiddenDir, "file.md"), "hidden content");

      // Create normal directory
      const normalDir = path.join(tempDir, "normal");
      fs.mkdirSync(normalDir);
      fs.writeFileSync(path.join(normalDir, "file.md"), "normal content");

      const result = scanDirectory(tempDir, 0);

      assert.equal(
        result.length,
        1,
        "Should find only 1 directory (ignore hidden)"
      );
      assert.equal(
        result[0].category,
        "normal",
        "Should find the normal directory"
      );
    } finally {
      cleanupTempDir(tempDir);
    }
  });

  testRunner.it(
    "getDirectFilenames should return only filenames, not directories",
    () => {
      const aiDir = path.join(fixturesPath, "ai");
      const filenames = getDirectFilenames(aiDir);

      assert.isArray(filenames, "Should return array");
      assert.true(
        filenames.includes("overview.md"),
        "Should include overview.md"
      );
      assert.false(
        filenames.includes("machine-learning"),
        "Should not include directory names"
      );
    }
  );

  testRunner.it("getDirectFilenames should ignore hidden files", () => {
    tempDir = createTempDir();

    try {
      // Create hidden and normal files
      fs.writeFileSync(path.join(tempDir, ".hidden.md"), "hidden");
      fs.writeFileSync(path.join(tempDir, "visible.md"), "visible");

      const filenames = getDirectFilenames(tempDir);

      assert.true(
        filenames.includes("visible.md"),
        "Should include visible files"
      );
      assert.false(
        filenames.includes(".hidden.md"),
        "Should ignore hidden files"
      );
    } finally {
      cleanupTempDir(tempDir);
    }
  });

  testRunner.it(
    "countFilesRecursively should count all files in subdirectories",
    () => {
      const aiDir = path.join(fixturesPath, "ai");
      const count = countFilesRecursively(aiDir);

      // ai/overview.md + ai/machine-learning/basics.md + ai/machine-learning/advanced.md = 3
      assert.equal(
        count,
        3,
        "Should count all files recursively in ai directory"
      );
    }
  );

  testRunner.it("countFilesRecursively should ignore hidden files", () => {
    tempDir = createTempDir();

    try {
      // Create file structure with hidden files
      fs.writeFileSync(path.join(tempDir, "visible1.md"), "content");
      fs.writeFileSync(path.join(tempDir, ".hidden.md"), "hidden");

      const subDir = path.join(tempDir, "subdir");
      fs.mkdirSync(subDir);
      fs.writeFileSync(path.join(subDir, "visible2.md"), "content");
      fs.writeFileSync(path.join(subDir, ".hidden2.md"), "hidden");

      const count = countFilesRecursively(tempDir);

      assert.equal(
        count,
        2,
        "Should count only visible files (2), ignore hidden ones"
      );
    } finally {
      cleanupTempDir(tempDir);
    }
  });

  testRunner.it(
    "scanDirectory should respect depth limit (current implementation)",
    () => {
      const result = scanDirectory(fixturesPath, 0);

      const webCategory = result.find((cat) => cat.category === "web");
      assert.true(webCategory !== undefined, "Should find web category");

      if (webCategory!.subCategories) {
        const frontendCategory = webCategory!.subCategories.find(
          (sub) => sub.category === "frontend"
        );
        assert.true(
          frontendCategory !== undefined,
          "Should find frontend subcategory"
        );

        if (frontendCategory!.subSubCategories) {
          const reactCategory = frontendCategory!.subSubCategories.find(
            (sub) => sub.category === "react"
          );
          assert.true(
            reactCategory !== undefined,
            "Should find react sub-subcategory"
          );

          // At depth 2 (3rd level), should not go deeper
          assert.true(
            reactCategory!.subSubCategories === undefined,
            "Should not have further levels at depth 2 (current limitation)"
          );
        }
      }
    }
  );

  testRunner.it(
    "scanDirectory should correctly set point values for each depth",
    () => {
      const result = scanDirectory(fixturesPath, 0);

      const webCategory = result.find((cat) => cat.category === "web");
      assert.true(webCategory !== undefined, "Should find web category");

      // At depth 0, point should be total files in entire subtree
      assert.true(
        webCategory!.point > 0,
        "Category at depth 0 should have positive point count"
      );

      if (webCategory!.subCategories) {
        const frontendCategory = webCategory!.subCategories.find(
          (sub) => sub.category === "frontend"
        );
        if (frontendCategory) {
          // At depth 1, point should be files in this subtree
          assert.true(
            frontendCategory.point > 0,
            "Subcategory at depth 1 should have positive point count"
          );

          if (frontendCategory.subSubCategories) {
            const reactCategory = frontendCategory.subSubCategories.find(
              (sub) => sub.category === "react"
            );
            if (reactCategory) {
              // At depth 2, point should be files in this directory only
              assert.true(
                reactCategory.point > 0,
                "Sub-subcategory at depth 2 should have positive point count"
              );
            }
          }
        }
      }
    }
  );

  testRunner.it(
    "scanDirectory should handle non-existent directory gracefully",
    () => {
      const nonExistentPath = path.join(tempDir || "/tmp", "non-existent-dir");

      // Should not throw error, should return empty array
      const result = scanDirectory(nonExistentPath, 0);
      assert.isArray(
        result,
        "Should return array even for non-existent directory"
      );
      assert.equal(
        result.length,
        0,
        "Should return empty array for non-existent directory"
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
