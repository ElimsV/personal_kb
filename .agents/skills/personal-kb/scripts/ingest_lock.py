#!/usr/bin/env python3
"""Manage the repository-wide exclusive lock used by Personal KB INGEST."""

from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


LOCK_RELATIVE_PATH = Path(".kb-locks/ingest.lock")
METADATA_NAME = "owner.json"
DEFAULT_STALE_SECONDS = 7200


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / "index/catalog.md").is_file():
            return candidate
    raise RuntimeError("无法定位个人知识库根目录")


def lock_paths(repo_root: Path) -> tuple[Path, Path]:
    lock_dir = repo_root / LOCK_RELATIVE_PATH
    return lock_dir, lock_dir / METADATA_NAME


def read_metadata(metadata_path: Path) -> dict[str, object]:
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError) as exc:
        return {"metadata_error": str(exc)}


def lock_age_seconds(lock_dir: Path, metadata: dict[str, object]) -> int:
    raw = metadata.get("last_heartbeat") or metadata.get("started_at")
    if isinstance(raw, str):
        try:
            stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return max(0, int((utc_now() - stamp).total_seconds()))
        except ValueError:
            pass
    try:
        return max(0, int(utc_now().timestamp() - lock_dir.stat().st_mtime))
    except OSError:
        return 0


def lock_status(lock_dir: Path, metadata_path: Path, stale_after: int) -> dict[str, object]:
    if not lock_dir.is_dir():
        return {"status": "unlocked", "lock": str(lock_dir)}
    metadata = read_metadata(metadata_path)
    age = lock_age_seconds(lock_dir, metadata)
    return {
        "status": "locked",
        "lock": str(lock_dir),
        "age_seconds": age,
        "suspected_stale": age >= stale_after,
        "owner": metadata,
    }


def write_metadata(metadata_path: Path, metadata: dict[str, object]) -> None:
    temporary = metadata_path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, metadata_path)


def require_owner(metadata_path: Path, supplied_owner: str) -> dict[str, object]:
    metadata = read_metadata(metadata_path)
    recorded_owner = metadata.get("owner_token")
    if not recorded_owner or recorded_owner != supplied_owner:
        raise PermissionError("owner token 不匹配，拒绝修改或释放锁")
    return metadata


def command_acquire(args: argparse.Namespace, repo_root: Path) -> int:
    lock_dir, metadata_path = lock_paths(repo_root)
    lock_dir.parent.mkdir(parents=True, exist_ok=True)
    try:
        lock_dir.mkdir()
    except FileExistsError:
        print(json.dumps(lock_status(lock_dir, metadata_path, args.stale_after), ensure_ascii=False))
        return 2

    token = args.owner or str(uuid.uuid4())
    now = isoformat(utc_now())
    metadata: dict[str, object] = {
        "owner_token": token,
        "description": args.description,
        "host": socket.gethostname(),
        "pid_at_acquire": os.getpid(),
        "started_at": now,
        "last_heartbeat": now,
        "repo_root": str(repo_root),
    }
    try:
        write_metadata(metadata_path, metadata)
    except Exception:
        lock_dir.rmdir()
        raise
    print(json.dumps({"status": "acquired", **metadata}, ensure_ascii=False))
    return 0


def command_status(args: argparse.Namespace, repo_root: Path) -> int:
    lock_dir, metadata_path = lock_paths(repo_root)
    print(json.dumps(lock_status(lock_dir, metadata_path, args.stale_after), ensure_ascii=False))
    return 0


def command_heartbeat(args: argparse.Namespace, repo_root: Path) -> int:
    lock_dir, metadata_path = lock_paths(repo_root)
    if not lock_dir.is_dir():
        print(json.dumps({"status": "unlocked", "error": "锁不存在"}, ensure_ascii=False))
        return 2
    try:
        metadata = require_owner(metadata_path, args.owner)
    except PermissionError as exc:
        print(json.dumps({"status": "refused", "error": str(exc)}, ensure_ascii=False))
        return 3
    metadata["last_heartbeat"] = isoformat(utc_now())
    write_metadata(metadata_path, metadata)
    print(json.dumps({"status": "heartbeat", "owner_token": args.owner}, ensure_ascii=False))
    return 0


def command_release(args: argparse.Namespace, repo_root: Path) -> int:
    lock_dir, metadata_path = lock_paths(repo_root)
    if not lock_dir.is_dir():
        print(json.dumps({"status": "unlocked", "lock": str(lock_dir)}, ensure_ascii=False))
        return 0
    try:
        require_owner(metadata_path, args.owner)
    except PermissionError as exc:
        print(json.dumps({"status": "refused", "error": str(exc)}, ensure_ascii=False))
        return 3
    metadata_path.unlink(missing_ok=True)
    temporary = metadata_path.with_suffix(".tmp")
    temporary.unlink(missing_ok=True)
    try:
        lock_dir.rmdir()
    except OSError as exc:
        print(json.dumps({"status": "error", "error": f"锁目录未清空: {exc}"}, ensure_ascii=False))
        return 1
    try:
        lock_dir.parent.rmdir()
    except OSError:
        pass
    print(json.dumps({"status": "released", "owner_token": args.owner}, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="管理 Personal KB 的 INGEST 独占写锁")
    parser.add_argument("--repo", type=Path, help="知识库根目录；默认自动定位")
    parser.add_argument(
        "--stale-after",
        type=int,
        default=DEFAULT_STALE_SECONDS,
        help="多少秒无心跳后只标记为疑似失效；不会自动清锁",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    acquire = subparsers.add_parser("acquire", help="原子获取写锁")
    acquire.add_argument("--owner", help="可选 owner token；省略时自动生成")
    acquire.add_argument("--description", default="Personal KB INGEST")

    subparsers.add_parser("status", help="查看锁状态")

    heartbeat = subparsers.add_parser("heartbeat", help="更新锁心跳")
    heartbeat.add_argument("--owner", required=True)

    release = subparsers.add_parser("release", help="释放自己持有的锁")
    release.add_argument("--owner", required=True)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = (args.repo.resolve() if args.repo else find_repo_root(Path.cwd().resolve()))
    commands = {
        "acquire": command_acquire,
        "status": command_status,
        "heartbeat": command_heartbeat,
        "release": command_release,
    }
    try:
        return commands[args.command](args, repo_root)
    except (OSError, RuntimeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
