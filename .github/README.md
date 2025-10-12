# GitHub Actions Setup 🚀

This directory contains the GitHub Actions workflow and scripts to automatically build and deploy a showcase website for the Java projects.

## What It Does

The workflow:
1. **Compiles** all Java projects in the repository
2. **Runs** each program and captures the output
3. **Generates** a beautiful static website showing:
   - Source code with syntax highlighting
   - Compilation status
   - Program output
4. **Deploys** to GitHub Pages automatically

## Files

- `workflows/build-showcase.yml` - Main GitHub Actions workflow
- `scripts/generate-site.py` - Python script that generates the HTML website

## Setup Instructions

### 1. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to **Pages** (under "Code and automation")
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. Save the settings

### 2. Trigger the Workflow

The workflow runs automatically on:
- Every push to the `main` branch
- Every pull request to the `main` branch
- Manual trigger via "Actions" tab

To manually trigger:
1. Go to the **Actions** tab
2. Select "Build Java Showcase Website"
3. Click **Run workflow**

### 3. View Your Website

After the workflow completes successfully, your website will be available at:
```
https://bigBrodyG.github.io/JavaProjects/
```

## Local Testing

You can test the site generation locally:

```bash
# Create bin directories
mkdir -p Cerchio/bin mergeArray/bin OggettoCD/bin Punto/bin Rettangolo/bin vocalcount/bin

# Compile projects
javac -d Cerchio/bin Cerchio/src/*.java
javac -d mergeArray/bin mergeArray/src/*.java
javac -d OggettoCD/bin OggettoCD/src/*.java
javac -d Punto/bin Punto/src/*.java
javac -d Rettangolo/bin Rettangolo/src/*.java
javac -d vocalcount/bin vocalcount/src/*.java

# Run programs and capture output
cd Cerchio/bin && java Cerchio > ../../docs/cerchio-output.txt 2>&1; cd ../..
cd mergeArray/bin && java mergeArrays > ../../docs/mergearray-output.txt 2>&1; cd ../..
cd OggettoCD/bin && java Cd > ../../docs/oggettocd-output.txt 2>&1; cd ../..
cd Punto/bin && java Punto > ../../docs/punto-output.txt 2>&1; cd ../..
cd Rettangolo/bin && java Rettangolo > ../../docs/rettangolo-output.txt 2>&1; cd ../..
cd vocalcount/bin && java voc_count > ../../docs/vocalcount-output.txt 2>&1; cd ../..

# Generate website
python3 .github/scripts/generate-site.py

# Open the website
# On Linux: xdg-open docs/index.html
# On macOS: open docs/index.html
# On Windows: start docs/index.html
```

## Customization

### Adding New Projects

To add a new project to the showcase, edit `.github/scripts/generate-site.py` and add an entry to the `projects` list:

```python
{
    'name': 'YourProjectName',
    'sources': ['YourProject/src/YourClass.java'],
    'output': 'docs/yourproject-output.txt',
    'compile': 'docs/yourproject-compile.log'
}
```

Then update the workflow file to compile and run your project.

### Styling

The website styling is embedded in the `generate-site.py` script. You can modify the CSS in the `<style>` section to customize colors, fonts, and layout.

## Troubleshooting

### Workflow fails with permission errors

Make sure GitHub Pages is set to use "GitHub Actions" as the source in repository settings.

### Website shows compilation errors

Check the Actions log to see what compilation errors occurred. You may need to fix Java syntax errors in your code.

### Program output not showing

Ensure your Java programs have a `main` method that produces output to `System.out`.

## Technologies Used

- **GitHub Actions** - CI/CD automation
- **Python 3** - Site generation
- **Highlight.js** - Syntax highlighting
- **GitHub Pages** - Static site hosting
