# A V12 audit of the x402 agent-payments protocol found 25 flaws

**Published:** Oct 22, 2026

> **Takeaway:** Agent payment clients and facilitators need strict instruction-type checks, origin binding on signatures, and hard spending limits.

## TL;DR

V12 reviewed the x402 codebase, which lets AI agents pay for resources by signing payments when a server returns HTTP 402. Of 25 flaws, three critical ones are covered. A Solana facilitator accepted an ApproveChecked instruction as a TransferChecked payment, so a merchant could ship goods without receiving tokens (V12 confirmed this in local tests, not on a live chain). A client wrapper signed Sign-In-With-X messages for any domain the server named. A client could be induced to authorize spending its whole token balance.

## Lessons

- The Solana verifier parsed the transaction without checking its instruction type. - _"The missing step was checking which instruction the transaction actually contained."_
- The login wrapper signed whatever domain the server supplied. - _"The automatic wrapper signed messages supplied in a `402` response without checking that their `domain` and `uri` matched the website the client had contacted."_
- Each critical bug crossed a different trust boundary. - _"Each issue crossed a different trust boundary: what counted as a payment, which website a signature was for, and who decided how much the wallet could spend."_
- An unfamiliar server could get an automated client to authorize its entire balance. - _"or get an automated client to authorize spending its entire balance of a supported token."_

---

**Topic:** AI Security  ·  **Domain:** Agent & Harness Security  
**Source:** [source](https://v12.sh/blog/x402)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 20 · Novelty 50 · Relevance 70 · Credibility 55 · **Composite 49** _(each 0-100)_  
**Tags:** `x402`, `agent-payments`, `solana`, `sign-in-with-x`, `wallet-security`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Agent-payment protocols are new; no earlier pool entry audits one, though generic signature-phishing and approval-vs-transfer confusion are known in DeFi. Verifier: General agent-payment and wallet-signing flaw classes (EIP-4361 SIWE phishing, unlimited approvals); Solana instruction-type confusion bugs. Delta: specific x40

_Source: [https://v12.sh/blog/x402](https://v12.sh/blog/x402)_  ·  [← back to index](../README.md)
