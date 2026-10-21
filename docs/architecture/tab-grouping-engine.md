# Tab Grouping Engine Specification

The grouping engine evaluates open browser tabs against user-defined rule matrices to assign them into titled, color-coded Chrome tab groups.

```mermaid
flowchart TD
    Start([Trigger Grouping]) --> FetchRules[Load Rules from Storage]
    FetchRules --> QueryTabs[Query chrome.tabs across Windows]
    QueryTabs --> GroupByWindow[Partition Tabs by windowId]
    
    GroupByWindow --> WindowLoop[Iterate each Window]
    WindowLoop --> QueryGroups[Query existing tabGroups in Window]
    QueryGroups --> TabLoop[Iterate tabs in Window]
    
    TabLoop --> CheckProtocol{Valid Web Protocol?\nhttp/https}
    CheckProtocol -- No --> SkipTab[Skip system/blank tabs]
    CheckProtocol -- Yes --> MatchRule{Match Hostname against\nRule Keywords}
    
    MatchRule -- No Match --> NextTab[Next Tab]
    MatchRule -- Matches Rule R --> CheckGroupExists{Group for R exists\nin Window?}
    
    CheckGroupExists -- Yes --> AddToGroup[chrome.tabs.group with existing groupId]
    CheckGroupExists -- No --> CreateGroup[chrome.tabs.group create new group]
    CreateGroup --> SetGroupMeta[chrome.tabGroups.update: Title & Color]
    SetGroupMeta --> CacheGroup[Record groupId in Window group map]
    
    AddToGroup --> NextTab
    CacheGroup --> NextTab
    SkipTab --> NextTab
    
    NextTab --> MoreTabs{More tabs in window?}
    MoreTabs -- Yes --> TabLoop
    MoreTabs -- No --> CheckCollapse{Collapse requested?}
    
    CheckCollapse -- Yes --> CollapseAll[chrome.tabGroups.update collapsed=true]
    CheckCollapse -- No --> MoreWindows{More windows?}
    CollapseAll --> MoreWindows
    
    MoreWindows -- Yes --> WindowLoop
    MoreWindows -- No --> End([Grouping Complete])
```

## Window Isolation Constraint

Chrome enforces strict window boundaries for tab groups: **a tab group ID is valid only within the window where it was created**. Attempting to move a tab from Window A into a Group ID belonging to Window B throws runtime exceptions (`chrome.tabs.group: Group belongs to another window`). The engine must partition tab processing by `windowId` and index group IDs independently per window.
