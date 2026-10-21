# Contributing to Entab-D

Thank you for your interest in contributing to Entab-D! Entab-D is a lightweight, privacy-conscious Chrome extension designed to automate tab organization, deduplication, and predictive workflows.

## Code of Conduct

Please treat all contributors, reviewers, and users with professional respect. Constructive collaboration is required across all pull requests and issue threads.

## Development Workflow

### Prerequisites

- Google Chrome (version 100+ supporting Manifest V3 and Tab Groups API).
- Python 3.9+ (if working on the optional local synchronization daemon).
- Git.

### Setting Up Local Environment

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/Inkesk-Dozing/entab-D.git
   cd entab-D
   ```
2. Open Chrome and navigate to `chrome://extensions`.
3. Toggle **Developer mode** to `ON` in the upper right.
4. Click **Load unpacked** and select the repository directory.

## Commit Message Conventions

Entab-D enforces the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` Adds a new user-facing capability or API feature.
- `fix:` Patches a bug or addresses runtime race conditions.
- `docs:` Modifies documentation or inline specifications.
- `refactor:` Code reorganization without behavioral alteration.
- `perf:` Execution speed or memory footprint improvements.
- `test:` Unit, mock, or integration test additions.
- `chore:` Build scripts, manifest updates, or administrative tasks.

*Example*: `feat: implement cross-window tab group consolidation`

## Pull Request Guidelines

1. **Link Issues**: Every PR must reference an existing issue from `/docs/issues/` (e.g., `Resolves #003`).
2. **Branch Naming**: Format branch names as `type/issue-number-short-description` (e.g., `fix/002-service-worker-persistence`).
3. **No Unrelated Changes**: Keep PR diffs focused on the targeted feature or bug fix.
4. **Code Quality**:
   - Ensure all JavaScript passes strict syntax validation without undeclared variables.
   - Guard against service worker suspension and asynchronous race conditions.
   - Do not request unneeded permissions in `manifest.json`.
