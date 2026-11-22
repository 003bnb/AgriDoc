# AgriDoc — Sous-système IA (Lead IA / ML / TensorFlow Lite)

Espace de travail **exclusivement IA**. Ce dossier ne contient aucun code Android et ne remplace aucune responsabilité des autres membres (UI, caméra, Room, navigation, intégration applicative).

## Périmètre

- Cultures V1 : **manioc, tomate, maïs**.
- Catégories : maladies, ravageurs visibles, dégâts visibles, carences nutritionnelles, plante saine, inconnu / non exploitable.
- Contrainte : **100 % hors-ligne**, inférence TFLite sur appareil.
- Règle : jamais de diagnostic affirmatif quand les preuves visuelles sont insuffisantes ; prévoir un mécanisme de rejet.

## Contenu

| Chemin | Rôle |
|---|---|
| `ai/docs/PHASE_A_DATA_AUDIT.md` | Inventaire des données, matrice culture × catégorie, classes disponibles/manquantes, qualité/équilibre, besoins de collecte au Cameroun |
| `ai/configs/class_nomenclature_v1_proposal.json` | Nomenclature proposée, lisible par machine — **proposition non validée**, aucune annotation réelle |
| `ai/configs/sources_v1.json` | Registre des sources vérifiées et mapping de classes proposé |
| `ai/docs/PHASE_B_IA_ARCHITECTURE.md` | Architecture hiérarchique retenue, contrat d'entrée/sortie, règles de rejet |
| `ai/pipeline/` | Pipeline de dataset reproductible (manifest, dédup, split anti-fuite, augmentations, labels, validation) |

## Frontière de livraison

Les artefacts binaires finaux (`.tflite`, `labels.txt`, contrat d'entrée/sortie) seront remis **à Balawe** pour intégration dans `app/src/main/assets/` (issue #02). Ils ne seront pas déposés directement dans `app/` par le sous-système IA.

## État d'avancement

- [x] Phase A — audit des données (aucune donnée téléchargée, aucun modèle entraîné)
- [x] Phase B — architecture IA (choix justifiés, contrat proposé)
- [x] Phase C — pipeline de dataset reproductible (scripts vérifiés, non exécutés sur données réelles)
- [ ] Phase D — entraînement et comparaison
- [ ] Phase E — incertitude et rejet
- [ ] Phase F — export TensorFlow Lite : comparaison **Float32 vs INT8** (taille, latence, dégradation) — consigne confirmée, en attente

## État d'exécution

Phases A–C livrées. **Phases D–F en attente sur décision explicite** : aucun téléchargement de dataset (CCMT brut ≈ 1,22 Go), aucune installation de dépendances ML, aucun entraînement, aucun export.
