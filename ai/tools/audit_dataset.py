#!/usr/bin/env python3
"""Audit non destructif d'un dataset local pour AgriDoc.

Ce script ne télécharge, ne modifie et ne supprime aucune donnée.
Il produit un rapport JSON décrivant :
- l'inventaire des fichiers image ;
- les hashes SHA-256 ;
- les doublons exacts ;
- les doublons visuels probables (hash perceptuel moyen) ;
- les métadonnées manquantes ou invalides ;
- la validation des classes selon la nomenclature ;
- les fuites possibles entre train, validation et test.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - dépendance d'exécution
    raise SystemExit("Pillow est requis pour audit_dataset.py") from exc


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

REQUIRED_METADATA_FIELDS = {
    "image_id",
    "source",
    "culture",
    "type_probleme",
    "classe",
    "validation_agronomique",
    "qualite_image",
    "ensemble",
}

ALLOWED_VALUES = {
    "source": {"PlantVillage", "PlantDoc", "collecte_camerounaise", "autre"},
    "culture": {"MANIOC", "TOMATE", "MAIS", "GLOBAL"},
    "type_probleme": {"MALADIE", "RAVAGEUR", "DEGAT_RAVAGEUR", "CARENCE", "SAIN", "INCONNU"},
    "qualite_image": {"EXCELLENTE", "BONNE", "MOYENNE", "EXPLOITABLE_DIFFICILE"},
    "luminosite": {"ADEQUATE", "INSUFFISANTE", "EXCESSIVE"},
    "nettete": {"NETTE", "LEGEREMENT_FLOUE", "FLOUE"},
    "ensemble": {"train", "validation", "test"},
    "diagnostic_confirme": {True, False, "true", "false", "True", "False", 1, 0},
    "validation_agronomique": {True, False, "true", "false", "True", "False", 1, 0},
    "consentement_agriculteur": {True, False, "true", "false", "True", "False", 1, 0, None, ""},
}


@dataclass
class ImageRecord:
    path: str
    sha256: str
    size_bytes: int
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None
    readable: bool = True
    error: Optional[str] = None
    average_hash: Optional[str] = None


@dataclass
class AuditReport:
    dataset_root: str
    nomenclature_path: Optional[str]
    image_count: int = 0
    readable_image_count: int = 0
    unreadable_images: List[Dict[str, str]] = field(default_factory=list)
    exact_duplicate_groups: List[List[str]] = field(default_factory=list)
    visual_duplicate_groups: List[List[str]] = field(default_factory=list)
    metadata_path: Optional[str] = None
    metadata_record_count: int = 0
    metadata_errors: List[Dict[str, Any]] = field(default_factory=list)
    class_counts: Dict[str, int] = field(default_factory=dict)
    class_status_counts: Dict[str, int] = field(default_factory=dict)
    source_counts: Dict[str, int] = field(default_factory=dict)
    split_counts: Dict[str, int] = field(default_factory=dict)
    split_leakage: List[Dict[str, Any]] = field(default_factory=list)
    class_status: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def average_hash(path: Path, size: int = 16) -> Optional[str]:
    """Calcule un hash perceptuel moyen simple, sans dépendance externe."""
    try:
        with Image.open(path) as image:
            grayscale = image.convert("L").resize((size, size), Image.Resampling.LANCZOS)
            pixels = list(grayscale.getdata())
    except Exception:
        return None
    average = sum(pixels) / len(pixels)
    bits = "".join("1" if pixel >= average else "0" for pixel in pixels)
    return format(int(bits, 2), "0{}x".format((size * size + 3) // 4))


def hamming_distance(left: str, right: str) -> int:
    if len(left) != len(right):
        raise ValueError("Les hashes perceptuels doivent avoir la même longueur")
    try:
        return (int(left, 16) ^ int(right, 16)).bit_count()
    except ValueError:
        return sum(a != b for a, b in zip(left, right))


def load_nomenclature(path: Optional[Path]) -> Dict[str, str]:
    if path is None:
        return {}
    with path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    classes = data.get("classes", [])
    return {item["id"]: item.get("status", "unknown") for item in classes if "id" in item}


def load_metadata(path: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    errors: List[Dict[str, Any]] = []
    records: List[Dict[str, Any]] = []
    try:
        if path.suffix.lower() == ".jsonl":
            with path.open("r", encoding="utf-8-sig") as stream:
                for line_number, line in enumerate(stream, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError as exc:
                        errors.append({"line": line_number, "error": str(exc)})
        elif path.suffix.lower() == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                for row in reader:
                    records.append(dict(row))
        else:
            errors.append({"path": str(path), "error": "Format de métadonnées non supporté (attendu .csv ou .jsonl)"})
    except OSError as exc:
        errors.append({"path": str(path), "error": str(exc)})
    return records, errors


def validate_record(record: Dict[str, Any], allowed_classes: Dict[str, str]) -> List[str]:
    problems: List[str] = []
    for field_name in sorted(REQUIRED_METADATA_FIELDS):
        if record.get(field_name) in (None, ""):
            problems.append("champ obligatoire manquant: {}".format(field_name))

    for field_name, allowed in ALLOWED_VALUES.items():
        if field_name in record and record.get(field_name) not in (None, ""):
            value = record.get(field_name)
            if field_name in {"diagnostic_confirme", "validation_agronomique", "consentement_agriculteur"}:
                if str(value).lower() not in {"true", "false", "1", "0", "none"} and value not in {True, False, 1, 0, None, ""}:
                    problems.append("valeur invalide pour {}: {!r}".format(field_name, value))
            elif value not in allowed:
                problems.append("valeur invalide pour {}: {!r}".format(field_name, value))

    classe = record.get("classe")
    if classe and allowed_classes and classe not in allowed_classes:
        problems.append("classe absente de la nomenclature: {!r}".format(classe))

    return problems


def audit_dataset(
    dataset_root: Path,
    metadata_path: Optional[Path],
    nomenclature: Dict[str, str],
    phash_threshold: int,
) -> AuditReport:
    report = AuditReport(
        dataset_root=str(dataset_root),
        nomenclature_path=None if metadata_path is None else str(metadata_path),
    )

    if not dataset_root.exists() or not dataset_root.is_dir():
        report.notes.append("Racine de dataset absente ou non répertoire : {}".format(dataset_root))
        return report

    image_paths = sorted(
        path for path in dataset_root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )

    records_by_path: Dict[str, ImageRecord] = {}
    sha_groups: Dict[str, List[str]] = defaultdict(list)
    phash_groups: Dict[str, List[str]] = defaultdict(list)

    for path in image_paths:
        record = ImageRecord(path=str(path), sha256="", size_bytes=path.stat().st_size)
        try:
            record.sha256 = sha256_file(path)
            with Image.open(path) as image:
                record.width, record.height = image.size
                record.format = image.format
            record.average_hash = average_hash(path)
            sha_groups[record.sha256].append(str(path))
            if record.average_hash is not None:
                phash_groups[record.average_hash].append(str(path))
        except Exception as exc:  # noqa: BLE001 - audit non destructif
            record.readable = False
            record.error = str(exc)
            report.unreadable_images.append({"path": str(path), "error": str(exc)})
        records_by_path[str(path)] = record
        report.image_count += 1
        if record.readable:
            report.readable_image_count += 1

    report.exact_duplicate_groups = [group for group in sha_groups.values() if len(group) > 1]

    # Doublons visuels probables : comparaison par distance de Hamming.
    readable_hashes = [(path, rec.average_hash) for path, rec in records_by_path.items() if rec.average_hash]
    visual_groups: List[List[str]] = []
    used = set()
    for i, (path_i, hash_i) in enumerate(readable_hashes):
        if path_i in used:
            continue
        group = [path_i]
        used.add(path_i)
        for path_j, hash_j in readable_hashes[i + 1:]:
            if path_j in used:
                continue
            try:
                if hamming_distance(hash_i, hash_j) <= phash_threshold:
                    group.append(path_j)
                    used.add(path_j)
            except ValueError:
                continue
        if len(group) > 1:
            visual_groups.append(group)
    report.visual_duplicate_groups = visual_groups

    metadata_records: List[Dict[str, Any]] = []
    metadata_errors: List[Dict[str, Any]] = []
    if metadata_path is None:
        for candidate_name in ("metadata.csv", "metadata.jsonl"):
            candidate = dataset_root / candidate_name
            if candidate.exists():
                metadata_path = candidate
                break
    if metadata_path is not None:
        report.metadata_path = str(metadata_path)
        metadata_records, metadata_errors = load_metadata(metadata_path)
        report.metadata_record_count = len(metadata_records)
        report.metadata_errors.extend(metadata_errors)

    for record_index, record in enumerate(metadata_records):
        problems = validate_record(record, nomenclature)
        if problems:
            report.metadata_errors.append({"record_index": record_index, "problems": problems})

    # Comptages par classe, source et ensemble.
    class_counter: Counter[str] = Counter()
    status_counter: Counter[str] = Counter()
    source_counter: Counter[str] = Counter()
    split_counter: Counter[str] = Counter()
    image_id_to_splits: Dict[str, set] = defaultdict(set)
    plant_to_splits: Dict[str, set] = defaultdict(set)
    phash_to_splits: Dict[str, set] = defaultdict(set)

    for record in metadata_records:
        classe = record.get("classe")
        if classe:
            class_counter[str(classe)] += 1
            if nomenclature:
                status_counter[nomenclature.get(str(classe), "unknown")] += 1
        source = record.get("source")
        if source:
            source_counter[str(source)] += 1
        ensemble = record.get("ensemble")
        if ensemble:
            split_counter[str(ensemble)] += 1
        image_id = record.get("image_id")
        if image_id and ensemble:
            image_id_to_splits[str(image_id)].add(str(ensemble))
        for group_field in ("plant_id", "parcelle_id", "plant", "parcelle"):
            if record.get(group_field) and ensemble:
                plant_to_splits[str(record.get(group_field))].add(str(ensemble))
        image_path = record.get("fichier_image") or record.get("image_path") or record.get("path")
        if image_path and ensemble:
            resolved = Path(image_path)
            if not resolved.is_absolute():
                resolved = dataset_root / resolved
            record_hash = records_by_path.get(str(resolved))
            if record_hash and record_hash.average_hash:
                phash_to_splits[record_hash.average_hash].add(str(ensemble))

    for image_id, splits in image_id_to_splits.items():
        if len(splits) > 1:
            report.split_leakage.append({"type": "image_id", "value": image_id, "splits": sorted(splits)})

    for group_value, splits in plant_to_splits.items():
        if len(splits) > 1:
            report.split_leakage.append({"type": "plant_or_parcel", "value": group_value, "splits": sorted(splits)})

    for phash, splits in phash_to_splits.items():
        if len(splits) > 1:
            report.split_leakage.append({"type": "perceptual_hash", "value": phash, "splits": sorted(splits)})

    report.class_counts = dict(sorted(class_counter.items()))
    report.class_status_counts = dict(sorted(status_counter.items()))
    report.source_counts = dict(sorted(source_counter.items()))
    report.split_counts = dict(sorted(split_counter.items()))
    report.class_status = nomenclature

    if not image_paths:
        report.notes.append("Aucune image trouvée dans la racine fournie.")
    if metadata_path is None:
        report.notes.append("Aucun manifeste metadata.csv ou metadata.jsonl trouvé automatiquement.")
    if nomenclature:
        unknown_classes = sorted({r.get("classe") for r in metadata_records if r.get("classe") and r.get("classe") not in nomenclature})
        if unknown_classes:
            report.notes.append("Classes présentes dans le manifeste mais absentes de la nomenclature : {}".format(", ".join(unknown_classes)))

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit non destructif d'un dataset AgriDoc")
    parser.add_argument("--dataset-root", type=Path, required=True, help="Racine du dataset à auditer")
    parser.add_argument("--metadata", type=Path, default=None, help="Manifeste CSV ou JSONL (auto-détecté si absent)")
    parser.add_argument("--nomenclature", type=Path, default=None, help="Fichier JSON de nomenclature")
    parser.add_argument("--output", type=Path, default=None, help="Fichier JSON de sortie (stdout si absent)")
    parser.add_argument("--phash-threshold", type=int, default=5, help="Distance de Hamming maximale pour un doublon visuel probable")
    args = parser.parse_args()

    nomenclature = load_nomenclature(args.nomenclature) if args.nomenclature else {}
    report = audit_dataset(args.dataset_root, args.metadata, nomenclature, args.phash_threshold)
    payload = asdict(report)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    else:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())