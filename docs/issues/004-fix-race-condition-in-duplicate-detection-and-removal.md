# Issue 004: [FIX] Race Condition and Unhandled Promise Rejections in Duplicate Tab Closure

**Labels**: `bug`, `performance`, `reliability`

---

## 1. Context & Problem Statement
When closing duplicates via `closeDuplicates()`, the routine executes in two disconnected asynchronous queries:
1. `findDuplicates()` queries `chrome.tabs.query({})` and computes duplicate pairs.
2. `closeDuplicates()` then executes a second `chrome.tabs.query({})` to map tab indices and sort IDs.

If any tab is closed by the user or an external process between step 1 and the execution of `chrome.tabs.remove(Array.from(toClose))`, Chrome throws an unhandled rejection:
```
Error: No tab with id: <tabId>.
```
This halts script execution mid-loop, leaving remaining duplicate tabs open and presenting a broken UI state in the popup.

---

## 2. Technical Root Cause Analysis
- Decoupled two-phase query model allows the tab environment state to drift between detection and closure.
- `chrome.tabs.remove(ids)` accepts an array of IDs; if any single ID in the array is invalid, the entire operation fails atomically unless handled with single-tab fallbacks or wrapped in error suppression.

---

## 3. Implementation Plan
- [ ] Refactor `closeDuplicates()` to perform atomic single-pass deduplication:
  ```javascript
  async function closeDuplicates({ keep = "oldest" } = {}) {
    const tabs = await chrome.tabs.query({});
    const byNorm = new Map();
    
    for (const tab of tabs) {
      if (!tab.url) continue;
      const norm = normalizeUrl(tab.url);
      if (!byNorm.has(norm)) byNorm.set(norm, []);
      byNorm.get(norm).push(tab);
    }
    
    const toClose = [];
    for (const [norm, list] of byNorm.entries()) {
      if (list.length <= 1) continue;
      list.sort((a, b) => a.id - b.id);
      const redundant = keep === "newest" ? list.slice(0, -1) : list.slice(1);
      toClose.push(...redundant.map(t => t.id));
    }
    
    let closedCount = 0;
    if (toClose.length > 0) {
      const results = await Promise.allSettled(toClose.map(id => chrome.tabs.remove(id)));
      closedCount = results.filter(r => r.status === 'fulfilled').length;
    }
    return { closed: closedCount };
  }
  ```
- [ ] Implement `Promise.allSettled` around tab removal to prevent one invalid tab ID from failing the entire batch.

---

## 4. Acceptance Criteria
1. Closing duplicate tabs never crashes if a user closes a tab concurrently.
2. The popup displays the exact number of tabs successfully terminated without throwing unhandled console errors.
3. Tests with 50+ duplicated tabs across multiple windows execute in under 300ms.
