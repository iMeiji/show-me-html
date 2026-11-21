---
name: show-me-html
description: Create self-contained HTML artifacts when a request benefits from spatial layout, visual hierarchy, diagrams, formulas, data charts, evidence, interaction, presentation, or an exportable one-off tool. Use for non-trivial docs, writeups, plans, specs, reports, explainers, summaries, comparisons, reviews, PR descriptions, mockups, diagrams, flowcharts, decks, slides, status updates, incident reports, research, quantitative analysis, playgrounds, editors, and tools. Stay in markdown for short chat replies, code-only answers, terminal-style instructions, and disposable summaries that are only a few bullets.
---


# Show Me HTML

Use this skill when HTML will make the shape of the work clearer than markdown. The goal is not "always output HTML"; the goal is to choose HTML when layout, hierarchy, color, motion, diagrams, or interaction materially improve understanding or action.

Treat source documents as raw material, not as the target structure. Preserve meaning, facts, evidence, formulas, and user intent, but redesign the presentation when another structure would make the content easier to understand.

## Decide the medium

Reach for a self-contained `.html` artifact when any of these are true:

- **Comparison:** two or more options must be weighed side by side.
- **Spatial structure:** timelines, diffs, maps, flows, states, before/after, architecture, or call graphs carry meaning.
- **Interaction:** the reader needs to tune, filter, drag, simulate, preview, or feel motion.
- **Reference use:** the result will be navigated non-linearly with tabs, anchors, panels, glossary, or filters.
- **Visual hierarchy:** status, severity, ownership, metrics, code, or design tokens need color and structured layout.
- **Quantitative reasoning:** formulas, statistical claims, charts, plots, or tables must be explained and inspected.
- **Evidence:** claims, research, sources, logs, code references, or data provenance must be distinguishable.
- **Round trip:** the reader needs to manipulate data and export the result back to markdown, JSON, prompt text, config, or CSV.
- **Sharing:** the artifact is meant to be read carefully, presented, reviewed, or sent to others.
- **Length:** the answer would become a long linear document.

Stay in markdown for short conversational answers, code snippets, command sequences, small checklists, and files intended to be hand-edited or diffed repeatedly.

## Artifact brief

Before building, silently lock this brief:

- Purpose: what job should the artifact do?
- Audience: who will read or use it, and how much context do they have?
- Content shape: comparison, timeline, report, review, diagram, deck, editor, prototype, or hybrid.
- Representation strategy: what should move from linear text into comparison, timeline, diagram, map, cards, dashboard, glossary, deck, simulator, or tool?
- Visual direction: the deliberate tone and one memorable design idea.
- Interactions: what state changes, if any, must the reader control?
- Chart strategy: for quantitative artifacts, whether ECharts is needed; if not, why a smaller SVG/CSS/table treatment is enough.
- Export path: for any editor/tool, what output format closes the loop?
- Constraints: offline use, privacy, screen size, accessibility, performance, and user-provided style.

## Universal rules

Every HTML artifact must:

1. Be a single self-contained `.html` file unless the user explicitly asks otherwise.
2. Work offline by default: inline CSS and JS; no required runtime server; avoid external assets unless the user provided them or they are clearly optional.
3. Use real layout, not markdown wrapped in tags. Render comparisons as columns, flows as diagrams, timelines as timelines, diffs as diffs.
4. Do not mirror the source document's heading order unless the user asks for faithful conversion. If the HTML outline looks like the markdown outline with styling, rethink the artifact shape.
5. Be readable within five seconds: title, short framing sentence, and clear primary structure above the fold.
6. Use semantic HTML first: `main`, `section`, `article`, `nav`, `table`, `button`, `a`, `label`, and ordered headings before ARIA patches.
7. Be responsive from phone to desktop with stable dimensions for fixed-format UI like boards, grids, slide canvases, charts, controls, and toolbars.
8. Be keyboard usable: visible `:focus-visible`, sensible tab order, real buttons for actions, real links for navigation.
9. Respect motion and comfort: honor `prefers-reduced-motion`, animate only purposeful moments, and avoid `transition: all`.
10. Handle real content: long text, empty states, narrow screens, large numbers, loading, errors, and destructive actions.
11. Export state for every interactive editor/tool. Without export, an editor is incomplete.
12. For factual or evidence-heavy artifacts, keep source notes close to important claims, distinguish fact from inference when it matters, and surface conflicting, stale, skipped, or uncertain data.
13. For data-heavy artifacts with benchmarks, multiple metrics, trend lines, rates, or comparison charts, default to ECharts per `math-and-data.md`. If using inline SVG/CSS/tables instead, state the reason in the final note and keep the underlying data inspectable.

## Reference selection

Read only the references needed for the task:

- `references/patterns.md`: comparisons, plans, reviews, reports, explainers, diagrams, decks, and other artifact shapes.
- `references/visual-direction.md`: typography, color, composition, motion, background detail, and avoiding generic generated aesthetics.
- `references/interface-quality.md`: accessibility, focus, forms, animation, content handling, performance, dark mode, locale, and interaction checks.
- `references/interactive-tools.md`: one-off editors, tuners, triage boards, state, persistence, reset, export, and failure states.
- `references/math-and-data.md`: formulas, equations, derivations, statistics, metrics, charts, plots, tables, and quantitative explainers.

If the request includes frontend design, UI polish, mockups, prototypes, visual exploration, or public-facing presentation, read `visual-direction.md`.

If the artifact contains any interaction, forms, navigation, custom controls, generated images, animation, or dense responsive layout, read `interface-quality.md`.

If the user will manipulate state or data, read `interactive-tools.md` before designing the controls.

If the artifact includes formulas, equations, statistical claims, charts, plots, tables, metrics, or quantitative reasoning, read `math-and-data.md`.

## Build workflow

1. Run a representation pass: identify the reader's job, content atoms, relationships, decisions, evidence, caveats, and latent visuals.
2. Choose the artifact shape and visual direction from the representation pass, not from the source document order.
3. For quantitative artifacts, decide the chart strategy before implementation: ECharts by default for substantive data visualization; SVG/CSS/table only when the chart is genuinely tiny or a table is clearer.
4. Sketch the layout around the content's structure, not around generic cards.
5. Implement the full single-file HTML with inline CSS and JS.
6. Add interactions only when they help the user understand, decide, or export.
7. Run a self-review against `interface-quality.md`.
8. Deliver the saved path (named `<slug>-YYYY-MM-DD.html`, see 文件名带日期 below) or artifact, plus a concise note on what it contains and any deliberate chart-library deviations.

Bad-looking HTML is worse than good markdown. If the result looks like a generic template, restart the visual direction before shipping.

## 本地补充说明

基于 hi-zhenyu 的 [show-me-html](https://github.com/hi-zhenyu/show-me-html)（MIT）。上面的流程和规则保持原版不变，下面只是在其上追加的约定。

- **默认视觉底板。** 以 `assets/skeleton.html` 为底，使用它的 CSS、亮/暗/跟随系统三态主题脚本和自动目录脚本。只替换 `<main id="doc">` 里的内容、`<title>` 和 `.chrome-title`。页面结构仍按 artifact brief 和内容来定，不套固定模板。只有用户要求别的风格时才不带底板。
- **先查组件清单再写 CSS。** 看板、横条、堆叠条、因果图、时间线、来源行等底板都有现成的类，清单见 `references/components.md`。页面自己的 `<style>` 只写清单里拼不出来的部分，颜色用 `data-tone`。
- **不要覆盖底板的版心和配色。** 页面自己的 `<style>` 只写内容组件（卡片、流程、列表等）的样式，不要改 `html`、`body`、`.layout`、`main#doc`、`.page-chrome`、`.chrome-inner` 的背景、边框和左右内边距（例如 `background:transparent`、`padding-inline:0`）；亮色背景和页边距由底板的 `--paper` 与 `--gutter` 决定，页面不另做"嵌入模式"。
- **别破坏折叠块的内边距。** 底板的 `<details>` 是带背景和边框的卡片，内边距靠 `summary` 的 padding 和子元素的 `margin-inline` 实现。页面里不要给 `summary` 写 `padding:..0`，也不要用 `margin:12px 0` 这类简写去改折叠块里的元素（会清掉左右空白），改上下间距请写 `margin-block`。
- **对齐正文左缘。** 标题、来源行、表格和卡片（.fig-box / .card / details）的左右边缘都要和正文栏对齐，不另加 `margin-inline`；`figure`、`blockquote`、`ul` 这类有浏览器默认缩进的元素交给底板重置，页面里不再写左右外边距。
- **卡片不套框，长证据统一收起。** 并排卡片（`.ev-grid`）只放标题、可信度标签和结论，卡片里不写“依据”行；不要在卡片里再放折叠块或带边框的子框（不要卡片套卡片）。完整证据、边界和来源统一放在卡片组下方一个默认收起的“证据与边界”折叠块里，该区块不重复卡片已写的内容，每张卡都要有对应条目；不做悬停显示（触屏、键盘和打印都看不到）。
- **文件名带日期。** 输出文件命名为 `<描述性短名>-YYYY-MM-DD.html`。短名用小写英文加连字符，概括主题，例如 `profilingmanager-anr-eval-2026-11-04.html`。日期取生成当天的本地日期；报告覆盖一段时间也用生成日期，不用区间。同一天重名时加 `-2`、`-3` 等后缀，不覆盖已有文件。
- **收尾自检。** 交付前运行 `python3 scripts/shoot.py <page>.html --matrix`（脚本在本 skill 目录下）。它截亮色、暗色、390px 手机、打印四张 2× 图，并列出溢出：`spill`（内容超出容器）、`clipped`（被裁掉）、`offpage`（超出视口）、`svg-shrunk`（SVG 在手机上缩到 60% 以下，字读不清）、`nested`（卡片里放了折叠块）。报告为 none 才算过；`svg-shrunk` 用 `.fig-scroll` 包住或另画窄版。再看手机图：正文左右都有边距，折叠块展开后文字不贴边，亮色背景是底板的暖灰纸色。
- **截图配图。** 要把图放进文档时，用 `scripts/shoot.py <page>.html --select '#board' '#ranking figure'` 按元素截图，加 `--theme dark` 或 `--width 390` 换主题和宽度。输出目录默认是 `$TMPDIR/show-me-html-shots/<页面名>/`，可用 `--out` 改。脚本自动查找 Chrome，找不到时设置 `CHROME=/path/to/chrome`。
- **自包含。** 字体由底板从 Google Fonts 异步加载，取不到时回退到系统字体栈（`--font-serif`、`--font-sans`、`--font-mono`），离线也能正常阅读；除此之外不引用其他 CDN、外部脚本或图片。图表可以用内联 SVG/CSS，并按第 13 条在最终说明里写明理由。
- **第 13 条的例外：截图进文档或要离线时用 CSS/SVG。** 页面要截成图片放进飞书等文档，或用户要求离线可用时，横条、堆叠条、因果图优先用底板的 `.smh-bars`、`.smh-stack`、`.f-*`，不引入 ECharts。原因是 ECharts 要从 CDN 加载，离线时画不出来；它的动画和悬停交互在截图里也看不到。在最终说明里写一句理由，例如「要截图放进飞书，用 CSS 条形图」。数据点多、需要缩放或要悬停看数值的图，仍然用 ECharts。
- **不编造数据。** 缺失的值写 `[DATA NEEDED: ...]`。自己算出的数字要标注算法，并说明原文没有这个数。
- **每组数字注明来源。** 每张表、每个案例、每组关键数字后面都要跟一行小字（`.src`），写数据来源、时间范围和查询日期；不知道的写 `[DATA NEEDED: 来源与时间范围]`。
- **细节默认收起。** 结论、关键数字和行动项保持可见；原因链、证据明细、日志和原始数据放进 `<details>`，默认收起。
- **长表随时能收起。** 展开后明显超过一屏的明细使用 `<details data-long-details>`，用法见 `references/components.md`「长折叠块」。底板提供吸顶标题和表尾收起按钮，收起后焦点与视口返回标题；不按固定行数自动改造短块，也不新增内部纵向滚动。交付前按 `references/interface-quality.md` 验证中部／底部收起、键盘、手机、导出和打印状态恢复。
- **脱敏。** 去掉内部主机名、绝对路径、人名、令牌和内网链接，除非用户要求保留。
- **可排序表格。** 底板自带原生可排序表格脚本（无外部依赖）：给 `<table>` 加 `class="sortable"` 即可点击表头升/降序，数字（含逗号、%、×、“约”等）按数值排序，中文按 localeCompare。
