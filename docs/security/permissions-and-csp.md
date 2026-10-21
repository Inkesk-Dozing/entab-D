# Permissions & Content Security Policy (CSP)

## Manifest V3 Permissions Contract

Entab-D enforces the principle of least privilege. The extension operates without requesting generic host permissions (`*://*/*`), ensuring browser activity cannot be monitored arbitrarily across arbitrary web pages.

### Required Permissions

| Permission | Justification |
| :--- | :--- |
| `tabs` | Required to inspect tab URLs (`tab.url`), tab IDs, and window IDs for grouping, deduplication, and predictive switching. |
| `tabGroups` | Required to query existing groups, create new groups, update titles, assign colors, and toggle collapsed states. |
| `storage` | Required to store user rules (`chrome.storage.sync`) and local predictive transition counters (`chrome.storage.local`). |

## Content Security Policy (CSP)

Manifest V3 strictly forbids executing remote code or un-sandboxed inline scripts:
```json
"content_security_policy": {
  "extension_pages": "script-src 'self'; object-src 'self';"
}
```

### Prohibitions
- No `eval()` or `new Function()` invocations.
- No inline script tags (`<script>alert(1)</script>`) inside `popup.html` or `options.html`.
- No remote script dependencies loaded from external CDNs. All assets and logic must exist natively inside the extension package.
