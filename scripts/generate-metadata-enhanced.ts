#!/usr/bin/env node

// Enhanced CLI script with unlimited hierarchy support
import { parseArgs, showHelp, showVersion, CLIParser } from "../src/cli";
import { runCLI } from "../src/index";

function main(): void {
  try {
    const options = parseArgs();

    // Handle help and version flags
    if (options.help) {
      showHelp();
      return;
    }

    if (options.version) {
      showVersion();
      return;
    }

    // Validate options
    CLIParser.validateOptions(options);

    // Run the metadata generation
    runCLI(options);
  } catch (error) {
    console.error("Error:", (error as Error).message);
    console.error("\nUse --help for usage information.");
    process.exit(1);
  }
}

// Run if this is the main module
if (require.main === module) {
  main();
}
