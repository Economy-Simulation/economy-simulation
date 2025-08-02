# 🚀 Smart Auto-Versioning System

This repository uses an intelligent automated versioning system that supports the complete pre-release lifecycle. The system analyzes your commits and automatically determines the appropriate version bump while preserving pre-release status.

## 📋 Overview

Our versioning system supports:
- **Alpha stage** (`a0`, `a1`, `a2`, ...)
- **Beta stage** (`b0`, `b1`, `b2`, ...)
- **Release Candidate stage** (`rc0`, `rc1`, `rc2`, ...)
- **Stable releases** (`1.0.0`, `1.1.0`, etc.)

## 🎯 Version Increment Types

### 1. **Stage Increments** 🔢
These increment only the stage number while keeping the same base version.

#### Alpha Increments
- **Pattern**: `0.1.0a0` → `0.1.0a1` → `0.1.0a2`
- **Use for**: Small iterations, minor tweaks, bug fixes within alpha
- **Commit message keywords**: 
  - `"[alpha increment]"`
  - `"[bump alpha]"`
  - `"[alpha bump]"`
  - `"[increment alpha]"`

#### Beta Increments
- **Pattern**: `0.1.0b0` → `0.1.0b1` → `0.1.0b2`
- **Use for**: Small iterations, refinements within beta
- **Commit message keywords**:
  - `"[beta increment]"`
  - `"[bump beta]"`
  - `"[beta bump]"`
  - `"[increment beta]"`

#### Release Candidate Increments
- **Pattern**: `0.1.0rc0` → `0.1.0rc1` → `0.1.0rc2`
- **Use for**: Final polishing, last-minute fixes
- **Commit message keywords**:
  - `"[rc increment]"`
  - `"[bump rc]"`
  - `"[rc bump]"`
  - `"[increment rc]"`
  - `"[release candidate increment]"`

### 2. **Stage Promotions** 📈
These move between different pre-release stages.

#### Alpha → Beta Promotion
- **Pattern**: `0.1.0a5` → `0.1.0b0`
- **Use for**: When alpha testing is complete and ready for broader testing
- **Commit message keywords**:
  - `"[alpha to beta]"`
  - `"[promote to beta]"`
  - `"[beta stage]"`

#### Beta → Release Candidate Promotion
- **Pattern**: `0.1.0b3` → `0.1.0rc0`
- **Use for**: When beta is feature-complete and ready for final testing
- **Commit message keywords**:
  - `"[beta to rc]"`
  - `"[promote to rc]"`
  - `"[release candidate stage]"`
  - `"[rc stage]"`

### 3. **Semantic Version Bumps** ✨🐛🚨
These increment the base version while preserving the current pre-release stage.

#### Patch Bumps (Bug Fixes)
- **Pattern**: `0.1.0a2` → `0.1.1a2`
- **Triggered by**: Automatic detection of bug fixes, small changes
- **Manual trigger**: Include `"fix"`, `"bug"`, `"patch"`, or `"hotfix"` in commit message

#### Minor Bumps (New Features)
- **Pattern**: `0.1.0a2` → `0.2.0a2`
- **Triggered by**: Automatic detection of new features, significant additions
- **Manual trigger**: Include `"feat"`, `"feature"`, `"add"`, `"new"`, or `"implement"` in commit message

#### Major Bumps (Breaking Changes)
- **Pattern**: `0.1.0a2` → `1.0.0a2`
- **Triggered by**: Automatic detection of breaking changes, major refactoring
- **Manual trigger**: Include `"break"`, `"breaking"`, `"major"`, or `"incompatible"` in commit message

### 4. **Final Graduation** 🎓
This removes the pre-release suffix and creates a stable release.

- **Pattern**: `0.1.0rc2` → `0.1.0`
- **Use for**: When ready for production release
- **Commit message keywords**:
  - `"[graduate from alpha]"`
  - `"[alpha graduation]"`
  - `"[graduate to stable]"`
  - `"[alpha -> stable]"`

## 📋 Complete Version Lifecycle Example

```
0.0.0a0  ← Initial alpha
  ↓ alpha increment: "[alpha increment]: initial implementation"
0.0.0a1  ← Alpha iteration
  ↓ minor: "feat: add user authentication"
0.1.0a1  ← New feature (preserves alpha stage)
  ↓ alpha increment: "[alpha increment]: refine auth flow"
0.1.0a2  ← Alpha refinement
  ↓ patch: "fix: resolve login timeout issue"
0.1.1a2  ← Bug fix (preserves alpha stage)
  ↓ promote to beta: "[alpha to beta]: ready for wider testing"
0.1.1b0  ← Beta stage
  ↓ beta increment: "[beta increment]: UI polish"
0.1.1b1  ← Beta iteration
  ↓ minor: "feat: add dashboard analytics"
0.2.0b1  ← New feature (preserves beta stage)
  ↓ promote to rc: "[beta to rc]: feature complete"
0.2.0rc0 ← Release candidate
  ↓ rc increment: "[rc increment]: final documentation"
0.2.0rc1 ← RC refinement
  ↓ graduate: "[graduate from alpha]: production ready"
0.2.0    ← Stable release! 🎉
```

## 🎮 How to Use (Squash Merge Workflow)

Since this repository uses **squash merges only**, follow these steps:

### Step 1: Create Your Feature Branch
```bash
git checkout -b feature/my-awesome-feature
# Make your changes and commits normally
```

### Step 2: Create Pull Request
When creating your PR, **the title and description don't matter for versioning**. The system only looks at the **final squash commit message**.

### Step 3: Set Squash Commit Message
When merging your PR, GitHub will show a "Squash and merge" button. **This is where you control the versioning**:

#### For Stage Increments:
```
[alpha increment]: refined user interface components

- Improved button styling
- Fixed spacing issues
- Updated color scheme
```

#### For Stage Promotions:
```
[alpha to beta]: authentication system complete

- All auth features implemented
- Unit tests passing
- Ready for broader testing
```

#### For Semantic Bumps (automatic detection):
```
feat: add real-time notifications

- Implemented WebSocket connection
- Added notification UI components
- Integrated with backend events
```

#### For Final Release:
```
[graduate from alpha]: version 1.0.0 ready for production

- All features tested and stable
- Documentation complete
- Performance optimized
```

## 🔍 Automatic Detection

The system automatically detects version bump types based on:

### Major Changes (🚨):
- Deleted core files
- Breaking change patterns in code
- Large refactoring (>100 lines in core files)
- Keywords: "breaking", "incompatible", "migration required"

### Minor Changes (✨):
- New files (especially APIs/interfaces)
- New functions/classes/methods
- Medium-sized changes (20-100 lines)
- Keywords: "feature", "implement", "add"

### Patch Changes (🐛):
- Small modifications (<20 lines)
- Documentation updates
- Test updates
- Keywords: "fix", "bug", "hotfix"

## ⚙️ Configuration Files

The versioning system is controlled by:
- `.github/workflows/version-check.yml` - GitHub Actions workflow
- `.github/scripts/analyze_version.py` - Version analysis script
- `backend/global_economy_sim/__about__.py` - Version storage

## 🛡️ Safety Features

- **Bot commit detection**: Prevents infinite loops by skipping version-bump commits
- **Environment variable override**: Set `SKIP_VERSIONING=true` to disable
- **Backward progression protection**: Prevents moving backwards in release stages
  - Cannot use alpha commands on beta/rc versions
  - Cannot use beta commands on rc versions  
  - Cannot promote backwards (e.g., rc → beta, beta → alpha)
  - Cannot graduate already stable versions
- **Stage validation**: Only works on appropriate pre-release versions for stage operations
- **Unknown pre-release type handling**: Safely preserves unknown pre-release identifiers
  - Logs unknown types for awareness
  - Preserves original identifier during semantic bumps
  - Prevents stage-specific operations on unknown types
- **Fallback**: Defaults to patch bump if analysis fails

### Unknown Pre-Release Type Handling

If the system encounters an unknown pre-release type (not `a`, `b`, or `rc`):

✅ **Safe Operations**:
- Semantic bumps preserve the unknown identifier: `0.1.0dev1` → `0.2.0dev1`
- Graduation works: `0.1.0dev1` → `0.1.0`

❌ **Blocked Operations**:
- Stage increments: `[alpha increment]` on `0.1.0dev1` → warning + fallback
- Stage promotions: `[alpha to beta]` on `0.1.0dev1` → warning + fallback

**Example with unknown type `dev`**:
```
Current: 0.1.0dev1
[alpha increment] → ⚠️ Warning + automatic analysis
feat: new feature → 0.2.0dev1 ✅ (preserves dev1)
[graduate from alpha] → 0.1.0 ✅ (graduates correctly)
```

### Backward Progression Examples

❌ **These will be ignored and trigger automatic analysis instead**:
- `[alpha increment]` when current version is `0.1.0b2` (beta)
- `[beta increment]` when current version is `0.1.0rc1` (release candidate)
- `[alpha to beta]` when current version is `0.1.0rc1` (already past beta)
- `[graduate from alpha]` when current version is `0.1.0` (already stable)

✅ **Valid progressions only**:
- `0.1.0a2` → `0.1.0a3` (alpha increment)
- `0.1.0a5` → `0.1.0b0` (alpha to beta)
- `0.1.0b3` → `0.1.0rc0` (beta to rc)
- `0.1.0rc2` → `0.1.0` (graduate to stable)

## 📝 Quick Reference

| Goal | Squash Commit Message Example |
|------|-------------------------------|
| Alpha iteration | `[alpha increment]: improved error handling` |
| Beta iteration | `[beta increment]: performance optimizations` |
| RC iteration | `[rc increment]: final bug fixes` |
| Alpha → Beta | `[alpha to beta]: core features complete` |
| Beta → RC | `[beta to rc]: ready for final testing` |
| RC → Stable | `[graduate from alpha]: production release` |
| Automatic patch | `fix: resolve memory leak in data processor` |
| Automatic minor | `feat: add export functionality` |
| Automatic major | `breaking: redesign authentication API` |

## 🚨 Important Notes

1. **Only squash commit messages matter** - individual commits in your branch are ignored
2. **Keywords must be in square brackets** - `[alpha increment]` works, but `alpha increment` won't
3. **Keywords are case-insensitive** - `[Alpha Increment]` works the same as `[alpha increment]`
4. **Stage operations only work on pre-release versions** - you can't increment alpha on a stable version
5. **Graduation works from any pre-release stage** - you can graduate directly from alpha, beta, or rc
6. **Version preservation** - semantic bumps (patch/minor/major) preserve your current pre-release stage

---

**Happy versioning! 🚀**
