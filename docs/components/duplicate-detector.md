# Component: Duplicate Detector & Cleaner

## Purpose
Identifies redundant open browser tabs by normalizing URLs (stripping query tracking tokens like UTM, GCLID, and fragments), grouping identical destinations, and safely closing duplicate instances based on user retention preferences (`oldest` vs `newest`).

## Source Location
`src/background/service_worker.js` (`normalizeUrl`, `findDuplicates`, `closeDuplicates`)

## Dependencies
- Native APIs: `chrome.tabs.query`, `chrome.tabs.remove`.
- Web Standards: Standard WHATWG `URL` constructor.

## Big-O Complexity

| Operation | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| **URL Normalization** | $O(U)$ | $O(U)$ | Where $U$ is URL length; parses parameters and trims tracking keys. |
| **Duplicate Scan** | $O(N \cdot U)$ | $O(N \cdot U)$ | Ingests $N$ open tabs into hash map keyed by normalized URL string. |
| **Duplicate Closure** | $O(D \log D)$ | $O(D)$ | Sorts $D$ duplicates by tab ID to distinguish oldest vs newest. |
| **Tab Termination** | $O(D)$ | $O(D)$ | Dispatches batch deletion of $D$ duplicate tabs. |

## Error Boundaries & Edge Cases
- Handles malformed URLs gracefully by catching parsing exceptions in `normalizeUrl`.
- Re-validates tab existence before dispatching `chrome.tabs.remove` to prevent unhandled promise rejections on tabs closed during scanning.
