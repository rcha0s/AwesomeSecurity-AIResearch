# PostgreSQL fixes a 22-year-old type confusion bug that enables code execution

**Published:** Nov 13, 2026

> **Takeaway:** Any role that can create objects should be treated as a possible route to code on the database host until the server and its extensions are both upgraded.

## TL;DR

CVE-2026-6460 lets a database user who can create objects change a composite type's field while old values are still held elsewhere, so the server reads those values as the new type, which can lead to code running as the PostgreSQL operating system user. The release fixes 52 flaws in total. Full protection also needs every C-language extension rebuilt, and client tools such as pg_dump and pg_restore need updating too.

## Lessons

- The bug class: changing a type while old values of that type are still in use. The fix adds version checks so the server can spot a value that no longer matches its type. - _"A field's type can be changed while older values of that type are still held in other parts of the server."_
- Patching only the server is not enough. C extensions built against older releases still load but may stay vulnerable. - _"Full protection from this flaw also requires rebuilding any C-language extensions installed on the server."_
- The researcher adapted the exploit for managed PostgreSQL services. The writeup does not give each provider's patch status, so tenants should not assume they are safe. - _"The writeup does not give each service's current patch status."_
- Restoring from a backup is an attack surface too. A crafted archive can make pg_restore run code on the machine doing the restore. - _"A crafted archive can make pg_restore run code as the user running it."_

## Threat · Conditions · Mitigations

- **Threat:** A low-privileged database user who can create or modify objects triggers type confusion and runs code as the PostgreSQL operating system user.
- **Conditions:** Any server version before 18.7, 17.12, 16.16, 15.20 or 14.25, and an attacker with a login that can create objects. Whether default privileges are enough for full code execution is unconfirmed.
- **Mitigations:** Update the server, rebuild C extensions at the same time, and update client tools on every machine.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [The Hacker News](https://thehackernews.com/2026/11/postgresql-patches-52-flaws-including.html)  ·  **Retrieved:** 2026-11-14  
**Scores:** Newness 28 · Novelty 70 · Relevance 82 · Credibility 46 · **Composite 60** _(each 0-100)_  
**Tags:** `postgresql`, `type-confusion`, `rce`, `database-security`, `managed-databases`, `c-extensions`, `pg-restore`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: No PostgreSQL entry is on file. The closest general prior art is earlier database memory-safety and authenticated-RCE bugs.

_Source: [https://thehackernews.com/2026/11/postgresql-patches-52-flaws-including.html](https://thehackernews.com/2026/11/postgresql-patches-52-flaws-including.html)_  ·  [← back to index](../README.md)
