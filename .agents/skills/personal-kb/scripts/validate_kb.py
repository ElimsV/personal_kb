#!/usr/bin/env python3
"""Validate Personal KB metadata, references, catalog coverage, and Source immutability."""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote


FRONTMATTER_BOUNDARY = "---"
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CATALOG_PATH = re.compile(r"^- Path:\s+(.+?)\s*$", re.MULTILINE)

SOURCE_REQUIRED = {
    "id",
    "title",
    "source_type",
    "imported_at",
    "capture_mode",
    "access_status",
    "content_sha256",
    "content_hash_scope",
    "status",
}
KNOWLEDGE_REQUIRED = {
    "id",
    "title",
    "topics",
    "questions",
    "keywords",
    "knowledge_type",
    "freshness",
    "confidence",
    "status",
    "created_at",
    "updated_at",
    "last_verified_at",
    "verification_scope",
    "external_evidence_status",
    "sources",
    "related_knowledge",
}
INGEST_RUN_REQUIRED = {
    "id",
    "title",
    "ingest_date",
    "recorded_at",
    "status",
    "trace_status",
    "source_count",
    "candidate_count",
    "create_count",
    "reinforce_count",
    "update_count",
    "conflict_count",
    "ignore_count",
    "affected_knowledge_count",
    "weak_match_count",
    "single_source_create_count",
    "externally_verified_source_count",
    "validation_warning_count",
    "validation_status",
    "source_ids",
    "knowledge_ids",
    "retry_of",
}
SOURCE_SECTIONS = {"# 来源说明"}
KNOWLEDGE_SECTIONS = {
    "# 当前结论",
    "# 判断依据",
    "# 应用方式",
    "# 适用边界",
    "# 不同观点与冲突",
    "# 我的认知",
    "# 来源",
    "# 演进记录",
}
INGEST_RUN_SECTIONS = {
    "# 运行摘要",
    "# 输入与抓取",
    "# 候选命题决策表",
    "# 写入映射",
    "# 质量检查",
    "# 调试信号与未解决问题",
    "# 验证结果",
    "# Review 记录",
}
CANDIDATE_HEADERS = [
    "ID",
    "候选命题",
    "Source IDs",
    "证据强度",
    "已有匹配与实质变化",
    "决策",
    "目标",
    "理由",
]
DECISIONS = {"CREATE", "REINFORCE", "UPDATE", "CONFLICT", "IGNORE"}
RUN_STATUSES = {"planned", "completed", "failed", "backfilled"}
TRACE_STATUSES = {"live", "reconstructed"}
VALIDATION_STATUSES = {"not_run", "passed", "passed_with_warnings", "failed"}
ALLOWED = {
    "knowledge_type": {"principle", "model", "method", "empirical", "fact", "opinion"},
    "freshness": {"very_slow", "slow", "medium", "fast", "very_fast"},
    "confidence": {"low", "medium", "high"},
    "status": {"active", "disputed", "deprecated"},
    "verification_scope": {
        "source_integrity",
        "source_consistency",
        "external_evidence",
        "user_experience",
    },
    "external_evidence_status": {"not_checked", "partial", "verified", "conflicting"},
    "capture_mode": {"user_supplied_fulltext", "authorized_fulltext", "metadata_and_digest"},
    "access_status": {"complete", "partial", "blocked"},
}


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / "index/catalog.md").is_file():
            return candidate
    raise RuntimeError("无法定位个人知识库根目录")


def parse_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        raise ValueError("缺少 YAML frontmatter 起始分隔符")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == FRONTMATTER_BOUNDARY)
    except StopIteration as exc:
        raise ValueError("缺少 YAML frontmatter 结束分隔符") from exc

    metadata: dict[str, object] = {}
    active_list: str | None = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and active_list:
            value = line[4:].strip().strip('"\'')
            assert isinstance(metadata[active_list], list)
            metadata[active_list].append(value)
            continue
        match = re.match(r"^([A-Za-z0-9_]+):(?:\s*(.*))?$", line)
        if not match:
            active_list = None
            continue
        key, raw = match.group(1), (match.group(2) or "").strip()
        if raw == "":
            metadata[key] = []
            active_list = key
        elif raw == "[]":
            metadata[key] = []
            active_list = None
        elif raw in {"null", "~"}:
            metadata[key] = None
            active_list = None
        else:
            metadata[key] = raw.strip('"\'')
            active_list = None
    return metadata, text


def validate_links(repo_root: Path, path: Path, text: str, errors: list[str]) -> None:
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(repo_root)}: 内部链接不存在: {raw_target}")


def parse_nonnegative_int(
    metadata: dict[str, object], key: str, relative: Path, errors: list[str]
) -> int:
    try:
        value = int(str(metadata.get(key)))
    except (TypeError, ValueError):
        errors.append(f"{relative}: {key} 必须是非负整数")
        return 0
    if value < 0:
        errors.append(f"{relative}: {key} 必须是非负整数")
        return 0
    return value


def parse_candidate_rows(text: str) -> tuple[list[dict[str, str]], str | None]:
    heading = "# 候选命题决策表"
    start = text.find(heading)
    if start < 0:
        return [], "缺少候选命题决策表"
    remainder = text[start + len(heading) :]
    next_heading = re.search(r"^#\s+", remainder, re.MULTILINE)
    section = remainder[: next_heading.start()] if next_heading else remainder
    table_lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return [], "候选命题决策表格式无效"

    def cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip("|").split("|")]

    headers = cells(table_lines[0])
    if headers != CANDIDATE_HEADERS:
        return [], f"候选命题决策表列必须为: {' | '.join(CANDIDATE_HEADERS)}"
    rows: list[dict[str, str]] = []
    for line in table_lines[1:]:
        values = cells(line)
        if values and all(re.fullmatch(r":?-{3,}:?", value) for value in values):
            continue
        if len(values) != len(headers):
            return [], f"候选命题决策表存在 {len(values)} 列的无效行"
        rows.append(dict(zip(headers, values)))
    return rows, None


def git_source_mutations(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", "status", "--porcelain=v1", "--", "sources"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ["无法检查 Source 的 Git 状态"]
    violations: list[str] = []
    for line in result.stdout.splitlines():
        code = line[:2]
        path = line[3:]
        if code not in {"??", "A ", " A"}:
            violations.append(f"已归档 Source 不应被修改、删除或重命名: {code} {path}")
    return violations


def tracked_source_paths(repo_root: Path) -> set[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "sources"],
        cwd=repo_root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return set()
    return {
        Path(raw.decode("utf-8"))
        for raw in result.stdout.split(b"\0")
        if raw
    }


def main() -> int:
    repo_root = find_repo_root(Path.cwd().resolve())
    errors: list[str] = []
    warnings: list[str] = []
    source_ids: dict[str, Path] = {}
    knowledge_ids: dict[str, Path] = {}
    knowledge_sources: dict[Path, list[str]] = {}
    canonical_urls: defaultdict[str, list[Path]] = defaultdict(list)
    ingest_run_ids: dict[str, Path] = {}
    ingest_run_retries: dict[Path, str] = {}
    ingest_status_counts: Counter[str] = Counter()
    ingest_metric_totals: Counter[str] = Counter()
    tracked_sources = tracked_source_paths(repo_root)

    source_files = sorted((repo_root / "sources").rglob("*.md"))
    knowledge_files = sorted((repo_root / "knowledge").rglob("*.md"))
    ingest_run_files = sorted((repo_root / "ingest_runs").rglob("*.md"))

    for path in source_files:
        relative = path.relative_to(repo_root)
        try:
            metadata, text = parse_frontmatter(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
            continue
        missing = sorted(SOURCE_REQUIRED - metadata.keys())
        if missing:
            message = f"{relative}: 缺少当前模板字段 {', '.join(missing)}"
            if relative in tracked_sources:
                warnings.append(f"历史 Source {message}")
            else:
                errors.append(message)
        source_id = metadata.get("id")
        if not isinstance(source_id, str) or not source_id.startswith("src-"):
            errors.append(f"{relative}: Source id 无效")
        elif source_id in source_ids:
            errors.append(f"{relative}: Source id 与 {source_ids[source_id]} 重复: {source_id}")
        else:
            source_ids[source_id] = relative
        for field in ("capture_mode", "access_status"):
            value = metadata.get(field)
            if value is not None and value not in ALLOWED[field]:
                errors.append(f"{relative}: {field} 值无效: {value}")
        missing_sections = sorted(section for section in SOURCE_SECTIONS if section not in text)
        if missing_sections:
            errors.append(f"{relative}: 缺少章节 {', '.join(missing_sections)}")
        if len(re.findall(r"^#\s+.+$", text, re.MULTILINE)) < 2:
            errors.append(f"{relative}: 缺少可识别的正文或结构化摘要章节")
        if relative not in tracked_sources and metadata.get("status") != "archived":
            errors.append(f"{relative}: 新 Source 的 status 必须为 archived")
        canonical_url = metadata.get("canonical_url")
        if isinstance(canonical_url, str) and canonical_url.startswith("http"):
            canonical_urls[canonical_url].append(relative)
        validate_links(repo_root, path, text, errors)

    for path in knowledge_files:
        relative = path.relative_to(repo_root)
        try:
            metadata, text = parse_frontmatter(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
            continue
        missing = sorted(KNOWLEDGE_REQUIRED - metadata.keys())
        if missing:
            errors.append(f"{relative}: 缺少 Knowledge 字段 {', '.join(missing)}")
        knowledge_id = metadata.get("id")
        if not isinstance(knowledge_id, str) or not knowledge_id.startswith("kn-"):
            errors.append(f"{relative}: Knowledge id 无效")
        elif knowledge_id in knowledge_ids:
            errors.append(f"{relative}: Knowledge id 与 {knowledge_ids[knowledge_id]} 重复: {knowledge_id}")
        else:
            knowledge_ids[knowledge_id] = relative
        for field in (
            "knowledge_type",
            "freshness",
            "confidence",
            "status",
            "verification_scope",
            "external_evidence_status",
        ):
            value = metadata.get(field)
            if value is not None and value not in ALLOWED[field]:
                errors.append(f"{relative}: {field} 值无效: {value}")
        refs = metadata.get("sources", [])
        if not isinstance(refs, list) or not refs:
            errors.append(f"{relative}: sources 必须是非空列表")
            knowledge_sources[relative] = []
        else:
            knowledge_sources[relative] = [str(item) for item in refs]
        missing_sections = sorted(section for section in KNOWLEDGE_SECTIONS if section not in text)
        if missing_sections:
            errors.append(f"{relative}: 缺少章节 {', '.join(missing_sections)}")
        validate_links(repo_root, path, text, errors)

    for path, refs in knowledge_sources.items():
        for source_id in refs:
            if source_id not in source_ids:
                errors.append(f"{path}: 引用不存在的 Source id: {source_id}")

    for path in ingest_run_files:
        relative = path.relative_to(repo_root)
        try:
            metadata, text = parse_frontmatter(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{relative}: {exc}")
            continue
        missing = sorted(INGEST_RUN_REQUIRED - metadata.keys())
        if missing:
            errors.append(f"{relative}: 缺少 Ingest Run 字段 {', '.join(missing)}")
        run_id = metadata.get("id")
        if not isinstance(run_id, str) or not run_id.startswith("ingest-"):
            errors.append(f"{relative}: Ingest Run id 无效")
        elif run_id in ingest_run_ids:
            errors.append(f"{relative}: Ingest Run id 与 {ingest_run_ids[run_id]} 重复: {run_id}")
        else:
            ingest_run_ids[run_id] = relative

        run_status = metadata.get("status")
        trace_status = metadata.get("trace_status")
        validation_status = metadata.get("validation_status")
        if run_status not in RUN_STATUSES:
            errors.append(f"{relative}: status 值无效: {run_status}")
        if trace_status not in TRACE_STATUSES:
            errors.append(f"{relative}: trace_status 值无效: {trace_status}")
        if validation_status not in VALIDATION_STATUSES:
            errors.append(f"{relative}: validation_status 值无效: {validation_status}")
        if run_status in {"completed", "backfilled"} and validation_status not in {
            "passed",
            "passed_with_warnings",
        }:
            errors.append(f"{relative}: 已完成运行必须记录通过的 validation_status")
        if run_status == "backfilled" and trace_status != "reconstructed":
            errors.append(f"{relative}: backfilled 运行必须使用 trace_status: reconstructed")

        missing_sections = sorted(section for section in INGEST_RUN_SECTIONS if section not in text)
        if missing_sections:
            errors.append(f"{relative}: 缺少章节 {', '.join(missing_sections)}")
        rows, table_error = parse_candidate_rows(text)
        if table_error:
            errors.append(f"{relative}: {table_error}")
            rows = []

        count_keys = {
            "CREATE": "create_count",
            "REINFORCE": "reinforce_count",
            "UPDATE": "update_count",
            "CONFLICT": "conflict_count",
            "IGNORE": "ignore_count",
        }
        candidate_count = parse_nonnegative_int(metadata, "candidate_count", relative, errors)
        source_count = parse_nonnegative_int(metadata, "source_count", relative, errors)
        affected_count = parse_nonnegative_int(
            metadata, "affected_knowledge_count", relative, errors
        )
        weak_match_count = parse_nonnegative_int(metadata, "weak_match_count", relative, errors)
        single_source_create_count = parse_nonnegative_int(
            metadata, "single_source_create_count", relative, errors
        )
        externally_verified_source_count = parse_nonnegative_int(
            metadata, "externally_verified_source_count", relative, errors
        )
        validation_warning_count = parse_nonnegative_int(
            metadata, "validation_warning_count", relative, errors
        )
        declared_counts = {
            decision: parse_nonnegative_int(metadata, key, relative, errors)
            for decision, key in count_keys.items()
        }
        if sum(declared_counts.values()) != candidate_count:
            errors.append(f"{relative}: 各决策数量之和不等于 candidate_count")
        if len(rows) != candidate_count:
            errors.append(f"{relative}: 候选表行数 {len(rows)} 不等于 candidate_count {candidate_count}")

        run_source_ids = metadata.get("source_ids", [])
        run_knowledge_ids = metadata.get("knowledge_ids", [])
        if not isinstance(run_source_ids, list):
            errors.append(f"{relative}: source_ids 必须是列表")
            run_source_ids = []
        if not isinstance(run_knowledge_ids, list):
            errors.append(f"{relative}: knowledge_ids 必须是列表")
            run_knowledge_ids = []
        run_source_ids = [str(value) for value in run_source_ids]
        run_knowledge_ids = [str(value) for value in run_knowledge_ids]
        if len(set(run_source_ids)) != source_count:
            errors.append(f"{relative}: source_ids 去重数量不等于 source_count")
        if len(set(run_knowledge_ids)) != affected_count:
            errors.append(f"{relative}: knowledge_ids 去重数量不等于 affected_knowledge_count")
        if single_source_create_count > declared_counts["CREATE"]:
            errors.append(f"{relative}: single_source_create_count 不能大于 create_count")
        if externally_verified_source_count > source_count:
            errors.append(f"{relative}: externally_verified_source_count 不能大于 source_count")

        actual_counts = Counter(row.get("决策", "") for row in rows)
        candidate_ids = [row.get("ID", "") for row in rows]
        if len(set(candidate_ids)) != len(candidate_ids):
            errors.append(f"{relative}: 候选 ID 重复")
        for decision in DECISIONS:
            if actual_counts[decision] != declared_counts[decision]:
                errors.append(
                    f"{relative}: {decision} 表格数量 {actual_counts[decision]} "
                    f"不等于元数据 {declared_counts[decision]}"
                )
        invalid_decisions = sorted(set(actual_counts) - DECISIONS)
        if invalid_decisions:
            errors.append(f"{relative}: 候选表含无效决策 {', '.join(invalid_decisions)}")

        for row in rows:
            candidate_id = row.get("ID", "未知候选")
            row_source_ids = set(re.findall(r"src-[A-Za-z0-9-]+", row.get("Source IDs", "")))
            if not row_source_ids:
                errors.append(f"{relative}: {candidate_id} 没有可识别的 Source ID")
            for source_id in row_source_ids:
                if source_id not in run_source_ids:
                    errors.append(f"{relative}: {candidate_id} 的 {source_id} 未列入运行 source_ids")
            target_ids = set(re.findall(r"kn-[A-Za-z0-9-]+", row.get("目标", "")))
            if row.get("决策") == "IGNORE":
                if target_ids:
                    errors.append(f"{relative}: {candidate_id} 为 IGNORE 但仍指定 Knowledge 目标")
            elif len(target_ids) != 1:
                errors.append(f"{relative}: {candidate_id} 必须指定一个 Knowledge 目标")
            else:
                target_id = next(iter(target_ids))
                if target_id not in run_knowledge_ids:
                    errors.append(f"{relative}: {candidate_id} 的 {target_id} 未列入 knowledge_ids")

        if run_status in {"completed", "backfilled"}:
            for source_id in run_source_ids:
                if source_id not in source_ids:
                    errors.append(f"{relative}: 已完成运行引用不存在的 Source id: {source_id}")
            for knowledge_id in run_knowledge_ids:
                if knowledge_id not in knowledge_ids:
                    errors.append(f"{relative}: 已完成运行引用不存在的 Knowledge id: {knowledge_id}")

        retry_of = metadata.get("retry_of")
        if isinstance(retry_of, str):
            ingest_run_retries[relative] = retry_of
        if isinstance(run_status, str):
            ingest_status_counts[run_status] += 1
        if run_status in {"completed", "backfilled"}:
            ingest_metric_totals.update(
                {
                    "runs": 1,
                    "sources": source_count,
                    "candidates": candidate_count,
                    "creates": declared_counts["CREATE"],
                    "reinforces": declared_counts["REINFORCE"],
                    "updates": declared_counts["UPDATE"],
                    "conflicts": declared_counts["CONFLICT"],
                    "ignores": declared_counts["IGNORE"],
                    "weak_matches": weak_match_count,
                    "single_source_creates": single_source_create_count,
                    "externally_verified_sources": externally_verified_source_count,
                    "validation_warnings": validation_warning_count,
                }
            )
        validate_links(repo_root, path, text, errors)

    for relative, retry_of in ingest_run_retries.items():
        if retry_of not in ingest_run_ids:
            errors.append(f"{relative}: retry_of 引用不存在的 Ingest Run: {retry_of}")

    for canonical_url, paths in canonical_urls.items():
        if len(paths) > 1:
            warnings.append(f"canonical_url 重复，需确认是否为版本关系: {canonical_url} -> {paths}")

    catalog_path = repo_root / "index/catalog.md"
    catalog_text = catalog_path.read_text(encoding="utf-8")
    catalog_entries = [Path(value.strip()) for value in CATALOG_PATH.findall(catalog_text)]
    counts = Counter(catalog_entries)
    knowledge_relatives = {path.relative_to(repo_root) for path in knowledge_files}
    for entry, count in counts.items():
        if not (repo_root / entry).is_file():
            errors.append(f"index/catalog.md: Path 不存在: {entry}")
        if count > 1:
            errors.append(f"index/catalog.md: Path 重复 {count} 次: {entry}")
    for missing_entry in sorted(knowledge_relatives - set(catalog_entries)):
        errors.append(f"index/catalog.md: 未收录 Knowledge: {missing_entry}")
    validate_links(repo_root, catalog_path, catalog_text, errors)
    errors.extend(git_source_mutations(repo_root))

    if warnings:
        print("警告：")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("验证失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"验证通过：{len(source_files)} 个 Source，{len(knowledge_files)} 个 Knowledge，"
        f"{len(catalog_entries)} 个目录条目，{len(ingest_run_files)} 个 Ingest Run；"
        "元数据、引用、决策计数、目录覆盖和 Source 不可变性均正常。"
    )
    candidates = ingest_metric_totals["candidates"]
    sources = ingest_metric_totals["sources"]
    create_rate = (
        f"{ingest_metric_totals['creates'] / candidates:.1%}" if candidates else "n/a"
    )
    verified_rate = (
        f"{ingest_metric_totals['externally_verified_sources'] / sources:.1%}"
        if sources
        else "n/a"
    )
    print(
        "Ingest 趋势："
        f"完成/回补 {ingest_metric_totals['runs']}，失败 {ingest_status_counts['failed']}，"
        f"Source {sources}，候选 {candidates}，CREATE 率 {create_rate}，"
        f"弱匹配 {ingest_metric_totals['weak_matches']}，"
        f"单一来源 CREATE {ingest_metric_totals['single_source_creates']}，"
        f"外部验证覆盖 {verified_rate}，历史校验警告 {ingest_metric_totals['validation_warnings']}。"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
