# Malicious native apps can hijack browser Native Messaging to steal password vaults

**Published:** Nov 3, 2026

> **Takeaway:** If your extension talks to a native helper, authenticate and encrypt that channel yourself; the browser does not.

## TL;DR

An IEEE S&P 2027 paper shows that a non-privileged malicious app on the user's machine can abuse the browser NativeMessaging API, which links extensions to native helper apps, to intercept their traffic or act as a confused deputy. The authors demonstrate full password-vault leakage and arbitrary document signing against 1Password, the EU eID system and Google Drive, whose extensions total over 532 million downloads. The root cause is that the channel has no root of trust or client attestation, and they propose encrypting messages with a secret shared out of band.

## Lessons

- Any unprivileged local app can sit on the extension-to-native channel and intercept or misuse it. - _"a novel attack that allows a non-privileged malicious native app to misuse browsers' native messaging capabilities to stealthily intercept sensitive communications or launch confused deputy attacks against other native apps"_
- The impact on real apps is severe: full vault leakage and signing documents in government workflows. - _"Our attacks have severe ramifications, including full password vault leakage, and arbitrary document signing in governmental workflows."_
- The design flaw is an untrusted channel with no root of trust or attestation of the other end. - _"native messaging being built on top of an untrusted communication channel without providing a root of trust or enforcing some form of client attestation"_
- Vendors can fix it at the app layer by encrypting messages with an out-of-band shared secret. - _"we propose a straightforward mitigation technique of message encryption with out-of-band secret sharing"_

## Threat · Conditions · Mitigations

- **Threat:** A malicious but unprivileged app on the user's machine intercepts or impersonates traffic between a browser extension and its native helper app.
- **Conditions:** An extension uses the NativeMessaging API to exchange secrets or authorize operations with a native app, and the messages are not authenticated end to end.
- **Mitigations:** Encrypt and authenticate native messaging traffic with a secret shared out of band, and treat the native channel as untrusted in the threat model.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [IEEE S&P (via arXiv)](http://arxiv.org/abs/2611.04291v1)  ·  **Retrieved:** 2026-11-04  
**Scores:** Newness 33 · Novelty 55 · Relevance 72 · Credibility 72 · **Composite 57** _(each 0-100)_  
**Tags:** `browser-extensions`, `native-messaging`, `confused-deputy`, `password-managers`, `eid`, `local-attacker`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Prior work studied malicious webpages and extensions attacking privileged browser APIs, and password-manager extension attacks; local-IPC impersonation and confused-deputy attacks on desktop apps are well known. The paper says NativeMessaging itself had not been examined.

_Source: [http://arxiv.org/abs/2611.04291v1](http://arxiv.org/abs/2611.04291v1)_  ·  [← back to index](../README.md)
