# Artifact Patterns

Use this reference to choose a structure that matches the content. HTML earns its keep when position, contrast, hierarchy, or interaction carries meaning.

## Comparison

Use for options, vendors, designs, approaches, architecture choices, tradeoffs, or recommendations.

- Layout: one column per option for 2-3 options; responsive grid for 4+ options.
- Normalize sections across options: framing, core idea, example, strengths, risks, cost, fit, verdict.
- Put hard metrics in the same row across options so scanning is fair.
- End with a recommendation or decision matrix; do not leave the reader to infer it.
- Avoid stacked prose sections that force the reader to hold every option in memory.

## Exploration and planning

Use for implementation plans, strategy options, project sequencing, technical approaches, or roadmap work.

- Start with the destination: goal, constraints, success criteria, and non-goals.
- Show phases as a timeline or lanes, not as a wall of bullets.
- Include a data-flow or system-flow diagram when more than two components interact.
- Separate decisions already made from open questions.
- Add acceptance checks near the relevant phase, not only at the end.

## Code review and PR writeup

Use when diffs, modules, ownership, risk, or reviewer focus matters.

- Treat the diff or module map as the spine of the page.
- Put annotations in the margin or side panel so code remains readable.
- Group findings by severity and affected area.
- Include "where to focus review" and "what changed" as short framing blocks.
- For module maps, show boundaries, dependencies, and hotspots visually.
- Avoid repeating entire files with prose between every chunk.

## Reports, research, and explainers

Use for status reports, incident reports, concept explainers, feature deep-dives, or learning material.

- Start with the answer: summary, status, or core insight.
- Use sidebars for glossary, assumptions, data sources, and related links.
- Use timelines for incidents and progress reports.
- Use live demos, sliders, or small simulations when behavior matters.
- Separate "what happened", "why it matters", and "what changes next".
- Avoid decorative charts; every visual must answer a question.

### Incident and investigation reports

Reuse the skeleton's classes (`.eyebrow`, `.lede`, `.metric-band`, `.stat-num`, `.src`, `.card`, `.badge`, `progress`); page CSS only styles content components and never touches `html`, `body`, `.layout`, `main#doc`, or `.page-chrome`.

1. **结论先行的首屏。** 顺序固定：小标题（领域 · 日期范围）→ 一句话结论作 `h1`（写结论，不写"××调研"）→ 导语段（影响、状态、下一步）→ 4 个关键数字。

```html
<section>
  <p class="eyebrow">[领域] · [起止日期，注明时区]</p>
  <h1>[一句话结论：问题集中在 X，主因是 Y]</h1>
  <p class="lede">[影响谁、多大范围]。状态：<strong>[已缓解]</strong>，下一步：[谁做什么]。</p>
  <div class="metric-band" aria-label="关键数字">
    <div><p>[指标]</p><p class="stat-num">2.4<small>%</small></p><p>[说明]</p></div>
    <div><p>[指标]</p><p class="stat-num">1,234<small>次</small></p><p>[说明]</p></div>
    <div><p>[指标]</p><p class="stat-num">−30<small>%*</small></p><p>[说明]</p></div>
    <div><p>[指标]</p><p class="stat-num">3<small>/5</small></p><p>[说明]</p></div>
  </div>
  <p class="src">来源：[系统/报表名]；范围：[时间范围]；查询于 [日期 时区]。*衍生数字：由 A÷B 计算，原文未给出。</p>
</section>
```

2. **数据来源行。** 每张表、每个案例、每组数字后面紧跟一行 `.src` 小字：数据来源、时间范围、查询日期。不知道的写 `[DATA NEEDED: 来源与时间范围]`，不要省略整行。

3. **根因/证据卡带可信度标签。** 卡片 = 图标 + 标题与一句说明 + 右侧标签。平行的根因卡全部展开；长证据（日志、查询、样本）放进卡内默认收起的 `<details>`。标签只用这一组固定词：

| 标签 | 含义 | badge |
| --- | --- | --- |
| 已实测 | 复现过或有对照实验 | `data-tone="cactus"` |
| 日志佐证 | 线上日志/指标直接支持，未复现 | `data-tone="sky"` |
| 推断 | 由间接证据推出，未直接观察到 | `data-tone="manilla"` |
| 待验证 | 假设，需要补数据或实验 | `data-variant="outline"` |

```html
<article class="card">
  <header style="display:flex;gap:.75rem;align-items:flex-start">
    <span aria-hidden="true">⏱</span>
    <div><h3>[根因标题]</h3><p>[一句话说明机制和影响面]</p></div>
    <span class="card-action"><span class="badge" data-tone="cactus">已实测</span></span>
  </header>
  <details>
    <summary>证据</summary>
    <p>[关键日志、复现步骤、对照数据]</p>
    <p class="src">来源：[系统]；范围：[时间范围]；查询于 [日期]。</p>
  </details>
</article>
```

图标用一个字符或一个复用的 `<symbol>`，不要每张卡内嵌整段 SVG。

4. **表格里的条形图。** 比率列旁边加一列 `<progress>`，给它固定列宽，数字列保持右对齐、可排序。

```html
<table class="table sortable">
  <thead><tr><th>[分组]</th><th>失败率</th><th style="width:30%">分布</th></tr></thead>
  <tbody>
    <tr><td>[A]</td><td>12.5%</td><td><progress max="100" value="12.5">12.5%</progress></td></tr>
    <tr><td>[B]</td><td>3.1%</td><td><progress max="100" value="3.1">3.1%</progress></td></tr>
  </tbody>
</table>
<p class="src">来源：[系统]；范围：[时间范围]；查询于 [日期]。</p>
```

`max` 取本表最大值或 100，在 `.src` 里写明用的是哪个。

5. **可勾选的改进清单。** 按责任面分组（如客户端 / 服务端），每项一个复选框，写清标准、负责人和期限；没定的写 `[DATA NEEDED: 责任方与期限]`。清单保持展开。

```html
<h2>改进项</h2>
<h3>客户端</h3>
<div class="field"><label><input type="checkbox" /> [可度量的改动：指标 / 阈值] —— [负责人]，[期限]</label></div>
<div class="field"><label><input type="checkbox" /> [第二条] —— [DATA NEEDED: 责任方与期限]</label></div>
<h3>服务端</h3>
<div class="field"><label><input type="checkbox" /> [改动] —— [DATA NEEDED: 责任方与期限]</label></div>
```

## Document transformation

Use when the user provides a document and asks for HTML. Treat the document as source material, not as a layout template.

- Preserve the content contract: facts, evidence, formulas, terminology, caveats, and user-requested emphasis.
- Change the presentation contract when it helps: reorder around reader questions, decisions, evidence, or workflows.
- Start with the artifact's job, not the document's first heading.
- Pull out latent structure: comparisons, timelines, taxonomies, processes, actors, inputs/outputs, assumptions, risks, and open questions.
- Convert dense prose into diagrams, side notes, matrices, callouts, cards, filters, or navigation only when the structure becomes clearer.
- Keep original-order navigation or an appendix when traceability matters.

Common transformations:

- Paper or technical report: answer-first summary, method map, architecture diagram, evidence panels, key formulas, limitations, and "why it matters".
- Strategy or proposal: decision framing, option comparison, tradeoff lanes, milestones, owner/risk map, and go/no-go checks.
- Tutorial or guide: stepper, prerequisites, runnable examples, expected output, pitfalls, and troubleshooting.
- PRD or spec: user goals, flows, state map, requirement matrix, edge cases, and acceptance checks.
- Data analysis: key finding dashboard, chart grid, source table, methodology notes, and uncertainty/caveats.
- Long essay or memo: narrative spine, thesis map, glossary, side notes, counterarguments, and action takeaways.

Avoid a styled transcript where each source heading becomes the same heading plus a card. That is markdown with decoration, not an HTML artifact.

## Diagrams and illustrations

Use when structure is clearer as a drawing.

- Prefer inline SVG for flowcharts, architecture, state machines, process maps, and technical illustrations.
- Keep text selectable and meaningful; use `<title>` and `<desc>` for SVGs.
- Draw the main path boldly and secondary/error paths quietly.
- If there are many details, make the diagram navigational and show detail in a panel.
- Avoid diagrams with so many nodes that layout stops communicating.

## Design systems and prototypes

Use when the request is about UI, tokens, components, motion, or interaction feel.

- Render actual component states, not screenshots or descriptions.
- Show variants in a contact sheet: size, intent, state, density, theme.
- For motion, expose timing/easing controls and show the resulting CSS/JS value.
- For flows, make only the decision points high fidelity; keep supporting screens lightweight.
- Include copy buttons when the artifact generates tokens, config, CSS, or specs.

## Decks and presentations

Use when the artifact will be walked through live.

- Build each slide as a full viewport section with arrow-key navigation.
- Keep one idea per slide.
- Vary slide types: thesis, chart, quote, diagram, before/after, decision, appendix.
- Show progress and current slide number.
- Support fullscreen and readable speaker-mode notes only if useful.
- Avoid making every slide the same card with different text.

## Pattern check

Before shipping, ask:

- Does the layout reveal the structure faster than markdown?
- Is the primary action or conclusion visually obvious?
- Would a reader know where to look first, second, and third?
- Is any interactivity essential, or is it just decoration?
- Can the artifact survive narrow screens and long content?
