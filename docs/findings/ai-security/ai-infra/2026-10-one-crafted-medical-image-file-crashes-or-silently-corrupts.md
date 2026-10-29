# One crafted medical image file crashes or silently corrupts MONAILabel inference

**Published:** Oct 27, 2026

> **Takeaway:** Machine learning pipelines that read numbers from uploaded files need explicit finiteness checks, because one NaN can corrupt medical output with no error.

## TL;DR

An unauthenticated attacker can upload a 132 KB medical image file (DICOM format) with NaN or infinity in fields such as PixelSpacing to MONAILabel's default web API. pydicom accepts those values in its default validation mode and MONAI builds its spatial transforms from them without checks. In the proof of concept every inference crashed with HTTP 500; the advisory warns that when the writer does not crash, wrong segmentation masks come back with HTTP 200. The file stays in the datastore, so later inference on it repeats the crash; the advisory points to MONAI release 1.6.1 and a fix commit.

## Lessons

- pydicom's value check only runs in a mode that is off by default, so NaN and infinity pass through. - _"The `is_valid_ds()` check only runs in RAISE validation mode, which is NOT the default."_
- The advisory warns of a silent outcome, a wrong medical result returned as a success, though its proof of concept only showed crashes. - _"If the output writer does not crash, the result is returned with HTTP 200 and zero warnings."_
- The poisoned file persists, so the attack repeats on every later request for that image. - _"The NaN DICOM persists in the datastore - any future inference on that image ID crashes the server again."_

## Threat · Conditions · Mitigations

- **Threat:** Denial of service and silent corruption of medical AI inference results from one unauthenticated upload.
- **Conditions:** A MONAILabel server with its default unauthenticated web API reachable over the network.
- **Mitigations:** Upgrade MONAI per the advisory, require authentication on the MONAILabel API, and validate that spatial metadata is finite before inference.

---

**Topic:** AI Security  ·  **Domain:** AI Infrastructure & Incident Response  
**Source:** [GitHub Advisory Database](https://github.com/advisories/GHSA-6hp3-vr39-rqw8)  ·  **Retrieved:** 2026-10-27  
**Scores:** Newness 20 · Novelty 35 · Relevance 65 · Credibility 70 · **Composite 46** _(each 0-100)_  
**Tags:** `medical-ai`, `input-validation`, `nan-injection`, `inference-integrity`, `monai`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: NaN and infinity injection into numeric parsers is a known input-validation bug class; using it to silently corrupt medical inference through a persistent datastore is the new angle.

_Source: [https://github.com/advisories/GHSA-6hp3-vr39-rqw8](https://github.com/advisories/GHSA-6hp3-vr39-rqw8)_  ·  [← back to index](../README.md)
