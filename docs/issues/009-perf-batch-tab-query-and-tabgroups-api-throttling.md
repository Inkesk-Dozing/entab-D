# Issue 009: [PERF] Batch Tab Operations and Asynchronous TabGroups API Throttling

**Labels**: `performance`, `optimization`, `tab-groups`

---

## 1. Context & Problem Statement
In `service_worker.js`, grouping iterates over tabs one by one and executes individual sequential API calls for each matching tab:
```javascript
for (const t of wtabs) {
  ...
  await chrome.tabs.group({ tabIds: [t.id], groupId });
}
```
When a user has 100+ open tabs, invoking `chrome.tabs.group` individually per tab produces severe UI stutter and can exceed Chrome's internal extension API rate limits, resulting in `MAX_WRITE_OPERATIONS_PER_MINUTE` errors.

---

## 2. Technical Design & Batching Architecture
`chrome.tabs.group` natively accepts an array of tab IDs (`tabIds: number[]`).
Instead of calling the API $N$ times for $N$ tabs, the grouper should aggregate all tab IDs belonging to the same target group within a window, and dispatch a single grouped call:

```mermaid
flowchart TD
    ScanTabs[Scan all tabs in window] --> BucketTabs[Accumulate into Map: GroupName -> tabId array]
    BucketTabs --> BatchDispatch[For each Group: chrome.tabs.group with all tabIds in single call]
    BatchDispatch --> ReduceAPI[API Calls reduced from O(N) to O(Groups)]
```

### Complexity Reduction

| Metric | Individual Invocation (Current) | Batched Invocation (Proposed) |
| :--- | :--- | :--- |
| **API Invocations** | $O(N)$ (100 tabs = 100 calls) | $O(G)$ (4 groups = 4 calls) |
| **Execution Latency** | ~1,200ms - 2,500ms | < 80ms |
| **Chrome IPC Overhead**| High | Negligible |

---

## 3. Implementation Plan
- [ ] Refactor `groupTabsByRules()` to bucket tabs by resolved rule before invoking any Chrome API:
  ```javascript
  const groupBuckets = new Map(); // ruleName -> [tabId, tabId, ...]
  ```
- [ ] Dispatch a single `chrome.tabs.group({ tabIds, groupId })` per populated bucket.
- [ ] Implement a 250ms debounce on automatic tab grouping events to prevent rapid cascade triggers during bulk bookmark opens or session restores.

---

## 4. Acceptance Criteria
1. Grouping 150 tabs across 5 groups requires no more than 5 `chrome.tabs.group` API calls.
2. Total grouping execution time drops by over 80% on large browser sessions.
3. Zero Chrome API rate limit exceptions during aggressive automated stress tests.
