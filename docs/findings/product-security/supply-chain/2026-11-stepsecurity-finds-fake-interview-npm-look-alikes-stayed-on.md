# StepSecurity finds fake-interview npm look-alikes stayed on npm for seven months

**Published:** Nov 13, 2026

> **Takeaway:** Interview assignments run on work laptops are an employer supply-chain risk, and the malware hides in build-time code and blockchain-resolved servers that install-script controls and static blocklists both miss.

## TL;DR

StepSecurity followed up JFrog's report on AccuraSoftHire, a fake company that gave job candidates take-home tests built on look-alike Tailwind plugins carrying the PolinRider loader. Two of the poisoned packages, tailwind-lines-clamps and tailwind-lineclamp, stayed on npm for 211 and 169 days and had more than 4,000 downloads in 2026. StepSecurity also decoded all 609 transactions from the Ethereum wallet the loader uses to find its server (the NullReceiver technique) and recovered eight server IPs, the newest posted on October 19.

## Lessons

- The loader runs when Tailwind builds the CSS, not at install time, so controls that only watch or disable npm install scripts miss it. - _"The loader does not run during `npm install`, so tools that only check install scripts do not see it."_
- A release-age cooldown would have blocked most of the short-lived look-alikes but not the two that lasted months. Catching those needs an inventory of the packages on developer machines. - _"A cooldown that blocks packages published in the last few days would have held back most of the short-lived ones, but not the two that lasted months."_
- Because the server address comes from public blockchain transactions, the attacker can move servers without republishing anything, and defenders can read back the full server history to build a complete blocklist. - _"To change servers, the attacker only has to send a new transaction. No package needs to change."_

## Threat · Conditions · Mitigations

- **Threat:** North Korea-linked operators pose as employers and get developers to run take-home projects on work laptops; a blockchain-resolved loader then steals browser, wallet, SSH, cloud and git credentials.
- **Conditions:** A developer runs a recruiter-supplied project build, a curl one-liner or an unpacked extension on a company machine that holds deployment or cloud credentials.
- **Mitigations:** Ban interview work on company devices, inventory packages on developer machines, alert on VS Code folderOpen tasks and unpacked extensions, apply release-age cooldowns, block all eight decoded server IPs, monitor build-time egress, and rotate all credentials on any exposed machine.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [StepSecurity](https://www.stepsecurity.io/blog/accurasofthire-fake-interview-developer-machines)  ·  **Retrieved:** 2026-11-13  
**Scores:** Newness 49 · Novelty 30 · Relevance 74 · Credibility 50 · **Composite 51** _(each 0-100)_  
**Tags:** `supply-chain`, `npm`, `typosquatting`, `dprk`, `fake-interview`, `polinrider`, `blockchain-c2`, `developer-endpoint`, `cooldown`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: JFrog's AccuraSoftHire research; OpenSourceMalware's NullReceiver and PolinRider write-ups; EtherHiding blockchain C2; the Binance theft entry citing fake recruitment interviews. New: measured npm dwell times (169 and 211 days) and the decoded eight-server history.

_Source: [https://www.stepsecurity.io/blog/accurasofthire-fake-interview-developer-machines](https://www.stepsecurity.io/blog/accurasofthire-fake-interview-developer-machines)_  ·  [← back to index](../README.md)
