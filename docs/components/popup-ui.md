# Component: Popup Interface (HUD)

## Purpose
Provides the primary lightweight graphical interface rendered when the user activates the extension icon. Offers instantaneous manual controls for grouping, duplicate management, auto-group toggle, and predictive tab recommendations.

## Source Location
`src/popup/popup.html`, `src/popup/popup.js`, `src/popup/popup.css`

## Dependencies
- APIs: `chrome.runtime.sendMessage`, `chrome.storage.sync`, `chrome.tabs.update`, `chrome.windows.update`.
- DOM APIs: Native DOM querying and dynamic element injection.

## Big-O Complexity

| Operation | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| **HUD Initialization** | $O(P)$ | $O(P)$ | Renders up to $P$ predictive suggestion DOM nodes on load. |
| **Duplicate Rendering** | $O(D)$ | $O(D)$ | Creates $D$ list elements for scanned duplicates. |
| **Tab Focus Switch** | $O(1)$ | $O(1)$ | Focuses window and updates tab `active: true`. |

## Error Boundaries & Edge Cases
- Automatically disables action buttons during async execution (e.g. "Scanning...", "Grouping...") to eliminate double-click re-entrancy.
- Gracefully handles empty states ("No duplicates found 🎉").
