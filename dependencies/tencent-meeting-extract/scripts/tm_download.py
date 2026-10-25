#!/usr/bin/env python3
"""腾讯会议录制视频提取下载器。

用法:
    # 单流模式: 先从浏览器 pageAssets 拿到签名 URL 后
    python3 tm_download.py probe <mp4_url> <meeting_code>          # 试探(206/大小)
    python3 tm_download.py download <mp4_url> <meeting_code> -o out.mp4

    # 双流模式: 从录制页 HTML 里自动解析两条 MP4 URL
    python3 tm_download.py auto <page_url> -o outdir/

meeting_code 是 meeting.tencent.com/cw/<code> 里的 code。
核心: CDN 校验 Referer, 必须带 https://meeting.tencent.com/cw/<code>。
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


def extract_code(page_url: str) -> str:
    m = re.search(r"meeting\.tencent\.com/(?:cw|crm)/([A-Za-z0-9]+)", page_url)
    if not m:
        raise SystemExit(f"无法从 URL 提取会议 code: {page_url}")
    return m.group(1)


def referer_for(page_url: str) -> str:
    code = extract_code(page_url)
    return f"https://meeting.tencent.com/cw/{code}"


def curl_probe(mp4_url: str, referer: str) -> dict:
    """Range 0-0 试探, 返回 {status, total_size, content_type}."""
    cmd = [
        "curl", "-sS", "--max-time", "30", "-r", "0-0",
        "-D", "-", "-o", os.devnull,
        "-H", f"User-Agent: {UA}",
        "-H", f"Referer: {referer}",
        mp4_url,
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout
    status = None
    total = None
    ctype = None
    for line in out.splitlines():
        if line.startswith("HTTP/2 ") or line.startswith("HTTP/1.1 "):
            status = int(line.split()[1])
        low = line.lower()
        if low.startswith("content-range:"):
            m = re.search(r"/(\d+)\s*$", line)
            if m:
                total = int(m.group(1))
        if low.startswith("content-type:"):
            ctype = line.split(":", 1)[1].strip()
    return {"status": status, "total_size": total, "content_type": ctype}


def curl_download(mp4_url: str, referer: str, out_path: str) -> str:
    """带断点续传的全量下载."""
    cmd = [
        "curl", "--fail", "-sS", "--max-time", "2800", "-C", "-",
        "-o", out_path,
        "-H", f"User-Agent: {UA}",
        "-H", f"Referer: {referer}",
        mp4_url,
    ]
    rc = subprocess.run(cmd).returncode
    if rc != 0:
        raise SystemExit(f"curl 退出码 {rc}")
    return out_path


def fetch_page(page_url: str) -> str:
    """抓录制页 HTML(带浏览器头)."""
    req = urllib.request.Request(page_url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def find_mp4_urls(html: str) -> list:
    """从 HTML/内嵌 JSON 里找带 token 的 MP4 签名 URL."""
    # 页面数据通常在 window.__INITIAL_STATE__ 或内嵌 JSON 中, 直接全局正则
    pat = re.compile(
        r"https://[a-z0-9.]+\.cos\.meeting\.tencent\.com/[^\"'\s]+?\.mp4\?[^\"'\s]+"
    )
    urls = pat.findall(html)
    # 去重保序
    seen = set()
    uniq = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def ffprobe_check(path: str) -> dict:
    """验证下载文件时长/流信息."""
    cmd = ["ffprobe", "-v", "error",
           "-show_entries", "format=duration,size",
           "-show_entries", "stream=index,codec_type,codec_name,width,height",
           "-of", "json", path]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"error": "ffprobe 解析失败", "raw": out[:500]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("probe", help="Range 试探签名 URL")
    p1.add_argument("mp4_url")
    p1.add_argument("meeting_code", help="cw/<code> 里的 code 或完整页面 URL")

    p2 = sub.add_parser("download", help="下载单条 MP4")
    p2.add_argument("mp4_url")
    p2.add_argument("meeting_code")
    p2.add_argument("-o", "--output", required=True)

    p3 = sub.add_parser("auto", help="从录制页自动解析并下载双流")
    p3.add_argument("page_url")
    p3.add_argument("-o", "--outdir", default=".")

    args = ap.parse_args()

    if args.cmd == "probe":
        ref = (referer_for(args.meeting_code)
               if "meeting.tencent.com" in args.meeting_code
               else f"https://meeting.tencent.com/cw/{args.meeting_code}")
        info = curl_probe(args.mp4_url, ref)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        if info["status"] != 206:
            print("非 206: 检查 Referer 是否为 https://meeting.tencent.com/cw/<code>", file=sys.stderr)
            sys.exit(1)

    elif args.cmd == "download":
        ref = (referer_for(args.meeting_code)
               if "meeting.tencent.com" in args.meeting_code
               else f"https://meeting.tencent.com/cw/{args.meeting_code}")
        info = curl_probe(args.mp4_url, ref)
        if info["status"] != 206:
            print(f"试探失败 status={info['status']}, 不会下载", file=sys.stderr)
            sys.exit(1)
        path = curl_download(args.mp4_url, ref, args.output)
        print(json.dumps({"path": path, **ffprobe_check(path)}, ensure_ascii=False, indent=2))

    elif args.cmd == "auto":
        code = extract_code(args.page_url)
        ref = f"https://meeting.tencent.com/cw/{code}"
        html = fetch_page(args.page_url)
        urls = find_mp4_urls(html)
        if not urls:
            print("页面里没找到 MP4 URL; 可能需要先播放或用 pageAssets", file=sys.stderr)
            sys.exit(1)
        os.makedirs(args.outdir, exist_ok=True)
        results = []
        for u in urls:
            m = re.search(r"(recording-[\w-]+\.mp4)", u)
            name = m.group(1) if m else f"stream_{len(results)}.mp4"
            out = os.path.join(args.outdir, name)
            print(f"下载 {name} ...", file=sys.stderr)
            curl_download(u, ref, out)
            results.append({"name": name, "path": out, **ffprobe_check(out)})
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
