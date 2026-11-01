# Alpine Linux rebuilt GitLab after its upgrade missed a Ruby patch

**Published:** Oct 28, 2026

> **Takeaway:** If you build GitLab yourself, check what runtime patches its official packages carry, and log outbound traffic so you can rule a compromise in or out.

## TL;DR

On October 20 and 21 a newly registered account sent crafted CI configurations to Alpine Linux's GitLab to exploit CVE-2026-97229, a CVSS 10.0 bug in Ruby's Onigmo regular expression engine, crashing workers 8 times. Alpine's upgrade to GitLab 19.3.6 did not fix it, because the fix is a patch GitLab applies to Ruby only in its official packages and Alpine's image used stock Ruby; self-built installs also need Ruby 3.3.13, 3.4.12 or 4.0.9. Alpine found no evidence of code execution but could not rule it out, so it rebuilt the instance, reset all passwords and secret keys, and verified packages and releases against records outside GitLab.

## Lessons

- A vendor's fix can live in a patched runtime it bundles, so upgrading the application alone leaves source or self-built installs vulnerable. - _"The fix isn’t in GitLab’s own code but in a patch to Ruby, which GitLab applies only in its official packages."_
- The attacker pulled Alpine's public container image, likely to tune the exploit to the exact build, so publishing your images helps attackers fit exploits to you. - _"The attacker also downloaded our GitLab container image, which suggests they were tuning the exploit to our exact build."_
- Without outbound connection logs, Alpine could not prove the exploit failed, which forced a full rebuild. - _"We had no logging of outbound network connections, and our hosting provider keeps none either."_
- Keeping signing keys off the forge and checking commits against independent records let Alpine clear its packages and releases despite the uncertainty. - _"The keys that sign Alpine packages and releases are not, and never have been, stored on the GitLab server."_

## Threat · Conditions · Mitigations

- **Threat:** An attacker with a self-registered account submits crafted CI configurations that trigger an Onigmo regex engine bug for possible code execution on the GitLab server, exposing user data, password hashes, two-factor authentication secrets, CI/CD variables, runner tokens and private repositories.
- **Conditions:** Self-managed GitLab without the October 12 fix, or GitLab built on standard Ruby older than 3.3.13, 3.4.12 or 4.0.9, with open account registration.
- **Mitigations:** Use GitLab's official packages or upgrade Ruby to a fixed release, apply critical GitLab releases within a day, log outbound and database connections and keep logs longer, keep signing keys off the forge, and sign release tags so releases can be verified outside GitLab.

---

**Topic:** Product Security  ·  **Domain:** Detection, Response & Threat Intel  
**Source:** [@sashk via Hacker News](https://alpinelinux.org/posts/GitLab-security-incident-CVE-2026-97229.html)  ·  **Author:** sashk  ·  **Retrieved:** 2026-10-29  
**Scores:** Newness 19 · Novelty 50 · Relevance 80 · Credibility 55 · **Composite 52** _(each 0-100)_  
**Tags:** `gitlab`, `ruby`, `onigmo`, `regex`, `incident-response`, `patch-management`, `forensics`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: The pool has GitLab's advisory for a different CVSS 10.0 regex RCE (CVE-2026-110264, 19.5.1 patch release), which is a vendor patch notice. This entry adds a first-hand incident: the fix lived in a bundled Ruby patch that self-built installs missed, plus the forensic limits that forced a rebuild.

_Source: [https://alpinelinux.org/posts/GitLab-security-incident-CVE-2026-97229.html](https://alpinelinux.org/posts/GitLab-security-incident-CVE-2026-97229.html)_  ·  [← back to index](../README.md)
