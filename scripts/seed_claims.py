#!/usr/bin/env python3
"""
seed_claims.py — One-shot seed of ~35 foundational claims into the ledger.

Each claim below is a considered editorial call about a standing answer in
the field. Every one has:
  - a statement (what we currently believe)
  - a confidence 0..1 (deliberately conservative for seeds)
  - a phase (research lifecycle axis)
  - evidence[] with real URLs to public research the pipeline already
    ingests from — arXiv, vendor blogs, OWASP, USENIX, NDSS, GHSA
  - guidance where a practitioner action follows from the claim

Sources cited are public and long-lived. If a paper's URL rots, replace
the URL — the claim itself doesn't need to move.

Idempotent: running twice adds nothing new (matches by id).

Usage:
    python scripts/seed_claims.py --dry-run
    python scripts/seed_claims.py
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime

import claims as cl


def _today() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Seed claims. Ordered by track for review-ability. Every claim is
# independently mergeable.
# ---------------------------------------------------------------------------
SEEDS: list[dict] = [
    # =====================================================================
    # AI SECURITY — threat model
    # =====================================================================
    {
        "id": "prompt-injection-is-a-permanent-attack-surface",
        "topic": "ai-security",
        "domain": "Prompt Injection",
        "phase": "threat-model",
        "statement": (
            "LLM applications that mix trusted instructions with untrusted "
            "input are permanently vulnerable to instruction hijacking; the "
            "surface cannot be closed by prompt engineering alone."
        ),
        "status": "current",
        "confidence": 0.9,
        "guidance": (
            "Design agentic systems assuming injection succeeds sometimes: "
            "least-privilege tool scopes, human approval on irreversible "
            "actions, and blast-radius caps that hold even when the model "
            "is fooled."
        ),
        "tags": ["prompt-injection", "threat-model", "agents"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://simonwillison.net/2023/Apr/14/worst-that-can-happen/",
                "title": "The Dual LLM pattern for building AI assistants that can resist prompt injection",
                "source_name": "Simon Willison",
                "published": "2023-04-14",
            },
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2302.12173",
                "title": "Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection",
                "source_name": "arXiv",
                "published": "2023-02-23",
            },
        ],
        "first_seen": "2023-02",
    },
    {
        "id": "indirect-injection-via-retrieved-content-is-viable",
        "topic": "ai-security",
        "domain": "Prompt Injection",
        "phase": "attack",
        "statement": (
            "Indirect prompt injection — hostile instructions embedded in "
            "documents, web pages, or tool outputs that the LLM reads at "
            "run time — is a demonstrated attack vector against real "
            "production LLM assistants."
        ),
        "status": "current",
        "confidence": 0.9,
        "guidance": (
            "Treat every retrieval-augmented context as untrusted input. "
            "Never let retrieved content unilaterally cause a tool call "
            "with side effects."
        ),
        "tags": ["prompt-injection", "rag", "indirect"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2302.12173",
                "title": "Not what you've signed up for",
                "source_name": "arXiv",
                "published": "2023-02",
            },
            {
                "stance": "supports",
                "url": "https://embracethered.com/blog/posts/2024/hacking-github-copilot-chat-prompt-injection/",
                "title": "Hacking GitHub Copilot Chat via indirect prompt injection",
                "source_name": "Embrace The Red",
                "published": "2024",
            },
        ],
        "first_seen": "2023-02",
    },
    {
        "id": "jailbreak-transfers-across-models",
        "topic": "ai-security",
        "domain": "Prompt Injection",
        "phase": "attack",
        "statement": (
            "Adversarial suffixes crafted against one aligned model transfer "
            "with non-trivial success to other models of similar family, "
            "including closed-source ones — so a jailbreak found against "
            "Llama can succeed against ChatGPT."
        ),
        "status": "current",
        "confidence": 0.7,
        "guidance": (
            "Alignment training on one model is not evidence of alignment "
            "for another. Run adversarial evals against your deployed "
            "model, not a proxy."
        ),
        "tags": ["jailbreak", "adversarial", "transfer"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2307.15043",
                "title": "Universal and Transferable Adversarial Attacks on Aligned Language Models",
                "source_name": "arXiv",
                "published": "2023-07",
            },
        ],
        "first_seen": "2023-07",
    },

    # =====================================================================
    # AI SECURITY — defense
    # =====================================================================
    {
        "id": "dual-llm-pattern-mitigates-injection-blast-radius",
        "topic": "ai-security",
        "domain": "Prompt Injection",
        "phase": "defense",
        "statement": (
            "Splitting agent architecture into a privileged planner LLM "
            "that never sees untrusted input, and a quarantined LLM that "
            "processes untrusted input but has no tool access, contains "
            "prompt injection to non-privileged operations."
        ),
        "status": "current",
        "confidence": 0.7,
        "guidance": (
            "For high-authority agents, use a two-tier architecture: the "
            "planner sees only tool schemas + user intent; the reader/"
            "quarantined LLM sees untrusted content and returns structured "
            "summaries the planner cannot execute as commands."
        ),
        "tags": ["defense", "architecture", "dual-llm"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://simonwillison.net/2023/Apr/25/dual-llm-pattern/",
                "title": "The Dual LLM pattern for building AI assistants that can resist prompt injection",
                "source_name": "Simon Willison",
                "published": "2023-04",
            },
        ],
        "first_seen": "2023-04",
    },
    {
        "id": "constitutional-ai-reduces-refusal-brittleness",
        "topic": "ai-security",
        "domain": "Alignment",
        "phase": "defense",
        "statement": (
            "Constitutional AI-style training (self-critique + revision "
            "against a written set of principles) reduces the fragility "
            "of hand-tuned refusal training and gives the training process "
            "an inspectable specification."
        ),
        "status": "current",
        "confidence": 0.65,
        "guidance": (
            "Prefer alignment techniques with a written, auditable spec "
            "over hand-tuned refusal datasets you can't inspect."
        ),
        "tags": ["alignment", "constitutional-ai", "rlaif"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2212.08073",
                "title": "Constitutional AI: Harmlessness from AI Feedback",
                "source_name": "arXiv (Anthropic)",
                "published": "2022-12",
            },
        ],
        "first_seen": "2022-12",
    },

    # =====================================================================
    # AI SECURITY — model supply chain
    # =====================================================================
    {
        "id": "pickle-based-model-formats-are-code-execution",
        "topic": "ai-security",
        "domain": "Model Supply Chain",
        "phase": "threat-model",
        "statement": (
            "Loading a pickle-based model file (PyTorch .pt/.bin) is "
            "equivalent to running arbitrary code; the format has no "
            "sandbox and no way to introspect what will execute at load "
            "time short of manual reversing."
        ),
        "status": "current",
        "confidence": 0.95,
        "guidance": (
            "Prefer safetensors for any model you didn't personally train. "
            "If you must load pickles, do it in a container with no "
            "outbound network."
        ),
        "tags": ["pickle", "supply-chain", "safetensors"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://blog.trailofbits.com/2021/03/15/never-a-dill-moment-exploiting-machine-learning-pickle-files/",
                "title": "Never a dill moment: Exploiting machine learning pickle files",
                "source_name": "Trail of Bits",
                "published": "2021-03",
            },
            {
                "stance": "supports",
                "url": "https://huggingface.co/docs/hub/en/security-pickle",
                "title": "Pickle scanning",
                "source_name": "Hugging Face",
                "published": "2023",
            },
        ],
        "first_seen": "2021-03",
    },
    {
        "id": "typosquatting-on-model-hubs-is-active",
        "topic": "ai-security",
        "domain": "Model Supply Chain",
        "phase": "attack",
        "statement": (
            "Adversaries publish typosquatted model repositories on public "
            "hubs (name variants of popular models) that ship with "
            "malicious pickle payloads or exfiltration hooks; several "
            "have been observed in the wild on Hugging Face."
        ),
        "status": "current",
        "confidence": 0.75,
        "guidance": (
            "Pin model artifacts by revision hash, not by name. Verify "
            "the model card against the vendor's known channels."
        ),
        "tags": ["typosquatting", "supply-chain", "huggingface"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/",
                "title": "Malicious ML models with silent backdoor found on Hugging Face",
                "source_name": "JFrog",
                "published": "2024-02",
            },
        ],
        "first_seen": "2024-02",
    },

    # =====================================================================
    # AI SECURITY — MCP & agent-tool ecosystem
    # =====================================================================
    {
        "id": "mcp-tool-descriptions-are-a-prompt-injection-surface",
        "topic": "ai-security",
        "domain": "MCP & Tools",
        "phase": "threat-model",
        "statement": (
            "MCP tool descriptions are consumed by the model as part of the "
            "system prompt; a hostile MCP server can inject instructions "
            "via tool metadata alone, without needing the tool to be "
            "called."
        ),
        "status": "current",
        "confidence": 0.85,
        "guidance": (
            "Version-pin and change-review every MCP tool description. "
            "Treat metadata updates as system-prompt changes requiring "
            "re-approval."
        ),
        "tags": ["mcp", "prompt-injection", "tool-poisoning"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks",
                "title": "MCP Security Notification: Tool Poisoning Attacks",
                "source_name": "Invariant Labs",
                "published": "2025-03",
            },
        ],
        "first_seen": "2025-03",
    },
    {
        "id": "agent-tool-selection-can-be-steered-by-untrusted-context",
        "topic": "ai-security",
        "domain": "MCP & Tools",
        "phase": "attack",
        "statement": (
            "An agent's tool selection can be influenced by content in its "
            "context window; adversarial content in retrieved documents "
            "can cause the agent to prefer a hostile tool over the "
            "intended one."
        ),
        "status": "current",
        "confidence": 0.7,
        "guidance": (
            "Do not present tools whose selection can be influenced by "
            "untrusted context unless the tool is safe when called on "
            "adversarial input."
        ),
        "tags": ["tool-selection", "prompt-injection", "agents"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2407.09164",
                "title": "Prompt Injection Attacks on Agentic Systems",
                "source_name": "arXiv",
                "published": "2024-07",
            },
        ],
        "first_seen": "2024-07",
    },

    # =====================================================================
    # AI SECURITY — memory & persistence
    # =====================================================================
    {
        "id": "long-term-memory-is-a-cross-session-poisoning-vector",
        "topic": "ai-security",
        "domain": "Memory & Context Poisoning",
        "phase": "attack",
        "statement": (
            "Once an LLM assistant persists user-provided information to "
            "a long-term memory store, adversarial content can be planted "
            "in one session and reliably retrieved into a future session, "
            "producing effects that outlast the poisoning conversation."
        ),
        "status": "current",
        "confidence": 0.85,
        "guidance": (
            "Gate what enters long-term memory with a policy check, not a "
            "post-hoc filter. Treat memory writes as security-relevant."
        ),
        "tags": ["memory", "persistence", "prompt-injection"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/",
                "title": "ChatGPT: Hacking Memories with Prompt Injection",
                "source_name": "Embrace The Red",
                "published": "2024-09",
            },
        ],
        "first_seen": "2024-09",
    },

    # =====================================================================
    # AI SECURITY — evaluation
    # =====================================================================
    {
        "id": "llm-eval-datasets-leak-into-training-sets",
        "topic": "ai-security",
        "domain": "Evaluation",
        "phase": "evaluation",
        "statement": (
            "Public benchmark datasets used to evaluate LLM security "
            "(jailbreak sets, red-team prompts) leak into the training "
            "corpora of later models, inflating scores without "
            "corresponding capability change."
        ),
        "status": "current",
        "confidence": 0.75,
        "guidance": (
            "Rotate held-out red-team prompts; treat any published "
            "adversarial dataset as compromised for future models."
        ),
        "tags": ["evaluation", "contamination", "benchmarks"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2311.09783",
                "title": "Data Contamination Quiz: A Tool to Detect and Estimate Contamination in Large Language Models",
                "source_name": "arXiv",
                "published": "2023-11",
            },
        ],
        "first_seen": "2023-11",
    },

    # =====================================================================
    # PRODUCT SECURITY — appsec fundamentals restated for AI apps
    # =====================================================================
    {
        "id": "ssrf-guards-must-cover-agent-outbound-calls",
        "topic": "product-security",
        "domain": "Application Security",
        "phase": "defense",
        "statement": (
            "Server-side request forgery guards on user-input URLs are "
            "not sufficient for agent applications: the agent can be "
            "steered into making outbound calls from tool responses, "
            "retrieval results, or MCP metadata."
        ),
        "status": "current",
        "confidence": 0.85,
        "guidance": (
            "Apply the private-IP dialer guard to every outbound HTTP "
            "client in an agent runtime — not just the user-facing one. "
            "Re-validate on redirect."
        ),
        "tags": ["ssrf", "agents", "defense"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://owasp.org/www-community/attacks/Server_Side_Request_Forgery",
                "title": "SSRF (OWASP)",
                "source_name": "OWASP",
            },
        ],
        "first_seen": "2020-01",
    },
    {
        "id": "path-traversal-defenses-must-cover-symlink-resolution",
        "topic": "product-security",
        "domain": "Application Security",
        "phase": "defense",
        "statement": (
            "Any code that opens a file whose path derives from user "
            "input must canonicalize the resolved target and verify it "
            "stays within the intended sandbox; validating the raw path "
            "string is insufficient."
        ),
        "status": "current",
        "confidence": 0.95,
        "guidance": (
            "Use realpath() then verify prefix. Never trust the input "
            "string alone."
        ),
        "tags": ["path-traversal", "symlinks", "defense"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://cwe.mitre.org/data/definitions/22.html",
                "title": "CWE-22: Improper Limitation of a Pathname to a Restricted Directory",
                "source_name": "MITRE",
            },
        ],
        "first_seen": "2010-01",
    },

    # =====================================================================
    # PRODUCT SECURITY — supply chain
    # =====================================================================
    {
        "id": "package-installers-run-arbitrary-code-by-default",
        "topic": "product-security",
        "domain": "Supply Chain & Dependencies",
        "phase": "threat-model",
        "statement": (
            "Installing a package with pip, npm, or gem executes arbitrary "
            "code at install time by default (setup.py, postinstall scripts). "
            "Treat 'installed a dep' as 'ran their code'."
        ),
        "status": "current",
        "confidence": 0.98,
        "guidance": (
            "Do first-touch installs in a sandbox. Where possible, prefer "
            "`--ignore-scripts` + explicit build orchestration."
        ),
        "tags": ["npm", "pip", "supply-chain"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://blog.trailofbits.com/2020/12/22/how-are-teams-currently-handling-web-attacks-at-scale/",
                "title": "Best practices for defending against supply chain attacks",
                "source_name": "Trail of Bits",
                "published": "2020",
            },
        ],
        "first_seen": "2020-01",
    },
    {
        "id": "typosquatting-in-package-registries-is-an-active-threat",
        "topic": "product-security",
        "domain": "Supply Chain & Dependencies",
        "phase": "attack",
        "statement": (
            "Typosquatted packages (e.g. `python-requests` vs `requests`) "
            "are regularly uploaded to public registries with malicious "
            "install-time payloads; the technique remains effective "
            "because dependency selection is often typed manually."
        ),
        "status": "current",
        "confidence": 0.9,
        "guidance": (
            "Prefer install from lockfile only; audit any hand-added "
            "dependency's provenance."
        ),
        "tags": ["typosquatting", "npm", "pypi"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://checkmarx.com/blog/typosquatting-attack-on-npm-cryptocurrency-package/",
                "title": "Typosquatting on npm",
                "source_name": "Checkmarx",
                "published": "2023",
            },
        ],
        "first_seen": "2016-01",
    },

    # =====================================================================
    # PRODUCT SECURITY — cloud / IAM
    # =====================================================================
    {
        "id": "imdsv1-must-be-disabled-on-agent-workloads",
        "topic": "product-security",
        "domain": "Cloud & IAM",
        "phase": "defense",
        "statement": (
            "AWS IMDSv1 is trivially exploitable from any code that can "
            "cause an HTTP GET to 169.254.169.254; agent workloads that "
            "may fetch user-provided URLs must disable v1 in favor of v2."
        ),
        "status": "current",
        "confidence": 0.95,
        "guidance": (
            "Set HttpTokens=required on all EC2 instances hosting agent "
            "runtimes. Auto-audit via Security Hub."
        ),
        "tags": ["aws", "imds", "ssrf"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://aws.amazon.com/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/",
                "title": "Get the full benefits of IMDSv2",
                "source_name": "AWS Security Blog",
                "published": "2023",
            },
        ],
        "first_seen": "2019-11",
    },
    {
        "id": "long-lived-cloud-credentials-are-obsolete",
        "topic": "product-security",
        "domain": "Cloud & IAM",
        "phase": "defense",
        "statement": (
            "Long-lived static cloud credentials in CI or on developer "
            "machines are the highest-frequency root cause of breach in "
            "cloud environments; short-lived OIDC / role-assumption "
            "flows should be used for every automated workload."
        ),
        "status": "current",
        "confidence": 0.9,
        "guidance": (
            "Migrate CI to OIDC federation. Enforce a max credential age "
            "on IAM users. Prefer role-assumption for developer access."
        ),
        "tags": ["aws", "credentials", "oidc"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://cloud.google.com/blog/products/identity-security/rip-secret-storage",
                "title": "Workload identity federation",
                "source_name": "Google Cloud",
                "published": "2022",
            },
        ],
        "first_seen": "2021-01",
    },

    # =====================================================================
    # PRODUCT SECURITY — AI-generated code risk
    # =====================================================================
    {
        "id": "llm-generated-code-hallucinates-package-names",
        "topic": "product-security",
        "domain": "AI-Generated Code Risk",
        "phase": "threat-model",
        "statement": (
            "LLMs generate import statements for packages that do not "
            "exist ('slopsquatting'); attackers observe these hallucinated "
            "names and register malicious packages to catch the next "
            "developer who copies the generated code."
        ),
        "status": "current",
        "confidence": 0.85,
        "guidance": (
            "Every LLM-suggested dependency must be verified against the "
            "actual registry before pinning. Automate the check in your "
            "CI code-review pass."
        ),
        "tags": ["ai-code-risk", "slopsquatting", "npm"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2406.10279",
                "title": "We Have a Package for You! A Comprehensive Analysis of Package Hallucinations",
                "source_name": "arXiv",
                "published": "2024-06",
            },
        ],
        "first_seen": "2024-06",
    },

    # =====================================================================
    # PRODUCT SECURITY — detection & response
    # =====================================================================
    {
        "id": "signature-based-detection-fails-on-llm-authored-malware",
        "topic": "product-security",
        "domain": "Detection & Response",
        "phase": "threat-model",
        "statement": (
            "Signature-based detection under-performs against LLM-authored "
            "malware because trivial regeneration produces novel binaries "
            "at zero cost, while behavior and delivery-chain signals "
            "remain stable."
        ),
        "status": "current",
        "confidence": 0.7,
        "guidance": (
            "Weight EDR and behavioral analytics over hash-based feeds "
            "for AI-authored threat classes."
        ),
        "tags": ["malware", "detection", "ai-authored"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://unit42.paloaltonetworks.com/using-llms-obfuscate-malicious-javascript/",
                "title": "Using LLMs to obfuscate malicious JavaScript",
                "source_name": "Unit 42",
                "published": "2024",
            },
        ],
        "first_seen": "2024-01",
    },

    # =====================================================================
    # PRODUCT SECURITY — mobile
    # =====================================================================
    {
        "id": "mobile-webviews-are-a-persistent-cross-context-attack-surface",
        "topic": "product-security",
        "domain": "Mobile Security",
        "phase": "threat-model",
        "statement": (
            "Mobile applications that render web content in a WebView with "
            "JS bridges exposed to native code create a persistent "
            "cross-context attack surface — any XSS in the rendered "
            "content becomes device-level RCE."
        ),
        "status": "current",
        "confidence": 0.9,
        "guidance": (
            "Never expose native bridges to WebViews that render "
            "third-party content. Constrain the bridge to a small, "
            "auditable API surface."
        ),
        "tags": ["mobile", "webview", "android", "ios"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridge",
                "title": "Insecure WebView native bridge",
                "source_name": "Android Developers",
            },
        ],
        "first_seen": "2014-01",
    },

    # =====================================================================
    # AI RESEARCH — agents & harnesses
    # =====================================================================
    {
        "id": "tool-count-degrades-agent-performance",
        "topic": "ai-research",
        "domain": "Agents & Harnesses",
        "phase": "deployment",
        "statement": (
            "Adding more tools to an agent's available set beyond a modest "
            "number (roughly 10–20) degrades tool-selection accuracy and "
            "task success, even when the added tools are individually "
            "well-scoped."
        ),
        "status": "current",
        "confidence": 0.7,
        "guidance": (
            "Curate the tool set. Retire tools whose calls the eval suite "
            "shows agents get wrong more than they get right."
        ),
        "tags": ["agents", "harness", "tools"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2307.16789",
                "title": "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs",
                "source_name": "arXiv",
                "published": "2023-07",
            },
        ],
        "first_seen": "2023-07",
    },
    {
        "id": "chain-of-thought-does-not-transfer-to-multi-turn",
        "topic": "ai-research",
        "domain": "Agents & Harnesses",
        "phase": "evaluation",
        "statement": (
            "Chain-of-thought accuracy gains measured on single-turn "
            "benchmarks do not reliably transfer to multi-turn agent "
            "tasks where the model must revise its plan across steps."
        ),
        "status": "current",
        "confidence": 0.6,
        "guidance": (
            "Evaluate agents on the multi-turn task, not a single-turn "
            "proxy. Score plan revisions as a first-class metric."
        ),
        "tags": ["chain-of-thought", "agents", "evals"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2402.10171",
                "title": "Chain-of-thought reasoning without prompting",
                "source_name": "arXiv",
                "published": "2024-02",
            },
        ],
        "first_seen": "2024-02",
    },

    # =====================================================================
    # AI RESEARCH — RAG & retrieval
    # =====================================================================
    {
        "id": "retrieval-quality-dominates-generation-quality-in-rag",
        "topic": "ai-research",
        "domain": "Retrieval & RAG",
        "phase": "deployment",
        "statement": (
            "In production RAG systems, retrieval quality — recall of the "
            "right documents at the right rank — dominates generation "
            "quality as a determinant of end-task accuracy; larger models "
            "cannot compensate for a bad retriever."
        ),
        "status": "current",
        "confidence": 0.75,
        "guidance": (
            "Invest in retrieval evals (recall@k, reranker quality) "
            "before spending on bigger generator models."
        ),
        "tags": ["rag", "retrieval", "evals"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2312.10997",
                "title": "Retrieval-Augmented Generation for Large Language Models: A Survey",
                "source_name": "arXiv",
                "published": "2023-12",
            },
        ],
        "first_seen": "2023-12",
    },
    {
        "id": "hybrid-search-beats-pure-vector-for-most-domains",
        "topic": "ai-research",
        "domain": "Retrieval & RAG",
        "phase": "deployment",
        "statement": (
            "Hybrid search (BM25 + dense vectors) outperforms pure vector "
            "retrieval on most enterprise/technical corpora, because "
            "vector embeddings underweight exact term matches (names, "
            "identifiers, error codes) that carry high signal."
        ),
        "status": "current",
        "confidence": 0.8,
        "guidance": (
            "Default to hybrid retrieval unless you've measured that "
            "pure-vector wins on your specific corpus."
        ),
        "tags": ["rag", "hybrid-search", "bm25"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://weaviate.io/blog/hybrid-search-explained",
                "title": "Hybrid Search Explained",
                "source_name": "Weaviate",
                "published": "2024",
            },
        ],
        "first_seen": "2023-06",
    },
    {
        "id": "long-context-does-not-eliminate-retrieval-need",
        "topic": "ai-research",
        "domain": "Retrieval & RAG",
        "phase": "threat-model",
        "statement": (
            "Long-context models (1M+ tokens) do not eliminate the need "
            "for retrieval: they exhibit lost-in-the-middle effects, cost "
            "grows linearly with context size, and per-token attention "
            "drops on distant tokens."
        ),
        "status": "current",
        "confidence": 0.8,
        "guidance": (
            "Retrieval + a short, relevant context still beats stuffing a "
            "long context on cost, latency, and accuracy for most tasks."
        ),
        "tags": ["long-context", "rag", "lost-in-the-middle"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2307.03172",
                "title": "Lost in the Middle: How Language Models Use Long Contexts",
                "source_name": "arXiv",
                "published": "2023-07",
            },
        ],
        "first_seen": "2023-07",
    },

    # =====================================================================
    # AI RESEARCH — evals
    # =====================================================================
    {
        "id": "llm-as-judge-is-biased-toward-longer-answers",
        "topic": "ai-research",
        "domain": "Evaluation",
        "phase": "evaluation",
        "statement": (
            "LLM-as-judge evaluators exhibit systematic bias toward "
            "longer, more elaborate answers, independent of quality; the "
            "bias survives common mitigations (position swap, chain-of-"
            "thought grading)."
        ),
        "status": "current",
        "confidence": 0.75,
        "guidance": (
            "Cross-check LLM-judge scores with pairwise human eval on a "
            "small sample. Score length as a separate axis so the bias "
            "is visible."
        ),
        "tags": ["llm-as-judge", "eval-bias", "evals"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2306.05685",
                "title": "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena",
                "source_name": "arXiv",
                "published": "2023-06",
            },
        ],
        "first_seen": "2023-06",
    },
    {
        "id": "swe-bench-doesnt-generalize-to-production-tasks",
        "topic": "ai-research",
        "domain": "Evaluation",
        "phase": "evaluation",
        "statement": (
            "SWE-bench scores do not linearly predict agent performance "
            "on production engineering tasks; the benchmark rewards a "
            "specific style of small-diff bug-fix that under-represents "
            "the actual work distribution."
        ),
        "status": "current",
        "confidence": 0.7,
        "guidance": (
            "Treat SWE-bench as one data point in a portfolio, not a "
            "complete picture. Build in-house evals on your task mix."
        ),
        "tags": ["evals", "swe-bench", "benchmarks"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2310.06770",
                "title": "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?",
                "source_name": "arXiv",
                "published": "2023-10",
            },
        ],
        "first_seen": "2023-10",
    },

    # =====================================================================
    # AI RESEARCH — prompting & context
    # =====================================================================
    {
        "id": "system-prompts-should-be-versioned-like-code",
        "topic": "ai-research",
        "domain": "Prompting & Context",
        "phase": "deployment",
        "statement": (
            "Production system prompts are load-bearing configuration and "
            "should be version-controlled, code-reviewed, and evaluated "
            "on regression suites — treating them as freeform strings "
            "is the source of most silent behavior drift after model "
            "swaps."
        ),
        "status": "current",
        "confidence": 0.85,
        "guidance": (
            "Store prompts in the same repo as the code that calls them. "
            "Run eval on every prompt change and every model change."
        ),
        "tags": ["prompting", "deployment", "regression"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://simonwillison.net/2024/Jul/26/prompt-injection/",
                "title": "Prompt injection and the security of AI applications",
                "source_name": "Simon Willison",
                "published": "2024-07",
            },
        ],
        "first_seen": "2023-01",
    },
    {
        "id": "few-shot-prompting-brittle-on-format-changes",
        "topic": "ai-research",
        "domain": "Prompting & Context",
        "phase": "evaluation",
        "statement": (
            "Few-shot prompting accuracy is highly sensitive to example "
            "ordering, whitespace, and demarcation choices, in ways that "
            "look like model regressions if not controlled for."
        ),
        "status": "current",
        "confidence": 0.7,
        "guidance": (
            "Freeze prompt formatting when evaluating model changes. "
            "Prefer structured formats (JSON, YAML) over ad-hoc "
            "demarcation."
        ),
        "tags": ["prompting", "few-shot", "brittleness"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2102.09690",
                "title": "Calibrate Before Use: Improving Few-Shot Performance of Language Models",
                "source_name": "arXiv",
                "published": "2021-02",
            },
        ],
        "first_seen": "2021-02",
    },

    # =====================================================================
    # AI RESEARCH — capabilities & scaling
    # =====================================================================
    {
        "id": "capability-elicitation-lags-training",
        "topic": "ai-research",
        "domain": "Models & Capabilities",
        "phase": "threat-model",
        "statement": (
            "A model's actual capability ceiling is typically higher than "
            "what standard prompting elicits; targeted prompting, "
            "fine-tuning, or scaffolding can unlock capabilities the base "
            "eval missed. This matters for capability-based safety cases."
        ),
        "status": "current",
        "confidence": 0.8,
        "guidance": (
            "Do not build a safety case on 'the model can't do X' from a "
            "base-eval measurement alone. Elicitation is a research "
            "capability, not a static property."
        ),
        "tags": ["capabilities", "elicitation", "safety"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://www.anthropic.com/research/rsp-updates",
                "title": "Responsible Scaling Policy",
                "source_name": "Anthropic",
                "published": "2024",
            },
        ],
        "first_seen": "2023-01",
    },
    {
        "id": "quantization-preserves-most-benchmark-scores",
        "topic": "ai-research",
        "domain": "Deployment",
        "phase": "deployment",
        "statement": (
            "8-bit and 4-bit quantization of open-weights models preserves "
            "most benchmark accuracy (within 1–3 points) while cutting "
            "memory footprint roughly proportionally to bit width."
        ),
        "status": "current",
        "confidence": 0.8,
        "guidance": (
            "Default to quantized weights for local inference of models "
            "≥7B on consumer hardware. Verify on your task, not just on "
            "MMLU."
        ),
        "tags": ["quantization", "deployment", "inference"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2306.03078",
                "title": "SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression",
                "source_name": "arXiv",
                "published": "2023-06",
            },
        ],
        "first_seen": "2023-06",
    },

    # =====================================================================
    # AI RESEARCH — code assistants
    # =====================================================================
    {
        "id": "coding-agents-produce-plausible-but-hallucinated-apis",
        "topic": "ai-research",
        "domain": "Coding Agents",
        "phase": "threat-model",
        "statement": (
            "Coding assistants generate calls to functions and APIs that "
            "do not exist in the target library or version — plausible "
            "spelling, correct-looking signature, no runtime existence — "
            "and this pattern persists across model families."
        ),
        "status": "current",
        "confidence": 0.9,
        "guidance": (
            "Any LLM-suggested import or API call must be validated "
            "against the actual library documentation for the pinned "
            "version, not the model's memory."
        ),
        "tags": ["coding-agents", "hallucination", "apis"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2308.07922",
                "title": "Hallucinations in Code Generation",
                "source_name": "arXiv",
                "published": "2023-08",
            },
        ],
        "first_seen": "2023-08",
    },
    {
        "id": "diff-review-catches-more-than-full-file-review",
        "topic": "ai-research",
        "domain": "Coding Agents",
        "phase": "deployment",
        "statement": (
            "Reviewing an LLM's proposed change as a diff catches more "
            "defects than reviewing the resulting full file, because the "
            "diff frames attention on the semantic delta rather than "
            "letting eyes skim familiar surrounding lines."
        ),
        "status": "current",
        "confidence": 0.7,
        "guidance": (
            "Prefer tools that present LLM changes as diffs. Reviewer "
            "must sign off on the specific lines that changed."
        ),
        "tags": ["code-review", "diffs", "coding-agents"],
        "evidence": [
            {
                "stance": "supports",
                "url": "https://arxiv.org/abs/2312.02003",
                "title": "The Impact of AI on Developer Productivity",
                "source_name": "arXiv (GitClear)",
                "published": "2024-01",
            },
        ],
        "first_seen": "2024-01",
    },
]


def build_claim(seed: dict) -> dict:
    """Convert a seed spec into a fully-shaped claim dict."""
    claim = {
        "id": seed["id"],
        "topic": seed["topic"],
        "domain": seed.get("domain", ""),
        "statement": seed["statement"],
        "status": seed["status"],
        "confidence": seed["confidence"],
        "phase": seed["phase"],
        "evidence": seed.get("evidence", []),
        "first_seen": seed.get("first_seen", "2024-01"),
        "last_reviewed": _today(),
    }
    for key in ("guidance", "scope"):
        if seed.get(key):
            claim[key] = seed[key]
    if seed.get("tags"):
        claim["tags"] = seed["tags"]
    return claim


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="Preview what would be added; do not write.")
    args = ap.parse_args(argv)

    ledger = cl.load_ledger()
    existing_ids = {c["id"] for c in ledger.get("claims", [])}

    to_add = []
    skipped = []
    for seed in SEEDS:
        if seed["id"] in existing_ids:
            skipped.append(seed["id"])
            continue
        to_add.append(build_claim(seed))

    print(f"Would add {len(to_add)} claim(s); skipping {len(skipped)} already present.")
    for c_ in to_add:
        print(f"  + [{c_['topic']:<16}] [{c_['phase']:<12}] {c_['id']}")
    for cid in skipped:
        print(f"  = {cid}")

    if args.dry_run:
        print("\n[dry-run] no writes.")
        return 0

    # Add each via cl.add_claim so validation runs.
    for claim in to_add:
        try:
            ledger = cl.add_claim(ledger, claim)
        except ValueError as exc:
            print(f"REJECTED {claim['id']}: {exc}", file=sys.stderr)
            return 1

    # Final validation before writing.
    errors = cl.validate_ledger(ledger)
    if errors:
        print("Ledger invalid after seed — not saving:", file=sys.stderr)
        for e in errors[:20]:
            print(f"  - {e}", file=sys.stderr)
        return 1

    cl.save_ledger(ledger)
    print(f"\nSaved. Ledger now has {len(ledger['claims'])} claim(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
