#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import difflib
import os
import re
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Tuple


TS_EXTS = {".ts", ".tsx", ".js", ".jsx"}


@dataclass
class FileChange:
    path: str
    replaced_blocks: int
    inserted_t_import: bool


def _run_git(args: List[str], cwd: str) -> str:
    p = subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout


def _git_show(ref: str, path: str, cwd: str) -> Optional[str]:
    try:
        return _run_git(["show", f"{ref}:{path}"], cwd=cwd)
    except Exception:
        return None


def _git_diff_files(ref: str, paths: List[str], cwd: str) -> List[str]:
    out = _run_git(["diff", "--name-only", f"{ref}..HEAD", "--", *paths], cwd=cwd)
    files = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return files


_T_CALL_RE = re.compile(r"\bt\s*\(\s*(['\"])\s*([^'\"]+)\s*\1\s*\)")
_JSX_TAG_RE = re.compile(r"</?\s*[A-Za-z][A-Za-z0-9]*\b")
_JSX_TAG_NAME_RE = re.compile(r"</?\s*([A-Za-z][A-Za-z0-9]*)\b")


def _count_t_calls(lines: List[str]) -> int:
    return sum(1 for ln in lines if _T_CALL_RE.search(ln))


def _count_jsx_tags(lines: List[str]) -> int:
    return sum(len(_JSX_TAG_RE.findall(ln)) for ln in lines)


def _jsx_tag_names_in_line(line: str) -> set:
    return set(_JSX_TAG_NAME_RE.findall(line or ""))


def _block_similarity(a: List[str], b: List[str]) -> float:
    return difflib.SequenceMatcher(a=a, b=b).ratio()


def _has_t_import(text: str) -> bool:
    return bool(re.search(r"^\s*import\s+\{\s*t\s*\}\s+from\s+['\"][^'\"]+['\"];\s*$", text, flags=re.M))


def _build_t_import_line(file_path: str) -> str:
    # Compute relative import to src/i18n (index.ts exports t)
    # Example:
    #   src/views/Foo.tsx   -> ../i18n
    #   src/app/App.tsx     -> ../i18n
    #   src/Foo.tsx         -> ./i18n
    file_dir = os.path.dirname(file_path)
    rel = os.path.relpath("src/i18n", start=file_dir).replace(os.sep, "/")
    if not rel.startswith("."):
        rel = "./" + rel
    # import path should not include trailing "/index"
    return f"import {{ t }} from '{rel}';\n"


_IMPORT_FROM_LINE_RE = re.compile(r"\bfrom\s+['\"][^'\"]+['\"]\s*;?\s*$")
_IMPORT_SIDE_EFFECT_RE = re.compile(r"^\s*import\s+['\"][^'\"]+['\"]\s*;?\s*$")


def _find_import_stmt_end(lines: List[str], start_idx: int) -> int:
    i = start_idx
    n = len(lines)
    while i < n:
        ln = lines[i].rstrip("\n")
        if _IMPORT_SIDE_EFFECT_RE.match(ln):
            return i
        if _IMPORT_FROM_LINE_RE.search(ln):
            return i
        i += 1
    return start_idx


def _insert_import_after_imports(lines: List[str], import_line: str) -> Tuple[List[str], bool]:
    # Keep header comments, then imports, then insert.
    i = 0
    n = len(lines)

    # Skip shebang / encoding / leading comments / blank lines
    while i < n and (lines[i].startswith("#!") or lines[i].lstrip().startswith("//") or lines[i].strip() == ""):
        i += 1

    # Now consume import statement(s)
    last_import_end = None
    while i < n:
        if lines[i].lstrip().startswith("import "):
            end = _find_import_stmt_end(lines, i)
            last_import_end = end
            i = end + 1
            continue
        if lines[i].strip() == "":
            # allow blank lines inside import area
            i += 1
            continue
        break

    if last_import_end is None:
        insert_at = 0
    else:
        insert_at = last_import_end + 1

    # Insert only if not already present
    if any(import_line.strip() == ln.strip() for ln in lines):
        return lines, False

    new_lines = lines[:insert_at] + [import_line] + lines[insert_at:]
    new_text = "".join(new_lines)
    if re.search(r"(?m)^\s*import\s*\{\s*$\n\s*import\s+\{\s*t\s*\}\s+from\b", new_text):
        return lines, False
    return new_lines, True


def restore_file_from_ref(file_path: str, ref_text: str, head_text: str) -> Tuple[str, int, bool]:
    ref_lines = ref_text.splitlines(keepends=True)
    head_lines = head_text.splitlines(keepends=True)

    sm = difflib.SequenceMatcher(a=head_lines, b=ref_lines)
    opcodes = sm.get_opcodes()

    replaced_blocks = 0
    new_head_lines = list(head_lines)

    # Apply from back to front to keep indexes stable
    for tag, i1, i2, j1, j2 in reversed(opcodes):
        if tag != "replace":
            continue

        head_block = head_lines[i1:i2]
        ref_block = ref_lines[j1:j2]

        ref_t = _count_t_calls(ref_block)
        head_t = _count_t_calls(head_block)

        if ref_t == 0:
            continue

        # Only replace when ref has more t() calls than head in this block.
        if ref_t <= head_t:
            continue

        # Avoid processing huge blocks (still keep a safety cap)
        if (i2 - i1) > 200 or (j2 - j1) > 200:
            continue

        # Safer strategy: only replace individual lines that contain t('key') in ref.
        block_changed = False
        new_block = list(head_block)

        inner = difflib.SequenceMatcher(a=head_block, b=ref_block)
        for tag2, a1, a2, b1, b2 in inner.get_opcodes():
            if tag2 != "replace":
                continue

            hs = head_block[a1:a2]
            rs = ref_block[b1:b2]
            k = min(len(hs), len(rs))
            if k <= 0:
                continue

            for off in range(k):
                hln = hs[off]
                rln = rs[off]

                if _count_t_calls([rln]) == 0:
                    continue
                if _count_t_calls([hln]) > 0:
                    continue

                # Prevent structural JSX changes: require JSX tag name set to match.
                if _jsx_tag_names_in_line(hln) != _jsx_tag_names_in_line(rln):
                    continue

                new_block[a1 + off] = rln
                block_changed = True
                replaced_blocks += 1

        if block_changed:
            new_head_lines[i1:i2] = new_block

    new_text = "".join(new_head_lines)

    inserted_t_import = False
    if (_T_CALL_RE.search(new_text) is not None) and (not _has_t_import(new_text)):
        import_line = None
        # Prefer import line from ref if available
        m = re.search(
            r"^\s*import\s+\{\s*t\s*\}\s+from\s+(['\"])([^'\"]+)\1;\s*$",
            ref_text,
            flags=re.M,
        )
        if m:
            import_line = f"import {{ t }} from '{m.group(2)}';\n"
        else:
            import_line = _build_t_import_line(file_path)

        new_lines, inserted = _insert_import_after_imports(new_text.splitlines(keepends=True), import_line)
        new_text = "".join(new_lines)
        inserted_t_import = inserted

    return new_text, replaced_blocks, inserted_t_import


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Restore i18n t('key') usages that were overwritten during upgrade, "
            "by comparing current workspace with a git ref (e.g. backup-main-before-0.5.1)."
        )
    )
    parser.add_argument("--repo", default=".", help="Git repo root (default: current directory)")
    parser.add_argument("--ref", default="backup-main-before-0.5.1", help="Reference ref/branch/tag")
    parser.add_argument("--paths", nargs="+", default=["src"], help="Paths to scan (default: src)")
    parser.add_argument("--apply", action="store_true", help="Write changes to files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only (default)")
    parser.add_argument("--max-files", type=int, default=300, help="Safety limit")

    args = parser.parse_args()
    repo = os.path.abspath(args.repo)

    if not args.apply:
        args.dry_run = True

    files = _git_diff_files(args.ref, args.paths, cwd=repo)
    files = [f for f in files if os.path.splitext(f)[1] in TS_EXTS]
    files = files[: args.max_files]

    changes: List[FileChange] = []

    for path in files:
        abs_path = os.path.join(repo, path)
        if not os.path.isfile(abs_path):
            continue

        ref_text = _git_show(args.ref, path, cwd=repo)
        if ref_text is None:
            continue

        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                head_text = f.read()
        except Exception:
            continue

        new_text, replaced_blocks, inserted_import = restore_file_from_ref(path, ref_text, head_text)

        if replaced_blocks == 0 and not inserted_import:
            continue

        changes.append(FileChange(path=path, replaced_blocks=replaced_blocks, inserted_t_import=inserted_import))

        if args.apply:
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(new_text)

    print("=== restore_i18n_from_backup ===")
    print(f"ref: {args.ref}")
    print(f"apply: {args.apply}")
    print(f"files changed: {len(changes)}")
    print()

    for ch in changes:
        extra = " +import" if ch.inserted_t_import else ""
        print(f"- {ch.path}: replaced_blocks={ch.replaced_blocks}{extra}")

    if args.dry_run and not args.apply:
        print("\n(dry-run) No files were modified. Re-run with --apply to write changes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
