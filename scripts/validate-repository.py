#!/usr/bin/env python3
"""Validate the pre-build repository skeleton without privileges or network."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    ".gitattributes",
    ".gitignore",
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSE-DOCUMENTATION",
    "Makefile",
    "NOTICE",
    "README.md",
    "SECURITY.md",
    "docs/README.md",
    "docs/architecture.md",
    "docs/roadmap.md",
    "image/README.md",
    "infra/README.md",
    "kernel/README.md",
    "manifests/README.md",
    "packaging/README.md",
    "profile-assets/README.md",
    "scripts/README.md",
    "tests/README.md",
)
IGNORED_PARTS = {".git", "__pycache__"}
FORBIDDEN_PARTS = {"build", "cache", "dist", "downloads", "work"}
FORBIDDEN_SUFFIXES = (
    ".deb",
    ".img",
    ".img.xz",
    ".img.zst",
    ".pkg.tar.xz",
    ".pkg.tar.zst",
)
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "npm token": re.compile(r"\bnpm_[A-Za-z0-9]{20,}\b"),
    "Tailscale key": re.compile(r"\btskey-[A-Za-z0-9_-]{16,}\b"),
}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def repository_files() -> list[Path]:
    return sorted(
        (
            path
            for path in ROOT.rglob("*")
            if path.is_file()
            and not any(part in IGNORED_PARTS for part in path.relative_to(ROOT).parts)
        ),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def validate_docs(files: list[Path]) -> list[str]:
    failures: list[str] = []
    markdown = [path for path in files if path.suffix == ".md"]
    for path in markdown:
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().strip("<>")
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:"))
            ):
                continue
            target = unquote(target.split("#", 1)[0])
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                failures.append(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{path.relative_to(ROOT)}: missing link target: {target}")
    if not markdown:
        failures.append("repository has no Markdown documentation")
    return failures


def validate_repository(files: list[Path]) -> list[str]:
    failures: list[str] = []
    relative_files = {path.relative_to(ROOT).as_posix() for path in files}
    for required in REQUIRED_FILES:
        if required not in relative_files:
            failures.append(f"required file is missing: {required}")

    apache = ROOT / "LICENSE"
    if apache.is_file() and "Apache License" not in apache.read_text(encoding="utf-8"):
        failures.append("LICENSE is not the Apache License 2.0 text")
    docs_license = ROOT / "LICENSE-DOCUMENTATION"
    if docs_license.is_file() and "CC-BY-4.0" not in docs_license.read_text(encoding="utf-8"):
        failures.append("LICENSE-DOCUMENTATION does not declare CC-BY-4.0")

    for path in files:
        relative = path.relative_to(ROOT)
        relative_text = relative.as_posix()
        if any(part in FORBIDDEN_PARTS for part in relative.parts):
            failures.append(f"managed build output is present in source: {relative_text}")
        if relative_text.endswith(FORBIDDEN_SUFFIXES):
            failures.append(f"binary release artifact is present in source: {relative_text}")
        try:
            payload = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(payload):
                failures.append(f"{relative_text}: possible {label}")

    readme = ROOT / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        for required_phrase in (
            "尚未生成、发布或验证任何可刷写镜像",
            "Apache License 2.0",
            "Creative Commons Attribution 4.0",
        ):
            if required_phrase not in text:
                failures.append(f"README.md is missing status/license text: {required_phrase}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-only", action="store_true")
    args = parser.parse_args()
    files = repository_files()
    failures = validate_docs(files)
    if not args.docs_only:
        failures.extend(validate_repository(files))
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    scope = "documentation" if args.docs_only else "repository"
    print(f"{scope} validation passed ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
