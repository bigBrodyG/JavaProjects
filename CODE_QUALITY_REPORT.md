# Code Quality Report

## Summary of Changes

### 1. Error Detection & Resolution
- **Java Version Compatibility**: Fixed "invalid target release: 25" errors by downgrading target version to Java 21 in `pom.xml` for several projects.
  - Affected projects: `AuraApp` (formerly `AppDelPorcoDio`), `EsercitazioneVerifica`, `AuraProject` (formerly `AuradelPorDios`).

### 2. Professionalism & Naming
- **Offensive Content Removal**: Renamed projects and packages that contained offensive language.
  - `Laboratorio/JavaFX/AppDelPorcoDio` -> `Laboratorio/JavaFX/AuraApp`
  - `Laboratorio/JavaFX/AuradelPorDios` -> `Laboratorio/JavaFX/AuraProject`
- **Reference Updates**: Updated all package declarations, FXML controller paths, and Maven artifact IDs to reflect new names.

### 3. Code Quality Improvements
- **Code Smell: Repeated String Literals**:
  - Extracted "Stipendio effettivo: €" into a `private static final String` constant in `Laboratorio/Scuola/src/Main.java`.
- **Code Smell: Repetitive Logic**:
  - Refactored repetitive book information printing in `Esercizi/Libro/src/Libro.java` into a dedicated `stampaInfoLibro` helper method.
- **Exception Handling**:
  - Fixed an empty `catch (Exception ignored)` block in `Laboratorio/JavaFX/Impicciato/src/main/java/com/example/impicciato/ImpiccatoController.java` by adding `e.printStackTrace()`.

### 4. Build System Stability
- Verified that all 38 projects (Maven and plain Java) compile successfully using the root `compile_all.sh` script.

## Metrics
- **Errors Fixed**: 3 (Java version mismatch)
- **Offensive Terms Removed**: Numerous (across directories, files, and code)
- **Code Smells Refactored**: 2
- **Exception Handling Improvements**: 1
- **Projects Verified**: 38

## Recommendations
- **Standardize Java Version**: Ensure all new projects target Java 21 to match the environment.
- **CI/CD Integration**: Add automated checks for offensive language in new commits.
- **Refactoring**: Continue extracting common logic (like the book printing example) into reusable utility methods or classes.
