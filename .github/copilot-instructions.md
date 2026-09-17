# Copilot Instructions

These instructions guide GitHub Copilot when working in this repository.

## Project Context

This is a **beginner-friendly educational course** teaching GitHub Copilot CLI. The repo contains Markdown chapters (00–07), Python/C#/JavaScript sample apps, and supporting assets (images, demo GIFs, glossary). It is **not** a software product — it is technical courseware.

## Writing Conventions

- **Audience**: Beginners with no AI/ML experience. Explain every technical term on first use.
- **Tone**: Friendly, encouraging, practical. Avoid jargon without explanation.
- **Examples**: All code blocks and `copilot` commands must be copy-paste ready. Test them mentally before including.
- **Naming**: Use kebab-case for session names, file names, and identifiers (e.g., `book-app-review`, not `book app review`).
- **Command syntax**: Standardize flag format — use `--flag=value` consistently when a value is required, `--flag` when boolean.
- **Precision**: Don't over-specify tool behavior that may vary across shells or OS. Describe what the user will see, not implementation details.
- **Fallbacks**: When referencing tool version requirements (e.g., `gh` CLI version), always include upgrade instructions or a manual alternative.

## Content Conventions (from PR review patterns)

These patterns were mined from actual PR review feedback and represent recurring maintainer expectations:

- When showing multi-step workflows, ensure all prerequisite steps are included (e.g., `git add` before `git diff --staged`).
- When introducing a concept with an example, use consistent naming throughout the section — don't mix kebab-case and quoted names.
- When describing a command's behavior, match the level of specificity in the official release notes — don't state behavior that may differ across environments.
- If a feature requires a minimum tool version, mention the version AND provide a fallback path for users who can't upgrade yet.

## Sample Code Conventions

- **Primary sample**: Always use `samples/book-app-project/` (Python) for examples in chapters.
- **Test framework**: pytest — test files go in `samples/book-app-project/tests/` and follow `test_*.py` naming.
- **Python version**: 3.10+ (per `samples/book-app-project/pyproject.toml`).
- **Intentional bugs**: Files in `samples/book-app-buggy/` and `samples/buggy-code/` contain **deliberate bugs** for exercises. Never fix them.

## Build, Test, and Lint Commands

Run commands from the repository root unless a different directory is shown.

### Course content and demos

```bash
npm install
npm run release
```

`npm run release` runs the demo tape generation and GIF verification pipeline. The
individual scripts are available in `package.json` when only one pipeline step is
needed. There is no repository-wide lint script.

### Primary Python sample

```bash
cd samples/book-app-project
python -m pytest
python -m pytest tests/test_books.py::test_add_book
python -m pytest tests/test_book_app.py::test_read_command_marks_book_as_read
python book_app.py help
```

The Python sample uses `pytest`; its tests replace `books.DATA_FILE` with a
temporary path, so tests should not modify the checked-in `data.json`.

### JavaScript and C# samples

```bash
cd samples/book-app-project-js
npm test
node --test --test-name-pattern="should add a book" tests/test_books.js

cd ../book-app-project-cs
dotnet test Tests/BookApp.Tests.csproj
dotnet test Tests/BookApp.Tests.csproj --filter "FullyQualifiedName~BookCollectionTests"
```

## Chapter Structure

Every chapter (00–07) follows the same pattern in its `README.md`:

1. Real-World Analogy
2. Core Concepts
3. Hands-On Examples
4. Assignment
5. What's Next

Do not deviate from this structure when editing or adding chapter content.

## Architecture

This repository is courseware organized around a single learning path, not one
production application. The root README links chapters `00` through `07`; each
chapter combines an analogy, concepts, runnable hands-on examples, an assignment,
and a next step. The chapters use the Python book app as the primary example and
refer to parallel C# and JavaScript ports where language comparison is useful.

The book app has the same two-layer shape in each language: a CLI entry point
handles commands and user interaction, while a collection/data module owns book
operations and JSON persistence. The Python version is in
`samples/book-app-project/`, with `book_app.py` as the CLI, `books.py` as the
domain and persistence layer, `data.json` as sample state, and pytest tests under
`tests/`. The C# and JavaScript directories mirror this separation with their
language-specific test frameworks.

The `.github/scripts/` directory supports the course publishing workflow. The
root npm scripts generate chapter headers and terminal demos; generated demo
assets and source tapes are part of the teaching material, so check the relevant
chapter and asset references when changing demo commands.

## Markdown Formatting

- Use standard GitHub-Flavored Markdown.
- Images go in the repo-root `assets/` directory.
- Use relative links for cross-chapter references (e.g., `../03-development-workflows/README.md`).
- Emoji usage is encouraged for section headers (matching existing style).

## Maintenance Matrix

| Change Made | Files to Update |
|---|---|
| New chapter added | `README.md` (course table), `AGENTS.md` (structure table), `assets/learning-path.png` |
| Chapter content updated | The chapter's `README.md`, verify cross-references in adjacent chapters |
| New sample app variant added | `AGENTS.md` (structure table), `samples/` directory, relevant chapter references |
| Sample app code changed | `samples/book-app-project/tests/` (update/add tests), chapters referencing that code |
| Bug intentionally added to buggy samples | `samples/book-app-buggy/` or `samples/buggy-code/` only — do NOT update tests |
| New skill added | `.github/skills/{skill-name}/SKILL.md`, `samples/skills/` (example copy), Chapter 05 |
| New agent template added | `samples/agents/`, Chapter 04 |
| New MCP config added | `samples/mcp-configs/`, Chapter 06 |
| Glossary term introduced | `GLOSSARY.md` — add definition in alphabetical order |
| npm scripts changed | `package.json`, `AGENTS.md` (build section) |
| Devcontainer updated | `.devcontainer/devcontainer.json`, Chapter 00 (setup instructions) |
| Image or banner changed | `assets/` directory, any README referencing the image |
| Copilot CLI version requirements change | Chapter 00, Chapter 01, `.devcontainer/devcontainer.json` |
