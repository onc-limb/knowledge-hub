import * as fs from "fs";
import * as path from "path";

interface CategoryMetadata {
  category: string;
  point: number;
  names?: string[];
  subCategories?: CategoryMetadata[];
  subSubCategories?: CategoryMetadata[];
}

interface KnowledgeMetadata {
  categories: CategoryMetadata[];
  totalFiles: number;
  lastUpdated: string;
}

function scanDirectory(dirPath: string, depth: number = 0): CategoryMetadata[] {
  const categories: CategoryMetadata[] = [];

  try {
    const items = fs.readdirSync(dirPath, { withFileTypes: true });

    // Find subdirectories
    const subdirs = items.filter(
      (item) => item.isDirectory() && !item.name.startsWith(".")
    );

    // For each subdirectory, create a category
    for (const subdir of subdirs) {
      const subdirPath = path.join(dirPath, subdir.name);
      const directFiles = getDirectFilenames(subdirPath);

      const categoryData: CategoryMetadata = {
        category: subdir.name,
        point: 0, // Will be calculated later
      };

      // Add filenames if there are any direct files
      if (directFiles.length > 0) {
        categoryData.names = directFiles;
      }

      if (depth === 0) {
        // Level 1: dirs - scan for subdirectories (subdirs)
        const subCategories = scanDirectory(subdirPath, depth + 1);
        if (subCategories.length > 0) {
          categoryData.subCategories = subCategories;
        }
        // Count files in all subdirectories
        categoryData.point = countFilesRecursively(subdirPath);
      } else if (depth === 1) {
        // Level 2: subdirs - scan for sub-subdirectories
        const subSubCategories = scanDirectory(subdirPath, depth + 1);
        if (subSubCategories.length > 0) {
          categoryData.subSubCategories = subSubCategories;
        }
        // Count files in this subdirectory and its sub-subdirectories
        categoryData.point = countFilesRecursively(subdirPath);
      } else if (depth === 2) {
        // Level 3: sub-subdirs - only count files, no further nesting
        categoryData.point = countFilesRecursively(subdirPath);
      }

      categories.push(categoryData);
    }
  } catch (error) {
    console.error(`Error scanning directory ${dirPath}:`, error);
  }

  return categories;
}

function getDirectFilenames(dirPath: string): string[] {
  const filenames: string[] = [];

  try {
    const items = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const item of items) {
      if (item.name.startsWith(".")) continue;

      if (item.isFile()) {
        filenames.push(item.name);
      }
    }
  } catch (error) {
    console.error(`Error reading filenames in ${dirPath}:`, error);
  }

  return filenames;
}

function countFilesRecursively(dirPath: string): number {
  let count = 0;

  try {
    const items = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const item of items) {
      if (item.name.startsWith(".")) continue;

      if (item.isFile()) {
        count++;
      } else if (item.isDirectory()) {
        count += countFilesRecursively(path.join(dirPath, item.name));
      }
    }
  } catch (error) {
    console.error(`Error counting files in ${dirPath}:`, error);
  }

  return count;
}

function generateMetadata(): void {
  const knowledgesPath = path.join(process.cwd(), "knowledges");

  if (!fs.existsSync(knowledgesPath)) {
    console.error("knowledges directory not found");
    return;
  }

  // Check if knowledges directory has subdirectories
  const items = fs.readdirSync(knowledgesPath, { withFileTypes: true });
  const subdirs = items.filter(
    (item) => item.isDirectory() && !item.name.startsWith(".")
  );
  const filesInRoot = items.filter(
    (item) =>
      item.isFile() && !item.name.startsWith(".") && item.name !== "meta.json"
  ).length;

  let categories: CategoryMetadata[] = [];

  // Scan subdirectories (3-level hierarchy: root -> dirs -> subdirs -> sub-subdirs)
  if (subdirs.length > 0) {
    categories = scanDirectory(knowledgesPath, 0);
  }

  // Warning if root has files (excluding meta.json)
  if (filesInRoot > 0) {
    console.warn(
      `Warning: Found ${filesInRoot} files in root directory. Consider moving them to appropriate subdirectories.`
    );
  }

  const totalFiles =
    countFilesRecursively(knowledgesPath) -
    (fs.existsSync(path.join(knowledgesPath, "meta.json")) ? 1 : 0);

  const metadata: KnowledgeMetadata = {
    categories: categories,
    totalFiles: totalFiles,
    lastUpdated: new Date().toISOString(),
  };

  const outputPath = path.join(knowledgesPath, "meta.json");
  fs.writeFileSync(outputPath, JSON.stringify(metadata, null, 2));

  console.log(`Metadata generated successfully at ${outputPath}`);
  console.log(`Total files: ${totalFiles}`);
  console.log(`Categories: ${categories.length}`);

  // Display hierarchy structure
  console.log("\nHierarchy structure:");
  categories.forEach((category) => {
    const filesInfo = category.names ? ` [${category.names.join(", ")}]` : "";
    console.log(
      `├── ${category.category} (${category.point} files)${filesInfo}`
    );
    if (category.subCategories) {
      category.subCategories.forEach((subCat, index) => {
        const isLast = index === category.subCategories!.length - 1;
        const subFilesInfo = subCat.names
          ? ` [${subCat.names.join(", ")}]`
          : "";
        console.log(
          `│   ${isLast ? "└──" : "├──"} ${subCat.category} (${
            subCat.point
          } files)${subFilesInfo}`
        );
        if (subCat.subSubCategories) {
          subCat.subSubCategories.forEach((subSubCat, subIndex) => {
            const isSubLast = subIndex === subCat.subSubCategories!.length - 1;
            const prefix = isLast ? "    " : "│   ";
            const subSubFilesInfo = subSubCat.names
              ? ` [${subSubCat.names.join(", ")}]`
              : "";
            console.log(
              `${prefix}    ${isSubLast ? "└──" : "├──"} ${
                subSubCat.category
              } (${subSubCat.point} files)${subSubFilesInfo}`
            );
          });
        }
      });
    }
  });
}

// Run the script
generateMetadata();
