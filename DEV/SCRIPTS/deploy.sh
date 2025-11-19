#!/bin/bash
# TreeType Deployment Script - Fixed (v6)

set -e

echo "🚀 TreeType Deployment Script"
echo "=============================="

# Safety checks
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo "⚠️  Must be on main branch to deploy."
    exit 1
fi

if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  Uncommitted changes found. Please commit or stash."
    git status --short
    exit 1
fi

# Run tests with visible output
echo "🧪 Running tests..."
if ! pnpm run test; then
    echo "❌ Tests failed! Fix errors before deploying."
    exit 1
fi
echo "   ✅ Tests passed"

# Type check with visible output
echo "📝 Type checking..."
if ! pnpm run type-check; then
    echo "❌ Type errors found! Fix errors before deploying."
    exit 1
fi
echo "   ✅ No type errors"

# Build
echo "📦 Building production bundle..."
if ! pnpm run build; then
    echo "❌ Build failed!"
    exit 1
fi

# Create temporary directory OUTSIDE the repo
TMP_DIR=$(mktemp -d)
echo "   📁 Created temp directory: $TMP_DIR"

# Copy ONLY dist contents to temp (while still on main branch)
cp -r dist/* "$TMP_DIR/"
echo "   ✅ Build artifacts saved to temporary location"

# Get absolute path to repo (we'll need this)
REPO_DIR=$(pwd)

echo "🌿 Preparing gh-pages branch..."
# Fetch latest branches
git fetch origin

# Checkout gh-pages (create if doesn't exist)
if git rev-parse --verify origin/gh-pages > /dev/null 2>&1; then
    git checkout gh-pages
    git pull origin gh-pages
else
    git checkout --orphan gh-pages
fi

# Clean working directory - BUT PRESERVE .git/
# Remove all tracked files
git rm -rf . 2>/dev/null || true

# Remove untracked files/dirs EXCEPT .git
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

# Copy ONLY the build files from temp
cp -r "$TMP_DIR"/* .
touch .nojekyll

echo "📦 Files copied to gh-pages branch"

# Clean up temporary directory
rm -rf "$TMP_DIR"
echo "   🧹 Cleaned up temp directory"

# Show what we're about to commit
echo ""
echo "📋 Files in gh-pages branch:"
ls -lh
echo ""

# Commit and push
git add .
if git diff --staged --quiet; then
    echo "ℹ️  No changes to deploy"
else
    git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "⬆️  Pushing to GitHub..."
    git push origin gh-pages
    echo "✅ Deployment successful!"
fi

# Return to main
git checkout main
echo "↩️  Switched back to main branch"
echo ""
echo "🌍 Your site will be live at: https://akbargherbal.github.io/treetype/"
echo "   (Usually takes 30-60 seconds for first deployment)"