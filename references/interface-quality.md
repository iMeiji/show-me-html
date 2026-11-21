# Interface Quality Checklist

Use this reference before shipping any HTML artifact with interaction, controls, navigation, animation, dense layout, images, generated content, or public-facing polish.

## Accessibility

- Use semantic HTML before ARIA: `main`, `nav`, `section`, `article`, `table`, `button`, `a`, `label`.
- Icon-only buttons need `aria-label`; decorative icons need `aria-hidden="true"`.
- Form controls need visible labels or `aria-label`.
- Use `button` for actions and `a` with `href` for navigation.
- Interactive custom elements need keyboard support, but prefer native controls.
- Images need meaningful `alt`; decorative images use `alt=""`.
- Async updates such as copied state, validation, or save status need `aria-live="polite"`.
- Headings must be hierarchical. Include a skip link when there is repeated navigation.
- Heading anchors need `scroll-margin-top`.

## Focus and input

- Every interactive element needs a visible `:focus-visible` style.
- Never remove outlines without an equal or better replacement.
- Use `:focus-within` for compound controls.
- Keep tab order logical and avoid hidden focus traps.
- Touch targets should be large enough for coarse pointers.
- Use `touch-action: manipulation` for button-heavy interfaces.
- Avoid `autoFocus` unless there is one obvious primary desktop input.

## Forms and editable state

- Inputs need meaningful `name`, `type`, and `autocomplete`.
- Use `inputmode` for numeric, email, URL, search, and telephone fields when helpful.
- Do not block paste.
- Labels should be clickable and share the hit target with checkbox/radio controls.
- Keep submit buttons enabled until the request actually starts; then show progress.
- Put errors inline next to the relevant field and focus the first error on submit.
- Warn before navigation when unsaved work could be lost.

## Animation

- Honor `prefers-reduced-motion` with reduced or disabled animations.
- Prefer transform and opacity for animation.
- Never use `transition: all`; list changed properties explicitly.
- Set correct `transform-origin`.
- SVG transforms should happen on grouped wrappers when possible.
- Animations must be interruptible and respond to user input mid-transition.

## Typography and copy

- Use the ellipsis character via `&hellip;` in HTML text, not three periods.
- Use non-breaking spaces for compact units and commands, such as `10&nbsp;MB` or `Cmd&nbsp;K`.
- Use `font-variant-numeric: tabular-nums` for number columns.
- Use `text-wrap: balance` or `text-wrap: pretty` on headings where supported.
- Button labels should be specific: "Copy JSON", "Reset Filters", "Save API Key".
- Error messages should include the next step, not only the problem.
- Prefer active voice and second person in UI copy.

## Content handling

- Long user-provided strings must wrap, truncate, clamp, or scroll intentionally.
- Flex and grid children that contain text often need `min-width: 0`.
- Empty arrays, missing fields, and empty strings need designed states.
- Test short, average, and very long content.
- Avoid horizontal page scroll unless the artifact is intentionally a wide canvas.
- Use stable dimensions for boards, charts, cards, controls, and slide frames.

## Images and media

- Images need explicit `width` and `height` or a stable CSS aspect ratio.
- Below-fold images should be lazy loaded.
- Critical above-fold images should be prioritized only when they matter.
- Do not use vague stock-like images when the user needs to inspect a real object, product, place, state, or person.
- Generated or decorative images must not obscure text or controls.

## Performance

- Large lists over roughly 50 items need virtualization, pagination, filtering, or `content-visibility: auto`.
- Avoid layout reads in render loops: `getBoundingClientRect`, `offsetHeight`, `offsetWidth`, and `scrollTop`.
- Batch DOM reads and writes.
- Keep per-keystroke controlled input work cheap.
- Use CSS and native browser behavior before heavy JavaScript.
- Avoid unnecessary external fonts, libraries, and assets in self-contained artifacts.

## Navigation and state

- Stateful tabs, filters, pagination, and expanded panels should be deep-linkable when sharing matters.
- Links must support normal browser behavior such as open-in-new-tab.
- Destructive actions need confirmation or an undo window.
- Modals, drawers, and sheets need focus management and `overscroll-behavior: contain`.
- During drag, disable text selection and keep the dragged state clear.

## Theme, locale, and safety

- If supporting dark mode, set `color-scheme` and make native controls readable.
- Set the page background and theme color consistently.
- Use `Intl.DateTimeFormat` and `Intl.NumberFormat` for dates, numbers, and currency in JavaScript.
- Wrap brand names, code tokens, and identifiers with `translate="no"` when auto-translation could corrupt them.
- Do not disable pinch zoom with `user-scalable=no` or `maximum-scale=1`.

## Long collapsible blocks

For `details[data-long-details]`:

- At desktop and 390px widths, open a long block and scroll into its middle: the summary stays below the page toolbar and remains clickable.
- Close using both the summary and the footer button. Focus returns to the summary, its title is visible, and other blocks keep their state.
- Test Enter and Space on the summary, visible keyboard focus, and a footer touch target of at least 44px. With JavaScript disabled, the native summary still works.
- Check that narrow tables scroll horizontally inside their container without adding a second vertical scroll area. Short, unmarked details must remain unchanged.
- Export Markdown while the block is collapsed: all data remains present and the close button text is absent.
- Print: long blocks expand, summaries stop sticking, buttons disappear, and the previous open/closed states return after printing.

## Delivery QA

- Check at least one desktop and one narrow mobile viewport.
- Smoke-test every tab, filter, copy button, export button, reset action, and destructive confirmation.
- Verify SVG, canvas, formula, and chart regions are not blank and have fallback text or adjacent summaries.
- Stress long labels, long numbers, empty data, missing fields, and narrow containers.
- Confirm reduced-motion mode still communicates state changes.
- If verification is incomplete, say exactly what was not checked.

## Final pass

Before delivery, verify:

- No missing labels, alt text, visible focus, or keyboard path.
- No `transition: all`, unbounded text overflow, or accidental horizontal scroll.
- No interaction without feedback.
- No editor without export.
- No layout that only works at the viewport used during creation.
