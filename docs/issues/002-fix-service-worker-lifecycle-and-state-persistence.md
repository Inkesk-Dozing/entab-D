# Issue 002: [FIX] Service Worker State Invalidation and Asynchronous Event Re-hydration

**Labels**: `bug`, `chrome-extension`, `performance`

---

## 1. Context & Problem Statement
In `service_worker.js`, auto-grouping state is tracked using an in-memory module-level variable:
```javascript
let autoGroupEnabled = false;
chrome.storage.sync.get({ autoGroupEnabled: false }, (result) => {
  autoGroupEnabled = result.autoGroupEnabled;
});
```
Chrome service workers are suspended after 30 seconds of inactivity. When a subsequent tab event (e.g. `chrome.tabs.onCreated`) wakes the worker, `autoGroupEnabled` resets to `false`. If a tab event fires before the asynchronous `chrome.storage.sync.get` callback resolves, auto-grouping fails silently.

Additionally, tab event listeners set arbitrary fixed-duration timeouts (`setTimeout(..., 1000)`) without checking page load status (`changeInfo.status === 'complete'`), leading to race conditions where uncommitted or blank tab URLs are evaluated.

---

## 2. Technical Root Cause Analysis
1. Service workers in Manifest V3 are ephemeral and stateless; storing operational configuration in memory variables without guaranteed synchronous pre-load leads to stale reads on wakeup.
2. `chrome.tabs.onUpdated` fires multiple times per navigation (e.g. `loading`, `complete`, favicon changes). Relying on `setTimeout(..., 1000)` executes logic while the tab might still be redirecting or aborting, resulting in empty hostnames and misplaced tab groups.

---

## 3. Implementation Plan
- [ ] Refactor state hydration into an asynchronous cached helper:
  ```javascript
  async function isAutoGroupEnabled() {
    const data = await chrome.storage.sync.get({ autoGroupEnabled: false });
    return data.autoGroupEnabled === true;
  }
  ```
- [ ] Update `chrome.tabs.onUpdated` to execute strictly when navigation is finalized:
  ```javascript
  chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url && await isAutoGroupEnabled()) {
      await evaluateSingleTabGrouping(tab);
    }
  });
  ```
- [ ] Remove hardcoded `setTimeout` invocations and replace with debounced event queues.

---

## 4. Acceptance Criteria
1. When the service worker goes idle and is woken by creating a new tab, auto-grouping executes reliably without state loss.
2. Tab grouping does not fire on intermediate redirect URLs; it only executes once the tab reaches `complete` status.
3. Rapid tab creation (e.g., opening 10 bookmarks at once) processes cleanly without dropped events or unhandled exceptions.
