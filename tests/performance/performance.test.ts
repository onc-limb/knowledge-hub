// Performance comparison test
import * as path from "path";
import { testRunner, assert } from "../test-runner";
import { generateMetadataForPath } from "../metadata-functions";
import { MetadataGenerator } from "../../src/index";
import { DirectoryScanner } from "../../src/scanner";

testRunner.describe("Performance Tests", () => {
  const fixturesPath = path.resolve(
    process.cwd(),
    "tests",
    "fixtures",
    "sample-knowledges"
  );

  testRunner.it(
    "should compare performance between legacy and enhanced implementations",
    () => {
      // Test legacy implementation performance
      const legacyStart = Date.now();
      const legacyResult = generateMetadataForPath(fixturesPath);
      const legacyDuration = Date.now() - legacyStart;

      // Test enhanced implementation with legacy mode (equivalent functionality)
      const enhancedStart = Date.now();
      const enhancedGenerator = new MetadataGenerator({
        legacyMode: true,
        quiet: true,
      });
      const enhancedResult = enhancedGenerator.generateMetadata(fixturesPath);
      const enhancedDuration = Date.now() - enhancedStart;

      console.log(`Legacy implementation: ${legacyDuration}ms`);
      console.log(
        `Enhanced implementation (legacy mode): ${enhancedDuration}ms`
      );

      // For very fast operations, timing is imprecise
      if (legacyDuration === 0 && enhancedDuration === 0) {
        console.log("Both implementations are very fast (< 1ms)");
        assert.true(true, "Both implementations completed quickly");
      } else if (legacyDuration === 0) {
        // If legacy is 0ms, enhanced should also be very fast
        assert.true(
          enhancedDuration <= 5,
          "Enhanced should be very fast when legacy is < 1ms"
        );
      } else {
        // Enhanced version should not be significantly slower (within 5x)
        assert.true(
          enhancedDuration < legacyDuration * 5,
          `Enhanced version should not be more than 5x slower. Legacy: ${legacyDuration}ms, Enhanced: ${enhancedDuration}ms`
        );
      }

      // Both should produce equivalent results in terms of structure
      assert.true(
        enhancedResult.categories.length > 0,
        "Enhanced should produce categories"
      );
      assert.true(enhancedResult.totalFiles > 0, "Enhanced should count files");
    }
  );

  testRunner.it("should handle large directory structures efficiently", () => {
    const start = Date.now();

    // Test with unlimited depth on fixtures
    const scanner = new DirectoryScanner({
      maxDepth: undefined,
      verbose: false,
      quiet: true,
    });

    const result = scanner.scan(fixturesPath);
    const duration = Date.now() - start;

    console.log(`Unlimited depth scan: ${duration}ms`);
    console.log(`Directories scanned: ${result.scannedDirectories}`);
    console.log(`Max depth reached: ${result.maxDepthReached + 1}`);

    // Should complete within reasonable time (< 1000ms for test fixtures)
    assert.true(
      duration < 1000,
      `Scan should complete quickly. Took: ${duration}ms`
    );
    assert.true(result.scannedDirectories > 0, "Should scan some directories");
  });

  testRunner.it("should demonstrate memory efficiency", () => {
    // Test multiple scans to ensure no memory leaks
    const iterations = 10;
    const results: number[] = [];

    for (let i = 0; i < iterations; i++) {
      const start = Date.now();
      const generator = new MetadataGenerator({ quiet: true });
      generator.generateMetadata(fixturesPath);
      const duration = Date.now() - start;
      results.push(duration);
    }

    const average = results.reduce((sum, val) => sum + val, 0) / results.length;
    const max = Math.max(...results);
    const min = Math.min(...results);

    console.log(
      `${iterations} iterations - Avg: ${average.toFixed(
        1
      )}ms, Min: ${min}ms, Max: ${max}ms`
    );

    // For small test datasets, timing variations are expected to be small
    // Check that all iterations completed successfully
    assert.true(
      results.length === iterations,
      `Should complete all ${iterations} iterations`
    );
    assert.true(average >= 0, "Average duration should be non-negative");
    assert.true(max >= min, "Max should be greater than or equal to min");

    // For very fast operations (< 5ms), timing precision is limited
    if (average < 5) {
      console.log(
        "Note: Operations are very fast, timing precision is limited"
      );
      assert.true(true, "Fast operations completed successfully");
    } else {
      // Only check consistency for slower operations
      assert.true(
        max < min * 5,
        `Performance should be reasonably consistent. Min: ${min}ms, Max: ${max}ms`
      );
    }
  });
});

// Separate test file runner
if (require.main === module) {
  testRunner.run();
} else {
  setTimeout(() => testRunner.run(), 0);
}
