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
- If a request mixes modes, finish read-only review before making ingest changes.

Use the repository root that contains this Skill. Read AGENTS.md before acting.

## INGEST

1. Read every supplied source completely. Do not rely on a filename, excerpt, or summary when the full material is available.
2. Read index/catalog.md, then search knowledge/ for similar titles, questions, keywords, conclusions, and mechanisms.
3. Assess the material before extraction:
   - identify source type, author, date, completeness, first-hand versus second-hand status;
   - separate factual claims, empirical claims, methods, opinions, stories, analogies, and the source author's inferences;
   - record missing evidence and foreseeable harms.
4. Extract only durable candidate propositions that can stand alone and improve future decisions.
5. Assign exactly one decision to each candidate:
   - IGNORE: no durable value, pure repetition, or too weak to retain;
   - CREATE: a distinct reusable proposition does not yet exist;
   - REINFORCE: add support, explanation, application, or confidence to an existing node;
   - UPDATE: revise the conclusion, boundary, confidence, status, or method;
   - CONFLICT: retain a material contradiction without forcing false consensus.
6. Create one immutable Source snapshot under sources/YYYY/. Include provenance, import date, original location or URL, and a content hash when available. Do not silently rewrite a stored Source; create a new version if the source changes.
7. Create or edit Knowledge files under knowledge/<topic>/ using templates/knowledge.md:
   - keep one central proposition per file;
   - write a usable current conclusion, not an article summary;
   - distinguish source claims from the knowledge-base judgment;
   - include application, boundaries, counterarguments, confidence, freshness, sources, and an evolution record;
   - record verification_scope and external_evidence_status so Source consistency is not mistaken for external validation;
   - never promote a claim to fact solely because it appears in a saved source.
8. Update index/catalog.md for every created, renamed, materially changed, disputed, deprecated, or superseded Knowledge node.
9. Verify every Source and Knowledge link, check the full Git diff with readable Chinese paths, and confirm no unrelated files changed.
10. Report:
    - the Source snapshot;
    - decisions and affected Knowledge nodes;
    - important evidence boundaries or unresolved conflicts;
    - verification performed.

Do not commit or push unless the user explicitly asks.

### Ingest a URL

1. Preserve the submitted URL, then derive a canonical URL only for duplicate detection.
2. Open the page and obtain the rendered article body plus title, author or account, publication date, and retrieval date.
3. For mp.weixin.qq.com or another dynamically rendered or login-gated page, use an interactive browser when normal page retrieval is incomplete.
4. Never infer an article from a title, search snippet, repost summary, or comments. If the body remains partial or blocked, stop before changing Knowledge and ask the user to paste the text or upload an export/PDF.
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

1. Search index/catalog.md and knowledge/ for the topic, synonyms, related questions, and linked nodes.
2. Read the selected Knowledge nodes and all Source files needed to verify their provenance.
3. Produce a topic audit containing:
   - current best conclusion;
   - supporting and opposing evidence;
   - duplicate or overlapping nodes;
   - unresolved conflicts;
   - stale or weakly sourced claims;
   - missing viewpoints and next verification steps.
4. Recommend KEEP, MERGE, UPDATE, DISPUTE, DEPRECATE, or VERIFY, but keep the review read-only unless the user authorizes changes.

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
