---
name: lyric-translator-zh2en
description: "Use when translating Chinese (Simplified/Traditional/Cantonese-influenced) lyrics to English in .lrc files by inserting same-timestamp English lines under each Chinese lyric line in strict alternating format; preserve LRC structure, never translate existing English or metadata, and enforce semantic, rhythmic, and natural-English quality checks."
version: 1.0.0
scopes: ["workspace"]
tags: ["lyrics", "translation", "chinese", "english", "zh-en", "zh", "cn", "en", "inline-translation", "lrc", "subtitle", "karaoke", "timed-lyrics", "localization", "transcreation", "mandarin", "cantonese"]
---

# Chinese Lyrics Alternating-Overlay Translation Skill (ZH → EN)

**Goal:** Directly edit existing Chinese `.lrc` files, inserting an English translation line with the **same timestamp** immediately after each Chinese lyric line, producing a strict "original → translation → original → translation" alternating display.

---

## Executive Summary

When invoked, execute these 8 rules first:

1. Only process Chinese lyric lines. Do not touch existing English lines, metadata tags, blank lines, or pure sound-effect lines (`♪`/`♫`).
2. **Read the entire file in one `read_file` call first.** Identify song genre, emotional arc, and narrative perspective (first-person confession, third-person narrative, duet, anthem, etc.). Complete full-song analysis in memory before writing — never alternate between reading and writing.
   Hard rule: If the song has a clear duet or role-switching structure (e.g., 周华健 _ 齐豫 songs), map speakers first. Do NOT conflate different voices' "I/you" into one direction.
3. Scan 3–5 lines before and after each line to detect broken long sentences, topic-chains, and parallel structures spanning multiple timestamps.
4. Translate the semantic core (main action/emotion/anchor) first, then decide on modifiers. Do not front-load imagery before conveying meaning.
5. Translations must read like **natural English lyrics first, literature second**: singable, idiomatic, free of word-for-word Chinese sentence structure. Keep each English line to **6–14 words**; lines over 14 words must split to follow the original timestamp breakpoints.
6. Fragmented Chinese lines (parallel short lines, single-image lines, topic-chains cut across timestamps) must each produce a standalone English fragment — front lines must NOT "steal ahead" and pre-translate content belonging to a later timestamp.
7. Hook words, core imagery, and chorus key phrases must be translated **consistently across the entire song**. Repeated lines reuse the same English translation verbatim.
8. Before submitting: verify no English/metadata lines were touched, no third-line overlay was created, no over-interpretation was added, and no line exceeds the word limit.

---

## Absolute Constraints (Red Lines)

- **Format integrity**: Preserve all LRC timestamp formatting without exception. Lines with multiple timestamps (e.g., `[00:15.80][00:20.10]歌词`) must have all timestamps reproduced identically on the translation line.
- **Metadata immunity**: Never translate or modify lines beginning with `[ti:`, `[ar:`, `[al:`, `[by:`, `[offset:`, or similar metadata tags. Also skip lyrics-internal metadata lines (词：/曲：/编曲：/制作人：/录音: etc.).
- **No re-translation of existing English**: If a line is already in English (e.g., embedded English hook phrases like `oh no` / `yeah yeah` in a Chinese song), do not add a translation — treat it as-is.
- **Exclusive overlay rule**: Each Chinese lyric line may have **exactly one** same-timestamp English translation below it. If an existing English translation is already present, **overwrite/replace** it — never stack a third line.
- **Pure vocalise lines**: Lines consisting entirely of vocalise (`啦啦啦`, `哦哦哦`, `Na na na`) or musical fillers — keep as-is; do **not** insert a translation. (See Special Line Handling table below for edge cases.)
- **No over-interpretation**: Default to faithful meaning. Never add backstory, setting, or motivation absent from the original (see "Translation vs. Over-Interpretation" section).
- **Completeness**: Repeated lyric lines must each receive a translation. Never skip, merge, or collapse repeated lines.
- **Line length cap**: A single English translation line must not exceed **16 words**. If it does, split across the existing timestamp breakpoints — never cram everything into one line.
- **Skip rule**: Empty timestamp lines (content is blank or whitespace only) and pure sound-effect lines (`[01:23.45]♪`) pass through unchanged with no translation inserted.

---

## Agent Workflow (Chain of Thought)

Execute in this exact order:

### 0. Tool Call Protocol (Mandatory)

- **Read before write**: The first action must be a complete `read_file` of the entire lyric file. Do NOT interleave reads and writes (causes line-offset errors and accidental triple-layering).
- Perform full-song analysis in memory, then make a single pass of `edit_file` / `replace_string` to write all translations.
- For files over 200 lines, read in two segments, merge analysis in memory, then write in one pass.

### 1. Pre-Analysis

- [ ] Scan the full text. Label each line: Chinese lyric / existing English / metadata / special (blank, `♪`, vocalise, pure 啦啦/哦哦).
- [ ] Identify song genre and emotional register (Mandarin pop ballad, Cantonese rock anthem, 古风 classical-style, rap/hip-hop, 抒情, 励志, etc.) — genre determines acceptable English register and vocabulary level.
- [ ] Detect source dialect influence: is this a Cantonese-origin song translated to Mandarin (e.g., BEYOND, 张国荣, 陈百强)? If yes, watch for Cantonese sentence rhythm patterns that don't follow standard Mandarin grammar.
- [ ] If duet or multi-voice: build a speaker map (who says what, what does "我/你" refer to in each section).
- [ ] Lock in a consistent translation for: chorus hook phrases, core imagery words, title phrase, and recurring motifs.
- [ ] Scan for topic-chain lines and broken long sentences spanning multiple timestamps. Plan how to fragment their English equivalents.
- [ ] Check if same-timestamp English already exists. If yes — evaluate keep/replace; never stack.

### 2. Translation Pass

- [ ] Process each line: Chinese → English translation on the very next line, same timestamp.
- [ ] **Mandatory: add an English subject** where Chinese drops it (Chinese is pro-drop/topic-prominent; English requires explicit subjects). Choose the correct pronoun based on context (I / you / we / she / he / they).
- [ ] Reconstruct English tense based on aspect particles (了/着/过) and surrounding context — do not flatten all verbs to simple present (see "Tense & Aspect Reconstruction" section).
- [ ] Translate 成语 (4-character idioms) and Classical allusions by meaning, not character-by-character (see "Chengyu & Classical References" section).
- [ ] Blank lines / `♪` lines / vocalise lines → pass through, no translation.

### 3. Refinement

- [ ] Remove translation artifacts: awkward topic-fronting, over-literal measure-word rendering, stilted formal phrasing.
- [ ] Check that each line can be spoken naturally in one breath (≤ 14 words strongly preferred).
- [ ] Ensure chorus, hook, and core imagery translations are identical across all occurrences.
- [ ] For structurally parallel Chinese lines (排比/对偶), produce matching parallel English structures (see "Parallel Structure Preservation" section).
- [ ] Verify modal adverbs (偏偏/明明/终究/好想/只是) have been rendered with appropriate English equivalents.

### 4. Validation

- [ ] Original and translation lines strictly alternate; output is parseable by standard LRC players.
- [ ] No missed Chinese lines, no metadata translated, no existing English modified, no triple overlay.
- [ ] **Manual spot-check**: Randomly pick 1 line each from intro / verse / chorus / bridge. Read the English aloud. Confirm: natural phrasing, fits in one breath, no invented details, pronoun is correct.

---

## Chinese–English Linguistic Difference Handling Rules

### 1. Pro-Drop and Topic-Prominence → Mandatory Subject Restoration

Chinese is a **topic-prominent** language: the subject is frequently omitted, and the sentence topic (which may differ from the grammatical subject) is fronted. English requires explicit grammatical subjects. Restoring the correct subject is the single most important translation decision.

| Situation | Strategy | Example |
|:---|:---|:---|
| Single consistent first-person narrator | Use "I" consistently | `后来终于在眼泪中明白` → `at last, I came to understand through tears` |
| Second-person address | Use "you" | `可惜你早已远去` → `but you had long since disappeared` |
| Ambiguous subject | Read 3–5 lines for context; choose the most natural reading | — |
| Topic fronted (non-subject first) | Restructure into English SVO | `那个永恒的夜晚，十七岁仲夏` → `that timeless night, the midsummer of seventeen` |
| Collective/universal statement | Use "we" or impersonal phrasing | `天空海阔你与我` → `the sky and sea stretch wide — you and I` |

> **Topic-fronted line example**: Chinese: `风雨里追赶` (topic: wind and rain; implied subject: I). English: `I chase on through wind and rain` — subject "I" must be inserted. Do NOT output `in wind and rain chasing` (topic-literal artifact).

### 2. Tense & Aspect Reconstruction

Mandarin has **no grammatical tense**. Time is expressed through aspect particles (了/着/过), adverbs (曾经/以前/将来/正在), and context. You must infer the English tense from the full lyric context, not just the single line.

| Chinese marker | Core meaning | English tense/form | Example |
|:---:|:---|:---|:---|
| `了` (sentence-final) | Change of state / new situation | Often simple past or "now" + present | `总算学会了如何去爱` → `I finally learned how to love` |
| `了` (between verb+obj) | Completion of action | Simple past | `握着你手` → `held your hand` |
| `着` | Ongoing state / background | Present progressive or simple present | `怀着冷却了的心窝` → `carrying a heart grown cold` |
| `过` | Experiential: happened at some point | `have + V + ed` / `once` | `有没有爱过` → `have you ever loved` |
| `正在` / `在` | Active ongoing | Present progressive | `在风中大声的唱` → `singing out loud in the wind` |
| `将` / `会` (future) | Future intention | `will` / `going to` | `下一站是不是天堂` → `is the next stop heaven or not` |
| `曾经` / `那时候` | Past, emotionally framed | Simple past + optional "once" / "back then" | `那时候的爱情` → `the love we had back then` |
| No marker (default) | Timeless / lyric present | Simple present | `逆风的方向更适合飞翔` → `flying into the wind feels most right` |

> **Critical**: `了` is the most ambiguous particle. Do NOT default to past tense for every `了`. Example: `最美的愿望一定最疯狂` has no `了` but is a timeless statement → keep as present tense.

### 3. Chengyu (成语) and Classical Allusions

Chinese lyrics — especially 古风, rock anthems, and Cantonese pop — are dense with **4-character set phrases (成语)** and classical poetic vocabulary. **Never translate character-by-character.** Always translate the **established idiomatic meaning**.

| Chinese phrase | Literal characters | Correct English meaning | Example line |
|:---:|:---:|:---:|:---|
| `海阔天空` | sea-wide-sky-sky | boundless freedom / the wide-open world | `天空海阔你与我` → `with you, the world feels boundless` |
| `以刚克刚` | use-hard-overcome-hard | meet strength with strength / fight fire with fire | `坚持对我来说就是以刚克刚` → `to me, persistence means meeting force with force` |
| `如有所失` | like-have-something-lost | a sense of having lost something | `若有所失的感觉` → `a feeling like something has been lost` |
| `不羁放纵` | not-restrained-indulgent | wild and unrestrained / free-spirited | `不羁放纵爱自由` → `wild and free, I love my freedom` |
| `沧海` | vast-sea | the vast expanse / the immensity of time | `沧海一声笑` → `one laugh across the vast sea of time` |
| `消失在人海` | vanish-in-people-sea | vanish into the crowd | `消失在人海` → `vanish into the crowd` |

> **Key rule**: Look up the idiomatic meaning before translating. The word `海` (sea) in `人海` does NOT mean literal ocean — it means "crowd." Similarly, `天空海阔` in `海阔天空` is not about literal sky and ocean but about **open freedom**.

### 4. Parallel Structure Preservation (排比 / 对偶)

Chinese lyrics heavily rely on **parallel sentence structures** (排比), often with equal syllable counts and mirrored syntax. English must mirror the parallelism — do not collapse or unevenly expand parallel lines.

| Chinese pattern | English strategy | Example |
|:---|:---|:---|
| **4-4-4-4 rhythm groups** | Match with equal-weight English phrases | `握紧双手绝对不放 / 下一站是不是天堂` → `grip tight, never let go / is the next stop heaven` |
| **Anaphora (repeated opening)** | Repeat the same English opener | `我和我最后的倔强 / 我和我骄傲的倔强` → `my last stubborn streak / my proud stubborn streak` |
| **Antithetical couplets (对偶)** | Preserve contrast using parallel English syntax | `逆风的方向更适合飞翔` → preserve the paradox in English: `the headwind is the better direction to fly` |
| **Short parallel image lines** | Match word count as closely as possible | `栀子花 / 白花瓣` → `gardenia flowers / white petals` (not one long merged sentence) |

> **Warning**: Collapsing two parallel Chinese short lines into a single long English line destroys the visual rhythm the songwriter intended. Always respect the original line boundary.

### 5. Modal Adverbs — Emotional Precision Words

Chinese has a class of single-word modal adverbs that carry heavy emotional coloring. They have no direct one-word English translation and must be rendered through word choice, syntax, or added modals:

| Chinese word | Core feeling | English rendering strategy | Example |
|:---:|:---|:---|:---|
| `偏偏` | Against expectation / "of all things" / fate-like irony | `just`(emphatic) / `and yet` / `of all things` | `但偏偏雨渐渐大到我看你不见` → `but just then the rain grew so heavy I lost sight of you` |
| `明明` | "clearly / obviously" — speaker knows the truth but something contradicts it | `clearly` / `I know` / `even though I knew` | `明明就` → `and yet it's obvious` |
| `终究` | In the end / inevitably / after all | `in the end` / `after everything` / `inevitably` | `故事的最后你好像还是说了拜拜` → `in the end, you still said goodbye` |
| `好想` | Aching desire — more intense than just "want" | `I ache to` / `I so badly want to` / `I keep wanting` | `好想再问一遍` → `I ache to ask you one more time` |
| `只是` | "it's just that…" — mild pivot, resignation or qualification | `it's just` / `only` / `still` | `只是因为你` → `it's just because of you` |
| `总算` | Finally, after a long process / "at last" with relief-tinged exhaustion | `finally` / `at last` / `I've finally` | `我总算学会了` → `I've finally learned` |
| `不知不觉` | Without noticing / gradually, unconsciously | `without realizing it` / `somewhere along the way` | `不知不觉已变淡` → `without realizing it, the feeling had faded` |
| `好不容易` | With great difficulty / barely managed / "it wasn't easy, but…" | `with so much effort` / `barely` / `I could hardly` | `好不容易又能再多爱一天` → `and barely managed to love you one more day` |

### 6. Syllable Density & Line Length

Mandarin Chinese is largely monosyllabic: **one character = one syllable**. English words are polysyllabic (average ~1.5 syllables/word in common usage). This means:

| Chinese line length | Approximate English word count | Notes |
|:---:|:---:|:---|
| 2–4 characters | 2–5 words | Preserve brevity; do NOT pad short image-lines |
| 5–7 characters | 4–8 words | Standard single thought; translate cleanly |
| 8–11 characters | 6–11 words | May need minor restructuring |
| 12–16 characters | 8–14 words | Watch for run-on; consider splitting at natural breath point |
| 17+ characters | Split across timestamp breakpoints | Never force into one English line |

> **Short-line preservation example**: `栀子花` (3 chars) → `gardenia flowers` (2 words). Do NOT expand to `the beautiful white gardenia flowers` — preserve the original weight. Image-only short lines are **deliberate poetic choices**, not incomplete sentences to be filled out.

### 7. Reduplication (叠字/叠词) → English Intensifiers

Chinese uses reduplication both as an intensifier and to create a softer, more lyrical tone. The correct English mapping depends on the character type being reduplicated:

| Reduplication type | Chinese example | English strategy | Example |
|:---:|:---:|:---:|:---|
| **Adjective reduplication** (softer/warmer tone) | `慢慢地` | `slowly` / `gently, slowly` | `慢慢走` → `walk slowly` |
| **Verb reduplication** (try a little / do casually) | `想一想` | `think about it a bit` / `stop and think` | `想一想` → `stop and think` |
| **Onomatopoeia** (sound-based) | `叮叮咚咚` | translate the sound as imagery | `叮叮咚咚` → `chiming and ringing` |
| **Pure rhythm filler** (hook/vocalise) | `啦啦啦啦` | do NOT translate — pass through | `啦啦啦啦啦啦啦啦` → keep as-is |
| **Emotional intensifier** | `好好爱` | `truly love` / `love well` / `love with all you have` | `好好爱一个人` → `love someone with everything you've got` |

### 8. Register Mapping: Genre → English Register

Chinese pop spans a wide register spectrum. The English translation must match the source register — do not smooth every song into neutral pop English.

| Chinese genre / style | Key markers | English register target | Vocabulary examples |
|:---:|:---:|:---|:---|
| **现代流行情歌** (Modern Mandarin pop ballad) | Personal pronouns, emotional adverbs (偏偏/好想) | Warm, conversational, slightly lyrical | `disappeared into the crowd` / `I finally learned` |
| **粤语/港台摇滚** (Cantonese/HK-TW rock) | Strong parallel structure, idealistic vocabulary (理想/自由) | Anthemic, declamatory, energetic | `never let go` / `wild and free` / `who can stop me` |
| **古风 / 国风** (Classical-style Chinese) | Classical vocabulary (苍生/霜/剑/月), 4-char rhythm | Elevated, poetic, archaic-flavored | `the frost-covered night` / `beneath the ancient moon` |
| **说唱/嘻哈** (Mandarin rap/hip-hop) | Dense syllables, street vocabulary, boastful register | Colloquial, punchy, rhythmic | `my turf` / `step back` / `rolling deep` |
| **励志/热血** (Motivational anthem) | Direct imperative, universal "we", 不怕/坚持/倔强 | Bold, declarative, slightly theatrical | `I'm not afraid` / `hold on tight` / `I won't back down` |

> **Cantonese-origin song warning**: Songs by BEYOND, 张国荣, 陈百强, etc. were often composed in Cantonese and later translated to Mandarin. The Mandarin lyrics may be slightly unnatural or have unusual word choices. Translate the intended **emotional meaning**, not the sometimes awkward Mandarin character sequence.

### 9. Noun Phrases and Measure Words

Chinese uses **measure words** (量词) between numbers/demonstratives and nouns: `一首歌` (one-[song-MW]-song), `那个夜晚` (that-[general-MW]-night). The measure word itself carries no meaning in English and typically disappears.

| Chinese construction | English result | Note |
|:---:|:---:|:---|
| `一首歌的时间` | `the length of a song` / `one song's time` | Measure word `首` → not translated |
| `那个夜晚` | `that night` | Measure word `个` → not translated |
| `这些年来` | `all these years` / `over the years` | `这些年` → `all these years` |
| `有一天` | `one day` / `someday` | `有一天` is idiomatic for "someday" |

### 10. Negation Precision

Chinese has multiple negation words with distinct functions. Map each correctly:

| Chinese | Function | English |
|:---:|:---:|:---|
| `不` | Habitual/volitional negation | `don't` / `won't` / `doesn't` |
| `没（有）` | Factual non-occurrence (past) | `didn't` / `haven't` / `there wasn't` |
| `别` | Prohibition / imperative negation | `don't` (command) |
| `甭` | Colloquial: no need to | `don't bother` / `no need to` |
| `未` | Classical/literary: not yet | `not yet` / `never yet` |
| `绝不` | Absolute negation, emphatic | `never` / `absolutely not` / `I refuse to` |

> Example: `即使别人原谅，我也不能原谅` — `也不能` is volitional impossibility: → `even if others forgive me, I cannot forgive myself` (NOT "I didn't forgive").

---

## Translation vs. Over-Interpretation

Faithful translation expands **what the original implies**. Over-interpretation **invents new story, setting, or motivation** not present in the source.

| Original (Chinese) | Acceptable translation ✓ | Over-interpretation ✗ | Reason |
|:---:|:---:|:---:|:---|
| `消失在人海` | `vanished into the crowd` | `disappeared into the crowded subway platform` | "subway" is not in the source |
| `那个永恒的夜晚` | `that eternal night` | `that unforgettable night we spent under the stars` | "stars" and "we spent" are invented |
| `若有所失的感觉` | `a hollow feeling, like something's been lost` | `a feeling of regret after the breakup` | "breakup" and "regret" are inferred too far |
| `风雨里追赶` | `I chase on through wind and rain` | `I run through the storm chasing your shadow` | "shadow" is not in the source |
| `海阔天空` (song title context) | `the boundless sky` / `the wide-open world` | `the endless freedom of the ocean and the open sky above` | Over-expansion of a compact 4-char image |

---

## Common Failure Modes and Corrected Examples

**Failure 1: Dropping the subject entirely — English output reads like broken headlines.**

- Source: `后来终于在眼泪中明白`
- Wrong: `finally understood through tears` (subject missing)
- Correct: `I finally understood through my tears`

**Failure 2: Topic-fronted Chinese structure preserved literally in English.**

- Source: `风雨里追赶`
- Wrong: `in wind and rain chasing` (topic-literal word order)
- Correct: `I chase on through wind and rain`

**Failure 3: 成语 translated character-by-character, producing nonsense.**

- Source: `不羁放纵爱自由`
- Wrong: `not-fettered indulgent loves freedom`
- Correct: `wild and free, I love my freedom`

**Failure 4: Modal adverb `偏偏` dropped entirely, losing the irony.**

- Source: `但偏偏雨渐渐大到我看你不见`
- Wrong: `but the rain gradually grew too heavy for me to see you`
- Correct: `but just then the rain grew so heavy I lost sight of you` (`偏偏` = the cruel timing, "of all things, right then")

**Failure 5: `了` mechanically treated as simple past regardless of context.**

- Source: `我和我最后的倔强` (present self-declaration, no `了`)
- Wrong: `I and my last bit of stubbornness` (not even a verb — structural collapse from literal mapping)
- Correct: `this last stubbornness of mine` / `my final stubborn stand`

**Failure 6: Parallel short lines merged into one long line.**

- Source: `花落的那一天` / `教室的那一间` / `我怎么看不见`
- Wrong: `the day the flowers fell in that classroom I couldn't see anything` (all merged)
- Correct:
  - `the day the flowers fell`
  - `that classroom of ours`
  - `why couldn't I see`

**Failure 7: Register mismatch — rock anthem translated in soft ballad English.**

- Source (倔强): `我不怕千万人阻挡，只怕自己投降`
- Wrong: `I am not afraid of the masses blocking me; I only fear surrendering myself` (too formal)
- Correct: `I'm not afraid of a million standing in my way — I only fear giving up on myself`

**Failure 8: Reduplication padded incorrectly.**

- Source: `慢慢地`
- Wrong: `very very slowly and gradually`
- Correct: `slowly` / `gently, slowly`

---

## Special Line Handling

| Line type | Detection criteria | Action |
|:---|:---|:---|
| Empty timestamp line | `[01:23.45]` with blank/whitespace content | Pass through, no translation |
| Sound effect / interlude marker | `[01:23.45]♪` or `[01:23.45]♫` | Pass through unchanged, no translation |
| Pure vocalise | `啦啦啦啦` / `哦哦哦` / `La la la` / `Oh oh oh` | Pass through unchanged, no translation |
| Metadata line | `[ti:`, `[ar:`, `[al:`, `[by:`, `[offset:` | Never translate or modify |
| In-file production credits | `词：`, `曲：`, `编曲：`, `制作人：`, `录音：` etc. | Never translate or modify — treat as metadata |
| Existing English lyric line | Full English line within a Chinese song (e.g., `oh no` / `yeah yeah yeah`) | Pass through unchanged; do NOT insert English translation |
| Mixed Chinese+English line | Chinese lyrics with embedded English words (e.g., `Baby 你是我的唯一`) | Translate the Chinese portion, preserve the English word in place |
| Classical Chinese / archaic vocabulary | Lines with 之乎者也, 兮, 苍生, 霜 etc. | Translate with elevated English register, not casual pop English |

---

## Format Template

Source file: `cn/BEYOND - 海阔天空.lrc` (partial)

**Before translation:**
```
[01:09.63]原谅我这一生不羁放纵爱自由
[01:16.62]也会怕有一天会跌倒oh no
[01:22.84]背弃了理想谁人都可以
[01:29.10]哪会怕有一天只你共我
```

**After translation (correct):**
```
[01:09.63]原谅我这一生不羁放纵爱自由
[01:09.63]forgive me — wild and free, I've loved my freedom all my life
[01:16.62]也会怕有一天会跌倒oh no
[01:16.62]I too fear the day I might fall — oh no
[01:22.84]背弃了理想谁人都可以
[01:22.84]anyone can abandon their dreams
[01:29.10]哪会怕有一天只你共我
[01:29.10]so how could I fear the day it's only you and I
```

**Common mistake to avoid:**
```
[01:09.63]原谅我这一生不羁放纵爱自由
[01:09.63]forgive me for my unruly indulgent life loving freedom   ← literal word order preserved
[01:22.84]背弃了理想谁人都可以
[01:22.84]betrayed ideals any person can do it                     ← topic-fronted preserved, missing subject
```

---

## 7-Point Self-Check

Before finalizing any translation, verify all 7 points:

- [ ] **Subject restored**: Every English line has an explicit grammatical subject (I / you / we / she / he / they) unless it is a deliberate stylistic fragment (short image line). No "headline-style" subjectless sentences.
- [ ] **Tense is coherent**: Past events are in past tense, timeless statements in present, aching desires use modal verbs (`I want` / `I ache to`). The tense does not randomly oscillate within the same verse.
- [ ] **No chengyu are translated literally**: Every 4-character idiom has been looked up and rendered by idiomatic meaning, not character meaning.
- [ ] **Parallel lines are parallel**: If two adjacent Chinese lines share syntactic structure, the two English lines share syntactic structure. Equal-weight Chinese pairs → equal-weight English pairs.
- [ ] **Modal adverbs rendered**: `偏偏` / `明明` / `好想` / `终究` / `好不容易` — each one carries emotional weight that must appear in the English. None of them may simply disappear.
- [ ] **No triple overlay**: For every Chinese line, there is exactly one English translation line immediately below it. No line has two English lines beneath it.
- [ ] **Register consistent**: The English vocabulary and grammar throughout the song match the genre register identified in Step 1. A rock anthem does not become a soft ballad; a classical-style song does not become casual slang.
