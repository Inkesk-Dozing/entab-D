# Threat Modeling & Mitigation Analysis

Entab-D processes browser session data (tab URLs, window states, and user grouping rules). Securing this operational boundary requires defense-in-depth across the extension runtime, storage primitives, and the local sync daemon.

## Threat Assessment Matrix

| Threat ID | Threat Vector | Target Component | Impact | Severity | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TH-01** | Cross-Site Request Forgery / Arbitrary Daemon Access | `python/app.py` (Port 5055) | Malicious web page sends `POST /rules` to overwrite user rule set or extracts browsing categories. | **HIGH** | Bind server strictly to `127.0.0.1`, validate custom authorization header (`X-Entab-Token`), and reject non-extension CORS origin headers. |
| **TH-02** | URL Tracking Parameter Leakage | `service_worker.js` | Full URLs containing sensitive session tokens or PII stored in history. | **MEDIUM** | Comprehensive normalization stripping tracking keys (`utm_*`, `token`, `session`, `auth`) before saving transition logs. |
| **TH-03** | Local Storage Quota Exhaustion (DoS) | `predictor.js` (`tabTransitions`) | Unbounded transition map growth causes `QUOTA_BYTES` errors in `chrome.storage.local`. | **MEDIUM** | Implement Least-Recently-Used (LRU) eviction bounding transitions to maximum 500 keys. |
| **TH-04** | Restricted Scheme Manipulation | `chrome.tabs.group` | Malicious scripts attempt grouping `chrome://settings` or `chrome-extension://` paths. | **LOW** | Protocol validation filtering out non-`http`/`https` protocols prior to any API invocations. |
| **TH-05** | Stale Permissions & Over-Privilege | `manifest.json` | Extension requests broader access than required (e.g. `<all_urls>`, `webRequest`). | **LOW** | Strictly limit permissions to `tabs`, `tabGroups`, and `storage`. Reject arbitrary host permissions. |
