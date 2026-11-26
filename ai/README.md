# AgriDoc — Sous-système IA

Espace de travail **exclusivement IA**. Ce dossier ne contient aucun code Android et ne remplace aucune responsabilité des autres membres (UI, caméra, Room, navigation, intégration applicative).

## Périmètre V1

- Cultures : manioc, tomate, maïs.
- Problèmes : maladies, ravageurs visibles, dégâts visibles, carences nutritionnelles, plante saine, inconnu / non exploitable.
- Contrainte : **100 % hors-ligne**, inférence TFLite sur appareil.
- Règle : jamais de diagnostic affirmatif quand les preuves visuelles sont insuffisantes ; prévoir un mécanisme de rejet.

## Contenu

| Chemin | Rôle |
|---|---|
| `nomenclature/agridoc_v1_classes.json` | Nomenclature proposée et statuts de faisabilité |
| `tools/audit_dataset.py` | Audit non destructif d'un dataset local : inventaire, hashes, doublons, métadonnées, classes, fuites train/validation/test |
| `tools/check_manifest.py` | Validation d'un manifeste CSV ou JSONL |
| `tests/test_audit_dataset.py` | Tests unitaires des outils d'audit |

## État actuel

- Aucun dataset n'est présent dans ce dépôt.
- Aucun modèle `.tflite` ni `labels.txt` réel n'est présent.
- Les scripts sont des outils de préparation et de contrôle. Ils ne créent aucune donnée agronomique et ne téléchargent aucune source.
- PlantVillage et PlantDoc sont des sources vérifiées, non des datasets téléchargés.
- CCMT n'est pas identifié.
- La licence commerciale de PlantVillage n'est pas vérifiée.
- Les comptages d'images disponibles sont préliminaires et doivent être confirmés par `leaf_grouping` avant entraînement.

## Limites

- Les scripts ne valident pas la qualité agronomique d'une annotation.
- Les labels publics ne sont pas automatiquement considérés comme validés par un agronome.
- Les scripts ne génèrent aucun modèle et n'exécutent aucun entraînement.
- Les dimensions, le type, la normalisation et le seuil d'entrée doivent être extraits du modèle réel.