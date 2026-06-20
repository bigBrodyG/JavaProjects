```markdown
# JavaProjects Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns, coding conventions, and workflows used in the `JavaProjects` repository. The repository is written in Java and does not use a specific framework. It emphasizes clear file naming, consistent import/export styles, and a basic approach to testing. This guide will help you contribute code that matches the project's established practices.

## Coding Conventions

### File Naming
- Use **PascalCase** for all file names.
  - **Example:** `MyClass.java`, `DataProcessor.java`

### Import Style
- Use **relative imports** within the project.
  - **Example:**
    ```java
    import mypackage.utils.Helper;
    ```

### Export Style
- Use **named exports** (i.e., explicitly declare public classes).
  - **Example:**
    ```java
    public class DataProcessor {
        // class implementation
    }
    ```

### Commit Messages
- Freeform style, no strict prefixes.
- Average commit message length: ~68 characters.
  - **Example:**  
    `Add data processing logic for user input validation`

## Workflows

### Adding a New Java Class
**Trigger:** When you need to add new functionality or features  
**Command:** `/add-class`

1. Create a new `.java` file using PascalCase (e.g., `NewFeature.java`).
2. Write your class with a `public` modifier.
3. Use relative imports for any internal dependencies.
4. Add relevant methods and logic.
5. Commit your changes with a clear, descriptive message.

### Importing Internal Utilities
**Trigger:** When you need to use helper functions or utilities from within the project  
**Command:** `/import-utility`

1. Identify the utility class you need (e.g., `Helper.java`).
2. Use a relative import at the top of your file:
    ```java
    import mypackage.utils.Helper;
    ```
3. Use the utility methods as needed in your code.

### Writing and Running Tests
**Trigger:** When you add or modify functionality and want to ensure correctness  
**Command:** `/run-tests`

1. Create a test file matching the pattern `*.test.*` (e.g., `DataProcessor.test.java`).
2. Write test cases for your classes and methods.
3. Use the project's preferred testing approach (framework is unknown; follow existing test patterns).
4. Run the tests using your preferred Java test runner or IDE.
5. Review results and fix any issues before committing.

## Testing Patterns

- Test files follow the pattern: `*.test.*` (e.g., `MyClass.test.java`).
- The specific testing framework is not defined; follow the structure of existing tests.
- Place test files alongside or near the code they test.
- Write clear, descriptive test cases for each public method.

**Example:**
```java
public class DataProcessorTest {
    // test methods for DataProcessor
}
```

## Commands
| Command         | Purpose                                             |
|-----------------|-----------------------------------------------------|
| /add-class      | Add a new Java class following project conventions  |
| /import-utility | Import and use internal utility classes             |
| /run-tests      | Write and execute tests for your Java code          |
```
