# Data-processing reproduction

## Scope and environment

This is a data-only handoff. It reproduces snapshot-to-CSV serialization and aggregation, not experiments or plotting. Prepared and locally verified by Codex on 2026-11-04, Windows, CPython 3.12.14; Python standard library only. No pip installation, fonts, plotting backend, GPU, or network is needed after obtaining the files. Python >=3.9 is targeted, but only 3.12.14 has been tested here.

Input: `docs/source_snapshot.json` plus `config/aggregation.json` and `config/data_schema.json`. Individual source CSV hashes are in `data/sources.csv`; all input/code/output hashes and the UTC verification time are in `docs/validation.json`. Those hashes identify the prepared version without inventing a self-referential commit SHA. The Git commit containing this file identifies the delivered version.

## Commands (working directory: repository root)

```bash
python figures/fig_001_interaction_efficiency/code/prepare_data.py
python figures/fig_001_interaction_efficiency/code/prepare_data.py --check
```

The first command reconstructs raw CSV from the manual snapshot, calculates all derived tables, writes the dictionary/source inventory, and validates them. The second validates the existing bundle without modifying files. Running the first command again should preserve every CSV byte; only the JSON validation timestamp changes. Paths are resolved from the script, so another working directory also works.

## Checks and expected results

| Check | Expected |
| --- | --- |
| Raw schema/call rows | 12; unique source/dataset/model |
| Raw tool-view rows | 12; unique source/dataset/model |
| Raw EgoLink cost rows | 15; five backbones x three modes |
| Panel a/b/c/d rows | 8 / 8 / 3 / 8 |
| Backbones per aggregate | 3 distinct primary backbones |
| Normalized per-model costs | 15, with six compact-backbone rows excluded from c |
| Source percentage sign conflicts | 3, all TravelGym-v2 |
| Images / image manifest data rows | 0 / 0, intentionally deferred |
| CSV format | UTF-8, LF, no fabricated missing-value zeroes |
| Dictionary | Exact coverage of every field in each data CSV, sources CSV, and empty image manifest |

The validator also checks types, primary keys, source/dictionary coverage, source hashes, non-negative costs/calls, panel group sizes, and all processed cells against a fresh calculation from the raw CSVs. Means use 28-digit Decimal arithmetic without display rounding.

## Verification status

Local preparation and validation were executed for this handoff; see `validation.json` for the actual environment, time, counts and hashes. Verification of the deliverable is not an independent author rerun. Upstream logs/task matching, figure generation, preview rendering, and independent clean-clone reproduction remain unperformed. Status must remain `data-ready` until that work is completed and documented.
