# Weekly Code Quality Check & Fix Report

## Summary
A comprehensive code quality check was performed across all projects in the repository. Key issues addressed include build configuration errors, null-safety improvements, missing annotations, and code refactoring for better readability and maintainability.

## Metrics
- **Compilation Errors Fixed:** 3 (Java version mismatch in Maven projects)
- **Null-Unsafe Comparisons Fixed:** 5
- **Missing @Override Annotations Added:** 3
- **Repeated String Literals Extracted:** 1 (Multiple occurrences)
- **Dependency Updates:** 1
- **Code Smells Refactored:** 1 (If-else to switch)

## Detailed Changes

### 1. Error Detection & Resolution
- **Java Version Fix:** Updated `pom.xml` files in `AppDelPorcoDio`, `EsercitazioneVerifica`, and `AuradelPorDios` to use Java 21 instead of the invalid version 25. This resolved the "invalid target release" build failures.
- **Verified Build:** Successfully ran the global `compile_all.sh` script, confirming all 38 projects now compile successfully.

### 2. Warning Analysis & Cleanup
- **Missing @Override:** Added `@Override` to `toString()` methods in `InventarioPC.java`, `Cd.java`, and `PortaCD.java` to comply with Java best practices and suppress compiler warnings.
- **Dependency Update:** Updated `controlsfx` from `11.2.1` to `11.2.3` in `ConvertitoreXML`.

### 3. Code Quality Improvements
- **Null-Pointer Prevention:** Refactored string comparisons in `HelloController.java` and `Calcolatrice.java` to use the null-safe `"literal".equals(variable)` pattern.
- **Code Refactoring:** Converted a complex `if-else` chain in `Calcolatrice.java`'s `result()` method to a modern `switch` expression for better readability and performance.
- **Constants Extraction:** Extracted a repeated string format for book details in `Libro.java` into a `private static final String` constant.

### 4. Best Practices Enforcement
- **Naming Conventions:** While some project names remain as originally created to preserve history, internal code was checked for basic naming convention compliance.
- **Resource Cleanup:** Verified that `InputStream` and other resources in `ImpiccatoController.java` are handled using try-with-resources.

## Recommendations for Future Improvements
1. **Security:** Consider moving hardcoded credentials in `HelloController.java` to a secure configuration file or environment variables.
2. **Naming:** Standardize project directory names to follow professional conventions.
3. **Unit Testing:** Increase test coverage, especially for the core logic in `Laboratorio` and `Esercizi` projects.
4. **Project Structure:** Ensure all projects follow the standard Maven/Gradle structure to simplify automation.
