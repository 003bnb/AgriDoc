#!/usr/bin/env python3
"""AgriDoc IA - pipeline de dataset reproductible.

Uniquement la bibliotheque standard Python + Pillow (deja installee).
Aucun telephone reseau, aucun telechargement, aucun entrainement.

Sous-commandes :
  manifest  inventaire des images d'une source locale
  dedupe    detection des doublons et groupes d'images liees
  split     separation train/validation/test SANS fuite (par groupe)
  augment   augmentations realistes, uniquement sur le split train
  labels    generation provisionnelle de labels.txt
  validate  verification des regles anti-fuite et des effectifs

Exemple :
  python ai/pipeline/dataset_pipeline.py manifest --source CCMT_RAW \
      --root "D:/datasets/CCMT/Raw data/CCMT Dataset" --out ai/work/manifest.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageStat
except ImportError:
    sys.exit("Pillow est requis: pip install pillow")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
CROPS = {"cassava": "MANIOC", "manioc": "MANIOC", "maize": "MAIS",
         "corn": "MAIS", "tomato": "TOMATE", "tomate": "TOMATE"}
MANIFEST_FIELDS = [
    "path", "source", "crop", "class_id", "split_hint", "width", "height",
    "sha256", "dhash", "quality_ok", "quality_flags", "group_key",
    "licence", "validation_agronomique",
]


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(text: str) -> str:
    return " ".join(text.replace("_", " ").replace("-", " ").lower().split())


def dhash(path: Path, hash_size: int = 8) -> str:
    """Empreinte perceptuelle simple (difference de pixels voisins)."""
    with Image.open(path) as img:
        gray = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
        # Pillow >= 13 : get_flattened_data remplace getdata (deprecie).
        getter = getattr(gray, "get_flattened_data", None) or gray.getdata
        px = list(getter())
    bits = [px[row * (hash_size + 1) + col] > px[row * (hash_size + 1) + col + 1]
            for row in range(hash_size) for col in range(hash_size)]
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return f"{value:016x}"


def hamming(a: str, b: str) -> int:
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def quality(path: Path) -> tuple[bool, str, int, int, str]:
    """Controles deterministes : taille, exposition, nettete, empreinte."""
    with Image.open(path) as img:
        width, height = img.size
        gray = img.convert("L")
        mean = ImageStat.Stat(gray).mean[0]
        edges = ImageStat.Stat(gray.filter(ImageFilter.FIND_EDGES)).stddev[0]
    flags = []
    if min(width, height) < 128:
        flags.append("TOO_SMALL")
    if mean < 20 or mean > 235:
        flags.append("EXPOSURE")
    if edges < 2.0:
        flags.append("BLUR")
    return (not flags), "|".join(flags), width, height, dhash(path)


def load_config() -> dict:
    cfg = Path(__file__).resolve().parent.parent / "configs" / "sources_v1.json"
    return json.loads(cfg.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def map_class(rel: Path, source_cfg: dict) -> tuple[str, str]:
    """Retourne (culture, class_id) depuis l'arborescence source."""
    parts = [norm(p) for p in rel.parts[:-1]]
    crop = ""
    crop_key = ""
    class_part = ""
    for i, part in enumerate(parts):
        if part in CROPS:
            crop = CROPS[part]
            crop_key = part
            if i + 1 < len(parts):
                class_part = parts[i + 1]
            break
    if not class_part and parts:
        class_part = parts[-1]
    key = f"{crop_key}/{class_part}".strip("/")
    cmap = {norm(k): v for k, v in source_cfg.get("class_map", {}).items()}
    class_id = cmap.get(norm(key)) or cmap.get(norm(class_part)) or "CLASS_NON_MAPPEE"
    return crop, class_id


# ---------------------------------------------------------------------------
# Commandes
# ---------------------------------------------------------------------------
def cmd_manifest(args) -> None:
    cfg = load_config()["sources"][args.source]
    if cfg.get("utilisable") is False:
        sys.exit(f"Source {args.source} non utilisable : {cfg.get('raison')}")
    root = Path(args.root)
    if not root.is_dir():
        sys.exit(f"Dossier introuvable : {root}")
    rows = []
    for i, path in enumerate(sorted(root.rglob("*"))):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
            continue
        ok, flags, w, h, digest = quality(path)
        crop, class_id = map_class(path.relative_to(root), cfg)
        rows.append({
            "path": str(path.resolve()), "source": args.source, "crop": crop,
            "class_id": class_id,
            "split_hint": "train" if "train" in path.parts else ("test" if "test" in path.parts else ""),
            "width": w, "height": h, "sha256": sha256_file(path), "dhash": digest,
            "quality_ok": "1" if ok else "0", "quality_flags": flags,
            "group_key": f"{args.source}|{class_id}|{digest[:8]}",
            "licence": cfg["licence"], "validation_agronomique": "0",
        })
        if args.limit and len(rows) >= args.limit:
            break
    write_csv(Path(args.out), rows, MANIFEST_FIELDS)
    unmapped = sum(r["class_id"] == "CLASS_NON_MAPPEE" for r in rows)
    print(f"manifest: {len(rows)} images, {unmapped} non mappees -> {args.out}")


def cmd_dedupe(args) -> None:
    rows = read_csv(Path(args.manifest))
    by_class: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_class[r["class_id"]].append(r)
    parent: dict[str, str] = {r["path"]: r["path"] for r in rows}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for group in by_class.values():
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                if a["sha256"] == b["sha256"] or hamming(a["dhash"], b["dhash"]) <= args.distance:
                    union(a["path"], b["path"])
    clusters: dict[str, list[str]] = defaultdict(list)
    for p in parent:
        clusters[find(p)].append(p)
    group_rows = []
    mapping: dict[str, str] = {}
    for idx, (canonical, members) in enumerate(sorted(clusters.items())):
        gid = f"G{idx:06d}"
        group_rows.append({"group_id": gid, "canonical_path": canonical,
                           "member_paths": "|".join(sorted(members)), "size": len(members)})
        for m in members:
            mapping[m] = gid
    write_csv(Path(args.out), group_rows, ["group_id", "canonical_path", "member_paths", "size"])
    if args.groups_out:
        write_csv(Path(args.groups_out),
                  [{"path": p, "group_id": g} for p, g in sorted(mapping.items())],
                  ["path", "group_id"])
    print(f"dedupe: {len(rows)} images -> {len(group_rows)} groupes -> {args.out}")


def cmd_split(args) -> None:
    rows = read_csv(Path(args.manifest))
    groups: dict[str, str] = {}
    if args.groups:
        groups = {r["path"]: r["group_id"] for r in read_csv(Path(args.groups))}
    a, b, c = args.ratios
    if abs(a + b + c - 1.0) > 1e-6:
        sys.exit("Les ratios doivent totaliser 1.0")
    split_of_group: dict[str, str] = {}
    out = []
    for r in rows:
        gid = groups.get(r["path"], r["group_key"])
        if gid not in split_of_group:
            val = int(hashlib.sha256(f"{args.seed}:{gid}".encode()).hexdigest()[:8], 16) % 100
            split_of_group[gid] = "train" if val < a * 100 else ("val" if val < (a + b) * 100 else "test")
        out.append({"path": r["path"], "class_id": r["class_id"], "crop": r["crop"],
                    "group_id": gid, "split": split_of_group[gid], "quality_ok": r["quality_ok"]})
    write_csv(Path(args.out), out, ["path", "class_id", "crop", "group_id", "split", "quality_ok"])
    for name in ("train", "val", "test"):
        print(f"split {name}: {sum(r['split'] == name for r in out)} images")


def cmd_augment(args) -> None:
    splits = {r["path"]: r for r in read_csv(Path(args.split))}
    manifest = {r["path"]: r for r in read_csv(Path(args.manifest))}
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    transforms = ["horizontal_flip", "rotate_+8", "rotate_-8",
                  "brightness_0.9", "brightness_1.1", "crop_0.92"]
    rows = []
    for path, s in splits.items():
        if s["split"] != "train" or s.get("quality_ok") != "1":
            continue
        rnd = random.Random(f"{args.seed}:{path}")
        chosen = rnd.sample(transforms, min(args.per_image, len(transforms)))
        with Image.open(path) as img:
            base = img.convert("RGB")
        for i, t in enumerate(chosen):
            im = base.copy()
            if t == "horizontal_flip":
                im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            elif t.startswith("rotate_"):
                im = im.rotate(8 if t.endswith("+8") else -8, resample=Image.Resampling.BICUBIC, expand=False)
            elif t.startswith("brightness_"):
                factor = float(t.split("_")[1])
                im = Image.eval(im, lambda p, f=factor: min(255, int(p * f)))
            elif t == "crop_0.92":
                w, h = im.size
                nw, nh = int(w * 0.92), int(h * 0.92)
                x, y = rnd.randint(0, w - nw), rnd.randint(0, h - nh)
                im = im.crop((x, y, x + nw, y + nh)).resize((w, h), Image.Resampling.BICUBIC)
            dest = out_dir / f"{Path(path).stem}__aug{i}.jpg"
            im.save(dest, quality=92)
            rows.append({"path": str(dest.resolve()), "origin_path": path,
                         "transform": t, "class_id": s["class_id"], "split": "train"})
    write_csv(Path(args.out), rows, ["path", "origin_path", "transform", "class_id", "split"])
    print(f"augment: {len(rows)} variantes generees (train uniquement) -> {args.out}")


def cmd_labels(args) -> None:
    data = json.loads(Path(args.classes).read_text(encoding="utf-8"))
    classes = data["classes"]
    if args.only_verified:
        classes = [c for c in classes if c["statut"] == "source_verifiee"]
    ids = sorted({c["id"] for c in classes})
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(ids) + "\n", encoding="utf-8")
    print(f"labels: {len(ids)} lignes (PROVISIONNEL, a regenerer apres Phase F) -> {args.out}")


def cmd_validate(args) -> None:
    manifest = read_csv(Path(args.manifest))
    splits = read_csv(Path(args.split))
    by_path = {r["path"]: r for r in manifest}
    split_by_path = {r["path"]: r["split"] for r in splits}
    errors, warnings = [], []

    groups: dict[str, set[str]] = defaultdict(set)
    hashes: dict[str, set[str]] = defaultdict(set)
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for r in splits:
        p = r["path"]
        if p not in by_path:
            errors.append(f"Image absente du manifest: {p}")
            continue
        groups[r["group_id"]].add(r["split"])
        hashes[by_path[p]["sha256"]].add(r["split"])
        counts[(r["class_id"], r["split"])] += 1
        if r["split"] in ("val", "test") and "__aug" in p:
            errors.append(f"Image augmentee dans {r['split']}: {p}")
    for gid, ss in groups.items():
        if len(ss) > 1:
            errors.append(f"Fuite de groupe {gid} entre {sorted(ss)}")
    for sha, ss in hashes.items():
        if len(ss) > 1:
            errors.append(f"Meme SHA256 dans plusieurs splits: {sha[:12]}")
    for cls in sorted({c for c, _ in counts}):
        for split in ("val", "test"):
            n = counts.get((cls, split), 0)
            if n < args.min_eval:
                (errors if n == 0 else warnings).append(f"{cls}: {n} images en {split} (minimum {args.min_eval})")
    report = {"errors": errors, "warnings": warnings,
              "counts": {f"{c}|{s}": n for (c, s), n in sorted(counts.items())}}
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"validate: {len(errors)} erreur(s), {len(warnings)} avertissement(s) -> {args.report}")
    if errors:
        sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    m = sub.add_parser("manifest")
    m.add_argument("--source", required=True, help="Nom dans ai/configs/sources_v1.json")
    m.add_argument("--root", required=True, help="Dossier local des images brutes")
    m.add_argument("--out", required=True)
    m.add_argument("--limit", type=int, default=0, help="Nombre max d'images (test rapide)")
    m.set_defaults(func=cmd_manifest)

    d = sub.add_parser("dedupe")
    d.add_argument("--manifest", required=True)
    d.add_argument("--out", required=True, help="CSV des groupes")
    d.add_argument("--groups-out", default="", help="CSV optionnel path -> group_id")
    d.add_argument("--distance", type=int, default=5, help="Distance de Hamming maximale (dhash 64 bits)")
    d.set_defaults(func=cmd_dedupe)

    s = sub.add_parser("split")
    s.add_argument("--manifest", required=True)
    s.add_argument("--groups", default="", help="CSV path -> group_id (sortie de dedupe)")
    s.add_argument("--out", required=True)
    s.add_argument("--seed", type=int, default=20261122)
    s.add_argument("--ratios", nargs=3, type=float, default=[0.70, 0.15, 0.15])
    s.set_defaults(func=cmd_split)

    a = sub.add_parser("augment")
    a.add_argument("--manifest", required=True)
    a.add_argument("--split", required=True)
    a.add_argument("--out-dir", required=True)
    a.add_argument("--out", required=True)
    a.add_argument("--per-image", type=int, default=3)
    a.add_argument("--seed", type=int, default=20261122)
    a.set_defaults(func=cmd_augment)

    l = sub.add_parser("labels")
    l.add_argument("--classes", required=True)
    l.add_argument("--out", required=True)
    l.add_argument("--only-verified", action="store_true")
    l.set_defaults(func=cmd_labels)

    v = sub.add_parser("validate")
    v.add_argument("--manifest", required=True)
    v.add_argument("--split", required=True)
    v.add_argument("--report", required=True)
    v.add_argument("--min-eval", type=int, default=5)
    v.set_defaults(func=cmd_validate)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
