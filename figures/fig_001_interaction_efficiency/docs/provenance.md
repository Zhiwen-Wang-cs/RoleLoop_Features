# Provenance and accounting scope

## Input and extraction boundary

The source consists of three aggregate tables supplied by the manuscript author in this conversation. Original experiment files, logs, task IDs, run IDs, seeds, code revisions, task counts, and hardware records were not supplied. `source_snapshot.json` is a structured **manual transcription** of those tables. It is not an original experiment export and cannot establish raw-log reproducibility.

`code/prepare_data.py` deterministically serializes that snapshot into raw CSV, applies the explicit alias/mean configuration, and writes plotting inputs plus an arithmetic audit. This reproduces processing of the supplied aggregates; it does not reproduce the upstream experiments or reconstruct tool schemas from code. `data/sources.csv` uses repository-relative snapshot locators, supplies CSV checksums, and leaves unavailable upstream experiment IDs/revisions/hashes empty. The snapshot checksum is recorded separately in its source notes and validation report; it is not misrepresented as an experiment-log hash.

## Three distinct accounting layers

1. **Table 1 / panels a,b**: tool-description tokens were reconstructed by the author using interaction trajectories and current code, with a proxy tokenizer for GPT. ReAct is one request; RoleLoop is one P+E pair. Call counts are the supplied average logged calls/task, with RoleLoop counting Planner and Executor only. Counts cannot be assumed to mean actual business-tool executions rather than model requests. Do not divide a P+E pair by two, or multiply the P+E pair token count by combined P/E calls, without separate role frequencies.
2. **Table 2 / panel d**: fixed-trace reconstruction of tool-description overhead. The no-view condition was not rerun. Per-task columns retain the author's original scope **including Reporter**. The complete-library schema is not the ReAct-native schema from table 1. The P+E description sum and the cumulative per-task estimate have different units and weightings.
3. **Table 3 / panel c**: reported EgoLink2026 tokens/task and seconds/task. Token components, failed/incomplete-task denominator, matched task sets, auxiliary calls, timing boundaries, concurrency, and hardware need author confirmation. Muse's source row says `SAGE`; raw CSV retains that alias and processed data uses RoleLoop. No successful-task-only filtering is added. The GPT proxy-tokenizer note establishes only the schema-estimate tokenizer, not the tokenizer for this table.

## Aggregation and display

Panels a,b,d average three backbone-level aggregate values within each dataset/condition; c averages the same three backbones on EgoLink2026. Mean = sum(values)/3, unweighted. This is not a pooled-task mean, repeated-seed mean, or mean over three tasks. Task counts and standard errors remain unknown. Decimal arithmetic uses 28 significant digits and does not round before plotting. Percentage summaries, if used later, must state whether they use a ratio of means or a mean of ratios.

Use all supplied datasets in a,b,d. Keep EgoBench distinct from EgoLink2026; do not join their records merely because their names are related. `EcomBench` is spelling-normalized to ECom-Bench; other labels follow config. Original numerical precision is retained, but expanded k-based totals should not be interpreted as having new single-token measurement precision.

## Known issues — retain, do not silently repair

- All three TravelGym-v2 source saving percentages (-22/-27/-31) conflict in sign with the positive differences of supplied per-task token columns. Raw values are retained. The audit provides recalculations separately. Panel d may show the supplied absolute columns with a caption flag; it must not silently use a corrected percentage as confirmed evidence.
- Four supplied cumulative savings differ from subtraction by 100 tokens (EgoBench/Muse, EcomBench/Qwen, COMPASS/Muse, COMPASS/Qwen). These reflect the supplied rounding convention and are exposed in the audit.
- EgoBench P+E schema estimates differ slightly between source tables: Muse 2079 vs 2078; Qwen 2062 vs 2066. Each table retains its own values and scope; they are not averaged together.
- TravelGym's native ReAct tool descriptions are short, while RoleLoop adds protocol/specialized interfaces. Its P+E sum is therefore larger; panel a cannot claim lower descriptions on all four datasets.
- More calls alone do not establish better task success. Report framework success using its actual benchmark results, not inferred from these counts.
- The two compact backbones have higher RoleLoop tokens/task than ReAct. All five backbones and times remain available, so the selected three-backbone mean cannot support a universal efficiency claim. RoleLoop's reported time/task exceeds ReAct for every supplied backbone; token savings are not speed, dollar, or FLOP savings.
- These are inference-framework data. They do not validate RoleLoop-PO training sample efficiency or controlled success-vs-token-budget curves. Task matching to the manuscript's success table has not been established.
