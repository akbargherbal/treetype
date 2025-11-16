#!/bin/bash
# TreeType Phase 6 - Automated Repository Restructure
# Run this once to set up the new directory structure

set -e  # Exit on error

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TreeType Phase 6 - Repository Restructure${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if already restructured
if [ -d "snippets/python" ] && [ -f "snippets/metadata.json" ]; then
    echo -e "${YELLOW}⚠️  Repository appears to already be restructured${NC}"
    echo ""
    read -p "Continue anyway? This will overwrite existing structure. (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

echo -e "${GREEN}[1/6]${NC} Creating directory structure..."
mkdir -p build
mkdir -p snippets/{python,javascript,typescript,tsx}
mkdir -p sources/{python,javascript,typescript,tsx}
echo "   ✅ Directories created"

echo ""
echo -e "${GREEN}[2/6]${NC} Moving existing sample files..."
if [ -d "output/json_samples" ]; then
    if [ -f "output/json_samples/python_sample.json" ]; then
        mv output/json_samples/python_sample.json snippets/python/ 2>/dev/null || true
        echo "   ✅ Moved python_sample.json"
    fi
    if [ -f "output/json_samples/javascript_sample.json" ]; then
        mv output/json_samples/javascript_sample.json snippets/javascript/ 2>/dev/null || true
        echo "   ✅ Moved javascript_sample.json"
    fi
    if [ -f "output/json_samples/typescript_sample.json" ]; then
        mv output/json_samples/typescript_sample.json snippets/typescript/ 2>/dev/null || true
        echo "   ✅ Moved typescript_sample.json"
    fi
    if [ -f "output/json_samples/tsx_sample.json" ]; then
        mv output/json_samples/tsx_sample.json snippets/tsx/ 2>/dev/null || true
        echo "   ✅ Moved tsx_sample.json"
    fi
else
    echo -e "   ${YELLOW}⚠️  output/json_samples/ not found - skipping${NC}"
fi

echo ""
echo -e "${GREEN}[3/6]${NC} Copying parse_json.py to build/..."
if [ -f "parse_json.py" ]; then
    cp parse_json.py build/parse_json_backup.py
    echo "   ✅ Backup created: build/parse_json_backup.py"
    echo "   ℹ️  You'll need to replace build/parse_json.py with the new CLI version"
else
    echo -e "   ${YELLOW}⚠️  parse_json.py not found in root${NC}"
fi

echo ""
echo -e "${GREEN}[4/6]${NC} Making helper script executable..."
if [ -f "build/add_snippet.sh" ]; then
    chmod +x build/add_snippet.sh
    echo "   ✅ build/add_snippet.sh is now executable"
else
    echo -e "   ${YELLOW}⚠️  build/add_snippet.sh not found - you'll need to create it${NC}"
fi

echo ""
echo -e "${GREEN}[5/6]${NC} Renaming render_code.html → index.html..."
if [ -f "render_code.html" ]; then
    if [ -f "index.html" ]; then
        echo -e "   ${YELLOW}⚠️  index.html already exists - keeping both files${NC}"
        cp render_code.html index_new.html
        echo "   ✅ Created index_new.html instead"
    else
        mv render_code.html index.html
        echo "   ✅ Renamed render_code.html → index.html"
    fi
else
    echo -e "   ${YELLOW}⚠️  render_code.html not found${NC}"
fi

echo ""
echo -e "${GREEN}[6/6]${NC} Generating initial metadata..."
if [ -f "build/build_metadata.py" ]; then
    python build/build_metadata.py
    echo "   ✅ metadata.json generated"
else
    echo -e "   ${YELLOW}⚠️  build/build_metadata.py not found - skipping${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Restructure Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Update index.html to use new snippet paths:"
echo "   Change: output/json_samples/\${language}_sample.json"
echo "   To:     snippets/\${language}/\${language}_sample.json"
echo ""
echo "2. Test locally:"
echo "   python -m http.server 8000"
echo "   Visit: http://localhost:8000"
echo ""
echo "3. Verify all 4 languages work (Python, JS, TS, TSX)"
echo ""
echo "4. Test adding a new snippet:"
echo "   ./build/add_snippet.sh sources/python/test.py"
echo ""
echo "5. Check git status and commit when ready:"
echo "   git status"
echo "   git add build/ snippets/ index.html .gitignore"
echo "   git commit -m \"Phase 6: Repository restructure\""
echo ""
echo -e "${GREEN}Repository is now ready for Phase 6! 🚀${NC}"
echo ""