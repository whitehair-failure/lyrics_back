---
name: lyric-translator
description: "Use when translating song lyrics between Chinese (ZH), Japanese (JA), Korean (KO), and English (EN) in .lrc files. Supports all 12 direction combinations. Inserts same-timestamp translation lines in strict alternating format, preserving LRC structure."
version: 3.0.0
scopes: ["workspace"]
tags: ["lyrics", "translation", "lrc", "zh", "ja", "ko", "en", "inline-translation", "karaoke", "timed-lyrics", "localization", "transcreation", "j-pop", "k-pop", "c-pop"]
---

# 歌词双语交替翻译技能（统一入口）

**目标：** 编辑现有 `.lrc` 歌词文件，在每行源语歌词下方插入同时间戳的目标语译文，形成"原文—译文"严格交替的双语字幕格式。支持中/日/韩/英四种语言的全部 12 种翻译方向。

---

## 使用方法：每次翻译前必须加载两个文件

执行翻译前，**必须**按以下两步加载规则文件：

1. **加载通用规则**：读取本技能目录下的 `reference/common.md`（格式保护、工作流、红线约束，适用于所有翻译方向）。
2. **加载专项规则**：根据翻译方向，在下表中找到对应文件并读取。

两个文件均加载完毕后，再开始实际翻译操作。

---

## 语言对识别与专项规则文件对照表

| 翻译方向 | 源语言 | 目标语言 | 专项规则文件 |
|:---:|:---:|:---:|:---:|
| EN → JA | 英语 | 日语 | `reference/en2ja.md` |
| EN → KO | 英语 | 韩语 | `reference/en2ko.md` |
| EN → ZH | 英语 | 中文 | `reference/en2zh.md` |
| JA → EN | 日语 | 英语 | `reference/ja2en.md` |
| JA → KO | 日语 | 韩语 | `reference/ja2ko.md` |
| JA → ZH | 日语 | 中文 | `reference/ja2zh.md` |
| KO → EN | 韩语 | 英语 | `reference/ko2en.md` |
| KO → JA | 韩语 | 日语 | `reference/ko2ja.md` |
| KO → ZH | 韩语 | 中文 | `reference/ko2zh.md` |
| ZH → EN | 中文 | 英语 | `reference/zh2en.md` |
| ZH → JA | 中文 | 日语 | `reference/zh2ja.md` |
| ZH → KO | 中文 | 韩语 | `reference/zh2ko.md` |

---

## 翻译方向自动识别规则

若用户未明确指定翻译方向，按以下优先级识别：

1. **用户指令**：如"翻译成日语"、"translate to English"、"한국어로 번역"等明确指令，优先采用。
2. **文件名提示**：文件名含 `ja`/`jp`、`ko`/`kr`、`zh`/`cn`、`en` 等语言标识。
3. **歌词内容检测**：读取文件前几行歌词，识别字符系统：
   - 平假名/片假名大量出现 → 日语源文
   - 韩文字母（한글）→ 韩语源文
   - 拉丁字母为主 → 英语源文
   - 汉字为主且无假名/韩文 → 中文源文
4. **歧义处理**：若无法自动识别，向用户询问后再开始。

---

## 通用原则（加载 reference/common.md 后生效）

- **先读后写**：第一步必须完整读取目标 `.lrc` 文件，禁止边读边写。
- **全文分析**：在内存中完成全曲分析（情绪/视角/副歌统一）后，再统一写入。
- **严格交替格式**：每行源语下方只能有一行同时间戳译文，禁止叠加第三行。
- 所有格式约束、工作流步骤、特殊行处理，均见 `reference/common.md`。
