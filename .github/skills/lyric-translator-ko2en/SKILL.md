---
name: lyric-translator-ko2en
description: "Use when translating Korean lyrics to English in .lrc files by inserting same-timestamp English lines under each Korean lyric line in strict alternating format; preserve LRC structure, never translate existing English or metadata, and enforce semantic, rhythmic, and natural-English quality checks."
version: 1.0.0
scopes: ["workspace"]
tags: ["lyrics", "translation", "korean", "english", "ko-en", "ko", "en", "inline-translation", "lrc", "subtitle", "karaoke", "timed-lyrics", "localization", "transcreation", "k-pop"]
---

# Korean Lyric Interleaved Translation Skill (KO → EN)

**Goal:** Directly edit an existing Korean .lrc file by inserting a same-timestamp English translation line immediately after each Korean lyric line, producing an alternating "source–translation–source–translation" display format.

---

## Executive Summary

For rapid invocations, prioritize these 8 items first:

1. Process only Korean lyric lines. Leave existing English lines, metadata tags, pure blank lines, and pure sound-effect symbol lines (`♪`/`♫`) untouched.
2. **First, read the entire file in one `read_file` call** to grasp the dominant emotions, narrative perspective, and genre (K-pop idol, ballad, hip-hop, trot, K-indie, etc.). Complete full-song analysis in memory before writing anything; do NOT interleave reads and writes.
   **Red-line rule:** If the song has a duet or multi-voice structure, build a speaker-mapping table first. Do not conflate different speakers' `나/너` pronouns without explicit evidence.
3. Read 3–5 lines before and after each line to detect split sentences, connector-ending chains (`~고`/`~어서`/`~면서`), and code-switched Korean/English passages.
4. Translate the semantic core (verb phrase + emotional center) first, then decide on modifiers and English idioms. Skip unnecessary subjects when context is clear.
5. Translation should read like natural subtitles first, poetry second: clear, singable, and colloquial. Target **6–16 syllables** per English line; if a line exceeds 16, split at the original timeline breakpoint.
6. For long Korean lines, follow the original breath breaks; each resulting English line must be independently readable. Never "borrow" the next line's content to complete this line's meaning.
7. Maintain consistent English translation for the chorus, hooks, and core imagery. Reuse the same English translation for every repeated Korean line.
8. Final checks: no accidental modification of existing English or metadata, no triple-line insertion, no perspective distortion, no added plot elements, no line length overflow.

---

## Absolute Constraints (Red Lines)

- **Format integrity**: Preserve all LRC timestamp codes exactly. Some lines may carry multiple timestamps (e.g., `[00:15.80][00:20.10]lyrics`); keep every timestamp unchanged.
- **Metadata protection**: Never translate or modify lines beginning with `[ti:`, `[ar:`, `[al:`, `[by:`, `[offset:`, or embedded credit lines (`词：`/`曲：`/`编曲：`/`制作人：` etc.).
- **No re-translation**: Never re-translate or modify existing English lyric lines. If an English translation already exists at the same timestamp, overwrite/update it rather than inserting a third line.
- **Exclusive insertion**: Each Korean line must have exactly one English translation line immediately after it. Inserting a second translation (triple-line) is absolutely forbidden.
- **Pure filler/vocalization lines**: Preserve Korean vocalization fills (`오오오`, `아아아`, `에에에`) without inserting any translation. Also preserve pure English filler lines (`Oh oh oh`, `Na na na`) untouched.
- **No plot additions**: Paraphrase only what the original text already expresses. Never introduce characters, backstory, emotions, or settings not present in the source.
- **Completeness**: Every repeated lyric line must receive its own translation. Never skip or merge lines.
- **Line length cap**: A single English translation line must not exceed **18 syllables**. If it does, split at the original timeline breakpoint.
- **Skip rules**: Skip pure empty timestamp lines (no content or only whitespace) and pure sound-effect lines (`[01:23.45]♪`).

---

## Agent Execution Workflow (Chain of Thought)

Follow this exact sequence before and during translation:

### 0. Tool-Call Discipline (Enforced)

- **Read before you write**: The very first action must be a single `read_file` call covering the full file. Interleaving reads and writes is forbidden.
- **Complete all analysis in memory**, then issue a single batch of `edit_file` / `replace_string` calls.
- For files exceeding 200 lines, split into at most two read passes; consolidate analysis in memory before writing.

### 1. Pre-Analysis

- [ ] Identify every line type: Korean lyric, existing English, metadata, filler/vocalization, blank, sound-effect.
- [ ] Determine genre, emotional key, and narrative perspective (1st-person confession, 2nd-person address, 3rd-person story, etc.).
- [ ] If duet/multi-voice: build a speaker-mapping table ("who says which block").
- [ ] Lock chorus/hook English translation first, then handle verses and bridge.
- [ ] Decide on the English register: conversational/colloquial vs. literary/poetic, matching the genre and mood.

### 2. Draft Translation

- [ ] For each Korean line → insert an identical-timestamp English line below it.
- [ ] Prioritize short, direct expressions; do not pad with adjectives or backstory.
- [ ] Follow the original breath breaks; each line must be self-contained.
- [ ] For code-switched lines (e.g., `Wait a minute 이게 뭐지`): keep the source line unchanged. The translation line renders the full semantic meaning in natural English.
- [ ] Skip pure filler / ♪ lines — insert no translation.

### 3. Refinement

- [ ] Remove excessive formality, excessive poetic ornament, or added plot elements.
- [ ] Unify chorus/hook/key-image translations across all occurrences.
- [ ] Verify narrative perspective consistency and pronoun choices throughout.
- [ ] Check that Korean-culture terms (`오빠`, `한`, `흥`, `눈치`, `정`, etc.) are rendered with meaning-accurate English, not phonetic borrowing.

### 4. Quality Check

- [ ] Source and translation strictly alternate; the file is valid LRC.
- [ ] No missing lines, no metadata mishandled, no existing English modified, no triple insertions.
- [ ] **Spot-check**: Pull one random line each from intro, verse, chorus, and bridge — read the English aloud to confirm: meaning is clear, fits in one breath, contains no information not in the source.

---

## Korean–English Linguistic Difference Rules

> Korean is an agglutinative SOV language with a rich honorific system and highly developed sentence-final endings. English is an analytic SVO language with relatively flat morphology and heavy reliance on word order, auxiliaries, and prepositions. The mismatch creates systematic translation challenges.

### 1. Word Order Inversion: SOV → SVO

Every Korean sentence ends with the verb; English places the verb after the subject and before the object.

| Korean Structure | English Target Structure | Example |
|:---:|:---:|:---:|
| `S + O + V(ending)` | `S + V + O` | `난 너를 사랑해` → `I love you` |
| Long pre-noun modifier chain | Relative clause or split sentence | `날 반기는 하늘이` → `the sky that welcomes me` |
| Connector chain `V+고`/`V+어서` | Coordinated or subordinated clauses | `보고 싶어서 울었어` → `I cried because I missed you` |
| Sentence-final `~잖아` | "you know" / "after all" appended | `그렇잖아` → `that's just how it is, you know` |

### 2. Honorific and Speech-Level System → English Register

Korean has distinct speech levels (합쇼체/해요체/해체/반말), each conveying social distance and emotional warmth. Map these to English tone and diction.

| Korean Speech Level | Context | English Strategy |
|:---:|:---:|:---:|
| 합쇼체 (`습니다`/`십니까`) | Formal, respectful | Formal diction: "I shall", "would you" |
| 해요체 (`해요`/`세요`) | Polite, warm | Standard conversational: "I will", "please" |
| 해체/반말 (`해`/`야`/`거든`) | Casual, intimate | Colloquial: contractions, drop "please", informal phrasing |
| `그대` (literary "you") | Romantic/literary usage | "you" with elevated diction around it |

### 3. Korean Sentence-Final Endings → English Emotional Nuance

Korean verb endings carry rich emotional and pragmatic information that must be restored in English through word choice and punctuation.

| Korean Ending | Meaning/Nuance | English Rendering Strategy |
|:---:|:---:|:---:|
| `~잖아` | "as you know" / mild reproach | "you know" / "after all" / "obviously" |
| `~거든` | explanatory assertion | "because…" / "the thing is…" |
| `~나봐` | inference / uncertainty | "I think…" / "maybe…" / "I guess…" |
| `~ㄹ게` | promise / intention | "I will…" / "I'll be…" |
| `~지?` | soft confirmation-seeking | "right?" / "isn't it?" |
| `~고 싶어` | desire | "I want to…" / "I wish I could…" |
| `~밖에 없어` | exclusivity / "only" | "only…" / "nothing but…" |
| `~아/어야 해` | obligation / necessity | "I have to…" / "I need to…" |

### 4. Korean Culture-Specific Terms → Meaning-Based Translation

Never phonetically borrow untranslated Korean culture terms into the English line.

| Korean Term | Cultural Meaning | English Translation Strategy |
|:---:|:---:|:---:|
| `오빠` | older brother / term of endearment used by females toward older males | adapt to natural English term of address in context; keep "oppa" only if the song explicitly uses it as a named identifier |
| `한 (恨)` | deep, accumulated sorrow and resentment woven into Korean culture | "deep sorrow" / "aching grief" / "longing pain" |
| `흥 (興)` | joyful rhythmic excitement, Korean communal spirit | "exhilaration" / "the joy of it" / "the beat" |
| `눈치` | social awareness / reading the room | "pick up the vibe" / "read the situation" |
| `정 (情)` | deep emotional bond formed over time | "the bond between us" / "this feeling I can't shake" |
| `아잉` | cute pouty / coy appeal sound | render as tone: "(coyly)" / "aw, come on" |

### 5. Korean Onomatopoeia and Mimetic Words (의성어/의태어)

Korean has an extremely rich system of onomatopoeia and mimetic words. Never leave Korean syllables untranslated in the English line.

| Korean 의성어/의태어 | Core Sensation | English Equivalent |
|:---:|:---:|:---:|
| `두근두근` | fluttering heartbeat | "heart pounding" / "flutter in my chest" |
| `설레다` | excitement of anticipation / butterflies | "butterflies" / "heart racing" / "filled with anticipation" |
| `퐁당` | a light plop/splash into water | "splash right in" / "fall in headfirst" |
| `두리번두리번` | looking around restlessly | "looking around" / "searching every corner" |
| `흑흑` | sobbing sound | "sob" / "crying" |
| `뜨거워 뜨거워` | burning hot (emotional/physical) | "burning burning" / "so hot so hot" |

### 6. Korean Mixed-Language Lines (Code-Switching)

K-pop frequently mixes Korean and English in the same line. Handle carefully.

| Scenario | Treatment |
|:---:|:---:|
| Embedded English in Korean line (`Wait a minute 이게 뭐지`) | Keep source line unchanged. Translation line renders the full meaning naturally: "Wait a minute, what is this?" |
| Full English source line (`I'm just trying to play it cool`) | **Do not insert a translation** — treat as an existing English line and skip |
| Korean-adapted English words (`원샷`, `팩트체크`) | Translate to natural English: `원샷` → "one shot", `팩트체크` → "fact check" |
| MBTI references (`넌 J 난 완전 P`) | Keep MBTI letters; translate the frame: "You're a J, I'm total P" |
| Pure Korean filler (`오오오`, `에에에`) | Skip — no translation |

### 7. Korean Connector Endings → English Clauses

| Korean Connector | Meaning/Use | English Rendering |
|:---:|:---:|:---:|
| `~고` | sequence / coordination | "and" / "then" / comma join |
| `~어서/아서` | reason / prior action | "because" / "so" / "after" |
| `~면서` | simultaneous action | "while" / "as" |
| `~지만` | concession | "but" / "even though" |
| `~면/으면` | condition | "if" / "when" |
| `~도록` | extent / purpose | "so that" / "until" / "enough to" |

### 8. Korean Syllable Density and Line Rhythm

Korean is syllable-timed; English is stress-timed. Prioritize matching the number of **strong beats**, not total syllable count.

| Korean Line Length | Target English Syllable Range | Note |
|:---:|:---:|:---:|
| 2–4 syllables | 2–5 words | Preserve brevity; do not pad |
| 5–8 syllables | 4–9 words | Normal translation |
| 9–12 syllables | 7–13 words | Aim for similar beat count |
| 13+ syllables | Split or 10–16 words | Never exceed 18 syllables |

---

## Paraphrase vs. Plot-Addition Boundary

Paraphrase is natural development of **information already in the source**. Plot addition introduces **new characters, motivations, or settings not in the source**.

| Source | Acceptable Paraphrase ✓ | Over-paraphrase ✗ | Reason |
|:---:|:---:|:---:|:---:|
| `그냥 퐁당 빠지고 싶어` | `I just want to fall right in` | `I want to drown in your ocean of love` | "drown" and "ocean of love" are additions |
| `아름다워 사랑스러워` | `Beautiful, so lovely` | `You're the most beautiful person I've ever seen` | "most" and "ever" are additions |
| `기다릴게요` | `I'll wait for you` | `I'll wait here forever, no matter how long it takes` | "forever" and "no matter how long" are additions |
| `오빤 강남스타일` | `He's got that Gangnam style` | `He's the wealthy fashionable Gangnam playboy` | excessive cultural gloss |

---

## Common Error Types and Correct Translations

**Error Type 1: Keeping Korean SOV word order — produces unnatural English.**
- Source: `난 너만을 원해`
- Wrong: `I you only want`
- Correct: `I only want you`

**Error Type 2: Phonetically borrowing Korean honorific terms.**
- Source: `그대를 사랑해요`
- Wrong: `I love geuidae`
- Correct: `I love you` (or "I love thee" if the register warrants elevated diction)

**Error Type 3: Translating culture terms phonetically without meaning.**
- Source: `오빤 강남스타일`
- Wrong: `Oppa is Gangnam style`
- Correct: `He's got that Gangnam style`

**Error Type 4: Inserting a translation line after a pure English line.**
- Source line: `[01:22.40]Eh Sexy Lady` (pure English)
- Wrong: inserts `[01:22.40]Hey, sexy lady` below it
- Correct: skip this line — it is already English

**Error Type 5: Flattening Korean sentence-final endings, losing emotion.**
- Source: `기다릴게요 난 그대여야만 하죠`
- Wrong: `I am waiting, I should be yours` (flat, literal)
- Correct: `I'll keep waiting — you're the only one for me`

**Error Type 6: Over-translating Korean 의성어 — inserting plot.**
- Source: `그냥 퐁당 빠지고 싶어`
- Wrong: `I want to dive deep into the sea of your heart`
- Correct: `I just want to fall right in`

**Error Type 7: Mistranslating Korean connector endings.**
- Source: `보고 싶어서 울었어`
- Wrong: `I want to see you, I cried` (causal link missing)
- Correct: `I cried because I missed you so much`

**Error Type 8: Treating an entire code-switched line as Korean when it is pure English.**
- Source: `[01:02.40]I'm just trying to play it cool` (pure English)
- Wrong: inserts a Korean-to-English translation below it
- Correct: skip the line entirely

---

## Special Line Handling

| Line Type | Detection Criterion | Action |
|:---:|:---:|:---:|
| Pure empty timestamp | `[01:23.45]` with no content or only whitespace | Skip; no translation inserted |
| Pure sound-effect | `[01:23.45]♪` or `[01:23.45]♫` | Preserve as-is; no translation inserted |
| LRC metadata tag | `[ti:`, `[ar:`, `[al:`, `[by:`, `[offset:` | Never translate or modify |
| Embedded credit line | `词：` / `曲：` / `编曲：` / `制作人：` etc. | Never translate or modify |
| Pure English lyric line | Entire line already in English | Preserve as-is; do not insert translation |
| Korean vocalization fill | `오오오`, `아아아`, `에에에`, `뜨거워 뜨거워` (repeated vocalization) | Preserve as-is; no translation inserted |
| Code-switched line | Mixed Korean + English in one line | Source line unchanged; translation line renders full meaning in natural English |
| Korean `…` pause | Pause / trailing off | Render in English as `…` or absorbed into natural sentence rhythm |

---

## Format Template

**Input:**

```lrc
[ti:강남스타일 (江南Style)]
[ar:PSY]
[00:15.192]낮에는 따사로운 인간적인 여자
[00:18.505]커피 한잔의 여유를 아는 품격 있는 여자
[01:22.403]Eh Sexy Lady
[00:20.00]♪
[00:25.00]
```

**Correct Output:**

```lrc
[ti:강남스타일 (江南Style)]
[ar:PSY]
[00:15.192]낮에는 따사로운 인간적인 여자
[00:15.192]A warm and genuine woman in the daytime
[00:18.505]커피 한잔의 여유를 아는 품격 있는 여자
[00:18.505]A woman with the grace to savor a cup of coffee
[01:22.403]Eh Sexy Lady
[00:20.00]♪
[00:25.00]
```

> The pure English line `Eh Sexy Lady`, the `♪` line, and the blank line receive no translation and are preserved exactly as-is.

---

## 7-Point Final Self-Check

- [ ] **Word order**: Every English translation follows natural SVO order; no Korean-order artifacts remain in any line.
- [ ] **Culture terms**: All culture-specific Korean terms (`오빠`, `한`, `눈치`, `정`, etc.) are rendered with meaning, not phonetic borrowing.
- [ ] **Onomatopoeia / mimetic words**: All Korean 의성어/의태어 are translated to natural English equivalents; no Korean syllables remain in the English line.
- [ ] **Code-switching**: Existing pure English lines in the source were left untouched; mixed-language lines have their Korean portion rendered naturally in the English translation line.
- [ ] **No triple insertion**: Each Korean source line has exactly one English translation line below it; no existing translation was duplicated.
- [ ] **Sentence-final endings**: Emotional nuance from `~잖아`/`~거든`/`~ㄹ게`/`~지?` etc. has been restored through English word choice and punctuation.
- [ ] **Register consistency**: The English register (formal/casual/poetic) is consistent throughout the song and matches the genre and mood established in Step 1.
