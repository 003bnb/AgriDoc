#!/usr/bin/env python3
"""Validation d'un manifeste de dataset AgriDoc.

Usage :
    python check_manifest.py --manifest metadata.csv --nomenclature ../nomenclature/agridoc_v1_classes.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from audit_dataset import (  # noqa: E402
    load_metadata,
    load_nomenclature,
    validate_record,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Valide un manifeste AgriDoc")
    parser.add_argument("--manifest", type=Path, required=True, help="Manifeste CSV ou JSONL")
    parser.add_argument("--nomenclature", type=Path, default=None, help="Fichier JSON de nomenclature")
    parser.add_argument("--dataset-root", type=Path, default=None, help="Racine optionnelle pour vérifier l'existence des images")
    args = parser.parse_args()

    nomenclature = load_nomenclature(args.nomenclature) if args.nomenclature else {}
    if args.dataset_root is not None and args.dataset_root.is_symlink():
        result = {
            "manifest": str(args.manifest),
            "record_count": 0,
            "error_count": 1,
            "errors": [{"path": str(args.dataset_root), "error": "La racine du dataset est un lien symbolique : validation refusée."}],
            "valid": False,
        }
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1
    records, errors = load_metadata(args.manifest)

    all_errors = list(errors)
    for index, record in enumerate(records):
        problems = validate_record(record, nomenclature)
        if args.dataset_root is not None:
            image_name = record.get("fichier_image") or record.get("image_path") or record.get("path")
            if image_name:
                image_path = Path(image_name)
                if not image_path.is_absolute():
                    image_path = args.dataset_root / image_path
                if not image_path.exists():
                    problems.append("fichier image introuvable: {}".format(image_path))
        if problems:
            all_errors.append({"record_index": index, "problems": problems})

    result = {
        "manifest": str(args.manifest),
        "record_count": len(records),
        "error_count": len(all_errors),
        "errors": all_errors,
        "valid": len(all_errors) == 0,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())