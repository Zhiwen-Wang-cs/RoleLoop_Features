# Plotting handoff: proposed 1 x 4 figure

The author will ask a collaborator to design the figure. **No new figure should be generated as part of this data handoff.** No previous rejected layout is an approved final design.

| Panel | Question and comparisons | Input | Display |
| --- | --- | --- | --- |
| a | Tool-description footprint, ReAct vs RoleLoop, all four datasets | `panel_a_tool_schema.csv` | tokens / 1000; distinct one-request vs P+E-pair units |
| b | Logged calls/task, ReAct vs RoleLoop, all four datasets | `panel_b_calls_per_task.csv` | calls/task; RoleLoop P/E only |
| c | Total recorded tokens/task, ReAct / Summary / RoleLoop | `panel_c_tokens_per_task.csv` | EgoLink2026 only; tokens / 1000 |
| d | Internal RoleLoop no-view vs with-view overhead, all four datasets | `panel_d_tool_views.csv` | estimated tool-description tokens/task / 1000; Reporter included |

All means use the three primary backbones named in config. The original per-model rows, two compact-backbone cost records, and time/task are preserved for alternatives and limitations. No per-task or repeated-run samples exist here, so error bars/CI must not be invented.

## Visual inputs, not a final layout

- Dataset order: EB=EgoBench, EC=ECom-Bench, TG=TravelGym-v2, CP=COMPASS. EL=EgoLink2026 for c.
- Palette from Figures 1–3: blue `#2F5597`, orange `#C55A11`, green `#548235`; corresponding fills in `config/plot_handoff.json`.
- Requested structure: four bar charts in one row. The collaborator may revise typography, spacing, legend placement, labels, and bar widths.
- Preserve zero baselines for bars and units; avoid giving P+E sums a per-call label, using call counts as success, or comparing panel d no-view directly to ReAct.
- Keep method labels concise; move model sets, roles, accounting, abbreviations, and reconstruction caveats to the caption.
- Use full precision for calculations; decide visible rounding in the plotting implementation.
- Deliver final vector PDF/SVG and a PNG preview, document dependencies and fonts, and fill `images/manifest.csv` only after actually generating outputs.

## Draft caption for the collaborator to adapt

**Interaction and token costs of RoleLoop.** Bars show unweighted means over Qwen3.8-27B, Muse-Glimmer-30B, and GPT-5.6-sol. EB, EC, TG, CP, and EL denote EgoBench, ECom-Bench, TravelGym-v2, COMPASS, and EgoLink2026. (a) Reconstructed tool-description tokens for one ReAct request versus one RoleLoop Planner–Executor pair; request units differ, and GPT uses a proxy tokenizer. (b) Logged calls per task, counting P/E only for RoleLoop. (c) Recorded EgoLink2026 tokens per task for the same three backbones. (d) Estimated tool-description overhead per task within RoleLoop, with and without tool views, including Reporter. The no-view condition is a fixed-trace reconstruction, not a rerun ablation. TravelGym source percentage signs conflict with the supplied absolute token columns; only the latter are displayed. Tool-description estimates in (a,d) differ from total recorded tokens in (c).
