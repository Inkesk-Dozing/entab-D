# Component: Tab Grouper Engine

## Purpose
Scans all open tabs across active browser windows, matches tab URLs against user-configured keyword rules, creates or updates color-coded tab groups, and optionally collapses groups to declutter the workspace.

## Source Location
`src/background/service_worker.js` (`groupTabsByRules`)

## Dependencies
- Native APIs: `chrome.tabs.query`, `chrome.tabGroups.query`, `chrome.tabs.group`, `chrome.tabGroups.update`.
- Storage: `chrome.storage.sync` (`rules`).

## Big-O Complexity

| Operation | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| **Tab Partitioning** | $O(N)$ | $O(N)$ | Partitions $N$ tabs across $W$ windows. |
| **Rule Matching** | $O(N \cdot R \cdot K)$ | $O(1)$ | $N$ tabs tested against $R$ rules with average $K$ keywords. |
| **Group Lookup** | $O(G)$ | $O(G)$ | Queries and indexes $G$ existing groups per window. |
| **Overall Execution** | $O(N \cdot R \cdot K + G)$ | $O(N + G)$ | Dominant factor is tab count and keyword matching. |

## Error Boundaries & Edge Cases
- **Restricted Schemes**: Skips `chrome://`, `chrome-extension://`, `edge://`, `about:blank`, and `devtools://` where Chrome prohibits grouping operations.
- **Window Mismatch**: Prevents assigning tabs to group IDs created in separate browser windows.
