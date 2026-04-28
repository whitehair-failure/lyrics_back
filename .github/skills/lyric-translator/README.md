# lyric-translator-skill

> **Agent Skill** — Translates song lyrics between Chinese (ZH), Japanese (JA), Korean (KO), and English (EN) in `.lrc` timed-lyrics format.

All **12 direction pairs** supported: EN↔JA · EN↔KO · EN↔ZH · JA↔KO · JA↔ZH · KO↔ZH

| Language | Docs |
|---|---|
| 中文 | [README.zh.md](README.zh.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 한국어 | [README.ko.md](README.ko.md) |

---

## Install

### npm path

```bash
npx skills add lyric-translator-skill
```

### GitHub path

```bash
npx skills add YOUR_USERNAME/lyric-translator-skill
```

### Scope options

**Workspace-scoped** (recommended — applies to current project only):

```bash
npx skills add lyric-translator-skill --scope workspace
```

Installs to `.github/skills/lyric-translator/` in your current directory.

**User-scoped** (applies to all your projects):

```bash
npx skills add lyric-translator-skill --scope user
```

Installs to `~/.agents/skills/lyric-translator/`.

#### Manual install (no CLI required)

```bash
git clone https://github.com/YOUR_USERNAME/lyric-translator-skill.git
# workspace-scoped
mkdir -p .github/skills/lyric-translator
cp -r lyric-translator-skill/SKILL.md lyric-translator-skill/reference \
       .github/skills/lyric-translator/
```

---

## Supported Translation Pairs

| Direction | Source | Target |
|:---:|:---:|:---:|
| EN → JA | English | Japanese |
| EN → KO | English | Korean |
| EN → ZH | English | Chinese |
| JA → EN | Japanese | English |
| JA → KO | Japanese | Korean |
| JA → ZH | Japanese | Chinese |
| KO → EN | Korean | English |
| KO → JA | Korean | Japanese |
| KO → ZH | Korean | Chinese |
| ZH → EN | Chinese | English |
| ZH → JA | Chinese | Japanese |
| ZH → KO | Chinese | Korean |

---

## Usage

Once installed, Agent activates this skill automatically when you use phrases like:

- `translate lyrics`, `bilingual subtitles`, `lrc translation`
- `j-pop lyrics`, `k-pop lyrics`, `c-pop lyrics`
- `번역` (KO) · `翻訳` (JA) · `翻译` (ZH)

### Example prompts

```
Translate this .lrc file to Japanese
Add Korean subtitles to these Chinese lyrics
英訳して — translate these JA lyrics to English
这首歌翻译成中文
```

---

## Output Format

Each source lyric line gets a same-timestamp translation line inserted immediately below it, producing a strict alternating bilingual layout:

```lrc
[01:23.45]愛してる
[01:23.45]I love you
[01:28.00]夢の中で会おう
[01:28.00]Let's meet in a dream
```

Timestamps, metadata lines (`[ti:]` `[ar:]` `[al:]` etc.), blank lines, and sound-effect lines (`♪`) are never modified.

---

## Package Contents

```
lyric-translator-skill/
├── SKILL.md              ← Entry point (loaded first by Copilot)
└── reference/
    ├── common.md         ← Shared rules for all 12 pairs
    ├── en2ja.md
    ├── en2ko.md
    ├── en2zh.md
    ├── ja2en.md
    ├── ja2ko.md
    ├── ja2zh.md
    ├── ko2en.md
    ├── ko2ja.md
    ├── ko2zh.md
    ├── zh2en.md
    ├── zh2ja.md
    └── zh2ko.md
```

---

## License

MIT
