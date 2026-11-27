import csv
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "tools"
import sys

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from audit_dataset import (
    average_hash,
    audit_dataset,
    hamming_distance,
    load_metadata,
    load_nomenclature,
    sha256_file,
    validate_record,
)
from PIL import Image


class TestAuditDataset(unittest.TestCase):
    def test_sha256_file_is_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.txt"
            path.write_text("AgriDoc", encoding="utf-8")
            self.assertEqual(
                sha256_file(path),
                "3775fe9f64401667e017453aacd8f83e3d16cdf9229a8cac4812425ddd34d74e",
            )

    def test_average_hash_has_expected_length(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "image.png"
            Image.new("RGB", (32, 32), color=(10, 20, 30)).save(path)
            result = average_hash(path)
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 64)

    def test_hamming_distance(self):
        self.assertEqual(hamming_distance("00", "00"), 0)
        self.assertEqual(hamming_distance("00", "0f"), 4)

    def test_load_metadata_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "metadata.csv"
            with path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["image_id", "classe"])
                writer.writeheader()
                writer.writerow({"image_id": "img1", "classe": "MAIS_SAIN"})
            records, errors = load_metadata(path)
            self.assertEqual(errors, [])
            self.assertEqual(records, [{"image_id": "img1", "classe": "MAIS_SAIN"}])

    def test_load_metadata_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "metadata.jsonl"
            path.write_text('{"image_id": "img1", "classe": "MAIS_SAIN"}\n', encoding="utf-8")
            records, errors = load_metadata(path)
            self.assertEqual(errors, [])
            self.assertEqual(records[0]["image_id"], "img1")

    def test_validate_record_detects_missing_and_unknown_class(self):
        nomenclature = {"MAIS_SAIN": "validated_for_experimentation"}
        record = {"source": "PlantVillage", "culture": "MAIS"}
        problems = validate_record(record, nomenclature)
        self.assertTrue(any("champ obligatoire manquant" in problem for problem in problems))
        self.assertTrue(any("champ obligatoire manquant: classe" in problem for problem in problems))

    def test_validate_record_accepts_valid_record(self):
        nomenclature = {"MAIS_SAIN": "validated_for_experimentation"}
        record = {
            "image_id": "img1",
            "source": "PlantVillage",
            "culture": "MAIS",
            "type_probleme": "SAIN",
            "classe": "MAIS_SAIN",
            "validation_agronomique": True,
            "qualite_image": "BONNE",
            "ensemble": "train",
        }
        self.assertEqual(validate_record(record, nomenclature), [])

    def test_audit_empty_dataset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            report = audit_dataset(root, None, {}, 5)
            self.assertEqual(report.image_count, 0)
            self.assertEqual(report.readable_image_count, 0)
            self.assertTrue(any("Aucune image" in note for note in report.notes))

    def test_audit_detects_exact_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            image = Image.new("RGB", (16, 16), color=(1, 2, 3))
            image.save(root / "a.png")
            image.save(root / "b.png")
            report = audit_dataset(root, None, {}, 5)
            self.assertEqual(report.image_count, 2)
            self.assertEqual(len(report.exact_duplicate_groups), 1)

    def test_audit_detects_split_leakage_by_image_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            Image.new("RGB", (16, 16), color=(1, 2, 3)).save(root / "a.png")
            manifest = root / "metadata.csv"
            with manifest.open("w", encoding="utf-8", newline="") as stream:
                import csv

                writer = csv.DictWriter(
                    stream,
                    fieldnames=["image_id", "source", "culture", "type_probleme", "classe",
                                "validation_agronomique", "qualite_image", "ensemble"],
                )
                writer.writeheader()
                writer.writerow({
                    "image_id": "same",
                    "source": "PlantVillage",
                    "culture": "MAIS",
                    "type_probleme": "SAIN",
                    "classe": "MAIS_SAIN",
                    "validation_agronomique": "true",
                    "qualite_image": "BONNE",
                    "ensemble": "train",
                })
                writer.writerow({
                    "image_id": "same",
                    "source": "PlantVillage",
                    "culture": "MAIS",
                    "type_probleme": "SAIN",
                    "classe": "MAIS_SAIN",
                    "validation_agronomique": "true",
                    "qualite_image": "BONNE",
                    "ensemble": "test",
                })
            report = audit_dataset(root, manifest, {"MAIS_SAIN": "validated_for_experimentation"}, 5)
            self.assertEqual(len(report.split_leakage), 1)
            self.assertEqual(report.split_leakage[0]["type"], "image_id")

    def test_audit_detects_unreadable_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            (root / "broken.png").write_text("not an image", encoding="utf-8")
            report = audit_dataset(root, None, {}, 5)
            self.assertEqual(report.image_count, 1)
            self.assertEqual(report.readable_image_count, 0)
            self.assertEqual(len(report.unreadable_images), 1)

    def test_load_nomenclature(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nomenclature.json"
            path.write_text(json.dumps({"classes": [{"id": "MAIS_SAIN", "status": "validated_for_experimentation"}]}), encoding="utf-8")
            self.assertEqual(load_nomenclature(path), {"MAIS_SAIN": "validated_for_experimentation"})


    def test_manifest_rejects_parent_traversal(self):
        nomenclature = {"MAIS_SAIN": "validated_for_experimentation"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            record = {
                "image_id": "img1",
                "source": "PlantVillage",
                "culture": "MAIS",
                "type_probleme": "SAIN",
                "classe": "MAIS_SAIN",
                "validation_agronomique": True,
                "qualite_image": "BONNE",
                "ensemble": "train",
                "fichier_image": "../outside.png",
            }
            problems = validate_record(record, nomenclature, root)
            self.assertTrue(any("traversée hors racine" in problem for problem in problems))

    def test_manifest_rejects_absolute_path(self):
        nomenclature = {"MAIS_SAIN": "validated_for_experimentation"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            record = {
                "image_id": "img1",
                "source": "PlantVillage",
                "culture": "MAIS",
                "type_probleme": "SAIN",
                "classe": "MAIS_SAIN",
                "validation_agronomique": True,
                "qualite_image": "BONNE",
                "ensemble": "train",
                "fichier_image": "C:/outside.png",
            }
            problems = validate_record(record, nomenclature, root)
            self.assertTrue(any("chemin absolu" in problem for problem in problems))

    def test_manifest_rejects_missing_image(self):
        nomenclature = {"MAIS_SAIN": "validated_for_experimentation"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            record = {
                "image_id": "img1",
                "source": "PlantVillage",
                "culture": "MAIS",
                "type_probleme": "SAIN",
                "classe": "MAIS_SAIN",
                "validation_agronomique": True,
                "qualite_image": "BONNE",
                "ensemble": "train",
                "fichier_image": "missing.png",
            }
            problems = validate_record(record, nomenclature, root)
            self.assertTrue(any("fichier image introuvable" in problem for problem in problems))

    def test_load_metadata_malformed_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "metadata.jsonl"
            path.write_text('{"image_id": "img1"\n{bad json}\n', encoding="utf-8")
            records, errors = load_metadata(path)
            self.assertEqual(records, [])
            self.assertTrue(errors)

    def test_audit_detects_truncated_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            path = root / "truncated.png"
            Image.new("RGB", (16, 16), color=(1, 2, 3)).save(path)
            data = path.read_bytes()
            path.write_bytes(data[:-20])
            report = audit_dataset(root, None, {}, 5)
            self.assertEqual(report.image_count, 1)
            self.assertEqual(report.readable_image_count, 0)
            self.assertEqual(len(report.unreadable_images), 1)

    def test_audit_records_hash_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            Image.new("RGB", (16, 16), color=(1, 2, 3)).save(root / "image.png")
            with patch("audit_dataset.average_hash", return_value=None):
                report = audit_dataset(root, None, {}, 5)
            self.assertEqual(report.image_count, 1)
            self.assertEqual(report.readable_image_count, 1)
            self.assertEqual(report.validated_image_count, 0)
            self.assertEqual(len(report.hash_errors), 1)

    def test_audit_union_find_transitive_grouping(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            for name in ("a.png", "b.png", "c.png"):
                Image.new("RGB", (16, 16), color=(1, 2, 3)).save(root / name)
            calls = {"n": 0}

            def fake_distance(left, right):
                calls["n"] += 1
                # a-b and b-c are close, a-c is far: transitive grouping is required.
                if {left, right} == {"a", "b"} or {left, right} == {"b", "c"}:
                    return 0
                return 10

            with patch("audit_dataset.average_hash", side_effect=["a", "b", "c"]), patch("audit_dataset.hamming_distance", side_effect=fake_distance):
                report = audit_dataset(root, None, {}, 0)
            self.assertEqual(len(report.visual_duplicate_groups), 1)
            self.assertEqual(len(report.visual_duplicate_groups[0]), 3)

    def test_audit_ignores_symlinked_files_if_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            outside = Path(tmp) / "outside.png"
            Image.new("RGB", (16, 16), color=(1, 2, 3)).save(outside)
            link = root / "linked.png"
            try:
                os.symlink(outside, link)
            except OSError:
                self.skipTest("liens symboliques non supportés dans cet environnement")
            report = audit_dataset(root, None, {}, 5)
            self.assertEqual(report.image_count, 0)
            self.assertEqual(report.skipped_symlink_count, 1)

    def test_manifest_rejects_symlink_escape_if_supported(self):
        nomenclature = {"MAIS_SAIN": "validated_for_experimentation"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            outside = Path(tmp) / "outside.png"
            Image.new("RGB", (16, 16), color=(1, 2, 3)).save(outside)
            link = root / "linked.png"
            try:
                os.symlink(outside, link)
            except OSError:
                self.skipTest("liens symboliques non supportés dans cet environnement")
            record = {
                "image_id": "img1",
                "source": "PlantVillage",
                "culture": "MAIS",
                "type_probleme": "SAIN",
                "classe": "MAIS_SAIN",
                "validation_agronomique": True,
                "qualite_image": "BONNE",
                "ensemble": "train",
                "fichier_image": "linked.png",
            }
            problems = validate_record(record, nomenclature, root)
            self.assertTrue(problems)

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "dataset"
            root.mkdir()
            report = audit_dataset(root, None, {}, 5)
            self.assertEqual(report.image_count, 0)
            self.assertTrue(any("Aucune image" in note for note in report.notes))


if __name__ == "__main__":
    unittest.main()