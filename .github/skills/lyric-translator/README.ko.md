# lyric-translator-skill

> **에이전트 스킬** — 중국어（ZH）·일본어（JA）·한국어（KO）·영어（EN） 사이에서 `.lrc` 가사 파일을 번역합니다.

**12가지 방향 쌍** 전체 지원: EN↔JA · EN↔KO · EN↔ZH · JA↔KO · JA↔ZH · KO↔ZH

| 언어 | 문서 |
|---|---|
| English | [README.md](README.md) |
| 中文 | [README.zh.md](README.zh.md) |
| 日本語 | [README.ja.md](README.ja.md) |

---

## 설치

### npm 경로

```bash
npx skills add lyric-translator-skill
```

### GitHub 경로

```bash
npx skills add YOUR_USERNAME/lyric-translator-skill
```

### 설치 범위 옵션

**워크스페이스 범위**（권장 — 현재 프로젝트에만 적용）：

```bash
npx skills add lyric-translator-skill --scope workspace
```

현재 디렉토리의 `.github/skills/lyric-translator/`에 설치됩니다.

**사용자 범위**（모든 프로젝트에 적용）：

```bash
npx skills add lyric-translator-skill --scope user
```

`~/.agents/skills/lyric-translator/`에 설치됩니다.

#### 수동 설치（CLI 불필요）

```bash
git clone https://github.com/YOUR_USERNAME/lyric-translator-skill.git
# 워크스페이스 범위
mkdir -p .github/skills/lyric-translator
cp -r lyric-translator-skill/SKILL.md lyric-translator-skill/reference \
       .github/skills/lyric-translator/
```

---

## 지원 번역 방향

| 방향 | 원본 언어 | 대상 언어 |
|:---:|:---:|:---:|
| EN → JA | 영어 | 일본어 |
| EN → KO | 영어 | 한국어 |
| EN → ZH | 영어 | 중국어 |
| JA → EN | 일본어 | 영어 |
| JA → KO | 일본어 | 한국어 |
| JA → ZH | 일본어 | 중국어 |
| KO → EN | 한국어 | 영어 |
| KO → JA | 한국어 | 일본어 |
| KO → ZH | 한국어 | 중국어 |
| ZH → EN | 중국어 | 영어 |
| ZH → JA | 중국어 | 일본어 |
| ZH → KO | 중국어 | 한국어 |

---

## 사용 방법

설치 후 다음 키워드를 포함한 프롬프트에서 에이전트이 자동으로 이 스킬을 활성화합니다：

- `translate lyrics`, `bilingual subtitles`, `lrc translation`
- `j-pop lyrics`, `k-pop lyrics`, `c-pop lyrics`
- `번역` · `翻訳`（일본어）· `翻译`（중국어）

### 예시 프롬프트

```
이 .lrc 파일을 한국어로 번역해줘
이 중국어 가사에 한국어 자막 추가해줘
일본어 가사를 영어로 번역해줘
번역해줘 — translate these KO lyrics to Japanese
```

---

## 출력 형식

각 원본 가사 줄 바로 아래에 동일한 타임스탬프의 번역 줄이 삽입되어 엄격한 교대 이중 언어 형식이 생성됩니다：

```lrc
[01:23.45]愛してる
[01:23.45]사랑해
[01:28.00]夢の中で会おう
[01:28.00]꿈속에서 만나요
```

타임스탬프, 메타데이터 줄（`[ti:]` `[ar:]` `[al:]` 등）, 빈 줄, 효과음 줄（`♪`）은 변경되지 않습니다.

---

## 파일 구조

```
lyric-translator-skill/
├── SKILL.md              ← 스킬 진입점
└── reference/
    ├── common.md         ← 12개 방향 쌍 공통 규칙
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

## 라이선스

MIT
