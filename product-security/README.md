# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_10 vetted findings · updated 2026-10-29 · ranked by composite · findings from the latest 31 days · [39 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now: the editorial pass and the news gate. News is kept for good; findings are not._

- **[Oracle PeopleSoft zero-day used by ShinyHunters was three chained flaws](https://thehackernews.com/2026/10/shinyhunters-exploited-oracle.html)**
  _Why now: ShinyHunters has exploited this PeopleSoft chain since May. It teaches two things that transfer: a default loopback allowlist turns server-side request forgery into unauthenticated RCE, and path-matching WAF rules fall to a single… · active-exploitation · cve · newsworthy · high-relevance_
- **[InfraTrust report says network appliances wait on vendors for PHP2Shell fixes](https://www.bleepingcomputer.com/news/security/infratrust-report-warns-of-exploited-flaws-in-critical-network-infrastructure/)**
  _Why now: PHP2Shell is the theme of the week. This adds a lesson that changes what defenders do: appliances with PHP compiled into their firmware cannot be patched by customers, so pull their management interfaces off the internet now. · trending · active-exploitation · timely_
- **[Skimmers hijacked Convertr's self-hosted analytics script to steal checkout card data](https://www.bleepingcomputer.com/news/security/hackers-hijack-convertr-analytics-script-to-steal-payment-card-data/)**
  _Why now: A live Magecart incident in which one self-hosted analytics script skimmed every merchant's checkout. The lesson is concrete: treat every script loaded on checkout pages, analytics included, as payment-critical and check its integrity. · newsworthy · timely · high-relevance_
- **[Adobe patches eight critical flaws in Campaign Classic](https://thehackernews.com/2026/10/adobe-fixes-8-critical-campaign-classic.html)**
- **[Skyw4lker device code phishing campaign targets US manufacturing, tech and healthcare firms](https://thehackernews.com/2026/10/american-organizations-under-attack.html)**
- **[Volt Typhoon hides zero-day attacks behind rotating relays of hacked devices](https://www.bleepingcomputer.com/news/security/volt-typhoon-hides-zero-day-attacks-using-silent-train-framework/)**
- **[Authlib accepts a JSON web signature with no signatures as verified](https://github.com/advisories/GHSA-6v38-4h7w-rj9h)**
  _Why now: Critical authentication bypass in a widely used Python library; the fail-open empty-loop pattern is a test every verifier should have. · cve · timely · high-relevance_
- **[Wiz: Gheist used stolen GitHub tokens to dump secrets through Actions logs](https://www.darkreading.com/cyberattacks-data-breaches/gheist-stolen-github-tokens-cloud-secrets)**
  _Why now: Active campaign hitting private enterprise repos past GitHub's public-repo safeguard, with concrete hunt indicators and a token-lifetime fix. · active-exploitation · newsworthy · timely · high-relevance_
- **[Check Point: fake ChatGPT and Claude apps sideload malware via signed installers](https://research.checkpoint.com/2026/tricks-from-the-past-deployed-via-signed-chatgpt-and-claude-binaries/)**
  _Why now: Live campaign using fake ChatGPT and Claude desktop apps and signed vendor installers, with endpoint artifacts defenders can hunt. · active-exploitation · trending · timely_
- **[EDK2 network boot flaw lets attackers run code before Secure Boot](https://arstechnica.com/security/2026/10/code-execution-flaw-in-uefi-firmware-threatens-most-servers-on-planet-earth/)**
- **[Apple patches 286 flaws and backports exploited CoreGraphics fix to iOS 18](https://www.securityweek.com/ios-macos-27-2-patch-286-bugs-fix-for-exploited-flaw-backported-to-ios-18/)**
- **[Check Point uses OpenAI Daybreak to turn vulnerability research into signatures](https://openai.com/index/check-point-daybreak)**
- **[New unpatched PHP RCE (CVE-2026-115560) is separate from PHP2Shell](https://www.bleepingcomputer.com/news/security/php-shares-mitigation-for-new-and-unpatched-rce-vulnerability/)**
  _Why now: A third, still-unpatched PHP RCE (CVE-2026-115560) during the PHP2Shell week, with a one-line config mitigation every PHP operator can apply today. · newsworthy · cve · timely · high-relevance_
- **[PHP says Chainguard broke the PHP2Shell embargo with patched images](https://www.theregister.com/security/2026/10/22/php-blames-supply-chain-security-biz-chainguard-for-putting-huge-chunks-of-the-web-at-risk/5304611)**
  _Why now: The PHP2Shell embargo dispute shows how disclosure now breaks down (rumors, PoC video, early distributor binaries, AI rediscovery from a hint); a transferable lesson for patch planning. · trending · widely-reported · timely_
- **[The Hacker News weekly roundup leads with PHP2Shell exploitation attempts](https://thehackernews.com/2026/10/weekly-recap-this2shell-that2shell.html)**
- **[Trail of Bits: only Go and vcpkg verified every downloaded package](https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/)**
  _Why now: First cross-ecosystem test of package managers against a malicious registry; tells teams exactly which strict lockfile flags to turn on. · timely · high-relevance_
- **[Unit 42: CL-UNK-1211 hit government Linux servers with LLM-written payloads](https://unit42.paloaltonetworks.com/ai-campaign-targets-linux-infrastructure/)**
  _Why now: Live espionage campaign with LLM-written payloads and concrete Linux hunting leads (auto_prepend_file persistence, sudo-alias stealer). · newsworthy · trending · high-relevance_
- **[CISA KEV: exploited Fortinet CVE-2025-61624 lets read-write admins write or delete files](https://nvd.nist.gov/vuln/detail/CVE-2025-61624)**
  _Why now: Exploited in the wild per CISA KEV with a three-day deadline; Fortinet appliances are widely deployed and need patching now. · cve · active-exploitation · timely_
- **[tensorlake@0.5.144 npm worm spread from a hijacked admin account](https://safedep.io/tensorlake-npm-compromise-mini-shai-hulud)**
  _Why now: Live npm worm (two independent write-ups, SafeDep and StepSecurity) that published through the project's own trusted-publishing workflow and arms a home-directory wiper on token revocation: a concrete lesson that valid provenance doesn't… · newsworthy · widely-reported · active-exploitation · timely · high-relevance_
- **[Citrix NetScaler CVE-2026-88771 is a pre-auth command injection zero-day in default configuration](https://labs.watchtowr.com/oh-look-the-foot-gun-went-off-again-citrix-netscaler-preauth-command-injection-cve-2026-88771/)**
  _Why now: Pre-auth root command injection in NetScaler ADC/Gateway exploited as a zero-day in default configuration; concrete fixed builds, a sibling bug the upgrade alone doesn't fix, and log-hunting guidance. · cve · active-exploitation · timely · high-relevance_
- **[Google PageBreak finds 500+ XSS bugs with near-zero false positives](https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project)**
  _Why now: Google's production-scale numbers for AI web testing gated by non-AI exploit validators (500+ XSS, near-zero false positives, only 2 on its high-assurance frameworks) teach how to make agent-found bugs trustworthy. · trending · newsworthy · timely_
- **[F5 BIG-IP APM pre-auth heap overflow RCE (CVE-2026-94127) is exploited](https://labs.watchtowr.com/is-this-a-joke-in-the-auth-header-f5-big-ip-unauth-heap-overflow-to-rce-cve-2026-94127/)**
  _Why now: Pre-auth RCE in an internet-facing BIG-IP edge appliance, exploited in the wild; teaches emergency patching and minimal exposure for auth-path parsing on edge devices. · cve · active-exploitation · timely · high-relevance_
- **[JFrog Artifactory auth bypass chain exploited in the wild leaves persistent backdoors](https://www.wiz.io/blog/artifactory-under-attack-in-the-wild-exploitation-of-cve-2026-42016-cve-2026-4201)**
  _Why now: In-the-wild exploitation of a JFrog Artifactory auth-bypass chain leaving Groovy plugin backdoors; teaches what to hunt for on a core build-infrastructure system. · cve · active-exploitation · newsworthy_
- **[With ChatGPT, ITRES rebuilt two BruCON techniques whose source was never released](https://labs.itresit.es/2026/10/15/copycats-at-machine-speed-reproducing-frontier-windows-kernel-exploitation-research/)**
  _Why now: tl;dr sec-featured case of an LLM-assisted researcher rebuilding Windows kernel techniques from slides and a binary in about 24 hours; it changes how to weigh partial disclosure. · trending · newsworthy_
- **[OVHcloud CLI GitHub releases carried attacker binaries for 94 minutes, delivering GlassWorm](https://www.stepsecurity.io/blog/ovhcloud-cli-github-release-swap-glassworm)**
  _Why now: Live supply-chain incident: OVHcloud CLI release binaries swapped for 94 minutes to deliver GlassWorm; teaches release-asset verification and how to triage installs. · newsworthy · widely-reported · timely_
- **[Collabora CODE Server for Nextcloud command injection exploited in the wild (CVE-2026-110447)](https://nvd.nist.gov/vuln/detail/CVE-2026-110447)**
  _Why now: CISA KEV with a three-day deadline: exploited command injection in Nextcloud's built-in Collabora CODE server; the fix and the restart-window condition are concrete. · active-exploitation · cve · timely_
- **[Wiz turned PHP memory bugs into unauthenticated RCE on WordPress using AI](https://www.wiz.io/blog/php2shell-php-rce)**
  _Why now: Core PHP RCE chain built with frontier AI; patched October 21 with broad vendor mitigations. · newsworthy · timely · week-of-2026-10-13_
- **[Microsoft says Storm-0940 used the ARTEX pentest framework against 2,250+ tenants](https://www.microsoft.com/en-us/security/blog/2026/10/21/storm-0940-uses-artex-agentic-ai-connectwise-supply-chain-compromise/)**
  _Why now: Microsoft attributes machine-speed ConnectWise supply-chain follow-on attacks to an agentic pentest framework. · newsworthy · timely · week-of-2026-10-13_
- **[Unit 42: ransomware groups try PAN-OS CVE-2026-0257 to bypass GlobalProtect MFA](https://unit42.paloaltonetworks.com/active-exploitation-of-pan-os-cve-2026-0257/)**
  _Why now: Ransomware groups attempting a PAN-OS MFA bypass and pivoting to the hypervisor layer. · newsworthy · timely · week-of-2026-10-13_
- **[SOCRadar: INC and The Gentlemen ransomware affiliates ran intrusions through AI agents](https://socradar.io/blog/inc-gentlemen-ransomware-ai-infrastructure/)**
  _Why now: Exposed ransomware-affiliate servers show AI-agent-run intrusions against edge devices. · newsworthy · timely · week-of-2026-10-13_
- **[CrowdStrike: four newly seen actors ran agentic Claude Code intrusions](https://www.crowdstrike.com/en-us/blog/crowdstrike-uncovers-new-agentic-ai-campaigns/)**
  _Why now: Four exposed agentic Claude Code intrusion harnesses documented by CrowdStrike. · newsworthy · timely · week-of-2026-10-13_
- **[NorForge found exposed Cairn AI-pentest panels used by criminals and red teams](https://norforge.com/blog/inside_cairn)**
  _Why now: Exposed Cairn AI-pentest panels reveal attacker workflow and risk to legitimate red-team clients. · newsworthy · timely · week-of-2026-10-13_
- **[Wiz CIRT describes what an AI-driven cloud intrusion looks like](https://www.wiz.io/blog/anatomy-of-ai-driven-cloud-attacks)**
  _Why now: Field guide to observable traits of AI-driven cloud intrusions from real investigations. · newsworthy · timely · week-of-2026-10-13_
- **[Google: eight eMudhra CA keys had weak entropy and Chrome blocked them](https://blog.google/security/protecting-chrome-and-android-users-from-compromised-emudhra-intermediate-ca-certificates/)**
  _Why now: Weak-entropy CA keys blocked by Chrome within hours; root removal scheduled. · newsworthy · timely · week-of-2026-10-13_
- **[Two KSMBD RCE flaws hit public kernel lists with no patch](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html)**
  _Why now: Unpatched AI-found kernel RCEs reached public lists; process change worth knowing. · newsworthy · timely · week-of-2026-10-13_
- **[ANY.RUN ties 1,258 sandbox analyses to fake Claude, ChatGPT and Copilot](https://any.run/cybersecurity-blog/fake-ai-tools-us-companies/)**
  _Why now: Fake Claude and ChatGPT lures targeting developers, with detection angles. · newsworthy · timely · week-of-2026-10-13_
- **[GitLab patches CVE-2026-110264, a CVSS 10.0 unauthenticated RCE in the regex compiler](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-5-1-released/)**
  _Why now: Maximum-severity unauthenticated GitLab RCE across 12 years of releases; patch released. · newsworthy · timely · week-of-2026-10-13_
- **[Horizon3 shows FortiSIEM CVE-2026-106173 unauthenticated gRPC path traversal leads to RCE](https://horizon3.ai/attack-research/cve-2026-106173-deep-dive-fortisiem-grpc-path-traversal-file-write-rce/)**
  _Why now: Technical write-up of an unauthenticated FortiSIEM file-write RCE. · newsworthy · timely · week-of-2026-10-13_
- **[Arista VeloCloud Orchestrator SQL injection (CVE-2026-114625) is exploited in the wild](https://www.arista.com/en/support/advisories-notices/security-advisory/24838-security-advisory-0199)**
  _Why now: Vendor-confirmed active exploitation of an SD-WAN orchestrator flaw. · newsworthy · timely · week-of-2026-10-13_
- **[Pillow EPS handling lets attacker-controlled filenames inject Ghostscript arguments (GHSA-w889-685w-c8fh)](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh)**
  _Why now: Argument injection in a ubiquitous Python imaging library bypasses -dSAFER. · newsworthy · timely · week-of-2026-10-13_
- **[Railway says encrypted environment variables may have been accessed](https://blog.railway.com/p/security-disclosure-wednesday-october-21st)**
  _Why now: Hosting platform secrets exposure tied to attacks on AI inference providers; rotate keys. · newsworthy · timely · week-of-2026-10-13_
- **[Imperva shows a Node.js Brotli decoder bug (CVE-2026-111497) runs attacker code](https://www.imperva.com/blog/node2shell-from-brotli-data-to-remote-code-execution/)**
  _Why now: Node2Shell: Brotli decoder RCE in Node.js, validated against official builds and Express body parsing. · newsworthy · timely · week-of-2026-10-13_
- **[HPE bulletin HPESBNW05162 lists CVSS 10.0 unauthenticated RCE flaws in ArubaOS](https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbnw05162en_us&docLocale=en_US)**
  _Why now: Batch of CVSS 10.0 unauthenticated flaws in ArubaOS. · newsworthy · timely · week-of-2026-10-13_
- **[BeyondTrust Remote Support flaw lets a remote attacker perform file operations](https://www.beyondtrust.com/trust-center/security-advisories/bt26-05)**
  _Why now: Critical Remote Support advisory; self-hosted customers must patch manually. · newsworthy · timely · week-of-2026-10-13_
- **[Sentry's tunnelRoute skipped middleware for the whole tunnel path, not just rewrites](https://github.com/advisories/GHSA-mchm-gjx6-7h55)**
  _Why now: Critical GHSA in a ubiquitous Next.js SDK with a transferable lesson: middleware exemptions are authz bypasses wherever middleware is the only authorization check. · cve · newsworthy · high-relevance · timely_
- **[CISA KEV: Plex Media Server CVE-2026-96654 is exploited in the wild](https://nvd.nist.gov/vuln/detail/CVE-2026-96654)**
  _Why now: Exploited-in-the-wild Plex chain added to CISA KEV with a due date of today and a public plex2shell write-up; patch now. · active-exploitation · cve · timely_
- **[ESET: UAC-0099 used MythicRatatoskr with C2 inside Yggdrasil before Sandworm struck](https://thehackernews.com/2026/10/russian-linked-hackers-used-new-mesh.html)**
- **[Atlassian October 2026 bulletin lists 75 unique third-party CVEs](https://www.securityweek.com/atlassian-patches-75-third-party-flaws-in-data-center-and-server-products/)**
- **[Critical Pillow flaw lets one crafted FlashPix file run code](https://github.com/advisories/GHSA-5x8w-8jj5-q52h)**
- **[Abandoned Time4Popcorn updater allowed code execution on millions of PCs](https://www.bleepingcomputer.com/news/security/abandoned-popcorn-time-app-exposed-millions-of-device-to-rce-attacks/)**
- **[Pillow DoS: a 5.6 KB MIC file hangs n_frames](https://github.com/advisories/GHSA-22hg-r758-rrw9)**
  _Why now: Fresh HIGH advisory in Pillow, which nearly every Python upload path uses; the fix pattern (formats allowlist, drop olefile, wall-clock timeouts) applies today. · cve · timely · high-relevance_
- **[Wired: AWS logged PHP2Shell exploitation attempts days before the patch](https://www.wired.com/story/hackers-exploited-the-php-vulnerabilities-days-before-they-were-patched/)**
- **[Pillow multi-frame loaders reuse stale buffers, causing out-of-bounds writes](https://github.com/advisories/GHSA-v9pv-5gc8-w2m6)**
- **[Salesforce says AI finds vulnerabilities faster than engineers can fix them](https://www.salesforce.com/blog/managing-agentic-security-at-scale/)**
- **[Cloudflare pairs Daybreak findings with live traffic to draft WAF rules](https://openai.com/index/cloudflare-cyber)**
- **[OpenAI proposes a coordinated disclosure framework after AI-found PHP flaws](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities)**
- **[Pillow heap overflow saving TIFF to BytesIO also leaks stale heap bytes](https://github.com/advisories/GHSA-332p-7hrc-92wf)**
- **[Partisan Zmiy hid the Vasilek backdoor in VMware Tools for two years](https://thehackernews.com/2026/10/hackers-hid-vasilek-backdoor-in-vmware.html)**
- **[PHP Foundation ships emergency fix for two critical remote code execution bugs](https://www.theregister.com/security/2026/10/21/php-devs-publish-critical-bug-fix-as-site-owners-warned-pull-em-offline-if-youre-unpatched/5304519)**
- **[PHP Foundation ships fixes for two RCE flaws after a disclosure leak](https://simonwillison.net/2026/Oct/21/php-security-release/)**
- **[Pillow thumbnail() heap overflow on lossless JPEGs, found by Anthropic using Claude](https://github.com/advisories/GHSA-8g5g-8vmr-9782)**
- **[Eight eMudhra intermediate CA certificates with weak private keys get blocked globally](https://arstechnica.com/security/2026/10/the-internet-goes-on-high-alert-after-discovery-of-8-compromised-tls-certs/)**
- **[curl moves low and medium severity vulnerability reports to public GitHub](https://www.theregister.com/security/2026/10/20/swamped-curl-maintainers-take-low-level-flaws-public-to-survive-vulnerability-avalanche/5304198)**
- **[GitHub Security Lab found 24 Android vulnerabilities with its AI agent](https://github.blog/security/how-we-found-24-android-vulnerabilities-using-our-open-source-ai-security-agent/)**
  _Why now: 24 real, disclosed Android vulnerabilities (OsmAnd location tracking, a WebView account-takeover chain) found with an open-source agent you can run today, plus candid lessons on LLM severity misjudgment and false positives. · newsworthy · trending · timely · high-relevance_
- **[UpGuard uses OnlyFans takedown data to find hacked university and government sites](https://www.darkreading.com/vulnerabilities-threats/onlyfans-copyright-takedowns-expose-compromised-websites)**
- **[OpenAI says Sophos MDR agents cut average case time to ~89 seconds](https://openai.com/index/sophos)**
- **[Imperva publishes a DDoS readiness checklist covering BGP and GRE tunnel health](https://www.imperva.com/blog/ddos-readiness-is-your-ddos-protection-actually-on/)**
- **[Valid SQL crashes SQLGlot and SQLFluff with huge memory amplification](https://www.imperva.com/blog/the-hidden-dos-vector-in-sql-parsers/)**
- **[A Lean 4 string-slice mismatch let native_decide 'prove' Fermat's Last Theorem](https://blog.trailofbits.com/2026/09/09/a-proof-of-fermats-last-theorem-that-fits-the-margin/)**
- **[Trail of Bits runs an independent auditor for Signal's Key Transparency system](https://blog.trailofbits.com/2026/08/11/how-trail-of-bits-helps-verify-the-integrity-of-your-signal-chats/)**
- **[38.9% of agent-generated PRs carry a security smell](https://arxiv.org/abs/2607.12428)**
  _Why now: Large-scale, widely-discussed finding on coding-agent risk with a concrete gate: automated secret + dependency-integrity scanning on agent PRs, because human review misses 81%. · trending · high-relevance · teachable_

| Domain | Findings |
| --- | --- |
| Application Security | 3 |
| AI in the SDLC | 3 |
| Vulnerability Research & Red Teaming | 2 |
| Mobile & Device Security | 1 |
| Detection, Response & Threat Intel | 1 |

## Application Security

- **[Atlassian CVE-2026-21589 is a pre-auth file read in Data Center products](appsec/2026-10-atlassian-cve-2026-21589-is-a-pre-auth-file-read-in-data-cen.md)** · composite **63.09** · Oct 6, 2026  
  Patch every Atlassian Data Center product now; if you use Crowd, also rotate the Crowd application passwords and restrict Crowd by IP allowlist.  
  _[watchTowr Labs](https://labs.watchtowr.com/you-wont-hear-about-these-even-in-myths-atlassian-jira-confluence-and-more-pre-auth-arbitrary-file-read-cve-2026-21589/)_
- **[watchTowr breaks PaperCut NG/MF patches again with an auth bypass plus RCE](appsec/2026-10-watchtowr-breaks-papercut-ng-mf-patches-again-with-an-auth-b.md)** · composite **59.79** · Oct 9, 2026  
  When authorization is enforced per page instead of globally, patching individual pages invites repeated bypasses; PaperCut needed four patch rounds, and admins should be on 26.0.5 or later.  
  _[watchTowr Labs](https://labs.watchtowr.com/death-by-a-thousand-papercuts-papercut-pre-auth-rce-chain-and-patch-bypasses-wt-2026-0141-0144-cve-2026-82077-cve-2026-82078-cve-2026-81578/)_
- **[PortSwigger's Gareth Heyes bypassed six of eight popular vector-image sanitizers](appsec/2026-10-portswigger-s-gareth-heyes-bypassed-six-of-eight-popular-vec.md)** · composite **57.13** · Oct 27, 2026  
  If you accept SVG uploads, sanitize with DOMPurify or darylldoyle/svg-sanitizer, serve user files from a separate origin, and never let users influence response headers.  
  _[PortSwigger Research](https://portswigger.net/research/scalable-vector-grief)_

## AI in the SDLC

- **[Claude found 493 attack-surface issues across 25 open-source projects](ai-code/2026-10-claude-found-493-attack-surface-issues-across-25-open-source.md)** · composite **62.97** · Oct 20, 2026  
  Cutting pre-auth and default-reachable code lowers the severity of bugs you have not found, and an LLM can do this audit at scale.  
  _[Anthropic Research](https://www.anthropic.com/research/attack-surface-reduction)_
- **[Claude wrote machine-checked no-crash proofs for 239 OSS-Fuzz entry points](ai-code/2026-10-claude-wrote-machine-checked-no-crash-proofs-for-239-oss-fuz.md)** · composite **58.5** · Oct 22, 2026  
  If you maintain C/C++ with fuzz harnesses, those harnesses are now candidate proof specs: an LLM plus a proof checker can turn 'fuzzed a lot' into 'proved no crash' for the covered scope.  
  _[source](https://www.anthropic.com/research/formal-verification)_
- **[CheckerBench gives agents 300 CVE-derived tasks to write static-analysis checkers](ai-code/2026-10-checkerbench-gives-agents-300-cve-derived-tasks-to-write-sta.md)** · composite **49.29** · Oct 6, 2026  
  Agents can sometimes turn a CVE into a reusable checker, but more than half of attempts fail, so treat agent-written SAST rules as drafts to validate on vulnerable/fixed pairs before shipping them to…  
  _[Hugging Face Daily Papers](https://arxiv.org/abs/2610.07557)_

## Vulnerability Research & Red Teaming

- **[Anthropic's unreleased model built five attack chains against major software](offensive/2026-10-anthropic-s-unreleased-model-built-five-attack-chains-agains.md)** · composite **64.39** · Oct 27, 2026 · 🔗 +1 sources  
  Frontier models now build working multi-bug exploit chains against hardened targets with little human help, so defenders need to scan their own code at scale and at PR time.  
  _[Anthropic Research](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)_
- **[pwn.ai found a new Linux networking bug class escaping KVM guests](offensive/2026-10-pwn-ai-found-a-new-linux-networking-bug-class-escaping-kvm-g.md)** · composite **59.25** · Oct 19, 2026  
  VM isolation depends on the kernel's networking code, so patch KVM hosts and sandbox providers.  
  _[source](https://pwn.ai/blog/pwnescape)_

## Mobile & Device Security

- **[Citizen Lab: Candiru spyware reached Al Jazeera devices through targeted ads](mobile/2026-10-citizen-lab-candiru-spyware-reached-al-jazeera-devices-throu.md)** · composite **53.25** · Oct 15, 2026  
  Real-time ad bidding can deliver zero-click spyware; ad vendors cut off the abuser only after Citizen Lab disclosed it.  
  _[source](https://citizenlab.ca/research/how-discover-tech-turned-targeted-ads-into-a-pipeline-for-spyware/)_

## Detection, Response & Threat Intel

- **[333 Tor exit relays hijacked with the Ebury backdoor to intercept SSH](detection-response/2026-10-333-tor-exit-relays-hijacked-with-the-ebury-backdoor-to-inte.md)** · composite **48.0** · Oct 20, 2026  
  Never accept a changed SSH host key over Tor or any untrusted path; use key auth, and expect backdoored infrastructure hosts to be turned into traffic interceptors.  
  _[source](https://kaba.cx/posts/20261020_Tor/)_

---

[← Home](../README.md) · [Standing claims](../claims/product-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
