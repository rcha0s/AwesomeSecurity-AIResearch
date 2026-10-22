# Product Security

> Securing products: application security, supply chain, cloud & infra, identity, mobile, plus red teaming and threat modeling (AI-assisted or not).

_0 vetted findings · updated 2026-10-22 · ranked by composite · findings from the latest 31 days · [1 held for review](../REVIEW.md)._

## 📈 Trending & In the News

_Not new ideas - what the field is watching now, surfaced by the editorial pass._

- **[Pillow MIC images hang n_frames forever: an inherited method that depends on an overridden tell() (GHSA-22hg-r758-rrw9)](https://github.com/advisories/GHSA-22hg-r758-rrw9)**
  _Why now: Fresh HIGH advisory in Pillow, which nearly every Python upload path uses; the fix pattern (formats allowlist, drop olefile, wall-clock timeouts) applies today. · cve · timely · high-relevance_

| Domain | Findings |
| --- | --- |
| Application Security | 1 |

## Application Security

- **[Pillow MIC images hang n_frames forever: an inherited method that depends on an overridden tell() (GHSA-22hg-r758-rrw9)](appsec/2026-10-pillow-mic-images-hang-n-frames-forever-an-inherited-method.md)** · composite **40.75** · Oct 21, 2026 · ⚠️ _review_  
  Parse untrusted images under a timeout and restrict Image.open to the formats you expect.  
  _[source](https://github.com/advisories/GHSA-22hg-r758-rrw9)_

---

[← Home](../README.md) · [Standing claims](../claims/product-security.md) · [Newsletter](../NEWSLETTER.md) · [Trends](../TRENDS.md) · [Review queue](../REVIEW.md)
