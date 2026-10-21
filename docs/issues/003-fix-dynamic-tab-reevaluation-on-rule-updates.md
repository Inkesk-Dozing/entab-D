# Issue 003: [FIX] Implement Dynamic Tab Re-evaluation and Group Eviction on Rule Modification

**Labels**: `bug`, `enhancement`, `tab-groups`

---

## 1. Context & Problem Statement
Currently, when a user edits, renames, or deletes rules in `options.html` (e.g., changing a group rule from matching `google.com` to `bing.com`, or removing a keyword), tabs already placed inside the existing Chrome tab group are never re-evaluated or evicted.

As a consequence, tabs that no longer match the modified rule remain trapped inside the group indefinitely, corrupting workspace integrity.

---

## 2. Technical Root Cause Analysis
In `service_worker.js`, the `SAVE_RULES` message handler simply commits the new rule payload to `chrome.storage.sync.set({ rules: msg.rules })` and returns `{ ok: true }`. There is no reconciliation pass triggered to re-audit existing tab groups against the newly updated ruleset.

---

## 3. Implementation Plan
- [ ] Create a `reconcileTabGroups()` procedure triggered on `SAVE_RULES`:
  ```mermaid
  sequenceDiagram
      autonumber
      participant UI as Options Page
      participant SW as Service Worker
      participant Chrome as chrome.tabGroups / tabs
      
      UI->>SW: sendMessage({ type: "SAVE_RULES", rules })
      SW->>SW: Persist rules to storage
      SW->>Chrome: Query all existing tab groups and tabs
      SW->>SW: Cross-check each grouped tab's URL against active rules
      alt Tab no longer matches group rule
          SW->>Chrome: chrome.tabs.ungroup(tab.id)
      end
      SW->>SW: Re-run groupTabsByRules() to re-assign evicted tabs
      SW-->>UI: Return { ok: true, reevaluated: count }
  ```
- [ ] If an existing group has zero remaining tabs after eviction, verify that Chrome automatically dissolves the group or explicitly dissolve orphaned empty groups.
- [ ] Add an opt-in toggle in the Options dashboard: *"Automatically re-evaluate open tabs when rules change"*.

---

## 4. Acceptance Criteria
1. Modifying a rule's keywords immediately evicts non-matching tabs from that group.
2. If the evicted tab matches another valid rule, it is seamlessly transferred into the correct target group.
3. If the evicted tab matches no rules, it is ungrouped into the default window workspace.
