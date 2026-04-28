# lyric-translator-skill

> **エージェントスキル** — 中国語（ZH）・日本語（JA）・韓国語（KO）・英語（EN）間で `.lrc` 歌詞ファイルを翻訳します。

**12 方向ペア**すべてに対応：EN↔JA · EN↔KO · EN↔ZH · JA↔KO · JA↔ZH · KO↔ZH

| 言語 | ドキュメント |
|---|---|
| English | [README.md](README.md) |
| 中文 | [README.zh.md](README.zh.md) |
| 한국어 | [README.ko.md](README.ko.md) |

---

## インストール

### npm 経由

```bash
npx skills add lyric-translator-skill
```

### GitHub 経由

```bash
npx skills add YOUR_USERNAME/lyric-translator-skill
```

### スコープの指定

**ワークスペーススコープ**（推奨 — 現在のプロジェクトのみ有効）：

```bash
npx skills add lyric-translator-skill --scope workspace
```

スキルファイルはカレントディレクトリの `.github/skills/lyric-translator/` にインストールされます。

**ユーザースコープ**（すべてのプロジェクトで有効）：

```bash
npx skills add lyric-translator-skill --scope user
```

スキルファイルは `~/.agents/skills/lyric-translator/` にインストールされます。

#### 手動インストール（CLI 不要）

```bash
git clone https://github.com/YOUR_USERNAME/lyric-translator-skill.git
# ワークスペーススコープ
mkdir -p .github/skills/lyric-translator
cp -r lyric-translator-skill/SKILL.md lyric-translator-skill/reference \
       .github/skills/lyric-translator/
```

---

## 対応翻訳ペア

| 方向 | ソース言語 | ターゲット言語 |
|:---:|:---:|:---:|
| EN → JA | 英語 | 日本語 |
| EN → KO | 英語 | 韓国語 |
| EN → ZH | 英語 | 中国語 |
| JA → EN | 日本語 | 英語 |
| JA → KO | 日本語 | 韓国語 |
| JA → ZH | 日本語 | 中国語 |
| KO → EN | 韓国語 | 英語 |
| KO → JA | 韓国語 | 日本語 |
| KO → ZH | 韓国語 | 中国語 |
| ZH → EN | 中国語 | 英語 |
| ZH → JA | 中国語 | 日本語 |
| ZH → KO | 中国語 | 韓国語 |

---

## 使い方

インストール後、以下のキーワードを含むプロンプトでエージェントが自動的にこのスキルを起動します：

- `translate lyrics`、`bilingual subtitles`、`lrc translation`
- `j-pop lyrics`、`k-pop lyrics`、`c-pop lyrics`
- `번역`（韓国語）· `翻訳` · `翻译`（中国語）

### プロンプト例

```
この .lrc ファイルを日本語に翻訳して
この中国語の歌詞に韓国語字幕を追加して
英訳して
Add English subtitles to this .lrc file
```

---

## 出力フォーマット

各ソース行のすぐ下に同じタイムスタンプの翻訳行が挿入され、厳密な交互バイリンガル形式が生成されます：

```lrc
[01:23.45]愛してる
[01:23.45]I love you
[01:28.00]夢の中で会おう
[01:28.00]Let's meet in a dream
```

タイムスタンプ・メタデータ行（`[ti:]` `[ar:]` `[al:]` など）・空行・効果音行（`♪`）は変更されません。

---

## ファイル構成

```
lyric-translator-skill/
├── SKILL.md              ← スキルエントリポイント
└── reference/
    ├── common.md         ← 全 12 ペア共通ルール
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

## ライセンス

MIT
