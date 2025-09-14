// Simple test runner using Node.js built-in modules
import * as fs from "fs";
import * as path from "path";

export interface TestResult {
  name: string;
  passed: boolean;
  error?: Error;
  duration: number;
}

export interface TestSuite {
  name: string;
  tests: TestResult[];
  totalPassed: number;
  totalFailed: number;
  totalDuration: number;
}

export class TestRunner {
  private suites: TestSuite[] = [];
  private currentSuite: TestSuite | null = null;

  describe(suiteName: string, fn: () => void): void {
    this.currentSuite = {
      name: suiteName,
      tests: [],
      totalPassed: 0,
      totalFailed: 0,
      totalDuration: 0,
    };

    fn();

    this.currentSuite.totalPassed = this.currentSuite.tests.filter(
      (t) => t.passed
    ).length;
    this.currentSuite.totalFailed = this.currentSuite.tests.filter(
      (t) => !t.passed
    ).length;
    this.currentSuite.totalDuration = this.currentSuite.tests.reduce(
      (sum, t) => sum + t.duration,
      0
    );

    this.suites.push(this.currentSuite);
    this.currentSuite = null;
  }

  it(testName: string, fn: () => void | Promise<void>): void {
    if (!this.currentSuite) {
      throw new Error("it() must be called within describe()");
    }

    const startTime = Date.now();
    let result: TestResult;

    try {
      const fnResult = fn();
      if (fnResult instanceof Promise) {
        // For async tests, we'll handle them synchronously for simplicity
        throw new Error("Async tests not supported in this simple runner");
      }

      result = {
        name: testName,
        passed: true,
        duration: Date.now() - startTime,
      };
    } catch (error) {
      result = {
        name: testName,
        passed: false,
        error: error as Error,
        duration: Date.now() - startTime,
      };
    }

    this.currentSuite.tests.push(result);
  }

  run(): void {
    console.log("Running tests...\n");

    let totalTests = 0;
    let totalPassed = 0;
    let totalFailed = 0;

    for (const suite of this.suites) {
      console.log(`📦 ${suite.name}`);

      for (const test of suite.tests) {
        const status = test.passed ? "✅" : "❌";
        console.log(`  ${status} ${test.name} (${test.duration}ms)`);

        if (!test.passed && test.error) {
          console.log(`      Error: ${test.error.message}`);
        }
      }

      console.log(
        `  ➡️  ${suite.totalPassed} passed, ${suite.totalFailed} failed (${suite.totalDuration}ms)\n`
      );

      totalTests += suite.tests.length;
      totalPassed += suite.totalPassed;
      totalFailed += suite.totalFailed;
    }

    console.log(
      `🏁 Test Results: ${totalPassed}/${totalTests} passed, ${totalFailed} failed`
    );

    if (totalFailed > 0) {
      process.exit(1);
    }
  }
}

// Simple assertion functions
export class Assert {
  static equal(actual: any, expected: any, message?: string): void {
    if (actual !== expected) {
      throw new Error(message || `Expected ${expected}, but got ${actual}`);
    }
  }

  static deepEqual(actual: any, expected: any, message?: string): void {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      throw new Error(
        message ||
          `Expected ${JSON.stringify(expected)}, but got ${JSON.stringify(
            actual
          )}`
      );
    }
  }

  static true(value: any, message?: string): void {
    if (value !== true) {
      throw new Error(message || `Expected true, but got ${value}`);
    }
  }

  static false(value: any, message?: string): void {
    if (value !== false) {
      throw new Error(message || `Expected false, but got ${value}`);
    }
  }

  static throws(fn: () => void, message?: string): void {
    try {
      fn();
      throw new Error(message || "Expected function to throw, but it didn't");
    } catch (error) {
      // Expected to throw
    }
  }

  static exists(filePath: string, message?: string): void {
    if (!fs.existsSync(filePath)) {
      throw new Error(message || `Expected file ${filePath} to exist`);
    }
  }

  static isArray(value: any, message?: string): void {
    if (!Array.isArray(value)) {
      throw new Error(message || `Expected array, but got ${typeof value}`);
    }
  }

  static isNumber(value: any, message?: string): void {
    if (typeof value !== "number") {
      throw new Error(message || `Expected number, but got ${typeof value}`);
    }
  }

  static isString(value: any, message?: string): void {
    if (typeof value !== "string") {
      throw new Error(message || `Expected string, but got ${typeof value}`);
    }
  }
}

// Export singleton instance
export const testRunner = new TestRunner();
export const assert = Assert;
