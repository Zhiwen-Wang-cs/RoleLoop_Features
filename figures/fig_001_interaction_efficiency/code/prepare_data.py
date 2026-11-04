#!/usr/bin/env python3
"""Serialize the supplied aggregate snapshot, aggregate CSVs, and validate.

No plotting, network access, upstream experiment rerun, or external package.
Use --check to validate existing files without rewriting anything.
"""
import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, getcontext
import hashlib
import json
from pathlib import Path
import platform
import sys

FIG = Path(__file__).resolve().parents[1]
REPO = FIG.parents[1]
CONFIG = json.loads((FIG / "config/aggregation.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((FIG / "config/data_schema.json").read_text(encoding="utf-8"))
SNAPSHOT = FIG / "docs/source_snapshot.json"
RAW_TABLES = {
    "schema_calls.csv": "schema_calls",
    "tool_views.csv": "tool_views",
    "egolink_costs.csv": "recorded_costs",
}
getcontext().prec = CONFIG["decimal_precision"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def headers(relative):
    return [field["column_name"] for field in SCHEMA[relative]]


def read_csv(relative):
    with (FIG / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def text(value):
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, Decimal):
        return format(value, "f")
    return str(value)


def stringify(rows):
    return [{key: text(value) for key, value in row.items()} for row in rows]


def write_csv(relative, rows):
    path = FIG / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers(relative), lineterminator="\n")
        writer.writeheader()
        writer.writerows(stringify(rows))


def normalize(row):
    result = dict(row)
    result["dataset"] = CONFIG["dataset_aliases"][row["dataset"]]
    result["model"] = CONFIG["model_aliases"][row["model"]]
    return result


def mean(rows, field):
    names = [row["model"] for row in rows]
    assert len(names) == len(set(names)) == len(CONFIG["primary_models"])
    assert set(names) == set(CONFIG["primary_models"])
    return sum(Decimal(row[field]) for row in rows) / Decimal(len(rows))


def panel_row(panel, dataset, method, condition, metric, value, unit, scope, source):
    return {"panel": panel, "dataset": dataset,
            "dataset_abbr": CONFIG["dataset_abbreviations"][dataset],
            "method": method, "condition": condition, "metric": metric,
            "mean_value": value, "unit": unit,
            "n_models": len(CONFIG["primary_models"]), "scope": scope,
            "source_id": source}


def derive():
    schema_rows = [normalize(row) for row in read_csv("data/raw/schema_calls.csv")]
    view_rows = [normalize(row) for row in read_csv("data/raw/tool_views.csv")]
    costs = [normalize(row) for row in read_csv("data/raw/egolink_costs.csv")]
    outputs = {f"data/processed/{name}": [] for name in CONFIG["expected_panel_rows"]}
    for dataset in CONFIG["datasets"]:
        schema = [r for r in schema_rows if r["dataset"] == dataset]
        views = [r for r in view_rows if r["dataset"] == dataset]
        for method, schema_field, calls_field, unit_scope, call_scope in [
            ("ReAct", "react_tool_description_tokens_per_request", "react_calls_per_task",
             "reconstructed_schema_one_react_request", "supplied_react_logged_calls"),
            ("RoleLoop", "roleloop_tool_description_tokens_per_pe_pair", "roleloop_pe_calls_per_task",
             "reconstructed_schema_one_planner_executor_pair", "supplied_roleloop_planner_executor_only_logged_calls"),
        ]:
            outputs["data/processed/panel_a_tool_schema.csv"].append(panel_row(
                "a", dataset, method, "standard", "tool_description_tokens", mean(schema, schema_field),
                "tokens", unit_scope, "author_table_1"))
            outputs["data/processed/panel_b_calls_per_task.csv"].append(panel_row(
                "b", dataset, method, "standard", "logged_calls_per_task", mean(schema, calls_field),
                "calls/task", call_scope, "author_table_1"))
        for condition, field in [
            ("no_views", "no_view_estimated_tool_description_tokens_per_task"),
            ("with_views", "with_view_estimated_tool_description_tokens_per_task"),
        ]:
            outputs["data/processed/panel_d_tool_views.csv"].append(panel_row(
                "d", dataset, "RoleLoop", condition, "estimated_tool_description_tokens_per_task",
                mean(views, field), "tokens/task", "fixed_trace_estimate_including_reporter", "author_table_2"))
    all_costs = []
    for row in costs:
        method = CONFIG["mode_aliases"][row["mode"]]
        all_costs.append({"source_id": row["source_id"], "dataset": row["dataset"],
                          "model": row["model"], "method": method, "source_mode": row["mode"],
                          "tokens_per_task": row["tokens_per_task"],
                          "time_seconds_per_task": row["time_seconds_per_task"],
                          "included_in_panel_c": row["model"] in CONFIG["primary_models"]})
    for method in ("ReAct", "Summary", "RoleLoop"):
        rows = [r for r in all_costs if r["method"] == method and r["included_in_panel_c"]]
        outputs["data/processed/panel_c_tokens_per_task.csv"].append(panel_row(
            "c", "EgoLink2026", method, "standard", "tokens_per_task", mean(rows, "tokens_per_task"),
            "tokens/task", "reported_total_tokens_composition_and_task_matching_unconfirmed", "author_table_3"))
    outputs["data/processed/recorded_costs_all_models.csv"] = all_costs
    audit = []
    for row in view_rows:
        no_view = Decimal(row["no_view_estimated_tool_description_tokens_per_task"])
        with_view = Decimal(row["with_view_estimated_tool_description_tokens_per_task"])
        saving = no_view - with_view
        reported_pct = Decimal(row["reported_saving_pct"])
        audit.append({"source_id": row["source_id"], "dataset": row["dataset"], "model": row["model"],
                      "reported_saving_pct": row["reported_saving_pct"],
                      "recomputed_saving_pct_from_tokens": Decimal(100) * saving / no_view,
                      "reported_saving_tokens_per_task": row["reported_saving_tokens_per_task"],
                      "recomputed_saving_tokens_per_task": saving,
                      "rounding_residual_tokens": saving - Decimal(row["reported_saving_tokens_per_task"]),
                      "percentage_sign_conflict": saving * reported_pct < 0})
    outputs["data/processed/tool_view_arithmetic_audit.csv"] = audit
    return outputs


def sources():
    rows = []
    for name, table in RAW_TABLES.items():
        relative = "data/raw/" + name
        snapshot_uri = "repo:figures/" + CONFIG["figure_id"] + "/docs/source_snapshot.json#tables/" + table
        rows.append({"source_id": "author_table_" + str(len(rows) + 1),
                     "file_path": (FIG / relative).relative_to(REPO).as_posix(),
                     "origin_uri": snapshot_uri,
                     "experiment_id": "", "run_id": "", "source_revision": "", "source_sha256": "",
                     "csv_sha256": sha(FIG / relative),
                     "extraction_command": "python figures/" + CONFIG["figure_id"] + "/code/prepare_data.py",
                     "notes": "Author-supplied aggregates, manually transcribed; no upstream experiment logs or hashes provided. Reproducible serialization starts at the bundle snapshot. snapshot_sha256=" + sha(SNAPSHOT)})
    return rows


def dictionary_rows():
    return [{"file_path": path, **field} for path, fields in SCHEMA.items() for field in fields]


def write_dictionary():
    with (FIG / "docs/data_dictionary.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["file_path", "column_name", "dtype", "unit", "description", "allowed_values", "missing_value", "required"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(dictionary_rows())


def validate():
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    counts = {}
    for name, table in RAW_TABLES.items():
        relative = "data/raw/" + name
        rows = read_csv(relative)
        assert rows == snapshot["tables"][table], f"Raw CSV differs from supplied snapshot: {name}"
        assert len(rows) == CONFIG["expected_raw_rows"][name]
        fields = ["source_id", "dataset", "model"] + (["mode"] if name == "egolink_costs.csv" else [])
        keys = [tuple(row[key] for key in fields) for row in rows]
        assert len(keys) == len(set(keys)), f"Duplicate raw keys: {name}"
    for relative, fields in SCHEMA.items():
        raw = (FIG / relative).read_bytes()
        assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf"), f"CSV is not UTF-8/LF: {relative}"
        with (FIG / relative).open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            assert reader.fieldnames == headers(relative), f"Unexpected fields: {relative}"
            rows = list(reader)
        counts[relative] = len(rows)
        for row in rows:
            for field in fields:
                value = row[field["column_name"]]
                if field["required"] == "true":
                    assert value != "", f"Missing required cell in {relative}"
                if value == "":
                    continue
                if field["dtype"] in {"integer", "number"}:
                    number = Decimal(value)
                    assert number.is_finite()
                    if field["dtype"] == "integer":
                        assert number == number.to_integral_value()
                    if field["allowed_values"] == ">=0":
                        assert number >= 0
                if field["dtype"] == "boolean":
                    assert value in {"true", "false"}
    expected = derive()
    for path, rows in expected.items():
        assert read_csv(path) == stringify(rows), f"Processed output differs from fresh calculation: {path}"
    for name, n in CONFIG["expected_panel_rows"].items():
        rows = read_csv("data/processed/" + name)
        assert len(rows) == n
        keys = [(r["panel"], r["dataset"], r["method"], r["condition"]) for r in rows]
        assert len(keys) == len(set(keys))
        assert all(r["n_models"] == str(len(CONFIG["primary_models"])) for r in rows)
    costs = read_csv("data/processed/recorded_costs_all_models.csv")
    assert len(costs) == 15
    assert sum(r["included_in_panel_c"] == "false" for r in costs) == 6
    audit = read_csv("data/processed/tool_view_arithmetic_audit.csv")
    conflicts = [r for r in audit if r["percentage_sign_conflict"] == "true"]
    assert len(conflicts) == CONFIG["expected_sign_conflicts"]
    assert all(r["dataset"] == "TravelGym-v2" for r in conflicts)
    assert read_csv("data/sources.csv") == sources()
    with (FIG / "docs/data_dictionary.csv").open(encoding="utf-8", newline="") as stream:
        assert list(csv.DictReader(stream)) == dictionary_rows()
    assert not list((FIG / "images").glob("*.png"))
    assert not list((FIG / "images").glob("*.pdf"))
    assert not list((FIG / "images").glob("*.svg"))
    assert counts["images/manifest.csv"] == 0
    panel_c = read_csv("data/processed/panel_c_tokens_per_task.csv")
    values = {r["method"]: Decimal(r["mean_value"]) for r in panel_c}
    paths = sorted(set([SNAPSHOT, FIG / "docs/data_dictionary.csv"]
                       + [FIG / p for p in SCHEMA]
                       + list((FIG / "config").glob("*.json"))
                       + list((FIG / "code").glob("*.py"))))
    return {"status": "data-ready", "experiment_rerun": False, "plot_generated": False,
            "independent_reproduction": False, "row_counts": counts,
            "source_percentage_sign_conflicts": len(conflicts),
            "source_rounding_residual_rows": sum(Decimal(r["rounding_residual_tokens"]) != 0 for r in audit),
            "panel_c_roleloop_saving_vs_react_pct": text(Decimal(100) * (1 - values["RoleLoop"] / values["ReAct"])),
            "panel_c_roleloop_saving_vs_summary_pct": text(Decimal(100) * (1 - values["RoleLoop"] / values["Summary"])),
            "sha256": {p.relative_to(FIG).as_posix(): sha(p) for p in paths}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate without writing")
    args = parser.parse_args()
    if not args.check:
        snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        for name, table in RAW_TABLES.items():
            write_csv("data/raw/" + name, snapshot["tables"][table])
        for path, rows in derive().items():
            write_csv(path, rows)
        write_csv("data/sources.csv", sources())
        write_csv("images/manifest.csv", [])
        write_dictionary()
    report = validate()
    if not args.check:
        report.update({"verified_at_utc": datetime.now(timezone.utc).isoformat(),
                       "verifier": "Codex local data-processing check; not an independent experiment rerun",
                       "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                                       "system": platform.system(), "release": platform.release(), "third_party_dependencies": []}})
        with (FIG / "docs/validation.json").open("w", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    else:
        recorded = json.loads((FIG / "docs/validation.json").read_text(encoding="utf-8"))
        assert report == {key: recorded[key] for key in report}, "Validation report differs; regenerate the bundle"
    print(json.dumps({"check_only": args.check, **{k: v for k, v in report.items() if k != "sha256"}}, indent=2))


if __name__ == "__main__":
    main()
