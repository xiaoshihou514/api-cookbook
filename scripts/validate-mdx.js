import fs from 'fs';
import { compile } from '@mdx-js/mdx';
import { glob } from 'glob';

async function validateMDX() {
  try {
    const mdxFiles = await glob('docs/**/*.mdx');
    
    for (const file of mdxFiles) {
      console.log(`Validating: ${file}`);
      try {
        const content = fs.readFileSync(file, 'utf8');
        await compile(content, { jsx: true });
        console.log(`✅ ${file} - Valid MDX`);
      } catch (error) {
        console.error(`❌ ${file} - MDX Error:`, error.message);
        process.exit(1);
      }
    }
    
    console.log(`\n🎉 All ${mdxFiles.length} MDX files are valid!`);
  } catch (error) {
    console.error('❌ Validation failed:', error.message);
    process.exit(1);
  }
}

validateMDX(); 