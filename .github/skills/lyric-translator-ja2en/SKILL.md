---
name: lyric-translator-ja2en
description: "Use when translating Japanese lyrics to English in .lrc files by inserting same-timestamp English lines under each Japanese lyric line in strict alternating format; preserve LRC structure, never translate Chinese/English or metadata, and enforce semantic, rhythmic, and natural-English quality checks."
version: 1.0.0
scopes: ["workspace"]
tags: ["lyrics", "translation", "japanese", "english", "ja-en", "jp", "en", "inline-translation", "lrc", "subtitle", "karaoke", "timed-lyrics", "localization", "transcreation"]
---

# Japanese Lyrics Alternating-Overlay Translation Skill (JA → EN)

**Goal:** Directly edit existing Japanese `.lrc` files, inserting an English translation line with the **same timestamp** immediately after each Japanese lyric line, producing a strict "original → translation → original → translation" alternating display.

---

## Executive Summary

When invoked, execute these 8 rules first:

1. Only process Japanese lyric lines. Do not touch existing English/Chinese lines, metadata tags, blank lines, or pure sound-effect lines (`♪`/`♫`).
2. **Read the entire file in one `read_file` call first.** Determine the overall theme, emotional arc, and narrative perspective (first-person confessional, third-person narrative, duet, etc.). Complete full-song analysis in memory before writing — never alternate between reading and writing.
   Hard rule: If the song is a duet or multi-voice narrative, map speakers first. Do NOT conflate different "I/you" voices into one.
3. Scan 3–5 lines before and after each line to detect broken long sentences, te-form chains, and mixed Japanese/English segments.
4. Translate the semantic core (main action/conclusion/emotional anchor) first, then decide on modifiers. Do not lead with imagery before meaning.
5. Translations must read like **natural English lyrics first, literature second**: singable, idiomatic, free of ESL phrasing. Keep each English line to **6–14 words**; lines over 14 words must be split to follow the original timestamp breakpoints.
6. Fragmented Japanese lines (te-form chains, run-on cut across timestamps) must each produce a standalone English fragment — front lines must NOT "steal ahead" and translate content belonging to a later timestamp.
7. Hook words, core imagery, and chorus key phrases must be translated **consistently across the entire song**. Repeated lines reuse the same English translation verbatim.
8. Before submitting: verify no English/metadata lines were touched, no third-line overlay was created, no over-interpretation was added, and no line exceeds the word limit.

---

## Absolute Constraints (Red Lines)

- **Format integrity**: Preserve all LRC timestamp formatting without exception. Lines with multiple timestamps (e.g., `[00:15.80][00:20.10]lyrics`) must have all timestamps reproduced identically on the translation line.
- **Metadata immunity**: Never translate or modify lines beginning with `[ti:`, `[ar:`, `[al:`, `[by:`, `[offset:`, or similar metadata tags.
- **No re-translation of existing English**: If a line is already in English (e.g., embedded English lyrics within the Japanese song), do not add a translation — treat it as-is.
- **No re-translation of Chinese**: If the file contains Chinese lines (bilingual source), do not touch them.
- **Exclusive overlay rule**: Each Japanese lyric line may have **exactly one** same-timestamp English translation below it. If an existing English translation is already present (e.g., a prior machine translation), **overwrite/replace** it — never stack a third line.
- **Pure vocalise lines**: Lines consisting entirely of vocalise (`Ah ah ah`, `La la la`, `Oh oh oh`) or Japanese phonetic filler (`ラララ`, `アハハ`) — keep as-is; do **not** insert a translation.
- **No over-interpretation**: Default to faithful meaning. Never add backstory, character motivation, or setting details absent from the original (see "Translation vs. Over-Interpretation" section).
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

- [ ] Scan the full text. Label each line: Japanese lyric / existing English / Chinese / metadata / special (blank, `♪`, vocalise).
- [ ] Identify song genre and emotional register (J-Pop ballad, rock anthem, Vocaloid electro-pop, anime OP/ED, etc.) — genre determines acceptable English register and vocabulary level.
- [ ] If duet or multi-voice: build a speaker map (who says what, what does "I/you" refer to in each section).
- [ ] Lock in a consistent translation for: chorus hook phrases, core imagery words, title phrase, and recurring motifs.
- [ ] Scan for te-form chains and broken long sentences spanning multiple timestamps. Plan how to fragment their English equivalents.
- [ ] Check if same-timestamp English already exists. If yes — evaluate keep/replace; never stack.

### 2. Translation Pass

- [ ] Process each line: Japanese → English translation on the very next line, same timestamp.
- [ ] **Mandatory: add an English subject** where Japanese drops it (Japanese is pro-drop; English is not). Choose the correct pronoun based on context (I / you / we / she / he / they).
- [ ] Translate verb endings for mood and tense — do not flatten all verbs to simple present (see "Verb & Tense Handling" section).
- [ ] For te-form chains: each fragment stands alone; the first fragment must not pre-empt the conclusion in the last fragment.
- [ ] Katakana English loanwords: restore to their English source form — do not re-translate back through the Japanese phonetic shell (see "Katakana Loanwords" section).
- [ ] Blank lines / `♪` lines / vocalise lines → pass through, no translation.

### 3. Refinement

- [ ] Remove ESL artifacts: awkward subject-verb order, over-literal particle rendering, stilted formal phrasing.
- [ ] Check that each line can be spoken naturally in one breath (≤ 14 words strongly preferred).
- [ ] Verify sentence-final particles have been reflected in English tone (see particle table).
- [ ] Ensure chorus, hook, and core imagery translations are identical across all occurrences.
- [ ] For structurally parallel Japanese lines (anaphora, parallel te-form), produce matching parallel English structures.

### 4. Validation

- [ ] Original and translation lines strictly alternate; output is parseable by standard LRC players.
- [ ] No missed Japanese lines, no metadata translated, no existing English/Chinese modified, no triple overlay.
- [ ] **Manual spot-check**: Randomly pick 1 line each from intro / verse / chorus / bridge. Read the English aloud. Confirm: natural phrasing, fits in one breath, no invented details, pronoun is correct.

---

## Japanese–English Linguistic Difference Handling Rules

### 1. Pro-Drop → Mandatory Subject Restoration

Japanese regularly omits subject pronouns. English grammar requires them. Restoring the correct pronoun is one of the most critical translation decisions:

| Situation | Strategy | Example |
|:---|:---|:---|
| Single consistent first-person narrator | Use "I" consistently | `心の全てを奪った` → `stole away my entire heart` |
| Second-person address (告白, narrative) | Use "you" | `君の姿` → `your silhouette` |
| Ambiguous subject (could be I or you) | Read 3–5 lines for context; choose the most natural reading | — |
| Duet: speaker switches mid-song | Track speaker map; switch pronouns accordingly | — |
| Third-person narration | Use "she" / "he" / "they" as context implies | `彼女は笑った` → `she smiled` |
| Collective/universal statement | Use "we" or impersonal phrasing | `二人でいよう` → `let's stay together` |

> **Warning**: Incorrect pronoun assignment is the #1 source of meaning corruption in ja→en translation. When uncertain, read the full song context before choosing.

### 2. SOV → SVO Word Order

Japanese is Subject-Object-Verb (SOV); English is Subject-Verb-Object (SVO). Reorder, do not translate word-by-word:

| Japanese structure | English structure | Example |
|:---|:---|:---|
| S + O + V | S + V + O | `僕の全てを奪った` → `stole everything from me` (not "my everything stole") |
| Adj + N | Adj + N (usually same) | `深い青` → `deep blue` |
| Verb-final modifying clause | Relative clause before noun, or restructured | `寂しい目をしてたんだ` → `her eyes looked so lonely` |
| Stacked modifiers before noun | Restructure into relative clause or appositive | `どこか儚い空気を纏う君は` → `you, wrapped in a somehow fleeting air` |

### 3. Sentence-Final Particles → English Tone & Punctuation

Sentence-final particles carry emotional information that must be mapped to English through **word choice, punctuation, and modal verbs** — they cannot simply be dropped:

| Particle | Core function | English mapping | Example |
|:---:|:---|:---|:---:|
| `ね` | Seeks agreement / softens assertion | Tag question, or soften with "right?", "isn't it" | `そうだね` → `that's true, isn't it` |
| `よ` | Assertion / emphasis | Stronger statement; use `!` or intensifiers like "I know" / "I tell you" | `信じてるよ` → `I believe in us` (with firm tone) |
| `な` | Self-directed musing / mild exclamation | Trailing `...` or introspective phrasing | `すごいな` → `so incredible…` |
| `かな` | Self-questioning / uncertainty | `I wonder` / `maybe` / `...?` | `どこかな` → `I wonder where you are` |
| `の` | Soft explanation / femininity marker | Fold into sentence naturally | `好きなの` → `because I like you` |
| `じゃない？` | Rhetorical, seeks affirmation | `right?` / `isn't that…?` | `青春じゃない？` → `isn't that what youth is?` |
| `って` | Quotation / topic-marking / hearsay | Quotation → `"..."` or `saying`; topic → rephrase | `好きだって？` → `you said you loved me?` |
| `さ` | Casual confidence / light emphasis | Casual tone; often absorbed into surrounding words | `分かり合えるさ` → `we'll understand each other` |

### 4. Te-Form Chains → English Coordination

Japanese uses te-form (～て) to chain multiple actions without re-stating the subject. English must explicitly coordinate:

| Strategy | When to use | Example |
|:---|:---|:---|
| `and` coordination | Two equal actions of similar weight | `溶けてゆくように` → `melting away` |
| Participle phrase | One action modifies another | `沈むように溶けてゆくように` → `sinking, dissolving into nothing` |
| Sequential `then` | Clear temporal sequence | `花束を抱えて歩いた` → `I walked, holding a bouquet` |
| Split across timestamps | When original Japanese is split across lines | Keep each English fragment standalone; front line must not conclude the chain |

> **Critical**: When a te-form chain is split across multiple timestamps, the English fragments must each be capable of standing alone while leaving the semantic conclusion for the final timestamp — mirror the original's musical suspense.

### 5. Verb Tense and Aspect

Japanese verbs encode aspect (completive/progressive) rather than time explicitly. Map to English tense based on context:

| Japanese form | English tense | Notes |
|:---:|:---:|:---|
| `〜た` (completive) | Simple past | `奪った` → `stole`; `笑った` → `smiled` |
| `〜ている` (ongoing state) | Present progressive or simple present | `見つめている` → `staring at` or `I stare` |
| `〜てしまう` (regrettable completion) | Past + emotional qualifier | `泣いてしまう` → `I end up crying` / `I can't stop crying` |
| `〜たい` (desire) | `want to` + verb | `言いたい` → `I want to say` |
| `〜よう` (volitional / let's) | `let's` / `I will` / `we'll` | `いよう` → `let's stay` |
| `〜ないで` (negative request) | `don't` + verb / `please don't` | `離さないでよ` → `don't let go` |
| `〜かもしれない` | `maybe` / `perhaps` / `might` | `消えてしまうかも` → `maybe I'll disappear` |
| `〜はず` | `should` / `supposed to` | `分かるはず` → `you should understand` |

### 6. Katakana Loanwords

Katakana loanwords fall into three categories — never phonetically re-transliterate them back into romanized Japanese:

| Category | Strategy | Example |
|:---|:---|:---|
| **Direct English loanword** | Restore the original English word | `テレキャスター` → `Telecaster`; `ドリーム` → `dream`; `スマイル` → `smile` |
| **Brand / proper noun** | Restore brand name as-is | `ティファニー` → `Tiffany` |
| **Distorted/adapted loanword** | Identify source word by sound, restore or approximate | `ナナメ` (斜め, but in katakana rhythm position) → treat as Japanese meaning "diagonal/sideways" |
| **Katakana-style Japanese mimetic** | Treat as Japanese onomatopoeia, not as an English loanword | `ハチャメチャ` → translate the meaning, not the sounds |
| **Embedded English lines** (not loanwords) | Treat as-is; do NOT insert English translation — they ARE English | `Boys be ambitious like this old man` → keep as-is, skip |

### 7. Japanese Onomatopoeia and Mimetics (擬音語・擬態語)

Do not transliterate; translate the sensation or imagery:

| Priority | Strategy | Examples |
|:---:|:---|:---|
| 1 | **Imagery/sensation verb** | `ドキドキ` → `heart racing` / `trembling`; `ソワソワ` → `restless` / `on edge` |
| 2 | **Adjective/adverb phrase** | `キラキラ` → `glittering` / `sparkling`; `ふわふわ` → `floating` / `light as air` |
| 3 | **Idiomatic equivalent** | `きょろきょろ` → `looking around nervously`; `うろうろ` → `pacing` / `wandering` |
| 4 | **Rhythm-position mimetics** | If the word occupies a pure rhythmic/hook position (e.g., `ハチャメチャ`), prioritize a punchy English equivalent over a literal gloss: `ハチャメチャ` → `all over the place` / `chaotic` |

### 8. Japanese Pronouns and Gendered/Register Speech

Japanese has multiple first/second-person pronoun options encoding gender and social register. Map to appropriate English register:

| Japanese | Register/Gender | English translation strategy |
|:---:|:---:|:---|
| `僕` (boku) | Masculine, soft/youthful | `I` (gentle tone; avoid overly macho phrasing) |
| `俺` (ore) | Masculine, rough/assertive | `I` (stronger tone; can use more direct/aggressive English) |
| `私` (watashi) | Neutral/feminine formal | `I` (neutral to formal register) |
| `あたし` (atashi) | Feminine, casual | `I` (lighter, more casual English register) |
| `君` (kimi) | Affectionate/poetic "you" | `you` (warm register; can use `darling` / `my love` in very intimate contexts) |
| `あなた` (anata) | Formal/romantic "you" | `you` (slightly formal or tender) |
| `お前` (omae) | Rough/intimate "you" | `you` (blunt or intimate; context-dependent) |

> The pronoun register also signals what **overall English register** to aim for. A `俺/お前` song (like うっせぇわ) should sound aggressive and colloquial in English. A `僕/君` J-Pop ballad should sound softer and more poetic.

### 9. High-Context Compression → English Explicitness

Japanese is a high-context language — subjects, objects, and causal connections are routinely omitted. English lyrics need a baseline level of explicitness. The challenge is adding **just enough** without over-interpreting:

| Situation | Strategy |
|:---|:---|
| Missing subject | Add the correct pronoun (Rule 1 above) |
| Missing object | Infer from context; use "it" or rephrase if uncertain |
| Implicit causality (`〜から`/`〜ので` omitted) | Add "because" / "so" only if it sounds natural; otherwise restructure |
| Poetic ellipsis (deliberate omission for atmosphere) | Preserve the ellipsis — use `...` or fragmented phrasing in English |
| Implied negative emotion (understatement) | Do not amplify — translate the surface level and trust the English reader |

### 10. Natural English Lyric Register

The most important meta-rule: **the English translation must sound like it was written as English lyrics, not translated from Japanese.**

Checklist for natural English lyric style:
- [ ] No inverted subject-verb for no reason (`stolen was my heart` is archaic; avoid unless intentional)
- [ ] Contractions are welcome (`I've`, `you're`, `don't`, `won't`) — Japanese songs are almost always informal register
- [ ] Avoid literal particle translation: `に` is not always "to/in/at" — choose what flows
- [ ] Avoid literal `〜の` → `of` chains: `心の全ての底の痛みの` → NOT `the pain of the bottom of all of my heart` → YES `the deepest pain in my heart`
- [ ] Aim for stress-timed rhythm: English lyrics feel natural when stressed syllables fall on strong beats; check that key stress words don't all cluster on weak positions
- [ ] Short lines: English words are longer than Japanese characters — a 5-character Japanese line may need only 3–4 English words; do not pad

---

## Translation vs. Over-Interpretation

Faithful translation expands **what the original implies**. Over-interpretation **invents new story, setting, or motivation** not present in the source.

| Original | Acceptable translation ✓ | Over-interpretation ✗ | Reason |
|:---:|:---:|:---:|:---|
| `沈むように溶けてゆくように` | `like I'm sinking, like I'm dissolving away` | `like I'm sinking into the ocean, dissolving into her embrace` | "ocean" and "embrace" are not in the source |
| `二人だけの空が広がる夜に` | `on a night when our own sky stretches wide` | `on a starry night when just the two of us lay on the rooftop` | "stars" and "rooftop" are invented |
| `さよならだけだった` | `all it was — was goodbye` | `she only said goodbye because she had given up on the relationship` | causation is invented |
| `目が合った` | `our eyes met` | `our eyes met and we both knew it was love` | "knew" and "love" are inferred too far |
| `テレキャスター背負った` | `Telecaster on his back` | `carrying his battered old Telecaster to band practice` | "battered," "old," and "practice" are invented |

---

## Common Failure Modes and Corrected Examples

**Failure 1: Forgetting to add a subject — output sounds like a machine translation.**

- Source: `初めて会った日から`
- Wrong: `from the day met for the first time` (missing subject)
- Correct: `from the day we first met`

**Failure 2: SOV word order preserved in English.**

- Source: `僕の心の全てを奪った`
- Wrong: `my heart's everything stole`
- Correct: `stole everything in my heart`

**Failure 3: Sentence-final particle dropped, emotion lost.**

- Source: `離さないでよ` (`よ` = emphatic plea)
- Wrong: `don't let go`
- Correct: `please, don't let go` or `don't you let go`

**Failure 4: Te-form chain front-line "steals ahead."**

- Source: `[00:01]沈むように` / `[00:02]溶けてゆくように`
- Wrong: `[00:01]sinking and dissolving into nothing` / `[00:02]like it's all fading away` (first line pre-empts second)
- Correct: `[00:01]like I'm slowly sinking` / `[00:02]like I'm dissolving away` (each line standalone, conclusion deferred)

**Failure 5: Katakana loanword phonetically re-transliterated.**

- Source: `テレキャスター背負った`
- Wrong: `terekya suta on my back` / `with a telecast on my back`
- Correct: `Telecaster slung on my back`

**Failure 6: Over-literal `〜の` genitive chaining.**

- Source: `心の奥の痛み`
- Wrong: `the pain of the interior of the heart`
- Correct: `the ache deep in my heart`

**Failure 7: Register mismatch — aggressive Japanese song translated in soft poetic English.**

- Source (うっせぇわ): `はぁ？うっせぇうっせぇうっせぇわ`
- Wrong: `ah, how terribly noisy you are` (way too polite)
- Correct: `huh? shut up shut up just shut UP` (match the raw, aggressive register)

**Failure 8: Parallel short lines padded to unequal lengths.**

- Source: `私は雨 / 君は風`
- Wrong: `I am the gentle falling rain` / `you are wind`
- Correct: `I am the rain` / `you are the wind` (parallel structure, equal weight)

---

## Special Line Handling

| Line type | Detection criteria | Action |
|:---|:---|:---|
| Empty timestamp line | `[01:23.45]` with blank/whitespace content | Pass through, no translation |
| Sound effect / interlude marker | `[01:23.45]♪` or `[01:23.45]♫` | Pass through unchanged, no translation |
| Pure vocalise | `Oh oh oh oh` / `La la la` / `ラララ` / `アハハ` etc. | Pass through unchanged, no translation |
| Metadata line | `[ti:`, `[ar:`, `[al:`, `[by:`, `[offset:` | Never translate or modify |
| Existing English lyric line | Full English line in a Japanese song | Pass through unchanged; do NOT insert English translation |
| Existing Chinese translation line | Full Chinese line | Pass through unchanged; do NOT touch |
| Embedded English phrase within Japanese | `Boys be ambitious like this old man` etc. | Pass through as-is; do not insert translation |
| Japanese line with `〜` (prolonged sound) | `行かないで〜` | In English, render as `...` or elongated expression: `don't go…` |
| Japanese line with `…` (ellipsis) | `私は…` | Preserve as `…` in English: `I…` |
| Dialog within lyrics | `「さよならだけだった」` | Keep quotation marks: `"all it was — was goodbye"` |

---

## Format Template and Example

**Input:**

```lrc
[ti:夜に駆ける]
[ar:YOASOBI]
[00:01.00]沈むように溶けてゆくように
[00:08.46]二人だけの空が広がる夜に
[00:30.94]「さよなら」だけだった
[01:41.39]二人でいよう
[03:00.35]ラララ
[03:05.00]
```

**Correct Output:**

```lrc
[ti:夜に駆ける]
[ar:YOASOBI]
[00:01.00]沈むように溶けてゆくように
[00:01.00]like I'm sinking, like I'm dissolving away
[00:08.46]二人だけの空が広がる夜に
[00:08.46]on a night when our own sky stretches wide
[00:30.94]「さよなら」だけだった
[00:30.94]"goodbye" — that was all it was
[01:41.39]二人でいよう
[01:41.39]let's stay together
[03:00.35]ラララ
[03:05.00]
```

> `ラララ` (pure vocalise) and the empty timestamp line pass through with no translation inserted.

---

## Quick Self-Check Before Output

Before submitting the file, run through this checklist:

1. **Timestamp regex validation**: Do all newly generated lines strictly match `^(\[\d{2}:\d{2}\.\d{1,3}\])+.*`? (Supports 1–3 digit milliseconds and multi-timestamp lines)
2. **Metadata safety check**: Has any translation been inserted below a metadata line (`[ti:`, `[ar:`, etc.)? If yes — remove it immediately.
3. **Overlay check**: Does any section show a "JP → EN → EN" triple layer? If yes — the prior English translation was not overwritten correctly; fix to "JP → EN" only.
4. **Completeness check**: Are there any Japanese lyric lines that have no English translation below them (excluding intentional skip types)?
5. **Subject audit**: Scan 5 random translation lines — does every sentence have a grammatical subject? If not, add the appropriate pronoun.
6. **Register audit**: Read the first chorus line aloud. Does the English **feel like** it belongs in a song of this genre? If it sounds like a textbook sentence, revise.
7. **Semantic spot-check**: From verse / chorus / bridge, pick 1 line each and read the English aloud. Confirm:
   - Meaning is clear?
   - Reads in one breath (≤ 14 words preferred)?
   - No invented details (people, places, events, motivations not in the source)?
   - Pronoun is correct given the speaker context?
