#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verbatim.py — 解析会议平台导出的逐字稿（TicNote 类），重建发言人归属并输出逐字稿骨架。

适用输入格式（TicNote 逐字稿 .docx 转出的文本）：
  ● SPEAKER_00 | 00:00:00
  发言文本（可多行）
  - - - - - - - - - - - - - - - - - - -
  段与段之间以分隔线分开；偶发段落直接标注真名（如 ● 心洋 | 00:02:00）。

用法：
  1) 先用 python-docx 或 textutil 把 .docx 转成纯文本：
       textutil -convert txt -stdout 逐字稿.docx > raw.txt
     （或 python -c "from docx import Document; ..."）
  2) 按本场会议修改下方 CONFIG 区的发言人映射规则。
  3) python3 verbatim.py raw.txt > part2_draft.md

输出：
  - 按时间分节的逐字稿骨架（原话保留，不摘要/润色/删除）
  - 全局术语纠正（GLOBAL_FIX，仅限"可确认的同音错字"，全部须登记修正对照表）
  - 行内标注（INLINE_NOTE：〔疑似：…〕〔待确认…〕〔用户纠正…〕）
  - 静音/休息区插入提示块（GAP 配置）

宪法约束提醒：
  - 逐字稿不得摘要、改写、删除口头语/重复/插话（宪法第十七条）
  - 发言人归属存疑处必须标注，不得默默合并（见 lessons-learned 第 4 条）
  - 所有修正必须写进最终文件的"修正对照表"（见 lessons-learned 第 6 条）
"""
import re
import sys

CONFIG = {
    # 发言人映射：按"时间段 + 内容逻辑"重归属。
    # 默认规则需按每场会议单独论证后修改（见 lessons-learned 第 4 条）。
    "default_speaker_map": {
        # "SPEAKER_00": "学员",
        # "SPEAKER_01": "导师",
    },
    # 分段时间点（秒）：某时间点之后切换映射（休息后 ASR track 含义可能变化）
    # "phase_breaks": [(2460, {"SPEAKER_02": "学员"})],
    # 静音/休息区（秒）：在该时间点前插入提示块
    # "gaps": [(2216, 2500, "00:36:56–00:41:40 休息空档，独立 ASR 输出静音幻觉文本，无有效语音")],
    # 全局术语纠正（仅限可确认的同音错字；每条都要进修正对照表）
    "global_fix": [
        # ("Daau", "DAU"), ("Gmv", "GMV"),
    ],
    # 行内标注：(时间戳秒, 原文子串, 替换后文本)
    "inline_note": [
        # (2700, "刘红军", "刘红军〔疑似：New Homepage——双引擎互证+知识库无人物记录〕"),
    ],
    # 分节标题：(起始秒, 标题)。留空则不分节。
    "sections": [
        # (0, "00:00:00 — 开场"),
    ],
}

HEADER_NOTE = """> **本部分说明（必读）**
>
> 1. 以下逐字稿以平台原始转写为底本，**未做摘要、改写、润色**；口头语、重复、自我修正、插话均原样保留（宪法第十七条）。
> 2. 发言人归属已按"时间段 + 对话结构 + 独立 ASR 交叉"重建；无法可靠判断的段落标注"（发言人归属存疑）"。
> 3. 可确认的 ASR 同音术语错误已就地纠正并全部登记于"修正对照表"；无法确认的内容保留原文并加〔待确认/疑似：…〕标记。
> 4. 时间戳为平台转写标注的段落起始时间。
"""

def parse(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    utts, cur = [], None
    for ln in lines:
        ln = ln.rstrip()
        if not ln or set(ln) <= {"-", " "}:
            continue
        if ln.startswith("—— 内容由"):
            continue
        m = re.match(r"^● (\S+) \| (\d\d):(\d\d):(\d\d)$", ln)
        if m:
            if cur and cur["text"]:
                utts.append(cur)
            ts = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
            cur = {"sp": m.group(1), "ts": ts, "text": ""}
            continue
        if cur is None:
            continue
        t = ln.strip()
        if not t or t.startswith("生成时间") or t.endswith("_transcript") or t == "转录内容":
            continue
        if not cur["text"]:
            cur["text"] = t
        else:
            last = cur["text"][-1]
            if re.match(r"^[A-Za-z0-9]", t) or re.match(r"[A-Za-z0-9]$", last):
                cur["text"] += " " + t
            else:
                cur["text"] += t
    if cur and cur["text"]:
        utts.append(cur)
    return utts

def fmt_ts(s):
    return "{:02d}:{:02d}:{:02d}".format(int(s // 3600), int(s % 3600 // 60), int(s % 60))

def map_speaker(u, cfg):
    sp, ts = u["sp"], u["ts"]
    # 真名标注直接保留
    if sp not in (set(cfg.get("default_speaker_map", {})) | {"SPEAKER_00", "SPEAKER_01", "SPEAKER_02", "SPEAKER_03"}):
        return sp
    mapping = dict(cfg.get("default_speaker_map", {}))
    for brk, extra in cfg.get("phase_breaks", []) or []:
        if ts >= brk:
            mapping.update(extra)
    return mapping.get(sp, sp + "（发言人归属存疑）")

def section_for(ts, sections):
    cur = None
    for start, title in sections:
        if ts >= start:
            cur = title
        else:
            break
    return cur

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    utts = parse(sys.argv[1])
    cfg = CONFIG
    print("<!-- UTTERANCES: {} -->".format(len(utts)), file=sys.stderr)
    out = [HEADER_NOTE, ""]
    gaps = sorted(cfg.get("gaps", []) or [])
    gap_idx = 0
    sections = cfg.get("sections", []) or []
    cur_sec = None
    for u in utts:
        ts = u["ts"]
        while gap_idx < len(gaps) and ts >= gaps[gap_idx][0]:
            g0, g1, gnote = gaps[gap_idx]
            out.append("> **【静音/空档区 {}–{}】** {}".format(fmt_ts(g0), fmt_ts(g1), gnote))
            out.append("")
            gap_idx += 1
        txt = u["text"]
        for a, b in cfg.get("global_fix", []):
            txt = txt.replace(a, b)
        for nts, src, dst in cfg.get("inline_note", []):
            if abs(ts - nts) <= 8 and src in txt:
                txt = txt.replace(src, dst)
        sec = section_for(ts, sections)
        if sec and sec != cur_sec:
            cur_sec = sec
            out.append("## " + sec)
            out.append("")
        out.append("**{}**〔{}〕：{}".format(map_speaker(u, cfg), fmt_ts(ts), txt))
        out.append("")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
