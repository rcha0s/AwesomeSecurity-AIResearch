# Valid SQL crashes SQLGlot and SQLFluff with huge memory amplification

**Published:** Oct 6, 2026

> **Takeaway:** Treat any parser that consumes user or LLM-generated text as a trust boundary: cap bytes, depth and node count before parsing, and upgrade SQLGlot/SQLFluff to versions with limits.

## TL;DR

SQLGlot and SQLFluff parse deeply nested or very wide but syntactically valid SQL with no depth or node limit: about 50 nesting levels hits Python's recursion limit, and a sub-2MB query builds an abstract syntax tree (AST) using over 1.5GB of RAM. Because apps parse before executing, one authenticated Superset SQL Lab user can kill or pin the shared worker pool, a Dify plugin query broke the daemon-to-worker bridge for about 60 seconds, and Pathway was OOM-killed at 8GB+. The same flaw shows up in Neo4j Cypher, graphql-js and graphql-core.

## Lessons

- Recursive-descent parsers without a depth cap fail on modest nesting. - _"At 50+ levels of nesting, the recursive descent parser exhausts the call stack."_
- The DoS fires in the pre-execution parse step, so database-side limits and query timeouts don't help. - _"An authenticated user with ordinary SQL Lab access is enough; the query never has to run."_
- Client-side input limits are not a control; enforce size caps on the server. - _"The frontend enforces a 3,000-character input limit. The backend does not."_
- The bug class is generic to parsers that build rich object trees, not specific to SQL. - _"Any parser that turns untrusted text into a rich object tree without bounding depth or node count is exposed."_

## Threat · Conditions · Mitigations

- **Threat:** An authenticated low-privilege user (or anyone reaching an exposed parse endpoint) sends a valid but deeply nested or very wide query that exhausts memory or CPU in the parser, crashing or hanging shared workers.
- **Conditions:** Application passes untrusted or LLM-generated SQL to unpatched SQLGlot or SQLFluff (or graphql-js/graphql-core/Cypher without limits) with no server-side size or depth cap.
- **Mitigations:** Upgrade parsers and keep recursion/node limits enabled; server-side byte/token/depth/column caps before parsing; parse timeouts; container memory limits; rate limiting; isolate plugin processes.

---

**Topic:** Product Security  ·  **Domain:** Application Security  
**Source:** [Imperva Threat Research](https://www.imperva.com/blog/the-hidden-dos-vector-in-sql-parsers/)  ·  **Retrieved:** 2026-10-25  
**Scores:** Newness 5 · Novelty 55 · Relevance 70 · Credibility 72 · **Composite 50** _(each 0-100)_  
**Tags:** `denial-of-service`, `parser`, `sqlglot`, `sqlfluff`, `apache-superset`, `dify`, `graphql`, `resource-exhaustion`, `cve-2026-46373`, `cve-2026-46374`  
**Source-checked (automated):** the lesson quotes were found in the source and a second model pass did not refute them (not human review) · closest prior art: Classic algorithmic-complexity and deep-nesting DoS (billion laughs, JSON/YAML nesting bombs, GraphQL depth/complexity limits, Imperva's own graphql-java DoS write-up). New here: CVEs in the two main Python SQL parsers, measured amplification ratios, and concrete cascades into Superset, Dify and Pathway.

_Source: [https://www.imperva.com/blog/the-hidden-dos-vector-in-sql-parsers/](https://www.imperva.com/blog/the-hidden-dos-vector-in-sql-parsers/)_  ·  [← back to index](../README.md)
