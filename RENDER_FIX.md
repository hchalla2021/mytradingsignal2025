# Render Deployment Fix - Python 3.13 → 3.11

## Problem
Render was using Python 3.13 instead of 3.11, causing pandas build failures with C++ compilation errors.

## Solution Applied

### 1. Python Version Files
- **`.python-version`**: Set to `3.11.9` (Render's primary version detection)
- **`runtime.txt`**: Updated to `python-3.11.9` (Heroku-style fallback)

### 2. Render Configuration (`render.yaml`)
- Set `PYTHON_VERSION` env var to `"3.11.9"`
- Updated `buildCommand` to use custom script: `bash scripts/render-build.sh`

### 3. Build Script (`scripts/render-build.sh`)
- Added Python version verification (fails if 3.13 detected)
- Upgrades pip, setuptools, wheel before installing packages
- Uses `--no-cache-dir` to ensure clean installs

### 4. Package Versions (`requirements.txt`)
- **pandas**: `2.0.3` (stable Python 3.11 support, no Cython issues)
- **numpy**: `1.24.3` (compatible with pandas 2.0.3)

## Render Dashboard Manual Steps (If Still Failing)

If deployment still uses Python 3.13:

1. Go to Render Dashboard → Your Service
2. Click **Settings**
3. Scroll to **Environment**
4. Find **Python Version** dropdown
5. Select **3.11** (not 3.13)
6. Click **Save Changes**
7. Trigger manual deploy

## Verification

After deployment succeeds, check logs should show:
```
🐍 Python version check:
Python 3.11.9
📦 Upgrading build tools...
📦 Installing backend dependencies...
✅ Backend build complete!
```

## Alternative: Use Pre-built Wheels

If issues persist, can switch to using only pre-built wheels:
```bash
pip install --only-binary=:all: pandas==2.0.3 numpy==1.24.3
```
Add `--only-binary=:all:` to pip install command in `render-build.sh`.
