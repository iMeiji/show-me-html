# 底板组件清单

`assets/skeleton.html` 已经带的类。写页面自己的 `<style>` 之前先在这里找；能拼出来就不另起类名。颜色一律走 `data-tone`（clay / fig / sky / cactus / olive / heather / kraft / manilla），它给元素提供 `--tone`、`--tone-surface`（淡底）和 `--tone-ink`（可读文字色）三个变量。

片段只写骨架，内容按 `patterns.md` 的规则填。

## 首屏与文字

| 类 | 用途 | 最小片段 |
| --- | --- | --- |
| `.eyebrow` | h1 上方的范围/日期小标签，mono 大写 | `<p class="eyebrow">领域 · 日期</p>` |
| `.lede` | h1 下的导语段 | `<p class="lede">影响、状态、下一步</p>` |
| `.metric-band` + `.stat-num` | 首屏 2–4 个关键数字 | `<div class="metric-band"><div><p>指标</p><p class="stat-num">2.4<small>%</small></p><p>说明</p></div></div>` |
| `.src` | 表格、图、数字组下面的来源行 | `<p class="src">来源：…；范围：…；查询于 …</p>` |
| `.hl` | 标题里唯一的答案词反色高亮 | `<h2>主因是<span class="hl">缓存</span></h2>` |
| `.smh-k` | 卡片顶部的 mono 编号/类别行，带 `--tone-ink` 时随列着色 | `<p class="smh-k">01 · 类别</p>` |

## 卡片与分组

| 类 | 用途 | 最小片段 |
| --- | --- | --- |
| `.card` | 卡片，可选 `header` / `section` / `footer`；`data-size="sm"` 收紧内边距；`data-tone` 换淡底 | `<article class="card"><header><h3>标题</h3></header><section><p>…</p></section></article>` |
| `.card[data-variant="ink"]` | 反色暗卡，一页最多一块，放决定性结论 | `<div class="card" data-variant="ink">…</div>` |
| `.ev-grid` | 并排结论卡 + 可信度标签，`data-cols="2|3"` | 见 `patterns.md` 第 3 条 |
| `.ev-legend` / `details.ev-more` | 卡片组下的标签说明行 / 收起的证据块 | 同上 |
| `.smh-grid` | 两列卡片，720px 以下单列 | `<div class="smh-grid"><article class="card">…</article>…</div>` |
| `.smh-board` > `.lane` | 状态看板：每列一种状态，列底色取 `data-tone`，列内放小卡；任何配方都能用，列数用 `--lanes` 改（默认 4），900px 两列、520px 单列，打印两列 | `<div class="smh-board"><div class="lane" data-tone="cactus"><h3><span class="badge" data-tone="cactus">已修复</span></h3><article class="card" data-size="sm"><h4>项名</h4><p class="smh-k"><code>id</code> · 次数</p><p>一句状态</p></article></div></div>` |
| `.item-group` > `.item` | 时间线/列表行：`figure`（时间）+ `section`（标题、说明）+ `aside`（徽章） | `<div class="item-group"><div class="item"><figure><time>11-09</time></figure><section><h4>事项</h4><p>…</p></section><aside><span class="badge">完成</span></aside></div></div>` |
| `.alert` | 状态条/提示框：svg 图标 + `h4` + `section`；`data-variant="destructive"` 红色 | `<div class="alert"><svg…/><h4>当前状态</h4><section><p>…</p></section></div>` |
| `.with-rail` + `.method-rail` | 主栏 + sticky 口径侧栏（样本、定义、来源） | `<div class="with-rail"><div>主栏</div><aside class="method-rail">口径</aside></div>` |
| `details` / `.accordion` | 默认收起的细节；多个连排包 `.accordion` | `<details><summary>证据明细</summary><p>…</p></details>` |
| `.tabs` | 标签页：`[role=tablist]` + `[role=tab]` + `[role=tabpanel]` | 结构按 WAI-ARIA tabs 写 |

`.board` / `.lane` 原本只在 `body[data-recipe="triage-board"]` 下有布局（横向滚动、顶部色线），`.smh-board` 是不依赖配方的版本。配方前缀的类（`.comparison-grid`、`.milestone-spine`、`.incident-timeline`、`.request-path` 等）只在对应 `data-recipe` 下生效，换配方前先确认。

## 标签与表单

| 类 | 用途 | 最小片段 |
| --- | --- | --- |
| `.badge` | 状态标签；`data-tone`、`data-variant="secondary|outline|destructive"` | `<span class="badge" data-tone="sky">处理中</span>` |
| `.btn` | 按钮；`data-variant="secondary|outline|ghost|link|destructive"`，`data-size="sm|lg|icon|icon-sm"` | `<button class="btn" data-variant="outline">导出</button>` |
| `.field` | 复选/表单行，改进清单用。`label` 里第一个子元素是复选框时，自动画成圆角勾选框，和第一行文字对齐，折行悬挂缩进，勾选后文字变灰；`role="switch"` 的开关不受影响 | `<div class="field"><label><input type="checkbox" /> 标准 —— 负责人</label></div>` |
| `.input` / `.label` / `.input-group` | 输入框与标签 | `<label class="label">名称<input class="input" /></label>` |
| `.kbd` | 键位 | `<kbd class="kbd">⌘K</kbd>` |

## 表格

| 类 | 用途 | 最小片段 |
| --- | --- | --- |
| `.table-container` > `table.table` | 明细表；容器负责横向滚动，宽表必须包 | `<div class="table-container"><table class="table">…</table></div>` |
| `table.sortable` | 点表头排序，数字按数值 | `<table class="table sortable">` |
| `progress` | 表格里的比率条，原生元素，打印保留底色 | `<td><progress max="100" value="12.5">12.5%</progress></td>` |

表格里的长标识符只在 `<wbr>` 处断行：在 `_`、`/` 后插 `<wbr>`。

## 图

| 类 | 用途 | 最小片段 |
| --- | --- | --- |
| `figure.fig-box` | 图的卡面 | `<figure class="fig-box">…<p class="src">来源</p></figure>` |
| `.fig-head` > `.fig-title` + `.fig-sub` | 图标题（写结论）+ 右侧单位/口径 | `<div class="fig-head"><span class="fig-title">结论</span><span class="fig-sub">单位 · 窗口</span></div>` |
| `.smh-bars` > `.b` | CSS 横条：`--w` = 值 ÷ 最大值；`.hot` 强调色只给一条、`.mine` 深墨；`data-tone` 按状态着色（压过 `.hot` / `.mine`） | `<div class="smh-bars" role="img" aria-label="…"><div class="b" data-tone="clay"><span>类别</span><i style="--w:100%"></i><b>4,206</b></div></div>` |
| `.smh-tracks` > `.b` | 共享刻度的分段进度条（如分端处理进度）：标签 + 轨道 + 右侧读数；段宽 `--w` = 段数量 ÷ 所有行最大总量，轨道底色即满刻度，各行长度可直接比较；段色 `data-tone`，不写 tone 为中性灰；零值段不输出；配 `.smh-legend` | `<div class="smh-tracks"><div class="b"><span>iOS</span><div class="t" role="img" aria-label="iOS：关闭 21，已解决 1，共 22"><i data-tone="cactus" style="--w:91.3%"></i><i data-tone="sky" style="--w:4.35%"></i></div><b>21/22 关闭</b></div></div><p class="smh-legend"><span data-tone="cactus">已关闭</span><span data-tone="sky">已解决</span></p>` |
| `.smh-stack` + `.smh-legend` | 堆叠条：段宽 `--w`、段色 `data-tone`；段内只写数字，段窄于 5rem 自动不显示数字，名称和占比写在图例 | `<div class="smh-stack" role="img" aria-label="A 62%，B 25%"><i data-tone="clay" style="--w:62.7%"><b>5400</b></i><i data-tone="cactus" style="--w:24.8%"><b>2133</b></i></div><p class="smh-legend"><span data-tone="clay">原生 62.7%</span><span data-tone="cactus">待发版 24.8%</span></p>` |
| `svg.smh-flow` + `.f-*` | SVG 流程/因果图。节点 `.f-node`（`.f-done` 已完成、`.f-hero` 当前重点、`.f-par` 虚线、`data-tone` 换描边）；文字 `.f-t` 标题、`.f-s` 说明（默认居中，加 `.f-start` 左对齐，`.f-em` 正文色加粗）；连线 `.f-line` + `.f-arrow` 箭头 | 见 `skeleton.html` `#charts`；多因一果见 `patterns.md`「Diagrams」 |
| `svg.smh-trend` + `.t-*` | SVG 折线：`.t-axis` 轴、`.t-ev` 主线、`.t-us` 虚线对照、`.t-dot` 点、`.t-v` 数值、`.t-u` 单位、`.t-x` 横轴标签 | 同上，按需自画 |
| `.fig-scroll` | 宽 SVG 的横向滚动容器：SVG 保持最小宽度（默认 38rem，用 `--min` 改），手机上横滑而不是缩到读不了；打印时取消 | `<div class="fig-scroll" tabindex="0" role="region" aria-label="可横向滚动的图"><svg class="smh-flow" viewBox="0 0 760 330">…</svg></div>` |
| `.diagram-wide` / `.diagram-narrow` | 宽窄两版图，640px 以下只显示窄版；横图在手机上必须竖排才读得懂时用，否则用 `.fig-scroll` | `<svg class="diagram-wide">…</svg><svg class="diagram-narrow">…</svg>` |

## 版式约定（不用写类）

- `.card`、`.lane` 里的长英文标识符会自动断行（`overflow-wrap:anywhere`），不撑破卡片；表格例外，见上。
- 网格子项写 `minmax(0, 1fr)`，不写裸 `1fr`，否则长内容会撑宽整列。
