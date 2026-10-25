#!/usr/bin/env python3
"""Verify every file listed in the package SHA256SUMS manifest."""
from pathlib import Path
import hashlib
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    failures = []
    entries = (root / 'SHA256SUMS').read_text(encoding='utf-8').splitlines()
    for line in entries:
        expected, name = line.split('  ', 1)
        path = (root / name).resolve()
        if root not in path.parents or not path.is_file():
            failures.append(f'缺失或无效路径：{name}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            failures.append(f'内容不一致：{name}')
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        return 1
    print(f'通过：{len(entries)} 个文件 SHA-256 一致（不含清单自身）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
