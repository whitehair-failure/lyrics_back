---
name: lyric-translator
description: "Use when translating song lyrics between Chinese (ZH), Japanese (JA), Korean (KO), and English (EN) in .lrc files. Supports all 12 direction pairs: EN↔JA, EN↔KO, EN↔ZH, JA↔KO, JA↔ZH, KO↔ZH. Trigger phrases: translate lyrics, bilingual subtitles, lrc translation, j-pop lyrics, k-pop lyrics, c-pop lyrics, 번역, 翻訳, 翻译."
version: 3.1.0
argument-hint: "translation direction (e.g. 'to Japanese', 'en→ko', 'Chinese')"
scopes: ["workspace"]
tags: ["lyrics", "translation", "lrc", "zh", "ja", "ko", "en", "inline-translation", "karaoke", "timed-lyrics", "localization", "transcreation", "j-pop", "k-pop", "c-pop"]
---

# Lyric Translator — Bilingual Interleaved .lrc

Edits an existing `.lrc` file by inserting a same-timestamp target-language line directly below each source lyric line, producing a strict alternating bilingual format. Supports all 12 direction pairs across Chinese, Japanese, Korean, and English.

---

## Required: Load Two Files Before Starting

Every session, **before reading or editing any `.lrc` file**, load both files:

1. **Shared rules** → `read_file("reference/common.md")`  
   Format protection, workflow, Red Lines, special-line handling — applies to all 12 pairs.

2. **Pair-specific rules** → `read_file("reference/{pair}.md")` — use the dispatch table below.  
   Linguistic transformation rules, line-length caps, and direction-specific examples.

---

## Direction Detection → Dispatch

If the user does not specify a direction, detect it with the priority order below, then load the matching file.

### Detection Priority

| Priority | Source | Signal |
|:---:|---|---|
| 1 | Explicit user instruction | "translate to Japanese", "한국어로", "翻成中文", "英訳して" |
| 2 | Filename hint | filename contains `ja`/`jp`, `ko`/`kr`, `zh`/`cn`, `en` |
| 3 | Content detection | Read first 5 lyric lines: hiragana/katakana → JA source; Hangul → KO source; mostly Latin → EN source; CJK without kana/hangul → ZH source |
| 4 | Ask user | Cannot determine direction → ask before proceeding |

### Dispatch Table

| Direction | Source | Target | Load |
|:---:|:---:|:---:|:---|
| EN → JA | English | Japanese | `reference/en2ja.md` |
| EN → KO | English | Korean | `reference/en2ko.md` |
| EN → ZH | English | Chinese | `reference/en2zh.md` |
| JA → EN | Japanese | English | `reference/ja2en.md` |
| JA → KO | Japanese | Korean | `reference/ja2ko.md` |
| JA → ZH | Japanese | Chinese | `reference/ja2zh.md` |
| KO → EN | Korean | English | `reference/ko2en.md` |
| KO → JA | Korean | Japanese | `reference/ko2ja.md` |
| KO → ZH | Korean | Chinese | `reference/ko2zh.md` |
| ZH → EN | Chinese | English | `reference/zh2en.md` |
| ZH → JA | Chinese | Japanese | `reference/zh2ja.md` |
| ZH → KO | Chinese | Korean | `reference/zh2ko.md` |

---

All workflow steps, format constraints, Red Lines, and special-line handling are defined in `reference/common.md`. All pair-specific rules (line-length caps, romanization, tone/register, linguistic examples) are in the matching `reference/{pair}.md`.
