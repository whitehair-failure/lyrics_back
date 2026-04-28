# lyric-translator-skill

> **Agent Skill** — 在中文（ZH）、日语（JA）、韩语（KO）、英语（EN）之间翻译 `.lrc` 歌词文件。

支持全部 **12 个方向对**：EN↔JA · EN↔KO · EN↔ZH · JA↔KO · JA↔ZH · KO↔ZH

| 语言 | 文档 |
|---|---|
| English | [README.md](README.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 한국어 | [README.ko.md](README.ko.md) |

---

## 安装

### npm 路径

```bash
npx skills add lyric-translator-skill
```

### GitHub 路径

```bash
npx skills add YOUR_USERNAME/lyric-translator-skill
```

### 安装范围选项

**工作区级**（推荐 — 仅对当前项目生效）：

```bash
npx skills add lyric-translator-skill --scope workspace
```

Skill 文件将安装至当前目录下的 `.github/skills/lyric-translator/`。

**用户级**（对所有项目生效）：

```bash
npx skills add lyric-translator-skill --scope user
```

Skill 文件将安装至 `~/.agents/skills/lyric-translator/`。

#### 手动安装（无需 CLI）

```bash
git clone https://github.com/YOUR_USERNAME/lyric-translator-skill.git
# 工作区级
mkdir -p .github/skills/lyric-translator
cp -r lyric-translator-skill/SKILL.md lyric-translator-skill/reference \
       .github/skills/lyric-translator/
```

---

## 支持的翻译方向

| 方向 | 源语言 | 目标语言 |
|:---:|:---:|:---:|
| EN → JA | 英语 | 日语 |
| EN → KO | 英语 | 韩语 |
| EN → ZH | 英语 | 中文 |
| JA → EN | 日语 | 英语 |
| JA → KO | 日语 | 韩语 |
| JA → ZH | 日语 | 中文 |
| KO → EN | 韩语 | 英语 |
| KO → JA | 韩语 | 日语 |
| KO → ZH | 韩语 | 中文 |
| ZH → EN | 中文 | 英语 |
| ZH → JA | 中文 | 日语 |
| ZH → KO | 中文 | 韩语 |

---

## 使用方法

安装后，当你在提示词中使用以下词语时，Agent 会自动激活此 skill：

- `translate lyrics`、`bilingual subtitles`、`lrc translation`
- `j-pop lyrics`、`k-pop lyrics`、`c-pop lyrics`
- `번역`（韩语）· `翻訳`（日语）· `翻译`

### 示例提示词

```
把这个 .lrc 文件翻译成日语
给这首韩语歌词添加中文字幕
这首日文歌翻译成英文
Add English subtitles to this .lrc file
```

---

## 输出格式

每一行源语言歌词下方插入一行相同时间戳的译文，形成严格交替的双语格式：

```lrc
[01:23.45]愛してる
[01:23.45]爱你
[01:28.00]夢の中で会おう
[01:28.00]在梦中相遇吧
```

时间戳、元数据行（`[ti:]` `[ar:]` `[al:]` 等）、空行及纯音效行（`♪`）不会被修改。

---

## 文件结构

```
lyric-translator-skill/
├── SKILL.md              ← Skill 入口文件
└── reference/
    ├── common.md         ← 12 个方向对共享的通用规则
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

## 许可证

MIT
