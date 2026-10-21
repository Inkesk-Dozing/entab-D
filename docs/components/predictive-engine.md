# Component: Predictive Engine (Markov Transition Modeler)

## Purpose
Constructs a localized, privacy-first Markov transition matrix modeling browser tab navigation patterns. Tracks directional tab switching frequencies ($A \rightarrow B$) and recommends the most probable next tab to the user in the popup HUD.

## Source Location
`src/behavior/predictor.js`

## Dependencies
- Native APIs: `chrome.storage.local`.
- Storage Keys: `predictiveToggle`, `tabHistory`, `tabTransitions`.

## Big-O Complexity

| Operation | Time Complexity | Space Complexity | Notes |
| :--- | :--- | :--- | :--- |
| **Record Transition** | $O(U)$ | $O(1)$ | URL normalization ($U$) followed by hash map frequency increment. |
| **Predict Next Tabs** | $O(T \log T + N)$ | $O(T + P)$ | Sorts $T$ outgoing transitions for current URL and filters against $N$ open tabs. |
| **State Eviction** | $O(M)$ | $O(M)$ | Prunes oldest keys if transition table exceeds boundary threshold $M$. |

## Error Boundaries & Edge Cases
- Disregards intra-tab reloads and identical consecutive URL switches ($A \rightarrow A$).
- Respects `predictiveToggle` boolean guard; terminates immediately when disabled to minimize CPU and storage overhead.
