# Entab-D Project Tracker & Historical Issues

> [!NOTE]
> This tracker has been elevated to the formal documentation architecture in [`/docs`](docs/).
> For the comprehensive roadmap and detailed issue specifications, see:
> - **Strategic Roadmap**: [`docs/roadmap.md`](docs/roadmap.md)
> - **Production Issue Specifications**: [`docs/issues/`](docs/issues/)

---

## Historical Issues Index

### 1. Tabs Not Ungrouping on Rule Update
* **Status**: Tracked in [`docs/issues/003-fix-dynamic-tab-reevaluation-on-rule-updates.md`](docs/issues/003-fix-dynamic-tab-reevaluation-on-rule-updates.md)
* **Description**: When a group's rules are changed, tabs already in that group are not re-evaluated.

### 2. Extension Toggle Ignores Existing Tabs
* **Status**: Tracked in [`docs/issues/002-fix-service-worker-lifecycle-and-state-persistence.md`](docs/issues/002-fix-service-worker-lifecycle-and-state-persistence.md)
* **Description**: When the extension is enabled, it does not scan or group tabs that are already open.

### 3. Cross-Window Group Consolidation
* **Status**: Tracked in [`docs/issues/005-feat-cross-window-tab-group-consolidation.md`](docs/issues/005-feat-cross-window-tab-group-consolidation.md)
* **Description**: Consolidating matching groups across multiple browser windows into a single window.

### 4. Rule Conflict Indicator
* **Status**: Tracked in [`docs/issues/006-feat-rule-conflict-detection-and-priority-resolution.md`](docs/issues/006-feat-rule-conflict-detection-and-priority-resolution.md)
* **Description**: Notifying users when rule keywords overlap and resolving evaluation precedence.