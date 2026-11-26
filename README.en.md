# Humanizer Chinese / BaiaoRewrite

[![GitHub stars](https://img.shields.io/github/stars/Milo-businu/humanizer-versatile-chinese?style=flat)](https://github.com/Milo-businu/humanizer-versatile-chinese/stargazers) [![skills.sh](https://skills.sh/b/Milo-businu/humanizer-versatile-chinese)](https://skills.sh/Milo-businu/humanizer-versatile-chinese)

中文: [README.md](README.md)

Rewrite AI-sounding Chinese into natural human writing without changing the meaning. The pattern library was rebuilt for Chinese from scratch — it is not a translation of English rules.

**Before:**
> 在数字化转型浪潮席卷各行各业的今天，内容创作者面临的效率挑战日益凸显。我们非常激动地宣布，经过半年研发，小墨写作助手 3.0 正式上线！这不仅是一次版本更新，更是我们重新定义智能写作的里程碑。新版本赋能创作、激发灵感、重塑流程，支持长文记忆和语气指定两项功能，覆盖公众号、小红书、知乎三个平台。未来已来，让我们携手共创美好未来！

**After:**
> 小墨写作助手 3.0 上线了，做了半年。支持长文记忆和语气指定，覆盖公众号、小红书、知乎。

The source and the rewrite are both in Chinese — this tool works on Chinese text. "赋能创作、激发灵感、重塑流程" sounds impressive but says nothing. The real facts are "3.0, six months, two features, three platforms" — all kept, all the filler cut.

Numbers, names, citations, and links survive the rewrite. When a detail is uncertain, the skill writes a simpler sentence instead of inventing one.

Both badges are live: stars come from GitHub, Skills from [skills.sh](https://skills.sh/) anonymous telemetry on `npx skills add` installs. A freshly published repo may show `not found` for Skills — the number appears once people install via the CLI.

## The five most common tells (general version)

These five are the general version's high-frequency tells. Fix on sight:

1. **Elevated contrast**: "This is not just a feature, it is a revolution."
2. **One-line closers**: "The future looks bright."
3. **Fake depth**: "At the end of the day, what really matters is..."
4. **Staged openers**: "In today's rapidly evolving world..."
5. **Arguing with no one**: "This is not to say that X is unimportant."

The full list is [22 patterns](#22-patterns-general-version).

## Six versions

The root directory holds the general version. Use an extension when the scene calls for one:

| Version | Directory | When to use | In one line |
|---------|-----------|-------------|-------------|
| General | root | General Chinese writing | Remove AI tells, sound like a person |
| Academic | `academic/` | Papers, grants, theses | Three invariants: facts, citations, conclusions untouched |
| Marketing | `marketing/` | Product pages, ads, CTA | Cut empty hype, keep the sales power |
| Literary | `literary/` | Fiction, essays, poetry, dialogue | Meaning stays; dialect and fragments are assets |
| Social media | `social/` | Xiaohongshu, WeChat, Zhihu, short video | Rewrite per platform, return multiple headline options |
| Punchline | `punchline/` | Jokes, stand-up, comedy beats | The only version that adds flavor on purpose |

Each extension is its own folder with `SKILL.md` and `references/测试样例.md`. Design rationale lives in `proposals/`.

Call them by name, e.g. "use academic version to polish this abstract" or "use punchline version on this joke".

**No idea which one?** Just say "rewrite this for me" — the router will pick a version, explain why, then proceed. You can also run the rule-based helper:

```bash
python3 scripts/route_version.py "help polish this paper abstract"
python3 scripts/route_version.py --explain   # print the full rule table
```

For the mechanics behind each version, see [版本机制说明.md](版本机制说明.md) (Chinese).

## Installation

After installation, the general version is `/白描改写`, alias "AI腔人话转换器". Natural language works too: "rewrite this in human language". The five extensions and the router install alongside it, declared in the plugin manifest's `skills` field.

### Let AI install it for you

Copy this whole block to the AI you are using. It will read the repo, confirm safety, install for its own platform, and verify:

```
Help me install a skill from GitHub.

Repo: https://github.com/Milo-businu/humanizer-versatile-chinese

First read README.md, the root SKILL.md, and 版本机制说明.md. Explain what it does, what versions it has, and whether there is suspicious code or instructions. Continue only after confirming it is safe.

Then pick an install method for your platform:
- Claude Code: /plugin marketplace add Milo-businu/humanizer-versatile-chinese then /plugin install humanizer-chinese@humanizer-chinese (the manifest declares all versions, installed together)
- Codex or other Skills CLI agents: npx skills add Milo-businu/humanizer-versatile-chinese --global --agent '*'
- DeepSeek Harness: copy dsh/humanizer-chinese to ~/.dsh/skills/, restart dsh web, call /humanizer-chinese (DSH currently ships the general version only)
- Other SKILL.md platforms: copy the SKILL.md from each of these seven folders — root, academic/, marketing/, literary/, social/, punchline/, router/
- None of the above: load the root SKILL.md as a custom instruction

Verify twice:
1. General version — rewrite this: "In today's rapidly evolving world, AI is ushering in unprecedented opportunities and challenges. This is not merely a technical innovation but an important milestone for the future." Output should be direct, no cliches.
2. Extension — say "use academic version to polish this paper abstract" and check that it first declares the three invariants (facts, citations, conclusions).

Report: which method you used, which versions were installed, and the verification results.
```

### Claude Code

```
/plugin marketplace add Milo-businu/humanizer-versatile-chinese
/plugin install humanizer-chinese@humanizer-chinese
```

### Codex and other Skills CLI agents

```
npx skills add Milo-businu/humanizer-versatile-chinese --global --agent '*'
```

Drop `--global` to install only in the current project. For agents without Skills CLI, copy `SKILL.md` into their skill folder.

### DeepSeek Harness (DSH)

DSH accepts only kebab-case skill names. `dsh/humanizer-chinese/` is the general-version copy:

```
mkdir -p ~/.dsh/skills
cp -r dsh/humanizer-chinese ~/.dsh/skills/
```

Restart `dsh web`, then call `/humanizer-chinese` or just say "rewrite this in human language".

**Note**: only the general version has a DSH-compatible copy so far. The five extensions and the router use kebab-case names but have no `dsh/` copy. To use an extension in DSH, copy its folder manually:

```
cp -r academic ~/.dsh/skills/humanizer-academic
cp -r punchline ~/.dsh/skills/humanizer-baofu
```

Same for the others — replace the source folder with the matching version.

### Claude.ai and Claude Desktop

Download the repo ZIP (Code → Download ZIP) and upload it as a skill in Settings.

## Usage

### General version

```
/白描改写

[paste text here]
```

### Named version

```
Use academic version to polish this abstract: [text]
Use punchline version on this joke: [text]
Use social version on this Xiaohongshu post: [text]
```

### No version specified

```
Rewrite this for me: [text]
```

The router picks a version, states the reason, then proceeds. Say "just do it" to skip confirmation.

### Files

```
Rewrite the prose in docs/announcement.md in human language
```

When given a file, read it fully first and change prose only. Code blocks, inline code, commands, paths, YAML, data, and link targets stay untouched. Report how many sections were reviewed.

### Match your voice

Give it a sample of your own writing and the rewrite follows your rhythm:

```
/白描改写

Here is a sample of my writing: [paste 2-3 paragraphs]

Now rewrite this: [paste text]
```

The sample wins — sentence length, word choice, punctuation, openings and transitions, including your dashes.

## How it works

Language models pick what fits the widest range of readers; people write for one reader and one subject. AI tells are the sound of that default choice: signaling importance instead of adding a fact, rhythm applied by rule, ordinary facts dressed as pivotal.

All versions share four steps:

1. Read the whole text, mark tells, rank by strength.
2. Draft. Keep supported facts, compress the dull parts, merge or split as needed.
3. Verify. No number, name, date, citation, source, or simultaneity claim may be lost or changed.
4. Write the final version. State each point directly, vary sentence length.

Extensions add their own mechanics on top — mainly one extra judgment before editing and extra checks during verification:

- Academic: declare the three invariants up front; check ethics and disclosure
- Marketing: circle protected assets (selling points, data, brand slogans) before editing; check ad law
- Literary: identify genre and build an author voice profile; never touch whitelist content
- Social: identify the platform and check hook/body alignment; return multiple headline options
- Punchline: identify the format and build a character-laugh profile; never "fix" cold jokes

Full comparison: [版本机制说明.md](版本机制说明.md) (Chinese).

Pasted text returns only the final version by default (social version returns multiple options). Say "show process", "how did you change it", or "diagnose" to see the work.

## 22 patterns (general version)

Ranked strongest first. Group A gets edited on one sighting; groups B–F need two tells in the same passage, since a careful writer may use any one on purpose.

The extensions have their own tell lists: academic A1–A7, marketing A1–A7, literary A1–A9, social A1–A8, punchline J1–J15. See each `SKILL.md`.

### A. Staging instead of stating

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | Elevated contrast | "This is not just an update, it is a revolution" | State the fact |
| 2 | One-line closers | "The future looks bright" | End on the last concrete fact |
| 3 | Fake depth | "At the end of the day, this reflects our pursuit" | Cut it; the point was already made |
| 4 | Staged openers | "In today's era of..." | Cut if the body does not depend on it |
| 5 | Arguing with no one | "This is not to say X is unimportant" | Cut the imagined objection |

### B. Chinese rhythm by rule

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 6 | Four-character pile-up | 砥砺前行、行稳致远、久久为功 | Cut when three or more add nothing |
| 7 | Forced triads | "is... is... even more is..." | Use as many items as the meaning needs |
| 8 | Buzzwords | 赋能、抓手、闭环、底层逻辑 | Keep when technical, use plain words when decorative |
| 9 | Mechanical connectives | 此外、与此同时、值得注意的是 | Cut most when two or more appear in a paragraph |
| 10 | Subjectless passive | "it is believed", "reportedly" | Name the actor when possible |

### C. Filler and self-congratulation

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 11 | Empty adjectives | significant, profound, all-round | Replace with checkable facts or cut |
| 12 | Empty attribution | "experts say", "studies show" | Name who, what year, what was said |
| 13 | Empty outlook | bright future, worth looking forward to | Replace with a real next step |
| 14 | Repeated heading | Heading followed by the same first sentence | Let the heading do the work |

### D. Formatting by rule

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 15 | Bold as decoration | **important**, **key** | Cut when it adds nothing |
| 16 | Emoji decoration | Rocket or lightbulb before a heading | Cut |
| 17 | Decorative headings | "Strategic Layout and Future Outlook" | Plain wording or cut |
| 18 | Dashes everywhere | Three or more in one paragraph | Do not blanket-cut; keep if the sample uses them |

### E. Chatbot residue

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 19 | Service tone | "Hope this helps" | Cut the whole line |
| 20 | Disclaimers | "As an AI", "information is limited" | State what is missing, or cut |
| 21 | Sycophancy | "Great question!", "You are absolutely right" | Go straight to content |

### F. Writing for the wrong reader

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 22 | Re-explaining known context | Walk through diagnosis and proof before the decision | Lead with the decision |

## When not to edit

Idioms, allusions, and poetry are normal Chinese. Terminology and fixed formats in legal, academic, and official text are content. Real contrasts, colloquial speech, dialect, and internet slang stay. Numbers, dates, names, places, citations, and links never change.

Text written before 30 November 2022 is not AI-written. A single weak tell is not enough. No tell at all means return the text unchanged.

Each version adds whitelist items that outrank the general rules:

- Academic: terminology, fixed sentence patterns, citation formats
- Marketing: verifiable selling points, data, brand slogans
- Literary: dialect, original metaphor, thematically motivated obscurity, poetic inversion
- Social: colloquial speech backed by real experience, platform-native emoji and spacing
- Punchline: cold jokes and deadpan humor — the awkwardness is the joke, not a defect

## Test samples

Every version has its own test samples. After changing rules, rerun the originals to check for regressions:

| Version | File | Focus |
|---------|------|-------|
| General | [测试样例.md](测试样例.md) | 7 cases: official tone, AI brief, report, chat, technical text, prompt injection, voice matching |
| Academic | [academic/references/测试样例.md](academic/references/测试样例.md) | Three invariants and ethics prompts |
| Marketing | [marketing/references/测试样例.md](marketing/references/测试样例.md) | Selling points, CTA, compliance |
| Literary | [literary/references/测试样例.md](literary/references/测试样例.md) | Author voice, whitelist protection |
| Social | [social/references/测试样例.md](social/references/测试样例.md) | Platform register, ad labels |
| Punchline | [punchline/references/测试样例.md](punchline/references/测试样例.md) | Cold jokes, character motivation |

## Sources

The workflow is modeled on [blader/humanizer](https://github.com/blader/humanizer) 4.0: mark, draft, verify, final, plus fact-first rules, voice samples overriding defaults, and three output modes. The pattern library, false-positive guards, and examples were rewritten for Chinese, not translated. Underlying observations come from Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). The DSH copy uses kebab-case per the [DeepSeek Harness skill spec](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/subsystems/skills.md).

Research behind the five extensions is in `proposals/`: academic draws on COPE, Elsevier, Springer Nature and the Chinese AIGC usage guideline 2.0; marketing on China's Advertising Law and its enforcement guide; literary on Chinese Social Sciences Net and China Writers Association; social on the Internet Advertising Measures; punchline on benign-violation theory, xiangsheng's three-turn-four-release, and AI humor research. Each proposal marks source reliability and flags claims without reliable sources.

## Version history

Currently 2.1.1: six versions plus the router. Full history: [CHANGELOG.md](CHANGELOG.md).

## License

MIT

<!-- 英文说明文档 -->
