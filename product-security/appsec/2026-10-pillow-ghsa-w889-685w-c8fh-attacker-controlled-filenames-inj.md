# Pillow GHSA-w889-685w-c8fh: attacker-controlled filenames inject Ghostscript arguments in EPS handling, even with -dSAFER

**Published:** Oct 23, 2026

> **Takeaway:** Take Ghostscript and EPS handling out of upload paths and watch for a patched Pillow release; the advisory lists only a suggested fix.

## TL;DR

The advisory reports that Pillow's EPS plugin builds the Ghostscript command line from the input file's name with no sanitization. A filename starting with '-' is read by Ghostscript as an option, and '@' triggers its argument-file syntax, so an attacker who controls the filename passed to Image.open can inject arguments that chain to command execution. Pillow's default -dSAFER does not stop it. The full command-execution chain also needs an attacker-controlled argument file. Tested on 12.3.0; the suggested fix is to normalize the path to an absolute path.

## Lessons

- The vulnerable step passes the file name to Ghostscript unsanitized. - _"A filename beginning with `-` is interpreted by Ghostscript as an option, giving command-line argument injection; chainable to RCE (see Impact)."_
- The default sandbox flag does not mitigate it. - _"it is not mitigated by Pillow's default -dSAFER setting."_
- The fix is to normalize the path so it can never parse as an option. - _"Normalize the filename to an absolute path before it is passed to Ghostscript"_

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [source](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh)  ·  **Retrieved:** 2026-10-24  
**Scores:** Newness 27 · Novelty 35 · Relevance 55 · Credibility 55 · **Composite 42** _(each 0-100)_  
**Tags:** `pillow`, `ghostscript`, `argument-injection`, `python`, `file-upload`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Argument injection into Ghostscript from image libraries is a known class (ImageMagick, Pillow's earlier EPS issues); this variant bypasses -dSAFER. Verifier: Ghostscript/ImageMagick delegate and option-injection issues (e.g., CVE-2018-16509, ImageTragick); Pillow EPS/Ghostscript CVE-2017-8291 class  
> ⚠️ _Pending review - auto-analyzed, not yet human-verified._

_Source: [https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh](https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh)_  ·  [← back to index](../README.md)
