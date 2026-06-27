#!/bin/bash
# treetype Snippet Helper Script
# Automates: parse → build metadata → stage files

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if input file provided
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Error: No input file specified${NC}"
    echo ""
    echo "Usage: $0 <source_file> [options]"
    echo ""
    echo "Examples:"
    echo "  $0 sources/python/views.py"
    echo "  $0 sources/javascript/hooks.js"
    echo ""
    exit 1
fi

INPUT_FILE="$1"

# Check if file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}❌ Error: File not found: $INPUT_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}treetype Snippet Workflow${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Parse the file
echo -e "${YELLOW}[1/3]${NC} Parsing source file..."
python3 build/parse_json.py "$INPUT_FILE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Parsing failed${NC}"
    exit 1
fi

echo ""

# Step 2: Build metadata
echo -e "${YELLOW}[2/3]${NC} Building metadata index..."
python3 build/build_metadata.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Metadata generation failed${NC}"
    exit 1
fi

echo ""

# Step 3: Stage files for commit
echo -e "${YELLOW}[3/3]${NC} Staging files for git commit..."

# Determine which files were created/modified
LANGUAGE_DIR=$(python3 -c "
import sys
from pathlib import Path
ext = Path('$INPUT_FILE').suffix
ext_map = {'.py': 'python', '.js': 'javascript', '.jsx': 'javascript', '.ts': 'typescript', '.tsx': 'tsx'}
print(ext_map.get(ext, 'unknown'))
")

if [ "$LANGUAGE_DIR" != "unknown" ]; then
    # Stage the active public language directory and metadata
    git add "public/$LANGUAGE_DIR/" 2>/dev/null || true
    git add "public/metadata.json" 2>/dev/null || true

    echo -e "${GREEN}✅ Files staged for commit${NC}"
    echo ""
    echo "Staged files:"
    git status --short | grep "^A " || echo "  (none)"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Review changes: git diff --staged"
    echo "  2. Commit: git commit -m \"Add new snippet: <name>\""
    echo "  3. Push: git push"
    echo ""
    echo -e "${GREEN}✅ Snippet workflow complete!${NC}"
else
    echo -e "${YELLOW}⚠️  Could not determine language directory${NC}"
    echo "   Manually stage files with: git add public/"
fi

echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"