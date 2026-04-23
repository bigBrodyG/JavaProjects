# CODE QUALITY REPORT

## Summary of Changes
Performed a comprehensive analysis of the codebase and addressed various issues ranging from compilation errors to code smells and best practices.

### 1. Error Detection & Resolution
- **Fixed Java Version Mismatches**: Updated `pom.xml` files in `AppDelPorcoDio`, `EsercitazioneVerifica`, and `AuradelPorDios` from Java 25 to Java 21 to match the environment JDK.
- **Resolved Compilation Failures**: All JavaFX projects now compile successfully after the version update.

### 2. Warning Analysis & Cleanup
- **Improved Exception Handling**: Fixed an empty catch block in `ImpiccatoController.java` by adding `printStackTrace()`.
- **Naming Conventions**: Renamed `convertitoreFXML.java` to `ConvertitoreFXML.java` and updated the class name to follow PascalCase.

### 3. Code Quality Improvements
- **Null-Safety in String Comparisons**: Refactored `variable.equals("literal")` to `"literal".equals(variable)` in `HelloController.java` and `Calcolatrice.java` to prevent potential `NullPointerException`.
- **String Literal Extraction**: Extracted repeated string literals (4+ occurrences) into `private static final String` constants in the following files:
  - `ConvertitoreController.java` ("Input Error")
  - `Esercizi/GestionePC/src/Main.java` ("Windows 11 Pro")
  - `Esercizi/Libro/src/Libro.java` (Separators and labels)
  - `Laboratorio/Scuola/src/Main.java` ("Stipendio effettivo: €")
  - `Laboratorio/Playlist/src/Main.java` ("Trap")

### 4. Metrics
- **Errors Fixed**: 3 (Java version mismatches causing build failures)
- **Code Smells Refactored**: 7+ (String literals, null-safety, naming)
- **Build Status**: 100% Success across all projects.

## Manual Review Required
- **Hardcoded Credentials**: `HelloController.java` contains hardcoded credentials (`admin`/`password123`). While improved for null-safety, these should be moved to a secure configuration or database in a production environment.

## Recommendations for Future Improvements
- **Automated Testing**: Implement JUnit tests for core logic to ensure long-term stability.
- **Dependency Management**: Periodically check for updates to JavaFX and Maven plugins.
- **Resource Management**: Systematically check all I/O operations for proper `try-with-resources` usage.
