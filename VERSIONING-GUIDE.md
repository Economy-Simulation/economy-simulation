# 🤖 Smart Auto-Versioning Guide

## Overview

This repository uses an intelligent auto-versioning system that works with GitHub's branch protection rules. The system creates pull requests for version bumps instead of pushing directly to main.

## How It Works

### 1. **Smart Analysis** 🧠
When you push to main, the AI analyzes your changes:
- **Major bump** 🚨: Breaking changes, deleted files, major refactoring
- **Minor bump** ✨: New features, API additions, significant new files
- **Patch bump** 🐛: Bug fixes, documentation, small improvements

### 2. **Auto Pull Request** 📝
The system creates a PR with:
- Automated version bump in `__about__.py`
- Detailed analysis of why the version was bumped
- Preview of the upcoming release

### 3. **Merge & Release** 🚀
When you merge the version bump PR:
- Git tag is automatically created
- GitHub release is generated
- Package is built and artifacts attached

## Branch Protection Compatibility

✅ **Works with branch protection rules**
- Requires PR reviews ✓
- Status checks must pass ✓  
- No direct pushes to main ✓

## Workflow Jobs

1. **`smart-version`** - Analyzes changes and creates version bump PR
2. **`auto-tag-and-release`** - Creates tags when version bump PR is merged
3. **`smart-release`** - Builds and publishes release when tag is created
4. **`pr-preview`** - Shows version impact preview on PRs

## Manual Override

If you need to override the version:
1. Edit `backend/global_economy_sim/__about__.py` manually
2. Commit with message containing "manual version" or "override version"
3. The system will skip auto-analysis

## Troubleshooting

### Common Issues:

**"Repository rule violations found"**
- ✅ **Fixed**: System now creates PRs instead of direct pushes

**"Changes must be made through a pull request"**
- ✅ **Expected**: Merge the auto-created version bump PR

**"Code scanning is waiting for results"**
- ⏳ **Normal**: Wait for CodeQL to complete, then merge PR

## Security Notes

- 🔒 All version bumps go through PR review process
- 🛡️ Branch protection rules are respected
- 🤖 Bot commits are clearly labeled
- 📋 Full audit trail in PR descriptions

---

*This guide explains the smart versioning system that automatically manages semantic versioning based on AI analysis of code changes.*
