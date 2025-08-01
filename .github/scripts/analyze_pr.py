#!/usr/bin/env python3
"""
PR Impact Analysis Script for GitHub Actions

This script analyzes proposed changes in pull requests to predict the likely version bump
that will be applied when the PR is merged to the main branch.

Used by: .github/workflows/version-check.yml  
Purpose: Provide developers with preview of version impact before merging
Dependencies: GitPython, subprocess
"""

import git
import subprocess
import re


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


def analyze_pr_impact():
    """Analyze PR changes and predict version bump"""
    try:
        # Get base version from origin/main without checking out
        repo = git.Repo('.')
        
        # Get base version by reading file content from main branch
        main_commit = repo.commit('origin/main')
        try:
            # Read __about__.py from main branch
            about_content = main_commit.tree['backend/global_economy_sim/__about__.py'].data_stream.read().decode('utf-8')
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', about_content)
            base_version = match.group(1) if match else "0.1.0"
        except (KeyError, AttributeError):
            base_version = "0.1.0"
        
        # Get current PR commit
        pr_commit = repo.head.commit
        changes = main_commit.diff(pr_commit)
        
        total_files = len(changes)
        python_files = len([c for c in changes if (c.a_path or c.b_path or '').endswith('.py')])
        new_files = len([c for c in changes if c.change_type == 'A'])
        deleted_files = len([c for c in changes if c.change_type == 'D'])
        
        # Simple heuristic for PR preview
        if deleted_files > 0 or total_files > 10:
            predicted_bump = "MAJOR 🚨"
        elif new_files > 0 or python_files > 3:
            predicted_bump = "MINOR ✨"
        else:
            predicted_bump = "PATCH 🐛"
        
        return {
            'base_version': base_version,
            'predicted_bump': predicted_bump,
            'total_files': total_files,
            'python_files': python_files,
            'new_files': new_files,
            'deleted_files': deleted_files
        }
        
    except Exception as e:
        print(f"❌ Error during PR impact analysis: {e}")
        # Return safe defaults
        return {
            'base_version': "0.1.0",
            'predicted_bump': "PATCH 🐛",
            'total_files': 0,
            'python_files': 0,
            'new_files': 0,
            'deleted_files': 0
        }


def create_pr_summary(analysis):
    """Create PR summary markdown"""
    summary = f"""## 🔮 Smart Version Preview

When this PR is merged, the smart versioning system will likely apply a **{analysis['predicted_bump']}** bump.

### 📊 Change Analysis
- **Files changed:** {analysis['total_files']}
- **Python files:** {analysis['python_files']}
- **New files:** {analysis['new_files']}
- **Deleted files:** {analysis['deleted_files']}

### 📦 Predicted Version Change
**{analysis['base_version']}** → **{analysis['predicted_bump']}**

---
*This is a preview. The actual version will be determined by AI analysis when merged to main.*
"""
    
    with open("pr_summary.txt", "w") as f:
        f.write(summary)
    
    return summary


def main():
    """Main execution function"""
    print("🔮 Analyzing PR impact...")
    
    try:
        analysis = analyze_pr_impact()
        summary = create_pr_summary(analysis)
        
        print("✅ PR analysis completed")
        print(f"📊 Files changed: {analysis['total_files']}")
        print(f"🐍 Python files: {analysis['python_files']}")
        print(f"➕ New files: {analysis['new_files']}")
        print(f"➖ Deleted files: {analysis['deleted_files']}")
        print(f"🎯 Predicted bump: {analysis['predicted_bump']}")
        
    except Exception as e:
        print(f"❌ Error during PR analysis: {e}")
        # Create fallback summary
        with open("pr_summary.txt", "w") as f:
            f.write("## 🔮 Smart Version Preview\n\n❌ Error analyzing PR changes. Manual review required.\n")


if __name__ == "__main__":
    main()
