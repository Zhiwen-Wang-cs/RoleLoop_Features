#!/usr/bin/env python3
"""Create an empty figure workspace without overwriting existing work."""

import argparse
from pathlib import Path
import re
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Example: fig_001_performance")
    args = parser.parse_args()
    if not re.fullmatch(r"fig_[0-9]{3}_[a-z][a-z0-9]*(?:_[a-z0-9]+)*", args.name):
        parser.error("Use fig_NNN_topic with a three-digit ID and lowercase snake_case topic.")

    repo = Path(__file__).resolve().parents[1]
    template = repo / "templates" / "figure"
    figures = repo / "figures"
    destination = figures / args.name
    if not template.is_dir():
        parser.error("The templates/figure directory is missing.")
    existing = sorted(figures.glob(args.name[:7] + "_*"))
    if existing:
        parser.error("Figure ID already exists: " + existing[0].name)
    if destination.exists():
        parser.error("Destination already exists; no files were changed.")

    shutil.copytree(template, destination)
    for path in destination.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".txt", ".csv"}:
            content = path.read_text(encoding="utf-8")
            with path.open("w", encoding="utf-8", newline="\n") as stream:
                stream.write(content.replace("{{FIGURE_ID}}", args.name))

    print("Created " + str(destination))
    print("Next: fill in its README and add an entry to figures/README.md.")
    print("This is an empty template; no experimental data or plots were generated.")


if __name__ == "__main__":
    main()
