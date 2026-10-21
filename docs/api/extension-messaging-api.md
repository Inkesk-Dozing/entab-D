# Extension Internal Messaging Contract

All communication between the user interface (`src/popup/`, `src/options/`) and the background service worker (`src/background/service_worker.js`) is managed through structured payloads via `chrome.runtime.sendMessage`.

## Message Routing Table

| Message Type | Direction | Payload Schema | Response Schema | Description |
| :--- | :--- | :--- | :--- | :--- |
| `GROUP_TABS` | UI ➔ SW | `{ type: "GROUP_TABS", collapse?: boolean }` | `{ ok: boolean, error?: string }` | Evaluates all open tabs against rules, groups them, and optionally collapses groups. |
| `FIND_DUPLICATES` | UI ➔ SW | `{ type: "FIND_DUPLICATES" }` | `{ ok: boolean, duplicates: DuplicateEntry[] }` | Scans all windows for normalized URL collisions. |
| `CLOSE_DUPLICATES`| UI ➔ SW | `{ type: "CLOSE_DUPLICATES", keep: "oldest" \| "newest" }` | `{ ok: boolean, closed: number, error?: string }` | Terminates duplicate tab instances, keeping specified reference tab. |
| `GET_RULES` | UI ➔ SW | `{ type: "GET_RULES" }` | `{ ok: boolean, rules: Rule[] }` | Retrieves active user rules from `chrome.storage.sync`. |
| `SAVE_RULES` | UI ➔ SW | `{ type: "SAVE_RULES", rules: Rule[] }` | `{ ok: boolean, error?: string }` | Persists modified rules and triggers tab re-evaluation. |
| `SET_AUTO_GROUP` | UI ➔ SW | `{ type: "SET_AUTO_GROUP", enabled: boolean }` | `{ ok: boolean }` | Toggles automatic grouping on tab creation/navigation. |
| `GET_PREDICTIONS`| UI ➔ SW | `{ type: "GET_PREDICTIONS" }` | `{ ok: boolean, predictions: PredictedTab[] }` | Returns ranked tab candidates based on transition history. |

## Data Models

### Rule
```typescript
interface Rule {
  name: string;      // e.g. "Study", "Research"
  color: "blue" | "cyan" | "green" | "yellow" | "red" | "pink" | "purple" | "orange" | "grey";
  keywords: string[]; // e.g. ["leetcode", "geeksforgeeks", "github.com"]
}
```

### DuplicateEntry
```typescript
interface DuplicateEntry {
  originalId: number;   // Tab ID of the retained reference
  duplicateId: number;  // Tab ID of the duplicate instance
  url: string;          // Normalized URL
  title: string;        // Page title
}
```

### PredictedTab
```typescript
interface PredictedTab {
  id: number;           // Tab ID
  windowId: number;     // Window ID
  url: string;          // Full URL
  title: string;        // Tab title
  score?: number;       // Transition probability weight
}
```
