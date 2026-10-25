---
name: tencent-meeting-extract
description: 从腾讯会议录制页链接（meeting.tencent.com/cw/ 或 /crm/）提取 MP4 双流（屏幕流+说话人视窗流）并下载到本地。当用户给出腾讯会议录制链接、要求下载会议视频、或全量多模态会议处理遇到腾讯会议链接时使用。核心坑：裸 curl 和浏览器直接导航都会 403，必须带原始页面 Referer 请求 CDN 签名 URL。
metadata:
  short-description: 腾讯会议录制视频提取下载
---

# 腾讯会议录制视频提取

从腾讯会议录制分享页提取 MP4 直链（带 token 的 CDN 签名 URL）并完整下载屏幕流/说话人视窗流，供后续 ASR、抽帧、投屏重建使用。

## 为什么会 403（必读）

腾讯会议录制的 MP4 存在腾讯云 COS（ylz.cos.meeting.tencent.com），URL 带 token 签名，但 token 本身不是全部校验——CDN 还校验请求上下文：

1. **裸 curl 不带任何头** → 403（无 Referer/UA）。
2. **Chrome 直接在地址栏打开签名 URL** → 403（导航请求不带 Referer）。
3. **带 `Referer: https://meeting.tencent.com/cw/<code>` + 浏览器 UA 的请求** → 206 Partial Content，正常下载。

结论：**Referer 是关键**。UA 建议带 Chrome 真实 UA，Origin 可选。

## 提取流程

### 第 1 步：打开录制页，从 pageAssets 拿签名 URL

用 CUA 在浏览器（IAB 或 Chrome）打开 `https://meeting.tencent.com/cw/<code>`（/crm/ 会 302 到 /cw/），等播放器加载后执行：

```javascript
// cua_repl.js 中，browserId 视环境而定（IAB 为 "2"，Chrome 为 "1"）
const assets = await browser.pageAssets.list(tab.id, { browser: browserId });
const mp4s = assets.filter(a => a.url && a.url.includes('.mp4') && a.url.includes('token='));
// 通常有两条：recording-1_screen.mp4（屏幕流，大）和 recording-1_speaker.mp4（说话人视窗，小）
```

pageAssets 拿不到时降级方案：播放视频后从网络请求里找，或 `browser.tabs.list()` 里找已打开的 ylz.cos 域名标签。

### 第 2 步：用带 Referer 的 curl 下载

```bash
# 先 Range 试探确认 206 和 content-range（总大小）
curl -sS -r 0-0 -D - -o /dev/null \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36' \
  -H "Referer: https://meeting.tencent.com/cw/<code>" \
  "$MP4_URL"

# 确认 206 后全量下载
curl -sS -C - -o recording_screen.mp4 \
  -H 'User-Agent: ...同上...' \
  -H "Referer: https://meeting.tencent.com/cw/<code>" \
  "$MP4_URL"
```

或直接用脚本（见 scripts/tm_download.py）。

### 第 3 步：验证完整性

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=index,codec_type,codec_name,width,height \
  -of default=noprint_wrappers=1 recording_screen.mp4
```

核对：时长与会议实际时长一致（页面显示）、文件大小与 content-range 总长一致、双流时长一致。

## 已验证的环境事实（2026-09-07 会议实测）

- 本机有 TUN 代理（fake-ip 198.18.x.x，ALL_PROXY=socks5://127.0.0.1:1082），**带 Referer 的 curl 走代理也能成功**，无需绕过代理。
- 屏幕流 135.5MB 下载约 15 秒；说话人视窗 70.7MB 约 11 秒。
- 双流时长一致（同一时间轴）：`recording-1_screen.mp4` 与 `recording-1_speaker.mp4` 均为同一会议全长。
- **MP4 音轨可能比用户提供的 WAV 更完整**：WAV 可能是平台裁剪版（缺开头 26s）。优先用 MP4 音轨做 ASR 基准；WAV 用于交叉验证。
- 页面上的平台逐字稿时间轴与 MP4 时间轴一致（平台稿 00:01 ≈ MP4 0s）。

## 后续处理衔接

下载完成后交给 full-multimodal-meeting-processing：
- 音轨：`ffmpeg -i in.mp4 -vn -ac 1 -ar 16000 out.wav` → whisper-cli ASR。
- 视觉：场景检测定位共享边界（`select='gt(scene,0.15)'` 找强切换，0.04 找滚动变化），按变化点抽帧 + view_image 逐帧查看。
- 屏幕流里共享文档的滚动是低阈值事件（0.04），强切换（0.15）只找得到开始/结束共享；两者结合才能完整覆盖。
- 共享结束后的黑场不代表缺内容——确认是否有人在共享即可。

## 常见失败与降级

| 症状 | 原因 | 处理 |
|---|---|---|
| curl 403 | 没带 Referer | 加 `-H "Referer: https://meeting.tencent.com/cw/<code>"` |
| Chrome 打开 URL 403 | 导航请求不带 Referer | 正常现象，用带头的 curl |
| pageAssets 无 mp4 | 播放器未加载/未播放 | 先点播放让视频开始加载，再 list |
| 404 或签名过期 | token 有时效 | 刷新页面重新拿 URL |
| 下载中断 | 网络波动 | `curl -C -` 断点续传 |
