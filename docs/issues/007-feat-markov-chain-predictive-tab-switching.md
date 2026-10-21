# Issue 007: [FEAT] Bounded Markov Transition Matrix with LRU Eviction and Recency Weighting

**Labels**: `enhancement`, `performance`, `machine-learning`

---

## 1. Context & Problem Statement
`src/behavior/predictor.js` records transitions between tabs to recommend the user's next destination in the popup HUD:
```javascript
this.transitions[normFrom][normTo] = (this.transitions[normFrom][normTo] || 0) + 1;
await chrome.storage.local.set({ tabTransitions: this.transitions });
```
This naive accumulation suffers from three critical flaws:
1. **Unbounded Storage Growth**: Over weeks of browsing thousands of unique URLs, `tabTransitions` will exceed Chrome's `QUOTA_BYTES_PER_ITEM` (8KB in sync, ~10MB in local) and throttle write operations.
2. **Frequency Bias over Recency**: An ancient tab transition performed 1,000 times last year will permanently suppress a new workflow established this week.
3. **Missing Listeners**: `chrome.tabs.onActivated` is not hooked properly into the service worker, meaning tab switches between already open tabs are frequently missed.

---

## 2. Technical Architecture & Math Formulation

### Time-Decayed Markov Frequency
Instead of raw integer counters, apply exponential recency decay $\lambda \in (0, 1)$ on transition updates:
$$S_{t+1}(A \rightarrow B) = S_t(A \rightarrow B) \cdot \lambda^{\Delta t} + 1$$
Where $\Delta t$ is days elapsed since last transition. This causes abandoned workflows to naturally fade over time.

### Storage Pruning (LRU)
- Hard limit: Maximum 300 source nodes, maximum 10 target destinations per node.
- Pruning policy: When node count exceeds 300, evict the bottom 20% of transitions based on lowest combined score and oldest timestamp.

---

## 3. Implementation Plan
- [ ] Hook `chrome.tabs.onActivated` and `chrome.windows.onFocusChanged` in `service_worker.js` to ensure tab switches are captured.
- [ ] Update `predictor.js` to store timestamps alongside transition counts:
  ```typescript
  interface TransitionEntry {
    count: number;
    lastAccessed: number;
  }
  ```
- [ ] Implement `pruneTransitions(limit = 300)` executing whenever storage is saved.
- [ ] Add global shortcut (`Alt + Shift + P`) to immediately switch to top predicted tab without opening the popup.

---

## 4. Acceptance Criteria
1. `chrome.storage.local` memory consumption for `tabTransitions` remains strictly bounded below 500KB.
2. Tab transitions older than 30 days decay gracefully in recommendation ranking.
3. Rapid tab switches between IDE, documentation, and local server render accurate top-candidate suggestions in the popup HUD.
