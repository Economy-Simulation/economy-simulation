#!/usr/bin/env python3
"""
Smart Version Analysis Script for GitHub Actions

This script analyzes git changes to automatically determine appropriate semantic version bumps.
It performs intelligent analysis of code changes, commit messages, and file patterns to decide
whether a MAJOR, MINOR, or PATCH version bump is appropriate.

Used by: .github/workflows/version-check.yml
Purpose: Maintain 100% automated versioning with zero developer intervention
Dependencies: GitPython, packaging, subprocess
"""

import os
import re
import sys
import git
import subprocess
from packaging import version


def run_cmd(cmd):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, cwd='.').strip()
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Error: {e}")
        raise


def get_version_from_file():
    """Read version directly from __about__.py"""
    try:
        with open('backend/global_economy_sim/__about__.py', 'r') as f:
            content = f.read()
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
            return "0.1.0"  # fallback
    except FileNotFoundError:
        return "0.1.0"  # fallback


def update_version_file(new_version):
    """Update version directly in __about__.py"""
    try:
        with open('backend/global_economy_sim/__about__.py', 'r') as f:
            content = f.read()
        
        updated_content = re.sub(
            r'(__version__\s*=\s*["\'])([^"\']+)(["\'])',
            f'\\g<1>{new_version}\\g<3>',
            content
        )
        
        with open('backend/global_economy_sim/__about__.py', 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated __about__.py with version {new_version}")
        return True
    except Exception as e:
        print(f"❌ Failed to update version file: {e}")
        return False


def increment_version(current_version, bump_type):
    """Increment version based on bump type"""
    try:
        ver = version.parse(current_version)
        if bump_type == "major":
            return f"{ver.major + 1}.0.0"
        elif bump_type == "minor":
            return f"{ver.major}.{ver.minor + 1}.0"
        else:  # patch
            return f"{ver.major}.{ver.minor}.{ver.micro + 1}"
    except Exception as e:
        print(f"❌ Error incrementing version: {e}")
        return current_version


def analyze_changes():
    """Analyze git changes to determine version bump type"""
    try:
        # Get the last commit (since this runs on push to main)
        repo = git.Repo('.')
        
        # Get changes in the last commit
        last_commit = repo.head.commit
        if not last_commit.parents:
            print("ℹ️  Initial commit detected")
            return "patch", "Initial commit"
        
        changes = last_commit.diff(last_commit.parents[0])
        
        major_indicators = []
        minor_indicators = []
        patch_indicators = []
        
        print("🔍 Analyzing code changes...")
        
        for change in changes:
            file_path = change.a_path or change.b_path
            if not file_path:
                continue
                
            print(f"  📁 Analyzing: {file_path}")
            
            # Skip version bumps from the bot itself
            if file_path == 'backend/global_economy_sim/__about__.py':
                continue
            
            # Check file types and change patterns
            if file_path.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c')):
                if change.change_type == 'D':
                    major_indicators.append(f"Deleted core file: {file_path}")
                elif change.change_type == 'A':
                    if 'api' in file_path.lower() or 'interface' in file_path.lower():
                        minor_indicators.append(f"New API/interface: {file_path}")
                    else:
                        minor_indicators.append(f"New file: {file_path}")
                elif change.change_type == 'M':
                    # Analyze the actual diff content
                    try:
                        diff_text = str(change.diff)
                        
                        # Major change indicators
                        if any(pattern in diff_text.lower() for pattern in [
                            'class.*deleted', 'def.*deleted', 'function.*deleted',
                            'breaking change', 'deprecated', 'removed',
                            'incompatible', 'migration required'
                        ]):
                            major_indicators.append(f"Breaking change detected in {file_path}")
                        
                        # Count lines changed (approximate)
                        additions = diff_text.count('+')
                        deletions = diff_text.count('-')
                        total_changes = additions + deletions
                        
                        if total_changes > 100:
                            if 'api' in file_path.lower() or 'core' in file_path.lower():
                                major_indicators.append(f"Major refactoring in core file: {file_path} ({total_changes} changes)")
                            else:
                                minor_indicators.append(f"Significant changes: {file_path} ({total_changes} changes)")
                        elif total_changes > 20:
                            minor_indicators.append(f"Medium changes: {file_path} ({total_changes} changes)")
                        else:
                            patch_indicators.append(f"Small fix: {file_path} ({total_changes} changes)")
                            
                        # Feature indicators
                        if any(pattern in diff_text.lower() for pattern in [
                            'def ', 'class ', 'function ', 'new.*feature',
                            'add.*method', 'implement'
                        ]):
                            minor_indicators.append(f"New functionality in {file_path}")
                            
                    except Exception as e:
                        print(f"  ⚠️  Could not analyze diff for {file_path}: {e}")
                        patch_indicators.append(f"Modified: {file_path}")
            
            # Configuration changes
            elif file_path.endswith(('.json', '.yaml', '.yml', '.toml', '.cfg', '.ini')):
                if 'package.json' in file_path or 'pyproject.toml' in file_path:
                    minor_indicators.append(f"Package configuration updated: {file_path}")
                else:
                    patch_indicators.append(f"Config updated: {file_path}")
            
            # Documentation
            elif file_path.endswith(('.md', '.rst', '.txt')):
                patch_indicators.append(f"Documentation updated: {file_path}")
            
            # Tests
            elif 'test' in file_path.lower() or file_path.endswith('_test.py'):
                patch_indicators.append(f"Tests updated: {file_path}")
        
        # Analyze commit message for additional context
        commit_msg = last_commit.message.lower()
        if any(word in commit_msg for word in ['break', 'breaking', 'major', 'incompatible']):
            major_indicators.append(f"Breaking change indicated in commit: {last_commit.message[:50]}...")
        elif any(word in commit_msg for word in ['feat', 'feature', 'add', 'new', 'implement']):
            minor_indicators.append(f"Feature indicated in commit: {last_commit.message[:50]}...")
        elif any(word in commit_msg for word in ['fix', 'bug', 'patch', 'hotfix']):
            patch_indicators.append(f"Fix indicated in commit: {last_commit.message[:50]}...")
        
        print(f"\n📊 Analysis Results:")
        print(f"  🚨 Major indicators: {len(major_indicators)}")
        for indicator in major_indicators[:3]:  # Show first 3
            print(f"    - {indicator}")
            
        print(f"  ✨ Minor indicators: {len(minor_indicators)}")
        for indicator in minor_indicators[:3]:
            print(f"    - {indicator}")
            
        print(f"  🐛 Patch indicators: {len(patch_indicators)}")
        for indicator in patch_indicators[:3]:
            print(f"    - {indicator}")
        
        # Decision logic
        if major_indicators:
            return "major", major_indicators[0]
        elif minor_indicators:
            return "minor", minor_indicators[0]
        elif patch_indicators:
            return "patch", patch_indicators[0]
        else:
            return "patch", "Default patch bump for changes"
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return "patch", "Fallback patch bump due to analysis error"


def write_github_outputs(data):
    """Write outputs for GitHub Actions"""
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            for key, value in data.items():
                f.write(f"{key}={value}\n")


def create_version_summary(current_version, new_version, bump_type, reason):
    """Create detailed summary for GitHub Actions"""
    bump_emoji = {"major": "🚨", "minor": "✨", "patch": "🐛"}
    bump_desc = {"major": "Breaking changes", "minor": "New features", "patch": "Bug fixes"}
    
    with open("version_summary.txt", "w") as f:
        f.write(f"## 🤖 Smart Auto-Version Update\n\n")
        f.write(f"**{current_version}** → **{new_version}**\n\n")
        f.write(f"**Type:** {bump_type.upper()} {bump_emoji[bump_type]} - {bump_desc[bump_type]}\n\n")
        f.write(f"### 🧠 AI Analysis\n")
        f.write(f"**Decision Reason:** {reason}\n\n")
        f.write(f"### Details\n")
        f.write(f"- Previous version: `{current_version}`\n")
        f.write(f"- New version: `{new_version}`\n")
        f.write(f"- Bump type: {bump_type.upper()}\n")
        f.write(f"- Analysis: Automatic based on code changes\n\n")
        f.write(f"---\n")
        f.write(f"*🚀 This version will be automatically tagged and released.*")


def main():
    """Main execution function"""
    # Ensure we're in the right directory
    os.chdir('.')
    print(f"📂 Working directory: {os.getcwd()}")
    
    # Get current version (file-based only for reliability)
    current_version = get_version_from_file()
    print(f"📦 Current version: {current_version}")
    
    # Check if this is a version bump commit from the bot
    repo = git.Repo('.')
    last_commit = repo.head.commit
    if "🤖 Auto-bump version" in last_commit.message:
        print("ℹ️  This is a version bump commit from the bot, skipping analysis")
        # Output skip signal
        write_github_outputs({
            "should-skip": "true",
            "skip-reason": "bot-commit"
        })
        return
    
    # Check if versioning should be skipped
    if os.getenv('SKIP_VERSIONING') == 'true':
        print("ℹ️  Skipping versioning as per environment variable")
        # Output skip signal
        write_github_outputs({
            "should-skip": "true",
            "skip-reason": "env-variable"
        })
        sys.exit(0)
    
    # Analyze and determine bump type
    bump_type, reason = analyze_changes()
    print(f"\n🎯 Decision: {bump_type.upper()} bump")
    print(f"📝 Reason: {reason}")
    
    # Calculate new version
    new_version = increment_version(current_version, bump_type)
    print(f"\n⬆️  Calculated new version: {current_version} → {new_version}")
    
    # Update version file
    if update_version_file(new_version):
        print(f"✅ Version bumped: {current_version} → {new_version}")
    else:
        print(f"❌ Failed to update version")
        # Output error signal and exit with error code
        write_github_outputs({
            "should-skip": "true",
            "skip-reason": "update-failed"
        })
        sys.exit(1)
    
    # Output for GitHub Actions
    write_github_outputs({
        "old-version": current_version,
        "new-version": new_version,
        "bump-type": bump_type,
        "reason": reason
    })
    
    # Create detailed summary
    create_version_summary(current_version, new_version, bump_type, reason)
    
    print(f"🎉 Successfully completed version analysis and update!")


if __name__ == "__main__":
    main()
