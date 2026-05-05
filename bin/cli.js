#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const targetDir = path.join(process.cwd(), '.agent');
const sourceDir = path.join(__dirname, '..');

const args = process.argv.slice(2);
const availableFrameworks = ['fastapi'];

let itemsToCopy = ['registry.json'];
let frameworksToFlatten = [];

if (args.length > 0) {
  const requestedFrameworks = args.filter(arg => availableFrameworks.includes(arg));
  if (requestedFrameworks.length > 0) {
    frameworksToFlatten = requestedFrameworks;
    console.log(`Installing specific skills: ${requestedFrameworks.join(', ')}...`);
  } else {
    console.log(`No valid frameworks found in arguments. Installing all skills...`);
    frameworksToFlatten = availableFrameworks;
  }
} else {
  console.log('Installing all Maha skills...');
  frameworksToFlatten = availableFrameworks;
}

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

try {
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  // Copy individual files (like registry.json)
  itemsToCopy.forEach(file => {
    const srcPath = path.join(sourceDir, file);
    const destPath = path.join(targetDir, file);
    if (fs.existsSync(srcPath)) {
      console.log(`Copying ${file}...`);
      fs.copyFileSync(srcPath, destPath);
    }
  });

  // Flatten framework contents into .agent/
  frameworksToFlatten.forEach(framework => {
    const frameworkPath = path.join(sourceDir, framework);
    if (fs.existsSync(frameworkPath)) {
      console.log(`Installing contents of ${framework} to .agent/...`);
      const items = fs.readdirSync(frameworkPath);
      items.forEach(item => {
        const srcPath = path.join(frameworkPath, item);
        const destPath = path.join(targetDir, item);
        copyRecursiveSync(srcPath, destPath);
      });
    }
  });

  console.log('Successfully installed Maha skills to .agent/');
} catch (error) {
  console.error('Error installing skills:', error.message);
  process.exit(1);
}
