# Pipeline de dataset — AgriDoc IA

Pipeline **reproductible** et **deterministe** (graine par defaut `20261122`), ecrit uniquement avec la bibliotheque standard Python et Pillow.

**Important :** ce pipeline ne telecharge rien, n'entraine rien et ne modifie aucun fichier Android. Il faut d'abord placer les images brutes localement (CCMT brut recommande, voir `ai/docs/PHASE_A_DATA_AUDIT.md`).

## Dependances

- Python 3.11+, Pillow (deja present sur la machine : `pillow 13.0.0`).
- Aucune dependance reseau, aucun appel a une API pendant l'execution.

## Commandes

```bash
# 1. Inventaire des images brutes CCMT (structure Raw data/CCMT Dataset/<Culture>/<Classe>/...)
python ai/pipeline/dataset_pipeline.py manifest --source CCMT_RAW \
  --root "D:/datasets/CCMT/Raw data/CCMT Dataset" --out ai/work/manifest.csv

# 2. Doublons exacts (SHA-256) et quasi-doublons (dhash 64 bits, distance <= 5)
python ai/pipeline/dataset_pipeline.py dedupe --manifest ai/work/manifest.csv \
  --out ai/work/groups.csv --groups-out ai/work/path_groups.csv

# 3. Separation 70/15/15 PAR GROUPE (aucune fuite plante/parcelle/image source)
python ai/pipeline/dataset_pipeline.py split --manifest ai/work/manifest.csv \
  --groups ai/work/path_groups.csv --out ai/work/split.csv

# 4. Augmentations uniquement sur le split train
python ai/pipeline/dataset_pipeline.py augment --manifest ai/work/manifest.csv \
  --split ai/work/split.csv --out-dir ai/work/augmented --out ai/work/augmented.csv

# 5. Labels provisionnels (a regenerer depuis le contrat reel apres Phase F)
python ai/pipeline/dataset_pipeline.py labels \
  --classes ai/configs/class_nomenclature_v1_proposal.json \
  --out ai/work/labels.proposal.txt --only-verified

# 6. Verification anti-fuite et effectifs
python ai/pipeline/dataset_pipeline.py validate --manifest ai/work/manifest.csv \
  --split ai/work/split.csv --report ai/work/validation_report.json --min-eval 5
```

## Transformations appliquees

| Etape | Transformation | Justification |
|---|---|---|
| `manifest` | SHA-256, dhash 64 bits, dimensions, controle taille/exposition/nettete | Tracabilite, detection des images inexploitables |
| `dedupe` | Union des images de meme SHA-256 ou de dhash proche | Eviter qu'une meme feuille/photo apparaisse dans deux ensembles |
| `split` | Attribution deterministe de chaque **groupe** a train/val/test (hash du groupe + graine) | Anti-fuite : toutes les images d'un meme groupe vont dans le meme split |
| `augment` | flip horizontal, rotation ±8°, luminosite ×0.9/×1.1, recadrage 92 % | Robustesse a la prise de vue reelle ; **aucune maladie ni insecte n'est synthetise** |
| `labels` | Tri alphabetique des identifiants de classe, un par ligne | Fichier de correspondance index → libelle |
| `validate` | Detection des fuites de groupe, doublons entre splits, effectifs min, images augmentees en evaluation | Porte de qualite avant entrainement |

## Regles de securite

1. **N'utiliser que le jeu CCMT brut** (`Raw Data.zip`, 1,22 Go). Le jeu augmente (6,81 Go) contient des variantes des memes images : le melanger avec un split de test creerait une fuite.
2. Les images `Cashew` sont hors perimeter V1 : les exclure ou les diriger vers `GLOBAL_INCONNU`.
3. Les classes CCMT ou l'insecte n'est pas clairement visible doivent etre reetiquetees `DEGAT_RAVAGEUR` apres audit visuel. Ne jamais deduire une espece d'un degat seul.
4. Les images de qualite insuffisante (`quality_ok = 0`) sont exclues de l'entrainement mais peuvent alimenter `GLOBAL_NON_EXPLOITABLE`.
5. `validation_agronomique` doit passer a `1` uniquement apres validation par le referent agronomique camerounais.
6. Le `labels.txt` final ne sera produit **apres** le gel du contrat du modele reel (Phase F). La sortie actuelle est explicitement `labels.proposal.txt`.
7. La separation `split` est **par groupe** mais ne garantit pas de quota par classe : c'est `validate` qui detecte une classe absente de `val`/`test`. Sur un petit jeu, ajuster `--seed` ou `--distance` (une distance de 5 peut regrouper des images visuellement proches).

## Etat

- [x] Scripts ecrits et verifies (syntaxe, `--help`, generation provisionnelle de labels)
- [x] Test de bout en bout sur 24 images **synthetiques de test** hors depot : `manifest`, `dedupe`, `split`, `augment` et `labels` fonctionnent ; `validate` detecte correctement une classe absente de la validation (comportement attendu)
- [ ] Execution reelle sur CCMT : en attente d'autorisation de telechargement (1,22 Go) et d'installation des dependances ML pour les phases D/E/F
