# Component: Background Service Worker

## Purpose
Coordinates extension lifecycle events, handles runtime messages from UI contexts, listens to browser tab lifecycle events, and routes requests to domain engines (Grouping, Deduplication, and Prediction).

## Source Location
`src/background/service_worker.js`

## Dependencies
- Native APIs: `chrome.runtime`, `chrome.tabs`, `chrome.tabGroups`, `chrome.storage.sync`, `chrome.storage.local`.
- Internal Modules: `src/behavior/predictor.js`.

## Big-O Complexity

| Operation | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| **Event Routing** | $O(1)$ | $O(1)$ | Switch/dispatch over message payload `type`. |
| **Rules Hydration** | $O(1)$ | $O(R \cdot K)$ | Reads rules array where $R$ is rule count and $K$ is average keywords. |
| **Auto-group Dispatch** | $O(R \cdot K)$ | $O(1)$ | Evaluates single newly updated tab against active keyword rules. |

## Error Boundaries & Edge Cases
- Handles service worker termination by re-hydrating configuration from storage on wake.
- Protects against invalid tab IDs or closed tabs during asynchronous execution.
