#!/usr/bin/env python3
"""
Convert src/llamafactory/webui/locales.py to vue-i18n JSON files.

Usage: python scripts/generate-i18n.py
Output: frontend/src/i18n/{en,zh,ru,ko,ja}.json
"""

import json
import re
import sys
from pathlib import Path


def extract_locales_dict(path: str) -> dict:
    """Import LOCALES from locales.py by reading and executing the file."""
    code = Path(path).read_text(encoding="utf-8")
    # Remove copyright header
    code = re.sub(r"# Copyright.*?\n(# .*?\n)*\n", "", code, flags=re.DOTALL)

    local_vars = {}
    exec(code, local_vars)
    return local_vars["LOCALES"]


def flatten_locales(locales: dict) -> dict[str, dict[str, str]]:
    """Convert nested LOCALES to {lang: {key: text}} format.

    Input:
    {
        "title": {
            "en": {"value": "..."},
            "zh": {"value": "..."},
        },
        "lang": {
            "en": {"label": "Language"},
        },
    }

    Output:
    {
        "en": {"title": "...", "lang": "Language"},
        "zh": {"title": "..."},
    }
    """
    langs: dict[str, dict[str, str]] = {}

    for key, translations in locales.items():
        for lang, fields in translations.items():
            if lang not in langs:
                langs[lang] = {}

            # Prefer "label", then "value", then any other field
            text = fields.get("label") or fields.get("value") or next(iter(fields.values()), "")
            # Strip HTML tags for the plain text version
            plain = re.sub(r"<[^>]+>", "", text).strip()
            langs[lang][key] = plain

    return langs


def main():
    repo_root = Path(__file__).resolve().parent.parent
    locales_py = repo_root / ".." / "src" / "llamafactory" / "webui" / "locales.py"
    output_dir = repo_root / "src" / "i18n"

    if not locales_py.exists():
        print(f"Error: {locales_py} not found", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    locales = extract_locales_dict(str(locales_py))
    flat = flatten_locales(locales)

    for lang, messages in flat.items():
        filepath = output_dir / f"{lang}.json"
        filepath.write_text(
            json.dumps(messages, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"[OK] {filepath} ({len(messages)} keys)", file=sys.stderr)

    # Generate index.ts
    index_ts = output_dir / "index.ts"
    lang_imports = "\n".join(
        f'import {lang} from "./{lang}.json";' for lang in sorted(flat.keys())
    )
    lang_exports = ", ".join(sorted(flat.keys()))
    index_ts.write_text(
        f"{lang_imports}\n\nexport const messages = {{ {lang_exports} }};\n"
    )
    print(f"[OK] {index_ts}", file=sys.stderr)


if __name__ == "__main__":
    main()
