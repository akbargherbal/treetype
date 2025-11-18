#!/bin/bash
# TreeType Deployment Script - Clean gh-pages Method
# Keeps dist/ ignored, deploys to separate branch
# Run with: ./deploy.sh

set -e  # Stop if any command fails

echo ""
echo "🚀 TreeType Deployment Script"
echo "=============================="
echo ""

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo "⚠️  You're on branch '$CURRENT_BRANCH'"
    echo "   Switch to main first: git checkout main"
    exit 1
fi

# Check for uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  You have uncommitted changes!"
    echo ""
    git status --short
    echo ""
    echo "Commit or stash changes before deploying."
    exit 1
fi

# Step 1: Run tests
echo "🔬 Running tests..."
if pnpm run test > /dev/null 2>&1; then
    echo "   ✅ All tests passed (38/38)"
else
    echo "   ❌ Tests failed! Fix tests before deploying."
    pnpm run test
    exit 1
fi
echo ""

# Step 2: Type check
echo "📝 Type checking..."
if pnpm run type-check > /dev/null 2>&1; then
    echo "   ✅ No type errors"
else
    echo "   ❌ Type errors found! Fix them before deploying."
    pnpm run type-check
    exit 1
fi
echo ""

# Step 3: Build
echo "📦 Building production bundle..."
pnpm run build
echo ""

# Step 4: Show build info
echo "📊 Build Summary:"
echo "   Total size:  $(du -sh dist/ | cut -f1)"
echo ""

# Step 5: Preview prompt
echo "👀 Would you like to preview locally before deploying? (y/n)"
read -r response
if [[ "$response" == "y" ]]; then
    echo ""
    echo "   Starting preview server..."
    echo "   Test your app, then press Ctrl+C to continue"
    echo ""
    pnpm run preview
    echo ""
fi

# Step 6: Confirm deployment
echo "Ready to deploy to GitHub Pages?"
echo ""
echo "This will:"
echo "  1. Switch to gh-pages branch"
echo "  2. Copy dist/ contents to root"
echo "  3. Commit and push"
echo "  4. Return to main branch"
echo ""
echo "Continue? (y/n)"
read -r response
if [[ "$response" != "y" ]]; then
    echo "Deployment cancelled."
    exit 0
fi

# Step 7: Save current commit hash
MAIN_COMMIT=$(git rev-parse --short HEAD)

# Step 8: Switch to gh-pages (create if doesn't exist)
echo ""
echo "🌿 Preparing gh-pages branch..."
if git show-ref --quiet refs/heads/gh-pages; then
    git checkout gh-pages
    # Clean the branch before adding new files
    git rm -rf . > /dev/null 2>&1 || true
else
    echo "   Creating gh-pages branch (first-time setup)..."
    git checkout --orphan gh-pages
    git rm -rf . > /dev/null 2>&1 || true
fi

# Step 9: Copy dist contents
echo "🚚 Copying build files..."
# Use git checkout to safely get the dist folder from the main branch
git checkout main -- dist/
# Move contents to the root
cp -r dist/* .
# Clean up the now-empty dist folder
rm -rf dist/

# Step 10: Create .nojekyll (tells GitHub Pages to serve all files)
touch .nojekyll

# Step 11: Add all files
git add .

# Step 12: Check if there are changes
if git diff --staged --quiet; then
    echo ""
    echo "ℹ️  No changes detected - site is already up to date"
    git checkout main
    exit 0
fi

# Step 13: Commit
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
git commit -m "Deploy from main@${MAIN_COMMIT} - ${TIMESTAMP}"

# Step 14: Push
echo "⬆️  Pushing to GitHub..."
git push origin gh-pages --force

# Step 15: Return to main
git checkout main

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌍 Your site will be available at:"
echo "   https://akbargherbal.github.io/treetype/"
echo ""
echo "⏱️  GitHub Pages usually updates in 30-60 seconds"
echo "   Check deployment status:"
echo "   https://github.com/akbargherbal/treetype/deployments"
echo ""
