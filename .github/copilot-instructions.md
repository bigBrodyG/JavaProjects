# Java School Projects - AI Agent Instructions

## Project Overview
This is a collection of educational Java projects for school, each demonstrating core OOP concepts. Projects are auto-compiled and showcased on GitHub Pages via CI/CD pipeline at https://bigBrodyG.github.io/JavaProjects/

## Project Structure Convention
Each project follows this standardized layout:
```
ProjectName/
├── src/           # Source files (*.java)
├── bin/           # Compiled .class files (auto-generated, gitignored)
├── lib/           # Optional external JARs
└── README.md      # Optional VS Code Java template
```

**Critical**: The `Main.java` file or a class with `public static void main(String[] args)` must exist in `src/` for the build pipeline to execute the project.

## Build & Execution Workflow

### Local Development
Compile and run any project from workspace root:
```fish
# Compile
javac -d ProjectName/bin ProjectName/src/*.java

# Run (from bin directory)
cd ProjectName/bin && java Main
```

### Automated CI/CD Pipeline
The `.github/workflows/auto-update-site.yml` workflow:
1. **Auto-discovers** all directories with `src/*.java` files
2. **Compiles** each project: `javac -d bin src/*.java`
3. **Executes** to capture output for the showcase
4. **Generates** HTML pages via `.github/scripts/generate-site.py`
5. **Deploys** to GitHub Pages automatically on push to `main`

The Python generator (`generate-site.py`) creates individual HTML pages with syntax highlighting, tabs for multiple source files, and animated output display.

## Code Patterns & Conventions

### Java Style
- **Author tags**: `@author giordii.dev` in Javadoc comments (see `02_Verifica_lab/`)
- **Validation**: Constructor parameter validation with `IllegalArgumentException` and descriptive messages
  ```java
  if (durataSec <= 0) {
      throw new IllegalArgumentException("durata > 0");
  }
  ```
- **Null checks**: Use `Objects.requireNonNull()` or explicit null checks with meaningful messages
- **Immutability**: Prefer `final` fields for domain objects (e.g., `Brano`, `Abitazione`)

### Common Imports & APIs
Projects extensively use:
- `java.util.ArrayList` for collections
- `java.time.LocalDate` for dates (e.g., `Playlist/`, `SpeseManager/`)
- No external dependencies or build tools (Maven/Gradle) - plain Java compilation

### Inheritance Patterns
See `Ereditarietà/` and `Immobili/` projects:
- Base classes: `Persona` → `Docente`/`Studente`
- Abstract classes: `Abitazione` (abstract) → `Appartamento`/`Villa` (concrete)
- Protected constructors in abstract base classes
- `@Override toString()` for readable output

### Data Structures
- **Manager pattern**: Classes like `MacchinaDistributrice`, `SpesaManager`, `LibreriaMusicale` manage `ArrayList` collections
- **No databases**: All data is in-memory for educational purposes
- **Italian naming**: Domain classes use Italian names (`Spese`, `Brano`, `Abitazione`)

## Testing & Validation
- No formal unit tests - projects are validated by running and checking output
- `Main.java` serves as integration test with hardcoded example data
- GitHub Actions captures stdout/stderr to verify successful execution

## Documentation Standards
- **Javadoc**: Used in formal projects like `02_Verifica_lab/` with parameter descriptions
- **READMEs**: Most projects use generic VS Code Java template; main README is in workspace root
- **Comments**: Minimal; code is self-documenting with Italian names for clarity

## Adding New Projects
1. Create `NewProject/src/` with Java files including a `main()` method
2. Push to `main` branch - CI/CD handles the rest automatically
3. Verify on GitHub Pages within ~2 minutes

## Common Issues
- **Missing main method**: Ensure at least one class has `public static void main(String[] args)`
- **Compilation errors**: Check `docs/projectname-compile.log` on GitHub Pages
- **Italian characters**: Source files use UTF-8 encoding for Italian text
