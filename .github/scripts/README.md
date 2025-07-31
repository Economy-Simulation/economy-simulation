# GitHub Actions Scripts

This directory contains Python scripts used by the GitHub Actions workflows to maintain a clean and modular codebase.

## Scripts

### `analyze_version.py`
**Purpose:** Main version analysis and bumping logic for the smart auto-versioning system.

**Features:**
- Analyzes git changes to determine appropriate version bump type (major/minor/patch)
- Updates version in `__about__.py` file
- Generates detailed analysis reports
- Handles bot commit detection to prevent infinite loops
- Creates GitHub Actions outputs for downstream steps

**Dependencies:** GitPython, packaging, subprocess

**Usage:** Called automatically by the `version-check.yml` workflow on pushes to main branch.

### `analyze_pr.py`  
**Purpose:** PR impact analysis for version bump prediction.

**Features:**
- Analyzes proposed changes in pull requests
- Predicts likely version bump type when PR is merged
- Generates PR summary for commenting
- Compares current PR branch with main branch

**Dependencies:** GitPython, subprocess

**Usage:** Called automatically by the `version-check.yml` workflow on pull request events.

### `requirements.txt`
**Purpose:** Python dependencies for the automation scripts.

**Contents:**
- `gitpython>=3.1.0` - Git repository interaction
- `packaging>=21.0` - Version parsing and manipulation

## Architecture Benefits

### Before Refactoring
- Large embedded Python scripts in YAML workflow files
- Difficult to test and debug individual components
- Poor code organization and readability
- Hard to maintain and update logic

### After Refactoring  
- ✅ Modular Python scripts with clear separation of concerns
- ✅ Easier testing and debugging of individual components
- ✅ Better code organization and maintainability
- ✅ Centralized dependency management
- ✅ Improved readability of both scripts and workflow files
- ✅ Reusable components for future automation needs

## Workflow Integration

The scripts are integrated into `.github/workflows/version-check.yml`:

1. **Main Branch Push:** Runs `analyze_version.py` to perform smart version analysis and bumping
2. **Pull Request:** Runs `analyze_pr.py` to predict version impact and comment on PR

Both scripts write output files that are consumed by subsequent workflow steps for commit messages, PR comments, and release notes.
