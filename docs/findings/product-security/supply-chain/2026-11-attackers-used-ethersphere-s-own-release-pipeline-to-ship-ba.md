# Attackers used Ethersphere's own release pipeline to ship backdoored bee-js and Swarm Desktop

**Published:** Nov 9, 2026

> **Takeaway:** Trusted publishing and valid provenance prove where a package was built, not that its source was reviewed, so release workflows need branch, tag and reviewer gates of their own.

## TL;DR

On November 9, 2026, an attacker with two compromised GitHub accounts published a malicious @ethersphere/bee-js 13.3.0 to npm and a trojanized Swarm Desktop 0.56.2, both through the project's legitimate GitHub Actions workflows. The npm package added a postinstall loader that runs JavaScript fetched from api[.]frameworkmetrics[.]xyz. It carried valid SLSA (Supply-chain Levels for Software Artifacts) provenance, because the publish job accepted any release event with tests skipped and no branch, reviewer or tag check. The desktop build was signed, notarized and pushed through the auto-updater, and the later stages reuse the Ethereum-contract command-and-control (C2) of the earlier SleepyDuck Open VSX campaign.

## Lessons

- Valid provenance from a legitimate trusted-publishing workflow could not tell the malicious release from a good one. - _"The legitimate 13.2.0 attestation has exactly the same shape, so provenance alone could not have told the two releases apart."_
- Provenance attests to the build location, not to code review. - _"It proves where a package was built, not that the source was reviewed."_
- The publish job ran on any release event with CI skipped and no check that the commit came from the protected branch. - _"Nothing in the workflow checks that the released commit belongs to the protected `upcoming` branch"_
- Without a long-lived token, the attacker simply drove the project's own OIDC trusted-publishing workflow. - _"No npm token was needed: the legitimate workflow, running legitimate workflow code from the tag"_
- Newer package managers that skip dependency install scripts by default would not have run the loader. - _"npm 12, pnpm 10 and later, Yarn Berry 4.14.0 and later, Bun and Deno skip unreviewed dependency scripts by default"_
- A manually dispatched workflow with a free-form branch input and no environment protection exposed code-signing secrets. - _"a manually triggered workflow that takes a free-form branch input, has no environment protection and hands the build the Apple and Windows signing certificates"_
- Commit author fields prove nothing. Push events tied to the authenticating credential identify the actor. - _"Author fields are client-set and worthless as evidence"_

## Threat · Conditions · Mitigations

- **Threat:** An attacker with maintainer and release-bot GitHub access publishes a remote-code loader through the project's own trusted-publishing and code-signing workflows.
- **Conditions:** Publish workflows that accept release events with CI skipped and no branch or reviewer gate, unprotected default branches, dispatchable workflows holding signing secrets, and clients that run dependency postinstall scripts by default.
- **Mitigations:** Pin publishing to commits on protected branches, require reviewers on publish environments, restrict signing secrets to protected workflows, require signed commits, use package managers that skip install scripts by default, and remove bee-js 13.3.0 and Swarm Desktop 0.56.2 and rotate Bee node keys and passwords on affected hosts.

---

**Topic:** Product Security  ·  **Domain:** Software Supply Chain  
**Source:** [Socket](https://socket.dev/blog/bee-js-compromise)  ·  **Retrieved:** 2026-11-09  
**Scores:** Newness 62 · Novelty 30 · Relevance 85 · Credibility 65 · **Composite 60** _(each 0-100)_  
**Tags:** `npm`, `supply-chain`, `github-actions`, `trusted-publishing`, `slsa-provenance`, `postinstall`, `electron`, `ethereum-c2`, `code-signing`  
**Also reported by:** [StepSecurity](https://www.stepsecurity.io/blog/ethersphere-bee-js-13-3-0-compromise), [SafeDep](https://safedep.io/blog/ethersphere-bee-js-npm-compromise) _(+2 corroborating)_  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The @asyncapi npm compromise and the SafeDep/StepSecurity npm worm entries already showed poisoned builds shipped with valid trusted-publishing provenance; new here are the release-event CI bypass, the signed auto-updated desktop build and the reuse of SleepyDuck's Ethereum C2.

_Source: [https://socket.dev/blog/bee-js-compromise](https://socket.dev/blog/bee-js-compromise)_  ·  [← back to index](../README.md)
