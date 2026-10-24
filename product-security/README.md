# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_1 vetted findings · updated 2026-10-24 · ranked by composite · findings from the latest 31 days · [8 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now: the editorial pass and the news gate. News is kept for good; findings are not._

- **[Sentry's Next.js tunnelRoute skipped middleware for everything under the tunnel path, not just the requests its rewrite served (GHSA-mchm-gjx6-7h55)](https://github.com/advisories/GHSA-mchm-gjx6-7h55)**
  _Why now: Critical GHSA in a ubiquitous Next.js SDK with a transferable lesson: middleware exemptions are authz bypasses wherever middleware is the only authorization check. · cve · newsworthy · high-relevance · timely_
- **[CISA KEV: Plex Media Server encoded-URI-scheme flaw CVE-2026-96654 exploited in the wild, part of a four-CVE chain](https://nvd.nist.gov/vuln/detail/CVE-2026-96654)**
  _Why now: Exploited-in-the-wild Plex chain added to CISA KEV with a due date of today and a public plex2shell write-up; patch now. · active-exploitation · cve · timely_
- **[Pillow DoS: a 5.6 KB MIC file hangs n_frames at 100% CPU (GHSA-22hg-r758-rrw9)](https://github.com/advisories/GHSA-22hg-r758-rrw9)**
  _Why now: Fresh HIGH advisory in Pillow, which nearly every Python upload path uses; the fix pattern (formats allowlist, drop olefile, wall-clock timeouts) applies today. · cve · timely · high-relevance_
- **[How we found 24 Android vulnerabilities using our open source AI security agent](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/)**
  _Why now: 24 real, disclosed Android vulnerabilities (OsmAnd location tracking, a WebView account-takeover chain) found with an open-source agent you can run today, plus candid lessons on LLM severity misjudgment and false positives. · newsworthy · trending · timely · high-relevance_
- **[Trail of Bits Runs an Independent, From-Scratch Auditor for Signal's Key Transparency System](https://blog.trailofbits.com/2026/08/11/how-trail-of-bits-helps-verify-the-integrity-of-your-signal-chats/)**
- **[38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428)**
  _Why now: Large-scale, widely-discussed finding on coding-agent risk with a concrete gate: automated secret + dependency-integrity scanning on agent PRs, because human review misses 81%. · trending · high-relevance · teachable_

| Domain | Findings |
| --- | --- |
| AI in the SDLC | 1 |

## AI in the SDLC

- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs](ai-code/2026-10-claude-wrote-machine-checked-no-crash-proofs-for-239-oss-fuz.md)** · composite **60.25** · Oct 22, 2026  
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.  
  _[source](https://www.anthropic.com/research/formal-verification)_

---

[← Home](../README.md) · [Standing claims](../claims/product-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
