# Issue 001: [FIX] Unify Directory Hierarchy, Enable Manifest V3 ES Modules, and Generate Missing Icon Assets

**Labels**: `bug`, `chrome-extension`, `critical`

---

## 1. Context & Problem Statement
The repository currently maintains two separate, divergent sets of files:
- Root-level legacy files (`service_worker.js`, `popup.html`, `options.html`, `popup.js`, `options.js`).
- Modularized files inside `src/` (`src/background/service_worker.js`, `src/popup/`, `src/options/`, `src/behavior/predictor.js`).

`manifest.json` points to root-level legacy files and lacks `"type": "module"` under `"background"`. Furthermore, `src/background/service_worker.js` contains `import Predictor from '../behavior/predictor.js';`. Attempting to load `src/background/service_worker.js` directly triggers a fatal browser runtime error:
```
Uncaught SyntaxError: Cannot use import statement outside a module
```
Additionally, `manifest.json` references icons (`icons/icon16.png`, `icons/icon32.png`, `icons/icon48.png`, `icons/icon128.png`), but the `icons/` directory is completely missing from the repository, leading to packaging failures and missing icon errors in `chrome://extensions`.

---

## 2. Technical Root Cause Analysis
1. Partial refactoring in previous commit (`b8697b4`) created the `src/` directory tree but did not update `manifest.json` entry points or delete stale root files.
2. Manifest V3 requires explicit module declaration for background service workers utilizing ES imports:
   ```json
   "background": {
     "service_worker": "src/background/service_worker.js",
     "type": "module"
   }
   ```
3. Icon binary assets were not checked into version control.

---

## 3. Implementation Plan
- [ ] Update `manifest.json` to point all entry points to `src/`:
  - `"action.default_popup"` ➔ `"src/popup/popup.html"`
  - `"options_page"` ➔ `"src/options/options.html"`
  - `"background.service_worker"` ➔ `"src/background/service_worker.js"`
  - Add `"background.type"` ➔ `"module"`
- [ ] Remove duplicate root files (`service_worker.js`, `popup.html`, `popup.js`, `popup.css`, `options.html`, `options.js`, `options.css`).
- [ ] Create `icons/` folder and generate standardized SVG/PNG icons at 16x16, 32x32, 48x48, and 128x128 pixels.
- [ ] Verify clean extension load in Chrome Developer Mode with zero warnings or missing file errors.

---

## 4. Acceptance Criteria
1. Loading the unpacked repository in Chrome Developer Mode proceeds with zero warnings, errors, or missing file alerts.
2. Background service worker initializes properly with ES module imports resolved.
3. Extension action badge renders the 16x16 and 32x32 icon assets accurately in the toolbar.
