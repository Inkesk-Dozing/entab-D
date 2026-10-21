# Security Policy

## Supported Versions

The Entab-D project actively maintains security updates on the following branches:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0.0 | :x:                |

## Reporting a Vulnerability

The Entab-D development team takes privacy and browser extension security seriously. Because browser extensions interact directly with browser session tabs, storage, and active URLs, security flaws must be isolated promptly.

### Reporting Protocol

1. **Do not disclose publicly**: Do not create public GitHub issues or forum posts detailing unpatched security vulnerabilities.
2. **Contact Email**: Submit vulnerability disclosures to `inkeskdozing@gmail.com` or via GitHub Private Vulnerability Reporting on the repository.
3. **Information Required**:
   - Extension version and Chrome browser build.
   - Proof of Concept (PoC) code or step-by-step reproduction instructions.
   - Attack vector description (e.g., URL leakage, arbitrary script execution, unauthenticated localhost daemon access).
   - Expected vs observed impact.

### Response Timelines

- **Initial Triage**: Within 48 hours of submission.
- **Status Update & Validation**: Within 5 business days.
- **Patch Release & Advisory**: Disclosed responsibly once a verified fix has been merged into `main`.

## Security Guidelines for Extensions

- Entab-D strictly adheres to the principle of least privilege in `manifest.json`.
- Tab URLs are parsed locally within the extension boundary; browsing history and active URLs are never transmitted to unauthorized third-party endpoints.
