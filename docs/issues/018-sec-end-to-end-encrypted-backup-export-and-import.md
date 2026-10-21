# Issue 018: [SEC] Encrypted Rule Export, Backup Import, and Cloud Sync Sanitization

**Labels**: `security`, `storage`, `enhancement`

---

## 1. Context & Problem Statement
Currently, users have no easy way to transfer their custom rules, group definitions, and color assignments across computers without manually re-typing them or using the experimental Python backend.
Directly exporting plaintext JSON files presents security and privacy risks: rules expose the user's specific internal company domains, sensitive intranet paths, or research targets.

---

## 2. Technical Architecture & Cryptographic Primitives

Implement client-side encryption for backup files using the Web Cryptography API (`window.crypto.subtle`):

```mermaid
flowchart TD
    RawRules[User Rules JSON] --> DeriveKey[PBKDF2 Key Derivation with User Passphrase + Salt]
    DeriveKey --> Encrypt[AES-GCM 256-bit Encryption]
    Encrypt --> ExportPackage[Package: { iv, salt, ciphertext, version: 1 }]
    ExportPackage --> DownloadFile[Download .entab.enc backup file]
```

---

## 3. Implementation Plan
- [ ] Implement encryption/decryption module in `src/utils/crypto.js`:
  - `exportEncryptedRules(passphrase: string): Promise<string>`
  - `importEncryptedRules(encryptedPayload: string, passphrase: string): Promise<Rule[]>`
  - Algorithm: AES-GCM with 256-bit key, PBKDF2 with 100,000 iterations and SHA-256.
- [ ] Add "Export Encrypted Backup" and "Import Backup" buttons in `options.html`.
- [ ] Support unencrypted JSON export for users who prefer raw editing, with a clear privacy warning modal.

---

## 4. Acceptance Criteria
1. Exporting with a passphrase generates an AES-GCM encrypted file that cannot be read without the password.
2. Importing with the correct passphrase decrypts and restores all rule groups and colors faithfully.
3. Entering an incorrect passphrase fails gracefully with a clear error without corrupting existing rules.
