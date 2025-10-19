# 🤖 Java Projects Automation

This repository automatically builds and showcases Java projects on GitHub Pages.

## � How It Works

When you push to the `main` branch, GitHub Actions automatically:

1. **Detects** all Java projects (any folder with a `src/` directory containing `.java` files)
2. **Compiles** each project using `javac`
3. **Runs** the compiled programs and captures their output
4. **Generates** a beautiful HTML showcase website
5. **Deploys** to GitHub Pages automatically

## ✨ Adding a New Project

Simply create a new folder with your project:

```
YourProject/
├── src/
│   ├── MainClass.java
│   └── OtherClasses.java
└── README.md (optional)
```

Then commit and push:
```bash
git add .
git commit -m "Add new project: YourProject"
git push
```

**That's it!** GitHub Actions handles everything automatically.

## 🛠️ Local Scripts

### 1. `generate-site.py` - Site Generator
Generates the complete static website with all project pages.

**Usage:**
```bash
python3 .github/scripts/generate-site.py
```

### 2. `auto-add-project.py` - Local Project Detection (Optional)
For testing locally before pushing. Automatically detects new projects and adds them.

**Usage:**
```bash
python3 .github/scripts/auto-add-project.py
```

**What it does:**
1. 🔍 Scans for Java projects
2. ⚙️ Compiles and runs each new project
3. 📝 Adds project configuration to `generate-site.py`
4. 🔄 Regenerates the website

**Note:** This is mainly for local testing. The GitHub workflow handles everything automatically when you push.

## 📦 Project Structure Requirements

For automatic detection, your project must:

1. Be in a directory at the workspace root
2. Have a `src/` subdirectory
3. Contain `.java` files
4. Have at least one class with `public static void main(String[] args)`

Example:
```
JavaProjects/
├── Cerchio/
│   └── src/
│       └── Cerchio.java ✓ (has main method)
├── Orario/
│   └── src/
│       ├── Orario.java
│       └── TestOrario.java ✓ (has main method)
└── MyNewProject/
    └── src/
        └── MyNewProject.java ✓ (has main method)
```

## 🔧 Manual Method (Old Way)

If you prefer manual control:

1. **Add project to `generate-site.py`:**
   ```python
   {
       'name': 'MyProject',
       'id': 'myproject',
       'sources': ['MyProject/src/File1.java', 'MyProject/src/File2.java'],
       'output': 'docs/myproject-output.txt',
       'compile': 'docs/myproject-compile.log',
       'description': 'Description of my project',
       'type': 'teoria'  # or 'laboratorio'
   }
   ```

2. **Create output files:**
   ```bash
   cd MyProject
   javac -d bin src/*.java
   java -cp bin MainClass > ../docs/myproject-output.txt
   ```

3. **Regenerate site:**
   ```bash
   python3 .github/scripts/generate-site.py
   ```

## 🎨 Project Types

- **`teoria`** (📚): Theory projects - shown with purple "Teoria" badge
- **`laboratorio`** (🔬): Lab projects - shown with green "Laboratorio" badge

## 📄 Generated Files

For each project, these files are created:

- `docs/{project}.html` - Interactive project page with code and output
- `docs/{project}-output.txt` - Captured program output
- `docs/{project}-compile.log` - Compilation logs/errors
- `docs/index.html` - Main index page with all projects

## 🌐 Website Features

Each project page includes:

- 📝 **Syntax-highlighted code** with multiple file tabs
- ▶️ **Interactive "Run" button** with animated output
- 📋 **Copy code button**
- 🎨 **Beautiful dark theme** with gradient effects
- 📱 **Responsive design** for mobile devices
- 🔙 **Navigation** back to index

## 🚀 Workflow Example

```bash
# 1. Create a new Java project
mkdir MyCalculator
mkdir MyCalculator/src
echo 'public class Calculator { 
    public static void main(String[] args) {
        System.out.println("2 + 2 = " + (2+2));
    }
}' > MyCalculator/src/Calculator.java

# 2. Auto-add it to the site
python3 .github/scripts/auto-add-project.py
# When prompted, choose 't' for teoria or 'l' for laboratorio

# 3. Check the result
open docs/index.html
# Or view docs/calculator.html directly
```

## 🛠️ Troubleshooting

**"No main class found"**
- Make sure at least one `.java` file has `public static void main(String[] args)`

**"Compilation failed"**
- Check the compile log in `docs/{project}-compile.log`
- Fix any syntax errors in your Java code

**"Project not detected"**
- Ensure your project has a `src/` directory
- Make sure `.java` files are directly in `src/`, not in subdirectories

**"Already exists"**
- The project is already in `generate-site.py`
- Remove it from the projects list if you want to re-add it

## 💡 Tips

- Run `auto-add-project.py` regularly to catch new projects
- Commit the generated `docs/` folder to version control
- The website can be hosted on GitHub Pages
- Test your Java code works before adding to site
- Use descriptive project names (they become page titles)

## 📚 Dependencies

- Python 3.6+
- Java Development Kit (JDK)
- `javac` and `java` in PATH

## 🤝 Contributing

When adding features to the automation:

1. Test with multiple project types
2. Handle edge cases (empty output, compilation errors)
3. Provide clear user feedback
4. Update this README

---

Made with ❤️ for automating Java project documentation
