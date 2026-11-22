# PHASE A — Audit des données AgriDoc V1

**Version :** 1.0
**Date :** 2026-11-22
**Auteur :** Lead IA / ML / TensorFlow Lite
**Statut :** Audit sources publiques + environnement local. **Aucune donnée n'a été téléchargée, aucun modèle n'a été entraîné, aucune annotation n'a été fabriquée.**

---

## 0. Avertissement méthodologique

Tout chiffre ci-dessous est soit **observé localement**, soit **mesuré depuis une source en ligne consultée le 2026-11-22**. Les compteurs sont distingués par nature :

- `images` : nombre réel de fichiers image listés (API GitHub / page Mendeley / article).
- `entrées leaf-map` : nombre d'entrées de mapping dans `leaf-map.json` (≈ 4 photos par groupe de feuille), **pas** un nombre d'images.
- `groupes-feuille` : nombre de groupes uniques (`:::identifiant`) dans `leaf-map.json` — utile pour la séparation anti-fuite.
- `annoncé` : valeur déclarée par un README/article mais non recomptée sur les fichiers.

Aucune source n'est considérée « validée pour production » uniquement sur la base d'un README.

---

## 1. Environnement et données locales — mesurés

| Élément | Observation | Preuve |
|---|---|---|
| Branche Git | `devop` (inchangée) | `git status --short --branch` |
| Fichiers non suivis préservés | `CLAUDE.md`, `docs/` (12 fichiers) | `git status --porcelain -uall` — **aucun modifié** |
| `app/src/main/assets/` | Uniquement `.gitkeep` ; aucun `.tflite`, aucun `labels.txt` | lecture du dossier |
| Images dans le dépôt | **0** fichier image (jpg/png/…) | recherche globale `**/*.{jpg,jpeg,png,…}` |
| Données/annotations dans le dépôt | **0** CSV/JSON de dataset, 0 script d'entraînement | recherche globale + arborescence |
| Modèles préentraînés | **0** (`.tflite`, `.pb`, `.pt`, `.onnx`, `.h5`) | recherche globale |
| Python | 3.11.9 | `python --version` |
| Paquets ML installés | **Pillow 13.0.0 uniquement** ; numpy, TensorFlow, torch, pandas, scikit-learn absents | `pip list` filtré |
| Espace disque C: | ~35 Go libres | `Get-PSDrive C` |

**Conclusion locale :** aucun dataset, aucune annotation, aucun modèle, aucun script IA n'existe dans le dépôt ou dans l'environnement. Le pipeline devra être construit avant tout entraînement.

---

## 2. Inventaire des datasets

### 2.1 Sources vérifiées en ligne le 2026-11-22

| Source | Identité vérifiée | Contenu mesuré / annoncé | Licence | Pertinence V1 | Décision |
|---|---|---|---|---|---|
| **CCMT** (Cashew, Cassava, Maize, Tomato) | ✅ Article *Data in Brief* 2023, DOI `10.1016/j.dib.2023.109306` (PMC10285554) ; Mendeley Data `bwh3zbpkpv` | **24 881 images brutes** (Cassava 7 508, Maize 5 389, Tomato 5 435, Cashew 6 549) ; 102 976 augmentées ; **22 classes** ; collecte Ghana oct.–déc. 2022 ; validation par virologues végétaux | ✅ **CC BY 4.0** (métadonnées Mendeley : `http://creativecommons.org/licenses/by/4.0`) | **Maximale** : couvre les 3 cultures V1 + ravageurs (armyworm, grasshopper, leaf beetle, green mite) | **Candidate prioritaire** — à télécharger (1,22 Go brut) |
| **PlantDoc** | ✅ `github.com/pratikkayal/PlantDoc-Dataset` (HTTP 200) | README : 2 598 images annoncées ; **API GitHub recursive tree : 2 579 fichiers image**, 28 classes `train/`, 27 `test/` | ✅ **CC BY 4.0** (`LICENSE.txt` lu) | Bonne : Tomate (9 classes `train/`), Maïs (3 classes) ; pas de manioc | Candidate secondaire (petits effectifs) |
| **PlantVillage** | ✅ `github.com/spMohanty/PlantVillage-Dataset` (HTTP 200) | README : 54 306 images annoncées, 14 espèces, 26 maladies ; **`leaf-map.json` : 40 328 clés → 31 classes, dont 9 Tomate, 0 Cassava, 0 Corn/Maize** | ❌ **Non déclarée explicitement** sur le README → utilisation commerciale non confirmée | Moyenne : uniquement tomate ; biais serre | **Non validée** (juridique) — bloquante |
| **iCassava / Kaggle Cassava Disease Classification** | ✅ Compétition Kaggle + article arXiv `1908.02900` ; TFDS `cassava` | 9 436 images labellisées (healthy 316/211, CMD 2658/1773, CBSD 1443/963, CBB 466/311, CGM 773/516 train/test) + 12 595 non labellisées ; Ouganda | ⚠️ Ambiguë : page Kaggle « Subject to Competition Rules » ; miroirs dérivés annoncés CC0 / CC BY 4.0 | Bonne pour manioc (maladies), mais CBSD surtout foliaire et licence à clarifier | Candidate sous réserve licence |
| **TOM2024** | ✅ *Data in Brief* 2025, Mendeley `3d4yg89rtr` | 25 844 images brutes / 12 227 labellisées, 30 classes tomate/oignon/maïs, Burkina Faso, 2022–2023 | À vérifier sur la page Mendeley | Bonne pour maïs/tomate + ravageurs | Candidate à licence à vérifier |
| **IITA Cameroun (données agronomiques)** | ✅ `data.iita.org` (essais manioc multi-lieux 2014–2016 ; pourriture racinaire 2024) | Données **tabulaires** (incidence, sévérité, rendement), pas d'images | Open Access (DOI `10.25502/hpny-t275/d`) | Validation agronomique uniquement | Utile comme référentiel, **pas entraînable** |
| **Campagnes CMD Cameroun (WAVE)** | ✅ *Crop Protection* 2022, DOI `10.1016/j.cropro.2022.106017` | 343 champs, 10 régions, 30 plantes/parcelle ; données « sur demande » | Article open access ; donnéesnon publiées | Contexte épidémiologique camerounais | Appui à la collecte, pas entraînable |
| **CCMT (ancienne affirmation du dépôt)** | ❌ Anciens documents `docs/DATASET_AUDIT.md:125-138`, `DATASET_INVENTORY.md:61-68` : « non identifié » | **Infirmé** : source identifiée, article + Mendeley + licence vérifiés | — | — | **Correction requise** (voir §7) |

### 2.2 Détail des classes mesurées

**PlantVillage — `leaf-map.json` (31 classes, 9 tomate).** Les compteurs sont des *entrées de mapping* et des *groupes-feuille* :

| Classe PlantVillage | Entrées leaf-map | Groupes-feuille uniques |
|---|---:|---:|
| `Tomato___Tomato_Yellow_Leaf_Curl_Virus` | 2 740 | 685 |
| `Tomato___Bacterial_spot` | 2 128 | 532 |
| `Tomato___Spider_mites Two-spotted_spider_mite` | 1 676 | 419 |
| `Tomato___Target_Spot` | 1 404 | 351 |
| `Tomato___Early_blight` | 1 000 | 250 |
| `Tomato___healthy` | 1 000 | 250 |
| `Tomato___Septoria_leaf_spot` | 1 000 | 250 |
| `Tomato___Leaf_Mold` | 952 | 238 |
| `Tomato___Late_blight` | 920 | 230 |

Aucune entrée contenant `Cassava`, `Corn` ou `Maize` dans ce fichier (comptage regex : 0 / 0 / 0). Le README annonce 14 espèces, mais **ce mapping précis ne couvre que 31 classes** : il ne peut pas servir à prouver la présence du maïs.

**PlantDoc — comptage réel via API GitHub (`git/trees/master?recursive=1`, `truncated: false`) :**

| Classe | `train/` | `test/` |
|---|---:|---:|
| `Tomato Septoria leaf spot` | 140 | 11 |
| `Tomato leaf bacterial spot` | 101 | 9 |
| `Tomato leaf late blight` | 101 | 10 |
| `Tomato Early blight leaf` | 79 | 9 |
| `Tomato leaf yellow virus` | 70 | 6 |
| `Tomato mold leaf` | 85 | 6 |
| `Tomato leaf mosaic virus` | 44 | 10 |
| `Tomato leaf` (saine) | 55 | 8 |
| `Tomato two spotted spider mites leaf` | **2** | **0** |
| `Corn leaf blight` | 180 | 12 |
| `Corn rust leaf` | 106 | 10 |
| `Corn Gray leaf spot` | 64 | **4** |

Écart README/API : 2 598 annoncés vs 2 579 fichiers image réellement listés (19 fichiers) — à investiguer avant import.

**CCMT — comptage officiel par classe (table 2 de l'article, images brutes) :**

| Culture | Classe | Images brutes | Catégorie |
|---|---|---:|---|
| Manioc | Bacterial blight | 2 614 | Maladie |
| Manioc | Brown spot | 1 481 | Maladie |
| Manioc | Green mite | 1 015 | Ravageur visible |
| Manioc | Healthy | 1 193 | Sain |
| Manioc | Mosaic | 1 205 | Maladie |
| Maïs | Fall armyworm | 285 | Ravageur visible |
| Maïs | Grasshopper | 673 | Ravageur visible |
| Maïs | Healthy | 208 | Sain |
| Maïs | Leaf beetle | 948 | Ravageur visible |
| Maïs | Leaf blight | 1 006 | Maladie |
| Maïs | Leaf spot | 1 259 | Maladie |
| Maïs | Streak virus | 1 010 | Maladie |
| Tomate | Healthy | 500 | Sain |
| Tomate | Leaf blight | 1 301 | Maladie |
| Tomate | Leaf curl | 518 | Maladie |
| Tomate | Septoria leaf spot | 2 343 | Maladie |
| Tomate | Verticillium wilt | 773 | Maladie |

Cashew (5 classes) est **hors périmètre V1** et doit être exclu ou dirigé vers `GLOBAL_INCONNU`.

---

## 3. Matrice culture × catégorie (disponibilité réelle)

Légende : ✅ source vérifiée avec effectif > 0 · ⚠️ effectif insuffisant / licence non vérifiée · ❌ aucune source vérifiée · ⛔ exclue du périmètre V1.

| Culture | Maladies | Ravageurs visibles | Dégâts de ravageurs | Carences | Sain | Inconnu / non exploitable |
|---|---|---|---|---|---|---|
| **Manioc** | ✅ CCMT : bacterial blight (2 614), brown spot (1 481), mosaic (1 205). ⚠️ iCassava : CMD/CBB/CGM (licence à clarifier). ⛔ CBSD : symptômes racinaires → exclue V1 | ✅ CCMT : green mite (1 015). ⚠️ iCassava CGM. **Whitefly** : vecteur documenté au Cameroun, pas de classe image dédiée | ❌ Aucune classe explicite ; CCMT « green mite » peut recouvrir dégâts + insecte → à redéfinir | ❌ Aucune source vérifiée | ✅ CCMT (1 193), ⚠️ iCassava (316/211) | ❌ À générer (main, ciel, sol, objets, flou) |
| **Tomate** | ✅ CCMT : leaf blight (1 301), septoria (2 343), leaf curl (518), verticillium (773). ✅ PlantDoc : 8 classes maladies. ✅ PlantVillage : 7 classes (groupes 230–685) | ⚠️ PlantVillage spider mites (419 groupes). ❌ PlantDoc spider mites : 2 images `train/`, 0 `test/`. ❌ Autres insectes | ❌ Aucune source vérifiée | ❌ Aucune source vérifiée | ✅ CCMT (500), PlantDoc (55), PlantVillage (250 groupes) | ❌ À générer |
| **Maïs** | ✅ CCMT : leaf blight (1 006), leaf spot (1 259), streak virus (1 010). ✅ PlantDoc : gray leaf spot (64/4), leaf blight (180/12), rust (106/10) | ✅ CCMT : fall armyworm (285), grasshopper (673), leaf beetle (948) | ❌ Pas de distinction dégât/insecte dans CCMT | ❌ Aucune source vérifiée | ✅ CCMT (208), PlantDoc (non détaillé) | ❌ À générer |
| **Global** | — | — | — | — | — | ❌ `GLOBAL_INCONNU`, `GLOBAL_NON_EXPLOITABLE` : à générer, 0 image |

---

## 4. Classes disponibles / classes manquantes

### 4.1 Disponibles après vérification (effectif > 0)

- **17 classes CCMT brutes** sur les 3 cultures cibles (table §2.2). C'est le seul jeu vérifié couvrant simultanément manioc, maïs, tomate **et** ravageurs visibles.
- **12 classes PlantDoc** cibles (9 tomate dont 1 ravageur quasi vide, 3 maïs), avec licence CC BY 4.0.
- **9 classes PlantVillage/Tomate** (groupes-feuille 230–685), mais licence commerciale non confirmée → non utilisables en l'état pour une app distribuée.

### 4.2 Manquantes ou non exploitables

| Besoin V1 | État | Conséquence |
|---|---|---|
| Carences nutritionnelles (manioc, tomate, maïs) | ❌ 0 image vérifiée dans toutes les sources | Classe à créer par collecte locale ; nutriment à préciser par un agronome (sinon classe ambiguë) |
| Dégâts de ravageurs non spécifiques (trous, galeries) | ❌ 0 classe explicite | Risque de prédire « ravageur » à partir de dégâts non spécifiques → interdit par le cahier des charges |
| `GLOBAL_INCONNU` / `GLOBAL_NON_EXPLOITABLE` | ❌ 0 image | Mécanisme de rejet impossible à entraîner sans images négatives |
| Validation camerounaise (variétés, lumière, stades) | ❌ 0 image | Biais de domaine garanti si on entraîne uniquement sur Ghana/serre/internet |
| Manioc : classe « ravageur » autre que green mite / whitefly | ❌ 0 image | À redéfinir avec l'agronome |
| Tomate : ravageurs autres que l'acarien | ❌ 0 image exploitable | PlantDoc spider mites = 2 images → insuffisant |
| Maïs : carences | ❌ 0 image | Collecte obligatoire |
| Licence PlantVillage | ❌ Non vérifiée | Blocage juridique potentiel |

**Aucune classe n'est « prête pour production »** : il manque simultanément le téléchargement effectif, le contrôle d'annotation, la validation agronomique locale et le seuil de confiance.

---

## 5. Problèmes de qualité et d'équilibre

| # | Problème | Preuve | Impact |
|---|---|---|---|
| Q1 | **Déséquilibre interne CCMT** : maïs sain 208 vs manioc bacterial blight 2 614 (~12×) | Article table 2 | F1 macro pénalisé ; biais vers les classes sur-représentées |
| Q2 | **PlantDoc spider mites : 2 images `train/`, 0 `test/`** | API GitHub | Classe inutilisable ; ne doit pas être annoncée comme couverte |
| Q3 | **PlantDoc `Corn Gray leaf spot` : 4 images en test** | API GitHub | Estimation de performance non fiable (≈ ±25 % par image) |
| Q4 | **Résolutions hétérogènes CCMT** : 400×400 à 4032×3024 | Article §2 | Prétraitement.resize obligatoire ; risque de perte de symptômes fins |
| Q5 | **Risque de fuite majeur avec CCMT « augmented »** : 102 976 images augmentées dérivées des 24 881 brutes | Article : « augmented » fourni avec train/test | **Interdiction formelle** de placer une image brute dans `train/` et sa version augmentée dans `test/` → utiliser **uniquement le jeu brut**, ou regrouper par image source |
| Q6 | **Biais de domaine** : PlantVillage serre/contrôlé, PlantDoc images scrapées, CCMT Ghana | README / article | Généralisation faible au Cameroun ; test local obligatoire |
| Q7 | **Décalage de licence** : PlantVillage non déclaré ; PlantDoc/CCMT CC BY 4.0 (attribution obligatoire) | README vs LICENSE | Blocage juridique / obligation de mention |
| Q8 | **Désaccord de comptage PlantDoc** : 2 598 annoncés vs 2 579 listés | README vs API GitHub | À résoudre avant import (19 fichiers) |
| Q9 | **Aucun seuil de confiance, aucun état « incertain » dans les données** | Audit code + absence de labels de rejet | Le rejet (phase E) devra être construit à partir d'un jeu de validation dédié |
| Q10 | **Aucune image locale, aucun script, aucun modèle préentraîné** | §1 | Le pipeline (phase C) doit être écrit avant toute mesure de performance |

---

## 6. Besoins de collecte complémentaire au Cameroun

Objectif : réduire le biais de domaine et couvrir les classes absentes. Les cibles chiffrées prolongent les critères déjà définis dans `docs/DATA_SPECIFICATION.md` et `docs/IA_IMPLEMENTATION_ROADMAP.md` (≥ 50–100 images/classe, ≥ 20 images/classe en test).

| Priorité | Besoin | Cible minimale proposée | Détail |
|---|---|---|---|
| P0 | **Validation locale des classes existantes** (manioc mosaic/bacterial blight/brown spot, maïs leaf blight/streak virus, tomate leaf curl/septoria/leaf blight) | ≥ 50 images par classe, dont ≥ 20 en test | Photographier en conditions réelles : lumière naturelle, variétés locales, stades jeunes/mûrs, deux faces de feuille |
| P0 | **Carences nutritionnelles** (3 cultures) | ≥ 50 images par nutriment retenu | Le nutriment doit être **spécifié** par l'agronome (N, P, K, Mg, Zn…) ; sinon classe « à redéfinir » |
| P0 | **Images négatives / rejet** | ≥ 50 par sous-classe | `GLOBAL_INCONNU` : main, ciel, sol, objet, feuille d'autre culture ; `GLOBAL_NON_EXPLOITABLE` : floue, sous/surexposée, coupée |
| P1 | **Ravageurs locaux visibles** | ≥ 50 par espèce identifiée | Manioc : green mite, whitefly (vecteur CMD) ; maïs : fall armyworm, criquet, leaf beetle ; tomate : acarien, autres insectes à préciser |
| P1 | **Dégâts de ravageurs** | ≥ 50 par type de dégât | Trous, galeries, déformations ; **ne pas étiqueter une espèce à partir du seul dégât** |
| P1 | **Métadonnées de collecte** | 100 % des images | Culture, catégorie, classe, région, localité, date, collecteur, parcelle/plante (anti-fuite), consentement, validation agronomique (`validation_agronomique = true`) |
| P2 | **Référent agronomique camerounais** | 1 minimum | Validation de 100 % des labels locaux ; arbitrage des confusions maladie/carence/dégât |

Zones suggérées par les documents existants (`DATASET_SPECIFICATION.md:166`, `CAMEROON_DATA_COLLECTION_PROTOCOL.md`) : Sud/Centre/Est, Ouest/Nord-Ouest, Extrême-Nord — à confirmer avec l'agronome. Données épidémiologiques de référence : campagnes WAVE (343 champs, 10 régions, DOI `10.1016/j.cropro.2022.106017`).

---

## 7. Corrections à apporter aux documents existants (non appliquées)

Ces fichiers sont **préservés à l'identique** ; les corrections sont proposées pour validation.

| Fichier | Assertion actuelle | Correction vérifiée |
|---|---|---|
| `docs/DATASET_AUDIT.md:77-138` | PlantDoc « non trouvé », CCMT « non identifié » | PlantDoc : URL correcte `pratikkayal/PlantDoc-Dataset` (200), CC BY 4.0. CCMT : article DOI `10.1016/j.dib.2023.109306`, Mendeley `bwh3zbpkpv`, CC BY 4.0, 24 881 images brutes |
| `docs/DATASET_INVENTORY.md:53-69` | PlantDoc 404, CCMT non identifié | Idem ; ajouter les comptages réels de l'API GitHub |
| `docs/DATASET_SOURCE_VERIFICATION.md:131-160` | CCMT non identifié | Idem |
| `docs/CLASS_FEASIBILITY_MATRIX.md:4,84` | 0 classe validée ; CCMT absent | CCMT fournit 17 classes cibles avec effectifs vérifiés ; la validation « production » reste à faire (licence OK, collecte locale manquante) |
| `docs/AGRI_DOC_V1_SPECIFICATION.md:126-129` | Contradiction C2 : Balawe fournirait le modèle | Confirmé : Keumeka/Messi produisent le modèle (issue #15), Balawe intègre les fichiers (issue #02) |

---

## 8. Points de décision avant la phase D

1. **Téléchargement CCMT brut (1,22 Go)** : nécessaire pour mesurer les images réelles, dédupliquer et entraîner. Non effectué à ce jour.
2. **Licence PlantVillage** : rester exclu tant que l'usage commercial n'est pas confirmé par écrit.
3. **iCassava / TOM2024** : vérifier précisément la licence avant incorporation.
4. **Installation des dépendances ML** : environnement actuel = Pillow seul ; TensorFlow/numpy nécessitent une installation (~centaines de Mo).
5. **Consigne de phase F confirmée** : comparaison **Float32 vs INT8** (taille du fichier, latence d'inférence, dégradation de précision). Décision enregistrée le 2026-11-22 ; aucune mesure n'est rapportée car aucun modèle n'a été entraîné.

**Aucune performance, aucune accuracy, aucun F1 et aucun modèle ne sont rapportés : ils n'existent pas encore.**
