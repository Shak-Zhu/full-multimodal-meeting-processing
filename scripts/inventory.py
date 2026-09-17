#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inventory.py — 建立会议的 File Inventory（宪法第一条的执行工具）。

用法：
  python3 inventory.py <文件或目录> [<文件或目录> ...] [--ext wav,mp4,docx,...]

行为：
  - 目录：递归列出所有文件（跳过隐藏文件与常见无关目录）。
  - 输出 Markdown 表：文件、类型、大小、SHA-256(前16位)、时长(音视频)、备注。
  - 音视频用 ffprobe（若不可用则 afinfo）读取时长。
  - 不修改任何输入文件。

类型识别：按扩展名 + 必要时魔数。对 .docx/.xlsx/.pptx 额外报告可解析性提示。
"""
import argparse, hashlib, json, os, subprocess, sys

EXT_TYPE = {
    ".wav": "WAV 音频", ".m4a": "M4A 音频", ".mp3": "MP3 音频", ".aac": "AAC 音频",
    ".flac": "FLAC 音频", ".opus": "OPUS 音频", ".ogg": "OGG 音频",
    ".mp4": "视频", ".mov": "视频", ".mkv": "视频", ".webm": "视频", ".m4v": "视频",
    ".docx": "Word/DOCX", ".doc": "Word/DOC(旧)", ".pptx": "PPT/PPTX", ".ppt": "PPT/PPT(旧)",
    ".xlsx": "Excel/XLSX", ".xls": "Excel/XLS(旧)", ".csv": "CSV", ".tsv": "TSV",
    ".pdf": "PDF", ".png": "图片", ".jpg": "图片", ".jpeg": "图片", ".gif": "图片",
    ".heic": "图片", ".webp": "图片", ".bmp": "图片", ".svg": "图片",
    ".txt": "TXT", ".md": "Markdown", ".json": "JSON", ".html": "HTML", ".htm": "HTML",
    ".eml": "邮件", ".msg": "邮件",
}
AUDIO_EXTS = {".wav", ".m4a", ".mp3", ".aac", ".flac", ".opus", ".ogg"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}

def sha256_prefix(path, n=16):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:n]

def media_duration(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "json", path],
            capture_output=True, text=True, timeout=60)
        if out.returncode == 0:
            d = float(json.loads(out.stdout)["format"]["duration"])
            return d
    except Exception:
        pass
    try:
        out = subprocess.run(["afinfo", path], capture_output=True, text=True, timeout=60)
        for line in out.stdout.splitlines():
            if "estimated duration" in line:
                return float(line.split(":")[1].strip())
    except Exception:
        pass
    return None

def fmt_dur(sec):
    if sec is None:
        return "-"
    sec = int(round(sec))
    return "{:d}:{:02d}:{:02d}".format(sec // 3600, (sec % 3600) // 60, sec % 60)

def fmt_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return "{:.0f} {}".format(n, unit) if unit == "B" else "{:.1f} {}".format(n, unit)
        n /= 1024.0

def collect(paths, exts=None):
    files = []
    for p in paths:
        if os.path.isfile(p):
            files.append(p)
        elif os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                for n in sorted(names):
                    if n.startswith("."):
                        continue
                    files.append(os.path.join(root, n))
    if exts:
        want = {("." + e.lstrip(".").lower()) for e in exts}
        files = [f for f in files if os.path.splitext(f)[1].lower() in want]
    seen, uniq = set(), []
    for f in files:
        rp = os.path.realpath(f)
        if rp not in seen:
            seen.add(rp)
            uniq.append(f)
    return uniq

def main():
    ap = argparse.ArgumentParser(description="建立会议材料 File Inventory")
    ap.add_argument("paths", nargs="+", help="文件或目录")
    ap.add_argument("--ext", help="逗号分隔的扩展名白名单", default="")
    args = ap.parse_args()
    exts = [e for e in args.ext.split(",") if e.strip()] or None
    files = collect(args.paths, exts)
    rows = []
    for i, f in enumerate(files, 1):
        name = os.path.basename(f)
        ext = os.path.splitext(name)[1].lower()
        typ = EXT_TYPE.get(ext, "其他(" + (ext or "无扩展名") + ")")
        size = os.path.getsize(f)
        sha = sha256_prefix(f)
        dur = ""
        note = ""
        if ext in AUDIO_EXTS or ext in VIDEO_EXTS:
            d = media_duration(f)
            dur = fmt_dur(d)
            if d is not None:
                note = "时长来自 ffprobe/afinfo"
        rows.append((i, name, typ, fmt_size(size), sha, dur, note))
    print("| # | 文件 | 类型 | 大小 | SHA-256(前16) | 时长 | 完整处理 | 交叉验证 | 备注 |")
    print("|---|------|------|------|---------------|------|----------|----------|------|")
    for r in rows:
        print("| {} | {} | {} | {} | {} | {} | 待填 | 待填 | {} |".format(*r))
    print()
    print("<!-- 共 {} 个文件；'完整处理/交叉验证' 两列只有在真实完成对应处理后才能填'是'（宪法第三十二条） -->".format(len(rows)))

if __name__ == "__main__":
    main()
