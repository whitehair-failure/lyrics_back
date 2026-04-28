# Lyric Translation — Shared Rules

Applies to all 12 direction pairs (ZH/JA/KO/EN). Use together with the matching `reference/{pair}.md` file.

---

## Quick Reference: 8 Core Rules

When invoked frequently, apply these 8 rules first:

1. **Source lines only**: Do not touch target-language lines, metadata lines, blank lines, or pure sound-effect lines (`♪`/`♫`).
2. **Read entire file first**: The first tool call must be a single `read_file` of the full lyrics file. Assess the song's subject, emotional tone, and narrative POV (first person / third person / duet / multi-voice) before writing anything. **Never interleave reads and writes.**  
   For duets/multi-voice: build a speaker map before translating — identical pronoun forms used by different voices must not be translated the same way.
3. **Pre-read context**: Before translating each line, review 3–5 lines before and after to catch long-sentence splits, chained grammar, and code-mixed passages.
4. **Core before modifier**: Translate the action/conclusion/emotional core first, then decide on modifiers and register.
5. **Singability over literalism**: Translations must be clear, natural, and singable. Single-line length must stay within the cap defined in the pair-specific file; split at natural breath points rather than cramming onto one line.
6. **Respect breath points**: Each translated line should be readable in isolation. Never front-load a subsequent line's conclusion into the current line.
7. **Consistent key terms**: Use the same translation for choruses, hooks, core imagery, and the song title throughout the entire file. Reuse identical wording for repeated lines.
8. **Final check before output**: Confirm no target-language lines were modified, no metadata was touched, no third line was stacked onto a source line, no plot points were added, and all line lengths are within cap.

---

## Absolute Constraints (Red Lines)

| Constraint | Rule |
|:---|:---|
| **Format Lock** | Preserve all LRC structure. Do not modify timestamp format. Lines with multiple timestamps (e.g. `[00:15.80][00:20.10]lyrics`) must keep all timestamps. |
| **Metadata Immunity** | Lines beginning with `[ti:` `[ar:` `[al:` `[by:` `[offset:` and embedded production credits (`词：`/`曲：`/`編曲：`/`作詞：`/`Lyrics:`/`Music:` etc.) must never be translated or modified. |
| **No Re-translation** | Do not re-translate or modify lines already in the target language. |
| **One Translation Per Source Line** | Each source line gets exactly one same-timestamp translation line inserted below it. If a translation already exists, overwrite/correct it — never stack a third line. |
| **Filler Line Passthrough** | Pure vocalization filler lines (`Oh oh oh`/`La la la`/`오오오`/`啦啦啦`/`あーあー` etc.) pass through unchanged — no translation inserted. |
| **No Plot Injection** | Paraphrase may expand information already in the source. It must never add plot points, characters, motivations, or identities not present in the original. |
| **Completeness** | Every repeated lyric line must be translated. Do not skip or merge lines. |
| **Line Length Cap** | Single translated lines must not exceed the cap specified in the pair-specific file. Split at natural breath points when over the limit. |
| **Skip Empty/SFX Lines** | Blank timestamp lines (empty or whitespace content) and pure sound-effect lines (`[01:23.45]♪`) pass through unchanged — no translation inserted. |

---

## Execution Workflow

### Step 0 — Tool Discipline (Mandatory)

**Read before write, always.**

- Call `read_file` once to load the entire lyrics file before any edits.
- Complete all analysis in memory, then write edits in a single pass using `replace_string_in_file` or `edit_file`.
- Do **not** alternate between reads and writes — this causes line-offset drift and translation stacking.
- For files over 200 lines: two `read_file` calls are acceptable, but merge the full analysis in memory before writing.

### Step 1 — Survey and Plan

- [ ] Scan the full file. Label each line as: source lyric / target-language line / metadata / special (blank / SFX / filler / production credit).
- [ ] Determine song subject, emotional tone, and narrative POV (first person, third person, duet, multi-voice).
- [ ] For duets/multi-voice: build a speaker map (who speaks in each section, what pronouns refer to whom).
- [ ] Lock in chorus, hook, and core-imagery translations to use consistently throughout.
- [ ] Flag long-sentence splits, chained grammar, and code-mixed passages. For lines with existing translations, decide: keep, overwrite, or skip (never stack).

### Step 2 — Translate (First Draft)

- [ ] Process each source line: insert one same-timestamp translation line directly below.
- [ ] Default to short and direct; avoid stacked modifiers and added plot points.
- [ ] Split lines at natural breath points; keep each line self-contained. Do not front-load the next line's conclusion.
- [ ] Code-mixed lines: preserve the source line as-is; translate the overall meaning naturally in the target line.
- [ ] Filler vocalization lines / pure `♪` lines → pass through unchanged.

### Step 3 — Refine

- [ ] Remove over-literary phrasing, excessive modifiers, and injected plot points.
- [ ] Unify chorus/hook/core-imagery translations across the whole file.
- [ ] Verify narrative POV and pronoun consistency throughout.
- [ ] Verify culture-specific terms (proper nouns, cultural references) are translated by meaning, not transliterated, where appropriate.

### Step 4 — Quality Check

- [ ] Source and translation lines strictly alternate; output is valid LRC.
- [ ] No missing lines, no modified metadata, no modified target-language lines, no stacked third lines.
- [ ] **Spot-check**: Read one line aloud from each of intro / verse / chorus. Confirm: meaning is clear, singable in one breath, contains no plot points not in the source.

---

## Paraphrase vs. Over-Interpretation

Paraphrase is natural expansion of **information already in the source**. Over-interpretation **adds new plot, identity, scene, or motivation** not present in the original.

| Judgment | Example |
|:---|:---|
| ✓ **Acceptable paraphrase** — extends implied emotion naturally | `want to disappear` → `想消失不见` |
| ✗ **Over-interpretation** — adds specifics not in the source | `想消失在失恋的痛苦里` ("heartbreak" is invented) |
| ✓ **Acceptable** — reorders into natural target-language expression | Idiom or colloquial naturalization |
| ✗ **Prohibited** — expands poetic ellipsis into prose annotation | `running in the rain` → `不顾一切地向前冲，忘记所有伤痛` (invented motivation) |

Concrete examples for your direction are in the pair-specific file.

---

## Special Line Handling

| Line Type | Detection Criterion | Action |
|:---:|:---|:---:|
| Blank timestamp line | `[01:23.45]` with empty or whitespace content | Pass through, no translation |
| Pure SFX / interlude marker | `[01:23.45]♪` or `[01:23.45]♫` | Pass through, no translation |
| LRC metadata tag | Starts with `[ti:` `[ar:` `[al:` `[by:` `[offset:` | Never translate or modify |
| Embedded production credit | Contains `词：` `曲：` `編曲：` `作詞：` `作曲：` `Lyrics:` `Music:` etc. | Never translate or modify |
| Already-target-language line | Entire line is in target language | Pass through, no translation |
| Already-English line (non-EN source) | Entire line is English (e.g. `Yeah yeah`, `Oh baby`) | Pass through, no translation |
| Filler vocalization | `오오오` / `あーあー` / `Oh oh oh` / `La la la` / `啦啦啦` etc. | Pass through, no translation |
| Code-mixed line | Source language mixed with other languages within the line | Preserve source line; translate overall meaning naturally |
| Ellipsis pause line | `…` denoting trailing-off or silence | Preserve `…` in translation, or carry the pause feeling into register |

---

## Format Reference

**Input:**
```lrc
[ti:Song Title]
[ar:Artist]
[00:15.19]Source lyric line one
[00:18.50]Source lyric line two
[01:22.40]Existing target-language line
[00:20.00]♪
[00:25.00]
```

**Correct output:**
```lrc
[ti:Song Title]
[ar:Artist]
[00:15.19]Source lyric line one
[00:15.19]Translated line one
[00:18.50]Source lyric line two
[00:18.50]Translated line two
[01:22.40]Existing target-language line
[00:20.00]♪
[00:25.00]
```

> `♪` lines, blank timestamp lines, already-target-language lines, and metadata lines pass through unchanged — no translation inserted.
