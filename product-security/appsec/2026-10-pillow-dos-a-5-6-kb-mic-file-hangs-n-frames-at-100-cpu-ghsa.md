# Pillow DoS: a 5.6 KB MIC file hangs n_frames at 100% CPU (GHSA-22hg-r758-rrw9)

**Published:** Oct 21, 2026

> **Takeaway:** Affects installs with olefile, back to Pillow 7.2.0. Parse untrusted images under a timeout and restrict Image.open to the formats you expect.

## TL;DR

A crafted 5.6 KB Microsoft Image Composer file makes Pillow loop forever at 100% CPU when code reads im.n_frames, on installs with the optional olefile package. MicImageFile overrides seek() and tell() but inherits TiffImageFile.n_frames, which relies on tell() advancing, so it re-parses the same directory endlessly. The hang raises no exception and grows no memory; the regression dates to Pillow 7.2.0 (2020).

## Lessons

- Exposure depends on an optional dependency: only installs with olefile register the MIC plugin. - _"This only affects installations that have the optional `olefile` package."_
- Root cause is a subclass that overrides the primitives an inherited method depends on; audit inherited methods when you change seek/tell semantics. - _"It does not override the `n_frames` property, so the inherited TIFF implementation runs"_
- Silent CPU hangs evade exception handlers and memory limits; untrusted parsing needs a wall-clock watchdog. - _"The call never returns, raises no exception, and does not grow memory, so only an external watchdog stops it."_
- The bug has shipped since Pillow 7.2.0. - _"first released in 7.2.0"_

## Threat · Conditions · Mitigations

- **Threat:** Denial of service: one crafted upload pins a worker at 100% CPU indefinitely.
- **Conditions:** olefile installed; the application opens an untrusted image and reads n_frames (e.g. is-animated checks, save_all re-saves).
- **Mitigations:** Upgrade Pillow when patched; restrict formats; remove olefile; enforce worker timeouts.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [source](https://github.com/advisories/GHSA-22hg-r758-rrw9)  ·  **Retrieved:** 2026-10-22  
**Scores:** Newness 27 · Novelty 30 · Relevance 45 · Credibility 70 · **Composite 40** _(each 0-100)_  
**Tags:** `dos`, `image-parsing`, `python`, `pillow`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Many prior Pillow decompression-bomb and parser-hang DoS advisories; the inherited-method/overridden-tell() root cause is a routine variation.  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://github.com/advisories/GHSA-22hg-r758-rrw9](https://github.com/advisories/GHSA-22hg-r758-rrw9)_  ·  [← back to index](../README.md)
