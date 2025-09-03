import * as fs from 'fs';
import * as path from 'path';

interface CategoryMetadata {
  category: string;
  point: number;
  subCategories?: CategoryMetadata[];
}

interface KnowledgeMetadata {
  categories: CategoryMetadata[];
  totalFiles: number;
  lastUpdated: string;
}

function scanDirectory(dirPath: string): CategoryMetadata[] {
  const categories: CategoryMetadata[] = [];
  
  try {
    const items = fs.readdirSync(dirPath, { withFileTypes: true });
    
    // Find subdirectories
    const subdirs = items.filter(item => item.isDirectory() && !item.name.startsWith('.'));
    
    // For each subdirectory, create a category
    for (const subdir of subdirs) {
      const subdirPath = path.join(dirPath, subdir.name);
      const subCategories = scanDirectory(subdirPath);
      
      // Count all files in this subdirectory (including nested ones)
      const totalFilesInSubdir = countFilesRecursively(subdirPath);
      
      const categoryData: CategoryMetadata = {
        category: subdir.name,
        point: totalFilesInSubdir
      };
      
      if (subCategories.length > 0) {
        categoryData.subCategories = subCategories;
      }
      
      categories.push(categoryData);
    }
    
  } catch (error) {
    console.error(`Error scanning directory ${dirPath}:`, error);
  }
  
  return categories;
}

function countFilesRecursively(dirPath: string): number {
  let count = 0;
  
  try {
    const items = fs.readdirSync(dirPath, { withFileTypes: true });
    
    for (const item of items) {
      if (item.name.startsWith('.')) continue;
      
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
  const knowledgesPath = path.join(__dirname, '..', 'knowledges');
  
  if (!fs.existsSync(knowledgesPath)) {
    console.error('knowledges directory not found');
    return;
  }
  
  // Check if knowledges directory has subdirectories or files
  const items = fs.readdirSync(knowledgesPath, { withFileTypes: true });
  const subdirs = items.filter(item => item.isDirectory() && !item.name.startsWith('.'));
  const filesInRoot = items.filter(item => item.isFile() && !item.name.startsWith('.') && item.name !== 'meta.json').length;
  
  let categories: CategoryMetadata[] = [];
  
  // Scan subdirectories
  if (subdirs.length > 0) {
    categories = scanDirectory(knowledgesPath);
  }
  
  // If root has files (excluding meta.json), add them as a root category
  if (filesInRoot > 0) {
    categories.push({
      category: 'root',
      point: filesInRoot
    });
  }
  
  const totalFiles = countFilesRecursively(knowledgesPath) - (fs.existsSync(path.join(knowledgesPath, 'meta.json')) ? 1 : 0);
  
  const metadata: KnowledgeMetadata = {
    categories: categories,
    totalFiles: totalFiles,
    lastUpdated: new Date().toISOString()
  };
  
  const outputPath = path.join(knowledgesPath, 'meta.json');
  fs.writeFileSync(outputPath, JSON.stringify(metadata, null, 2));
  
  console.log(`Metadata generated successfully at ${outputPath}`);
  console.log(`Total files: ${totalFiles}`);
  console.log(`Categories: ${categories.length}`);
}

// Run the script
generateMetadata();