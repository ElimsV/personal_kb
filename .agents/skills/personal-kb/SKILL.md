---
name: personal-kb
description: Maintain and use this Markdown personal knowledge base. Use for /ingest, /ask, or /review requests; for a bare http/https URL such as a WeChat article when no other intent is given; when the user asks to absorb articles, notes, webpages, documents, URLs, or personal experience into durable knowledge; when the user corrects or revises an existing belief; when answering from existing knowledge; or when auditing conclusions, sources, conflicts, confidence, freshness, and gaps. Do not use for unrelated repository work.
---

# Personal KB

Operate the repository as a traceable, evolving knowledge system. Treat stored knowledge as a prior, never as unquestionable truth.

## Select the mode

Infer the mode from the request:

- Choose INGEST for /ingest, “入库”, “沉淀”, “吸收资料”, or any request to change the knowledge base from new information.
- Choose INGEST for a message containing only one http/https URL unless the user gives a different intent.
- Choose ASK for /ask, “结合我的知识库回答”, or a question that should use existing knowledge.
- Choose REVIEW for /review, “复查主题”, “检查冲突/来源/时效”, or a knowledge audit.
- Choose REVIEW when the user wants to inspect an Ingest Run, candidate decisions, node matching, or knowledge-base growth quality.
- If a request mixes modes, finish read-only review before making ingest changes.

Use the repository root that contains this Skill. Read AGENTS.md before acting.

## INGEST

1. Acquire and normalize every supplied source before changing the repository:
   - batch independent retrieval and parsing when several sources are supplied;
   - preserve one local normalized body plus a compact manifest containing provenance, completeness, and hash;
   - load each complete normalized body into model context once; reuse the manifest and extracted propositions instead of printing or reading the same body again;
   - do not rely on prompt caching for correctness or context control.
2. Read index/catalog.md, then search knowledge/ for similar questions, conclusions, and mechanisms. Use titles and keywords only as recall aids.
3. Assess the material before extraction:
   - identify source type, author, date, completeness, first-hand versus second-hand status;
   - separate factual claims, empirical claims, methods, opinions, stories, analogies, and the source author's inferences;
   - record missing evidence and foreseeable harms.
4. Extract only durable candidate propositions that can stand alone and improve future decisions.
5. Draft one candidate decision row per proposition before writing. Assign exactly one decision:
   - IGNORE: no durable value, pure repetition, or too weak to retain;
   - CREATE: a distinct reusable proposition does not yet exist;
   - REINFORCE: add support, explanation, application, or confidence to an existing node;
   - UPDATE: revise the conclusion, boundary, confidence, status, or method;
   - CONFLICT: retain a material contradiction without forcing false consensus.
6. Before final matching or any repository write, acquire the exclusive lock:
   - run `python3 .agents/skills/personal-kb/scripts/ingest_lock.py acquire` and retain the returned owner token;
   - if another writer holds the lock, do not mutate the repository; wait or report the owner and lock age;
   - after acquiring it, re-read catalog.md and every matched Knowledge target, then revise the decision table against this current state;
   - run `heartbeat --owner <token>` before each write batch and `release --owner <token>` after validation, including after a recoverable failure;
   - never clear a suspected stale lock without user approval. ASK and REVIEW do not take the lock.
7. Create `ingest_runs/YYYY/YYYY-MM-DD-short-slug.md` from templates/ingest-run.md and set `status: planned`. Persist the final candidate table with: `ID | 候选命题 | Source IDs | 证据强度 | 已有匹配与实质变化 | 决策 | 目标 | 理由`. Record every candidate, including IGNORE, and never fabricate unavailable time, token, cache, or context-load telemetry.
8. Write in small, reviewable stages: new Source snapshots first, one Knowledge node at a time, and catalog.md last. Re-read an existing target immediately before editing it; do not use one giant patch for the whole ingest.
9. Create one immutable Source snapshot under sources/YYYY/. Include provenance, import date, original location or URL, and a content hash when available. Do not silently rewrite a stored Source; create a new version if the source changes.
10. Create or edit Knowledge files under knowledge/<topic>/ using templates/knowledge.md:
   - keep one central proposition per file;
   - write a usable current conclusion, not an article summary;
   - distinguish source claims from the knowledge-base judgment;
   - include application, boundaries, counterarguments, confidence, freshness, sources, and an evolution record;
   - record verification_scope and external_evidence_status so Source consistency is not mistaken for external validation;
   - never promote a claim to fact solely because it appears in a saved source.
11. Update index/catalog.md for every created, renamed, materially changed, disputed, deprecated, or superseded Knowledge node.
12. Fill the run log with the actual write mapping, decision counts, weak matches, evidence gaps, and unavailable telemetry while keeping `status: planned` and `validation_status: not_run`. Run `python3 .agents/skills/personal-kb/scripts/validate_kb.py`; record the result, set the run to `completed` or `failed`, and run the same command once more to validate the finalized log. Inspect the full Git diff with readable Chinese paths and confirm no unrelated files changed.
13. Preserve observability:
    - create a run log even when capture is blocked, all candidates are IGNORE, or validation fails;
    - keep the original decision table visible; after finalization, record corrections as dated review notes or create a new run linked by `retry_of` instead of silently rewriting history;
    - use run metrics to watch CREATE rate, weak-match count, single-source CREATEs, evidence coverage, and validation warnings over time.
14. Report:
    - the Source snapshot;
    - the Ingest Run log;
    - decisions and affected Knowledge nodes;
    - important evidence boundaries or unresolved conflicts;
    - verification performed.

Do not commit or push unless the user explicitly asks.

### Ingest a URL

1. Preserve the submitted URL, then derive a canonical URL only for duplicate detection.
2. Try normal retrieval once and check for the rendered article body plus title, author or account, publication date, and retrieval date.
3. If mp.weixin.qq.com or another dynamic/login-gated page is incomplete, switch directly to an interactive browser. Do not repeat equivalent fetch methods that return the same partial page.
4. If browser retrieval is still partial or blocked, stop before changing Knowledge and ask the user to paste the text or upload an export/PDF. Never infer an article from a title, search snippet, repost summary, or comments.
5. Search existing Source metadata for the canonical URL and content hash before creating a new Source.
6. Set original_url, canonical_url, retrieved_at, capture_mode, access_status, content_sha256, and content_hash_scope when available.
7. For third-party public webpages, store provenance, a structured content digest, and only short necessary quotations. Store complete text only when the user supplied it directly or confirms they own or may archive it.
8. Continue with the normal IGNORE / CREATE / REINFORCE / UPDATE / CONFLICT decision flow only after enough content is available.

### Ingest a user correction

1. Save the user's exact or faithfully normalized statement as a new user_reflection Source.
2. Treat the user's statement as evidence of their current view, not as external proof that the proposition is true.
3. Compare it with current Knowledge and choose CREATE, REINFORCE, UPDATE, or CONFLICT.
4. Preserve old Sources and evolution history. Mark replaced Knowledge deprecated or superseded instead of erasing it.

## ASK

1. Read index/catalog.md.
2. Select only 1—5 Knowledge files that clearly help answer the question, then read them fully.
3. Check each node's status, confidence, freshness, last_verified_at, verification_scope, external_evidence_status, sources, and boundaries.
4. Verify current external facts when the answer depends on unstable information. Prefer present evidence over stale stored conclusions.
5. Answer the user's actual situation:
   - lead with the current conclusion;
   - identify relevant knowledge-base priors;
   - distinguish stored knowledge, current external evidence, and this answer's inference;
   - surface conflicts, uncertainty, and decision conditions.
6. Link or name the Knowledge files used. Do not modify the repository unless the user also requests INGEST.

## REVIEW

1. For a topic review, search index/catalog.md and knowledge/ for the topic, synonyms, related questions, and linked nodes. For an ingest-quality review, open the relevant ingest_runs/ log and follow its Source and Knowledge links.
2. Read the selected Knowledge nodes and all Source files needed to verify their provenance.
3. Produce a topic audit containing:
   - current best conclusion;
   - supporting and opposing evidence;
   - duplicate or overlapping nodes;
   - unresolved conflicts;
   - stale or weakly sourced claims;
   - missing viewpoints and next verification steps.
4. When reviewing an Ingest Run, also audit candidate completeness, evidence calibration, existing-node match, decision type, write mapping, CREATE rate, weak matches, and whether IGNORE discarded useful knowledge.
5. Recommend KEEP, MERGE, UPDATE, DISPUTE, DEPRECATE, VERIFY, or REPROCESS, but keep the review read-only unless the user authorizes changes. If authorized, append a dated Review record or create a new run linked by retry_of; preserve the original decision table.

## Metadata vocabulary

- knowledge_type: principle | model | method | empirical | fact | opinion
- freshness: very_slow | slow | medium | fast | very_fast
- confidence: low | medium | high
- status: active | disputed | deprecated
- verification_scope: source_integrity | source_consistency | external_evidence | user_experience
- external_evidence_status: not_checked | partial | verified | conflicting
- capture_mode: user_supplied_fulltext | authorized_fulltext | metadata_and_digest
- access_status: complete | partial | blocked

Prefer calibrated uncertainty. A polished note is not evidence of truth.
