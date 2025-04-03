# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Test Commands

### C# (.NET)

- Build: `dotnet build <project-or-solution>`
- Run tests: `dotnet test`
- Run single test: `dotnet test --filter "FullyQualifiedName=Namespace.TestClass.TestMethod"`
- Watch tests: `dotnet watch test`

### JavaScript/TypeScript

- Build TypeScript: `npm run build`
- Start dev server: `npm run dev`

## Code Style Guidelines

### C# Style

- Follow TDD approach with xUnit
- Test naming: `When_<condition>_Should_<expected>`
- Use namespaces matching directory structure
- Require parameter null-checking
- Test classes must end with "Tests"
- Introduce interfaces only after multiple implementations
- Follow standard C# naming conventions (PascalCase for types/methods, camelCase for variables)

### TypeScript/JavaScript Style

- Prefer TypeScript over JavaScript for new code
- Use async/await for asynchronous operations
- Follow strict TDD principles from Cursor rules
