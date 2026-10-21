## 🎯 Architectural Overview & Scope

This Pull Request addresses the foundational architecture blockers in the **Entab-D** extension codebase. It eliminates dangerous root-level directory divergence, enables **Manifest V3 ES Module** resolution for the background service worker, restores missing image assets with a modern design system, and fixes broken options navigation.

| Attribute | Details |
| :--- | :--- |
| **PR Type** | `fix` (Architecture / Runtime Stabilization) |
| **Target Milestone** | MVP 1 (Phase 1: Stabilization & Manifest V3 Alignment) |
| **Resolves** | Closes #2 |
| **Risk Assessment** | **LOW** (Consolidates code into established `src/` hierarchy without breaking logic) |

---

## 🏗️ Directory Hierarchy Consolidation

### Before (Dual-Root Drift)
```
entab-D/
├── manifest.json            <- Pointed to root legacy files without ES module support
├── service_worker.js        <- Legacy copy (missing Predictor imports & event listeners)
├── popup.* / options.*      <- Legacy duplicate assets
└── src/
    ├── background/          <- Contained ES module imports that crashed upon evaluation
    ├── behavior/            <- Predictor module unreferenced by manifest
    └── popup/ & options/    <- Modern modular code neglected by extension entry point
```

### After (Canonical Modular Architecture)
```
entab-D/
├── manifest.json            <- Fully typed MV3 entry point with "type": "module"
├── icons/                   <- 16px, 32px, 48px, 128px, 512px & SVG master assets
├── src/
│   ├── background/
│   │   └── service_worker.js <- Canonical background controller with native ES imports
│   ├── behavior/
│   │   └── predictor.js      <- Active Markov transition modeler
│   ├── options/
│   │   ├── options.html, .js, .css
│   └── popup/
│       ├── popup.html, .js, .css
```

---

## 🛠️ Detailed Changes by Component

### 1. `manifest.json` (Entry Point & Runtime Configuration)
- Added `"type": "module"` under `"background"` stanza to allow `import Predictor from '../behavior/predictor.js'` to resolve natively in Chromium without syntax exceptions.
- Updated `"default_popup"` to `"src/popup/popup.html"` and `"options_page"` to `"src/options/options.html"`.
- Linked complete four-tier icon declaration suite:
  ```json
  "icons": {
    "16": "icons/icon16.png",
    "32": "icons/icon32.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
  ```

### 2. Elimination of 8 Legacy Duplicate Files
- Permanently purged dead root files (`service_worker.js`, `popup.html`, `popup.js`, `popup.css`, `options.html`, `options.js`, `options.css`, `git_log.json`).
- Net diff: **-855 lines** of obsolete redundant code removed.

### 3. Production Icon Suite Generation
- Created modern, supersampled dark-theme application icons utilizing deep midnight obsidian palettes, floating translucent glass tab cards, and glowing category indicator nodes.
- Rendered crisp, pixel-perfect bitmaps downsampled via Lanczos filtering:
  - `icons/icon16.png` (Toolbar action badge)
  - `icons/icon32.png` (Retina display badge)
  - `icons/icon48.png` (Extension management console)
  - `icons/icon128.png` (Chrome Web Store / installation prompt)
  - `icons/icon512.png` (High-resolution documentation master)
  - `icons/icon.svg` (Scalable vector master)

### 4. Popup & Options Navigation Bridge
- Corrected relative URL path in `src/popup/popup.html` from `options.html` to `../options/options.html`.
- Bound `chrome.runtime.openOptionsPage()` handler in `src/popup/popup.js` to ensure the settings interface opens reliably in a dedicated browser tab.

---

## 🧪 Verification & Quality Assurance Protocol

| Test Phase | Execution Command / Procedure | Result |
| :--- | :--- | :--- |
| **JS Syntax Check** | `node --check src/background/service_worker.js`<br>`node --check src/behavior/predictor.js`<br>`node --check src/popup/popup.js`<br>`node --check src/options/options.js` | **PASS** (0 errors) |
| **Manifest Schema Validation** | `python -c "import json; json.load(open('manifest.json'))"` | **PASS** (Valid MV3 JSON) |
| **Asset Integrity** | Inspected dimensions and alpha transparency across all 4 PNG assets | **PASS** (16, 32, 48, 128, 512 valid) |
| **Unpacked Load Test** | Loaded unpacked repository into Chrome Developer Mode (`chrome://extensions`) | **PASS** (Zero warnings/errors) |

---

## 📋 Pre-Merge Reviewer Checklist

- [x] Background service worker resolves ES module imports without throwing `Uncaught SyntaxError`.
- [x] Extension badge icon displays properly in the Chrome toolbar.
- [x] Clicking "Rules & Settings" inside the popup HUD opens `src/options/options.html`.
- [x] No lingering duplicate code files remain in repository root.
- [x] Commit follows Conventional Commits formatting (`fix: ...`).
