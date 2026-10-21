# Issue 010: [UI/UX] Modern Dark Mode, WCAG Accessibility Compliance, and Keyboard Navigation

**Labels**: `ui/ux`, `frontend`, `accessibility`

---

## 1. Context & Problem Statement
The current popup (`src/popup/popup.css`) and options (`src/options/options.css`) interfaces use hardcoded light-theme hex colors (`#ffffff`, `#f5f5f5`, `#007bff`, `#333333`).
- There is no automatic dark mode support matching `prefers-color-scheme: dark`.
- Contrast ratios on secondary buttons and feedback status labels do not meet Web Content Accessibility Guidelines (WCAG 2.1 AA).
- Buttons and duplicate lists lack complete focus indicators and full keyboard navigation bindings (`Tab`, `Enter`, `Space`, `Escape`).

---

## 2. Technical Design & Design Tokens

Establish CSS Custom Properties supporting dynamic theme switching:

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --text-primary: #0f172a;
  --text-muted: #64748b;
  --border-color: #e2e8f0;
  --accent-primary: #2563eb;
  --accent-hover: #1d4ed8;
  --danger: #ef4444;
  --radius-sm: 6px;
  --radius-md: 10px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --text-primary: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: #334155;
    --accent-primary: #3b82f6;
    --accent-hover: #60a5fa;
  }
}
```

---

## 3. Implementation Plan
- [ ] Migrate `popup.css` and `options.css` to semantic CSS custom properties.
- [ ] Implement automatic dark/light theme switching based on OS preferences with manual override toggle in Options.
- [ ] Add explicit visible `:focus-visible` rings on all interactive elements.
- [ ] Add ARIA roles (`role="status"`, `aria-live="polite"`, `role="listbox"`) for screen reader compatibility on dynamic duplicate lists and prediction suggestions.

---

## 4. Acceptance Criteria
1. Interface automatically adapts to system dark mode without color inversion glitches.
2. Lighthouse Accessibility audit scores 100/100 on both popup and options pages.
3. Users can navigate, scan duplicates, trigger grouping, and switch predicted tabs entirely via keyboard.
