# Oh My Posh: a directory name runs commands, because the prompt re-renders the resolved path through a template engine whose funcmap has cmd

**Topic:** Product Security  ·  **Domain:** Developer Tooling & Template Injection  
**Source:** [GitHub Advisory Database](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq)  ·  **Published:** Jul 24, 2026  ·  **Retrieved:** 2026-07-26  
**Scores:** 🆕 Newness 11 · ✨ Novelty 62 · 🎯 Relevance 78 · 🏛️ Credibility 70 · **Composite 55.25**  
**Tags:** `template-injection`, `rce`, `developer-tooling`, `supply-chain`, `go`  
**Verification:** ✓ independently verified · closest prior art: Go text/template SSTI and template injection generally; shell prompt injection via malicious git branch names and PS1; ANSI-escape injection via filenames; repo contents attacking dev tooling (.vscode/, .gitattributes, hooks). The delta is the sink: the attacker-controlled data is a filesystem directory name re-fed to the engine, it fires under the shipped default configuration, and the trigger is passive navigation. Nearest pool entry: the Shescape shell-escaping advisories (different mechanism - escaping, not double evaluation).

> **Takeaway:** Anything that renders your prompt, status bar or editor title is executing attacker-controlled repository metadata - treat it as a parser, not decoration.

## TL;DR

_The gist, not every detail - read the [full source](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq) for the complete write-up._

Oh My Posh composes the displayed path from raw folder names and then passes the whole composed string back through Go text/template, whose function map exposes cmd. A directory named with a template expression therefore executes commands as you the moment the prompt renders - under the built-in default configuration and every path style. Clone a repo, extract an archive, mount a share; the next command after cd is the trigger.

## What to learn

- The root cause is double evaluation, and it is a general antipattern: never re-parse a string as a template after untrusted data has been interpolated into it. Render each config template against its own inputs and concatenate the already-rendered pieces with the literal untrusted values. - _"Oh My Posh re-renders the resolved path string, which contains the raw folder names taken from the filesystem, through the Go `text/template` engine. That engine's function map exposes a `cmd` function that runs arbitrary OS commands."_ ✅
- A template function map is an authorization decision. Any renderer that touches untrusted data should get a data-only funcmap; exposing cmd/readFile/stat/glob to a display path converts a formatting bug into RCE. - _"use a data-only function map (no `cmd`/`readFile`/`stat`/`glob`) for path resolution"_ ✅
- Note the delivery model - this is a developer-machine attack triggered by filesystem contents you merely navigated into, firing on the next prompt render rather than on executing anything. Payloads cannot contain a path separator, which the reporter argues is not a real barrier; only the Windows slash-free proof is shown with output. - _"Arbitrary command execution as the victim user, triggered by navigating into attacker-supplied directory content: a subdirectory in a cloned repository, an extracted archive, a network share, or a removable drive."_ ✅

## Threat · Conditions · Mitigations

- **Threat:** Arbitrary command execution as the developer, from cloning a repository or extracting an archive that contains a maliciously named directory.
- **Conditions:** Victim runs Oh My Posh (the built-in default configuration is affected, and every path style) and the shell enters the directory or any descendant.
- **Mitigations:** Upgrade Oh My Posh; do not re-parse composed paths as templates; restrict the template function map used for path resolution.

---

_Source: [https://github.com/advisories/GHSA-6xj8-qv9j-xcjq](https://github.com/advisories/GHSA-6xj8-qv9j-xcjq)_  ·  [← back to index](../README.md)
