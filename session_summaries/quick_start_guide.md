# Session 20 Quick Start Guide

**⏱️ Total Time**: ~30 minutes  
**🎯 Goal**: Get Phase 6 structure up and running locally

---

## 📋 Prerequisites

Before starting, ensure you have:
- [x] Git installed and configured
- [x] Python 3.7+ installed
- [x] Required Python packages installed:
  ```bash
  pip install pandas tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-typescript
  ```
- [x] Current working directory is the TreeType repo root

---

## ⚡ 5-Minute Quick Start

```bash
# 1. Create the new artifacts
#    (Copy files from artifacts I created above into your repo)

# 2. Make scripts executable
chmod +x restructure.sh
chmod +x build/add_snippet.sh

# 3. Run automated restructure
./restructure.sh

# 4. Update index.html path (manual edit)
#    Find: output/json_samples/${language}_sample.json
#    Replace: snippets/${language}/${language}_sample.json

# 5. Test locally
python -m http.server 8000
# Visit: http://localhost:8000

# 6. Verify all 4 languages load correctly

# 7. Commit changes
git add build/ snippets/ index.html .gitignore restructure.sh
git commit -m "Phase 6 Session 20: Repository restructure"
```

---

## 📁 Files to Create

### From Artifacts Above

1. **build/build_metadata.py** ← Copy from artifact
2. **build/parse_json.py** ← Copy from artifact  
3. **build/add_snippet.sh** ← Copy from artifact
4. **.gitignore** ← Copy from artifact (replace existing)
5. **restructure.sh** ← Copy from artifact

### Manual Edits

6. **index.html** ← Rename from render_code.html, update 1 path

---

## 🧪 Testing Checklist

After restructure, verify:

```bash
# Check directory structure
tree -L 2

# Expected:
# ├── build/
# │   ├── build_metadata.py
# │   ├── parse_json.py
# │   └── add_snippet.sh
# ├── snippets/
# │   ├── metadata.json
# │   ├── python/
# │   ├── javascript/
# │   ├── typescript/
# │   └── tsx/
# ├── sources/
# └── index.html

# Check metadata
cat snippets/metadata.json | jq '.totalSnippets'
# Expected: 4

# Test parser
python build/parse_json.py --help
# Expected: Help text displays

# Test metadata builder
python build/build_metadata.py
# Expected: Success message

# Test helper script
echo 'def test(): pass' > sources/python/test.py
./build/add_snippet.sh sources/python/test.py
# Expected: Workflow completes, file staged

# Test web app
python -m http.server 8000
# Visit http://localhost:8000
# Expected: Typing game loads, all languages work
```

---

## 🎯 Success = Green Lights

✅ Directory structure matches expected layout  
✅ `snippets/metadata.json` exists with 4 snippets  
✅ `python build/parse_json.py --help` shows help  
✅ `python build/build_metadata.py` runs successfully  
✅ `./build/add_snippet.sh test.py` completes workflow  
✅ `http://localhost:8000` loads typing game  
✅ All 4 languages load without errors  
✅ All 3 presets work (Minimal, Standard, Full)  
✅ Git status shows new structure ready to commit

---

## 🚨 If Something Fails

### restructure.sh fails
**Check**: Are you in the repo root?
```bash
pwd  # Should show: .../TreeType
ls   # Should show: render_code.html, parse_json.py
```

### Parser fails with import errors
**Fix**: Install dependencies
```bash
pip install pandas tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-typescript
```

### 404 errors in browser
**Fix**: Update path in index.html
```javascript
// Should be:
fetch(`snippets/${language}/${language}_sample.json`)

// NOT:
fetch(`output/json_samples/${language}_sample.json`)
```

### No snippets in metadata
**Fix**: Ensure JSON files are in correct places
```bash
ls snippets/python/      # Should show: python_sample.json
ls snippets/javascript/  # Should show: javascript_sample.json
# etc.
```

---

## 🎓 What You've Accomplished

After completing Session 20, you have:

✅ **Production-ready repository structure**
- Organized directories (`build/`, `snippets/`, `sources/`)
- Clear separation of concerns
- Git-friendly ignore patterns

✅ **Powerful automation tools**
- CLI parser for any source file
- Metadata generator for dynamic loading
- One-command snippet workflow

✅ **Static snippet library**
- 4 sample snippets ready to practice
- Metadata index for filtering/search
- Language-organized structure

✅ **Foundation for Phase 6 complete**
- Ready for GitHub Pages deployment (Session 21)
- Ready for library browser UI (Session 21)
- Ready for stats tracking (Session 21)

---

## 📅 Next Steps

**Immediate** (before ending session):
- Review all changes with `git diff`
- Test thoroughly on `http://localhost:8000`
- Commit changes (but don't push yet)

**Session 21** (next session):
- Deploy to GitHub Pages
- Build library browser UI
- Implement dynamic snippet loading
- Test live deployment

**Session 22** (future):
- Add stats tracking (localStorage)
- Build export/import functionality
- Create settings panel
- Complete Phase 6

---

## 💡 Pro Tips

### Tip 1: Test workflow early
Add a real snippet to verify the workflow:
```bash
# Copy one of your Python files
cp ~/my_code/utils.py sources/python/

# Run workflow
./build/add_snippet.sh sources/python/utils.py

# Practice it!
# (Will be in library browser in Session 21)
```

### Tip 2: Keep sources/ organized
```
sources/
├── python/
│   ├── django/       # Framework-specific
│   ├── flask/
│   └── utils/
├── javascript/
│   ├── react/
│   └── vanilla/
└── typescript/
    └── angular/
```

### Tip 3: Use descriptive filenames
```
# Good:
sources/python/django_class_based_views.py
sources/javascript/react_custom_hooks.js

# Not great:
sources/python/test.py
sources/javascript/file1.js
```

Filenames become snippet names in the library!

### Tip 4: Batch add snippets
```bash
# Add all Python files at once
for file in sources/python/*.py; do
    ./build/add_snippet.sh "$file"
done
```

---

## 🎉 You're Ready!

**Session 20 is complete when**:
- ✅ All tests pass
- ✅ Local server works
- ✅ Changes committed to git
- ✅ You understand the new workflow

**Time to celebrate!** 🎊  
You've just transformed TreeType from a development prototype into a production-ready static web application with zero backend complexity.

---

**Next session**: Deploy to the world with GitHub Pages! 🚀
