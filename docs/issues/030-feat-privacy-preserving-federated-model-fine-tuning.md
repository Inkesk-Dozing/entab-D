# Issue 030: [AI-FEAT] Local On-Device Preference Refinement & Federated Learning Guard

**Labels**: `ai`, `privacy`, `machine-learning`, `roadmap-v2`

---

## 1. Context & Problem Statement
Every user has unique domain definitions. For a software engineer, `github.com` is "Work/Coding", while for an open-source hobbyist it might be "Personal", and for a recruiter it might be "Hiring".
A one-size-fits-all model will make misclassifications.

The extension must continuously adapt its on-device models to **learn user corrections** (e.g., when the user manually moves a tab from "Entertainment" to "Work", or renames a group) without ever transmitting browsing history or private URLs to any remote server.

---

## 2. Technical Architecture & Reinforcement Loop

```mermaid
flowchart TD
    UserMove[User moves Tab from Group A to Group B manually] --> CaptureCorrection[Capture Feedback: { domain, true_label: B, old_label: A }]
    CaptureCorrection --> UpdateLocalPrior[Update Local Dirichlet / Logistic Weight Prior]
    UpdateLocalPrior --> StoreWeights[Store refined weights in chrome.storage.local]
    StoreWeights --> NextInference[Future predictions for this domain use personalized weights]
    
    subgraph Privacy Wall
        StoreWeights -.x CloudServer[No outbound network requests]
    end
```

---

## 3. Implementation Plan
- [ ] Listen for manual tab movements using `chrome.tabGroups.onUpdated` and `chrome.tabs.onMoved`.
- [ ] Implement an on-device Online Perceptron / Logistic Regression weight updater running in Web Worker:
  - Takes features: domain tokens, path tokens, title n-grams.
  - Updates linear classifier weights on user corrections.
- [ ] Provide user transparency settings in Options:
  - *"View Learned Personal Preferences"*.
  - *"Reset AI Personalization to Factory Defaults"*.

---

## 4. Acceptance Criteria
1. When a user manually corrects a tab's group twice, the AI permanently remembers the preference for that domain.
2. 100% of weight adjustments happen locally in `chrome.storage.local`.
3. Resetting personalization restores default global models cleanly.
