# Component: Options Rule Manager

## Purpose
Renders a full-page administrative dashboard where users configure custom grouping definitions, choose color badges, assign comma-separated keywords or domain patterns, toggle predictive suggestions, and sync with the local Python daemon.

## Source Location
`src/options/options.html`, `src/options/options.js`, `src/options/options.css`

## Dependencies
- APIs: `chrome.runtime.sendMessage`, `chrome.storage.sync`, `chrome.storage.local`.
- External HTTP: Fetch API to `http://127.0.0.1:5055` for backup and restore.

## Big-O Complexity

| Operation | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| **Rule Rendering** | $O(R \cdot K)$ | $O(R \cdot K)$ | Iterates and builds HTML strings for $R$ rules with $K$ keywords. |
| **Rule Collection** | $O(R \cdot K)$ | $O(R \cdot K)$ | Queries DOM inputs, splits keywords by comma, and cleans whitespace. |
| **Local Daemon Sync** | $O(S)$ | $O(S)$ | Serializes rules to JSON payload where $S$ is payload byte length. |

## Error Boundaries & Edge Cases
- Sanitizes user input by stripping empty rule cards and trimming keyword strings.
- Displays non-blocking inline status messages on save/sync failures.
