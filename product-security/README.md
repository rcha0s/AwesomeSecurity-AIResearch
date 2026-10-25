# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_9 vetted findings · updated 2026-10-25 · ranked by composite · findings from the latest 31 days · [41 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now: the editorial pass and the news gate. News is kept for good; findings are not._

- **[tensorlake@0.5.144 npm worm (Mini Shai-Hulud): hijacked admin account committed payload via GitHub UI, ran trusted-publishing workflow; revoking stolen GitHub token wipes home directory](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud)**
  _Why now: Live npm worm (two independent write-ups, SafeDep and StepSecurity) that published through the project's own trusted-publishing workflow and arms a home-directory wiper on token revocation: a concrete lesson that valid provenance doesn't… · newsworthy · widely-reported · active-exploitation · timely · high-relevance_
- **[Citrix NetScaler ADC/Gateway pre-auth command injection (CVE-2026-88771): Perl script shells out logged input; zero-day in default configuration, fixed in 14.1-73.37 and 13.1-64.23](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/)**
  _Why now: Pre-auth root command injection in NetScaler ADC/Gateway exploited as a zero-day in default configuration; concrete fixed builds, a sibling bug the upgrade alone doesn't fix, and log-hunting guidance. · cve · active-exploitation · timely · high-relevance_
- **[Google PageBreak: non-AI exploit validators gate AI web-testing agent: 500+ XSS bugs, near-zero false positives, but only 2 in apps on Google's high-assurance frameworks](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project)**
  _Why now: Google's production-scale numbers for AI web testing gated by non-AI exploit validators (500+ XSS, near-zero false positives, only 2 on its high-assurance frameworks) teach how to make agent-found bugs trustworthy. · trending · newsworthy · timely_
- **[F5 BIG-IP APM Pre-Auth Heap Overflow RCE (CVE-2026-94127): Unchecked Authorization Header Copy, OAuth Endpoint Handler (APM 21.1.0, 17.5.0-17.5.1, 17.1.0-17.1.3; fixed by hotfixes)](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/)**
  _Why now: Pre-auth RCE in an internet-facing BIG-IP edge appliance, exploited in the wild; teaches emergency patching and minimal exposure for auth-path parsing on edge devices. · cve · active-exploitation · timely · high-relevance_
- **[JFrog Artifactory auth-bypass chain exploited in the wild, leaving Groovy plugin backdoors that survive patching and stolen token-signing keys](https://www.wiz.io/blog/artifactory-under-attack-in-the-wild-exploitation-of-cve-2026-42016-cve-2026-4201)**
  _Why now: In-the-wild exploitation of a JFrog Artifactory auth-bypass chain leaving Groovy plugin backdoors; teaches what to hunt for on a core build-infrastructure system. · cve · active-exploitation · newsworthy_
- **[ITRES Labs used ChatGPT to rebuild two BruCON Windows kernel techniques, whose source was never released, in about 24 hours](https://labs.itresit.es/2026/10/15/copycats-at-machine-speed-reproducing-frontier-windows-kernel-exploitation-research/)**
  _Why now: tl;dr sec-featured case of an LLM-assisted researcher rebuilding Windows kernel techniques from slides and a binary in about 24 hours; it changes how to weigh partial disclosure. · trending · newsworthy_
- **[OVHcloud CLI: attacker swapped binaries on five GitHub releases for 94 minutes, delivering the GlassWorm loader](https://www.stepsecurity.io/blog/ovhcloud-cli-github-release-swap-glassworm)**
  _Why now: Live supply-chain incident: OVHcloud CLI release binaries swapped for 94 minutes to deliver GlassWorm; teaches release-asset verification and how to triage installs. · newsworthy · widely-reported · timely_
- **[Collabora Built-in CODE Server for Nextcloud: OS command injection in proxy.php exploited in the wild (CVE-2026-110447)](https://nvd.nist.gov/vuln/detail/CVE-2026-110447)**
  _Why now: CISA KEV with a three-day deadline: exploited command injection in Nextcloud's built-in Collabora CODE server; the fix and the restart-window condition are concrete. · active-exploitation · cve · timely_
- **[PHP2Shell: Wiz used frontier AI to turn memory-safety bugs in core PHP (two CVEs) into unauthenticated RCE on WordPress, Drupal and Joomla](https://www.wiz.io/blog/php2shell-php-rce)**
  _Why now: Core PHP RCE chain built with frontier AI; patched October 21 with broad vendor mitigations. · newsworthy · timely · week-of-2026-10-13_
- **[Microsoft: China-aligned Storm-0940 used the agentic ARTEX pentest framework to hit 2,250+ tenants after the ConnectWise supply-chain compromise](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/)**
  _Why now: Microsoft attributes machine-speed ConnectWise supply-chain follow-on attacks to an agentic pentest framework. · newsworthy · timely · week-of-2026-10-13_
- **[Unit 42: ransomware groups try PAN-OS CVE-2026-0257 to bypass GlobalProtect MFA, and one case pivoted to vCenter and ESXi](https://unit42.paloaltonetworks.com/active-exploitation-of-pan-os-cve-2026-0257/)**
  _Why now: Ransomware groups attempting a PAN-OS MFA bypass and pivoting to the hypervisor layer. · newsworthy · timely · week-of-2026-10-13_
- **[SOCRadar: INC and The Gentlemen ransomware affiliates ran intrusions through AI agents, and exposed their own servers](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/)**
  _Why now: Exposed ransomware-affiliate servers show AI-agent-run intrusions against edge devices. · newsworthy · timely · week-of-2026-10-13_
- **[CrowdStrike: four newly seen actors ran agentic Claude Code intrusions; guardrails only slowed the weakest](https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/)**
  _Why now: Four exposed agentic Claude Code intrusion harnesses documented by CrowdStrike. · newsworthy · timely · week-of-2026-10-13_
- **[NorForge: exposed Cairn AI-pentest panels show criminals and some red teams running autonomous break-ins with open dashboards](https://norforge.com/blog/inside_cairn)**
  _Why now: Exposed Cairn AI-pentest panels reveal attacker workflow and risk to legitimate red-team clients. · newsworthy · timely · week-of-2026-10-13_
- **[Wiz CIRT: what an AI-driven cloud intrusion looks like, from machine tempo to pentest-labelled artifacts](https://www.wiz.io/blog/anatomy-of-ai-driven-cloud-attacks)**
  _Why now: Field guide to observable traits of AI-driven cloud intrusions from real investigations. · newsworthy · timely · week-of-2026-10-13_
- **[Google: eight eMudhra intermediate CA keys had weak entropy, so Chrome blocked them within two hours and is removing the root](https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/)**
  _Why now: Weak-entropy CA keys blocked by Chrome within hours; root removal scheduled. · newsworthy · timely · week-of-2026-10-13_
- **[Two CVSS 9.0 Linux KSMBD RCE flaws, found by an AI scanner, reached public kernel lists with no patch](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html)**
  _Why now: Unpatched AI-found kernel RCEs reached public lists; process change worth knowing. · newsworthy · timely · week-of-2026-10-13_
- **[ANY.RUN: 1,258 sandbox analyses tie fake Claude, ChatGPT and Copilot tools to infostealers, session theft and account phishing](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/)**
  _Why now: Fake Claude and ChatGPT lures targeting developers, with detection angles. · newsworthy · timely · week-of-2026-10-13_
- **[GitLab critical patch: CVE-2026-110264, a CVSS 10.0 unauthenticated RCE in the regex compiler, in every release since 7.0](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/)**
  _Why now: Maximum-severity unauthenticated GitLab RCE across 12 years of releases; patch released. · newsworthy · timely · week-of-2026-10-13_
- **[Horizon3 deep dive on FortiSIEM CVE-2026-106173: an unauthenticated gRPC path traversal plus a null byte becomes arbitrary file write and RCE](https://horizon3.ai/attack-research/cve-2026-106173-deep-dive-fortisiem-grpc-path-traversal-file-write-rce/)**
  _Why now: Technical write-up of an unauthenticated FortiSIEM file-write RCE. · newsworthy · timely · week-of-2026-10-13_
- **[Arista VeloCloud Orchestrator CVE-2026-114625: SQL injection lets any logged-in user become superuser operator, exploited in the wild](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199)**
  _Why now: Vendor-confirmed active exploitation of an SD-WAN orchestrator flaw. · newsworthy · timely · week-of-2026-10-13_
- **[Pillow GHSA-w889-685w-c8fh: attacker-controlled filenames inject Ghostscript arguments in EPS handling, even with -dSAFER](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh)**
  _Why now: Argument injection in a ubiquitous Python imaging library bypasses -dSAFER. · newsworthy · timely · week-of-2026-10-13_
- **[Railway security disclosure: encrypted environment variables may have been accessed, all users told to roll secrets](https://blog.railway.com/p/security-disclosure-wednesday-october-21st)**
  _Why now: Hosting platform secrets exposure tied to attacks on AI inference providers; rotate keys. · newsworthy · timely · week-of-2026-10-13_
- **[Node2Shell: Imperva shows CVE-2026-111497, a Brotli decoder bug in Node.js, runs attacker code via fetch() and Express body parsing](https://www.imperva.com/blog/node2shell-from-brotli-data-to-remote-code-execution/)**
  _Why now: Node2Shell: Brotli decoder RCE in Node.js, validated against official builds and Express body parsing. · newsworthy · timely · week-of-2026-10-13_
- **[HPE bulletin HPESBNW05162: CVSS 10.0 unauthenticated RCE and auth bypass flaws across ArubaOS AOS-10 and AOS-8](https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbnw05162en_us&docLocale=en_US)**
  _Why now: Batch of CVSS 10.0 unauthenticated flaws in ArubaOS. · newsworthy · timely · week-of-2026-10-13_
- **[BeyondTrust advisory BT26-05: CVSS 9.3 improper origin validation in Remote Support lets a remote attacker perform file operations](https://www.beyondtrust.com/trust-center/security-advisories/bt26-05)**
  _Why now: Critical Remote Support advisory; self-hosted customers must patch manually. · newsworthy · timely · week-of-2026-10-13_
- **[Sentry's Next.js tunnelRoute skipped middleware for everything under the tunnel path, not just the requests its rewrite served (GHSA-mchm-gjx6-7h55)](https://github.com/advisories/GHSA-mchm-gjx6-7h55)**
  _Why now: Critical GHSA in a ubiquitous Next.js SDK with a transferable lesson: middleware exemptions are authz bypasses wherever middleware is the only authorization check. · cve · newsworthy · high-relevance · timely_
- **[CISA KEV: Plex Media Server encoded-URI-scheme flaw CVE-2026-96654 exploited in the wild, part of a four-CVE chain](https://nvd.nist.gov/vuln/detail/CVE-2026-96654)**
  _Why now: Exploited-in-the-wild Plex chain added to CISA KEV with a due date of today and a public plex2shell write-up; patch now. · active-exploitation · cve · timely_
- **[ESET: UAC-0099 used new MythicRatatoskr backdoor with C2 inside the Yggdrasil mesh network before Sandworm wiped a Ukrainian firm](https://thehackernews.com/2026/10/russian-linked-hackers-used-new-mesh.html)**
- **[Atlassian October 2026 bulletin: 75 unique third-party CVEs across Data Center and Server products](https://www.securityweek.com/atlassian-patches-75-third-party-flaws-in-data-center-and-server-products/)**
- **[Critical Pillow flaw: one crafted FlashPix file opened with Image.open() can run code](https://github.com/advisories/GHSA-5x8w-8jj5-q52h)**
- **[Echo proxy middleware: rejected WebSocket upgrades bypass route-level access controls](https://github.com/advisories/GHSA-cxf3-9h37-7rr8)**
- **[Laravel TokenGuard authentication bypass via non-string API credentials rated critical](https://github.com/advisories/GHSA-f9x3-7vq9-cph6)**
- **[Wasmtime Cranelift bit-packing overflow lets crafted Wasm module escape the sandbox](https://github.com/advisories/GHSA-897f-g5gm-fmxm)**
- **[Abandoned Time4Popcorn updater (CVE-2026-30612) allowed code execution on millions of PCs; researchers disabled it](https://www.bleepingcomputer.com/news/security/abandoned-popcorn-time-app-exposed-millions-of-device-to-rce-attacks/)**
- **[Pillow DoS: a 5.6 KB MIC file hangs n_frames at 100% CPU (GHSA-22hg-r758-rrw9)](https://github.com/advisories/GHSA-22hg-r758-rrw9)**
  _Why now: Fresh HIGH advisory in Pillow, which nearly every Python upload path uses; the fix pattern (formats allowlist, drop olefile, wall-clock timeouts) applies today. · cve · timely · high-relevance_
- **[DOMPurify SAFE_FOR_TEMPLATES bypass: split expressions survive inside attached shadow roots](https://github.com/advisories/GHSA-cg2g-xh64-v4q7)**
- **[Pillow multi-frame loaders reuse stale buffers, causing out-of-bounds writes and possible code execution](https://github.com/advisories/GHSA-v9pv-5gc8-w2m6)**
- **[Salesforce: AI finds vulnerabilities faster than engineers can fix them; cluster root causes and close exploit chains](https://www.salesforce.com/blog/managing-agentic-security-at-scale/)**
- **[OpenAI proposes coordinated disclosure framework after AI-found critical PHP flaws, offers PHP version checker](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities)**
- **[Pillow heap overflow when saving TIFF to BytesIO also leaks stale heap bytes](https://github.com/advisories/GHSA-332p-7hrc-92wf)**
- **[Belarus-aligned Partisan Zmiy hid Vasilek backdoor in VMware Tools for nearly two years in Russian healthcare network](https://thehackernews.com/2026/10/hackers-hid-vasilek-backdoor-in-vmware.html)**
- **[Pillow thumbnail() heap overflow on lossless JPEGs, found by Anthropic using Claude](https://github.com/advisories/GHSA-8g5g-8vmr-9782)**
- **[Eight eMudhra intermediate CA certificates with trivially weak private keys trigger global blocking](https://arstechnica.com/security/2026/10/the-internet-goes-on-high-alert-after-discovery-of-8-compromised-tls-certs/)**
- **[curl moves low and medium severity vulnerability reports to public GitHub from October 26](https://www.theregister.com/security/2026/10/20/swamped-curl-maintainers-take-low-level-flaws-public-to-survive-vulnerability-avalanche/5304198)**
- **[How we found 24 Android vulnerabilities using our open source AI security agent](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/)**
  _Why now: 24 real, disclosed Android vulnerabilities (OsmAnd location tracking, a WebView account-takeover chain) found with an open-source agent you can run today, plus candid lessons on LLM severity misjudgment and false positives. · newsworthy · trending · timely · high-relevance_
- **[Mercury analytics app: a missing comma lets anyone open a root shell via /api/terminals](https://github.com/advisories/GHSA-f8c7-rwf9-fmgm)**
- **[Mercury still exposed to unauthenticated code execution via /api/kernels after terminals fix](https://github.com/advisories/GHSA-rv4m-xm3f-3ccq)**
- **[UpGuard researcher uses OnlyFans copyright takedown data to find hacked university and government sites](https://www.darkreading.com/vulnerabilities-threats/onlyfans-copyright-takedowns-expose-compromised-websites)**
- **[OpenAI: Sophos MDR agents on OpenAI Daybreak cut average agent-handled case time from ~38 minutes to ~89 seconds, resolve 52% of cases (vendor claims)](https://openai.com/index/sophos)**
- **[Imperva: DDoS readiness checklist (BGP prefix advertisement, GRE tunnel health, per-PoP traffic floors), vendor product post](https://www.imperva.com/blog/ddos-readiness-is-your-ddos-protection-actually-on/)**
- **[Parser exhaustion: valid SQL crashes SQLGlot and SQLFluff (CVE-2026-46373, CVE-2026-46374) with ~750x memory amplification, taking down Superset SQL Lab, Dify plugins and Pathway](https://www.imperva.com/blog/the-hidden-dos-vector-in-sql-parsers/)**
- **[A Lean 4 string-slice mismatch between logical definition and native code let native_decide 'prove' Fermat's Last Theorem](https://blog.trailofbits.com/2026/09/09/a-proof-of-fermats-last-theorem-that-fits-the-margin/)**
- **[Trail of Bits Runs an Independent, From-Scratch Auditor for Signal's Key Transparency System](https://blog.trailofbits.com/2026/08/11/how-trail-of-bits-helps-verify-the-integrity-of-your-signal-chats/)**
- **[38.9% of agent-generated PRs carry a security smell - but humans introduce most of the real leaked secrets](https://arxiv.org/abs/2607.12428)**
  _Why now: Large-scale, widely-discussed finding on coding-agent risk with a concrete gate: automated secret + dependency-integrity scanning on agent PRs, because human review misses 81%. · trending · high-relevance · teachable_

| Domain | Findings |
| --- | --- |
| Application Security | 3 |
| AI in the SDLC | 3 |
| Vulnerability Research & Red Teaming | 1 |
| Mobile & Device Security | 1 |
| Detection, Response & Threat Intel | 1 |

## Application Security

- **[Atlassian CVE-2026-21589: pre-auth file read via '::' path traversal in atlassian-plugins-webresource (Jira, Confluence, Bitbucket and 5 more Data Center products), chained to Crowd admin](appsec/2026-10-atlassian-cve-2026-21589-pre-auth-file-read-via-path-travers.md)** · composite **64.34** · Oct 6, 2026  
  Patch every Atlassian Data Center product now; if you use Crowd, also rotate the Crowd application passwords and restrict Crowd by IP allowlist.  
  _[watchTowr Labs](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/)_
- **[watchTowr breaks PaperCut NG/MF patches three times: Tapestry `service` auth bypass (CVE-2026-81578, bypasses WT-2026-0142/0143) chained with RCE (CVE-2026-82078, WT-2026-0141, CVE-2026-82077 via Scan to Fax)](appsec/2026-10-watchtowr-breaks-papercut-ng-mf-patches-three-times-tapestry.md)** · composite **61.04** · Oct 9, 2026  
  When authorization is enforced per page instead of globally, patching individual pages invites repeated bypasses; PaperCut needed four patch rounds, and admins should be on 26.0.5 or later.  
  _[watchTowr Labs](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/)_
- **[SourceHut account takeover via OSC 8 hyperlink XSS in ansi2html-rendered build logs (CVE-2026-92973; ansi2html >=1.7.0,<1.9.4, builds.sr.ht >=0.40.0,<0.105.1)](appsec/2026-09-sourcehut-account-takeover-via-osc-8-hyperlink-xss-in-ansi2h.md)** · composite **47.0** · Sep 24, 2026  
  Treat CI log output as untrusted HTML input: sanitize the output of any ANSI-to-HTML converter and back it with a strict Content-Security-Policy, because one injected escape sequence can become…  
  _[@arusekk via Hacker News](https://blog.arusekk.pl/posts/srht-account-takeover/)_

## AI in the SDLC

- **[Claude found 493 attack-surface issues in 25 projects; OpenSSH made ML-DSA parsing unreachable before auth](ai-code/2026-10-claude-found-493-attack-surface-issues-in-25-projects-openss.md)** · composite **64.22** · Oct 20, 2026  
  Cutting pre-auth and default-reachable code lowers the severity of bugs you have not found, and an LLM can do this audit at scale.  
  _[Anthropic Research](https://www.anthropic.com/research/attack-surface-reduction)_
- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points across 123 libraries at the RISC-V binary level by turning fuzz harnesses into specs](ai-code/2026-10-claude-wrote-machine-checked-no-crash-proofs-for-239-oss-fuz.md)** · composite **59.75** · Oct 22, 2026  
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.  
  _[source](https://www.anthropic.com/research/formal-verification)_
- **[CheckerBench: 300 CVE-derived tasks (297 CVEs, 85 CWEs, 5 ecosystems) for agent-written static-analysis checkers; mean Pass@1 32.30%, best 45.33% across 21 model-harness setups](ai-code/2026-10-checkerbench-300-cve-derived-tasks-297-cves-85-cwes-5-ecosys.md)** · composite **50.54** · Oct 6, 2026  
  Agents can sometimes turn a CVE into a reusable checker, but more than half of attempts fail, so treat agent-written SAST rules as drafts to validate on vulnerable/fixed pairs before shipping them to…  
  _[Hugging Face Daily Papers](https://arxiv.org/abs/2610.07557)_

## Vulnerability Research & Red Teaming

- **[PwnEscape: pwn.ai used an LLM research harness to find a new Linux networking bug class that escapes KVM guests (CVE-2026-99999)](offensive/2026-10-pwnescape-pwn-ai-used-an-llm-research-harness-to-find-a-new.md)** · composite **60.5** · Oct 19, 2026  
  VM isolation depends on the kernel's networking code, so patch KVM hosts and sandbox providers.  
  _[source](https://pwn.ai/blog/pwnescape)_

## Mobile & Device Security

- **[Citizen Lab: AdFection, zero-click Candiru spyware delivered through targeted ads bought via Discover-Tech](mobile/2026-10-citizen-lab-adfection-zero-click-candiru-spyware-delivered-t.md)** · composite **53.0** · Oct 15, 2026  
  Real-time ad bidding can deliver zero-click spyware; ad vendors cut off the abuser only after Citizen Lab disclosed it.  
  _[source](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/)_

## Detection, Response & Threat Intel

- **[333 Tor exit relays hijacked with the Ebury backdoor to intercept SSH passwords and unencrypted mail](detection-response/2026-10-333-tor-exit-relays-hijacked-with-the-ebury-backdoor-to-inte.md)** · composite **49.25** · Oct 20, 2026  
  Never accept a changed SSH host key over Tor or any untrusted path; use key auth, and expect backdoored infrastructure hosts to be turned into traffic interceptors.  
  _[source](https://kaba.cx/posts/20261020_Tor/)_

---

[← Home](../README.md) · [Standing claims](../claims/product-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
