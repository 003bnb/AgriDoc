import csv
import json
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()