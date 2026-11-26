# DATASET_INVENTORY — Inventaire des Datasets Examinés AgriDoc V1

**Version :** 1.2  
**Statut :** Inventaire basé sur l'examen réel des sources accessibles ; revu le 2026-11-24 (corrections de PlantDoc et de la structure PlantVillage)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi)  
**Dernière révision :** 2026-11-24

---

## 1. Objectif

Cet inventaire recense les datasets réellement examinés lors de la Mission 3, avec les résultats de l'examen et les limites identifiées. **Aucun dataset n'a été téléchargé ni stocké localement ; seuls les métadonnées (leaf-map.json, structures de dépôt) ont été consultées.** Cet inventaire est reproductible : toute personne peut refaire les mêmes vérifications en accédant aux mêmes sources.

---

## 2. Datasets Examinés

### 2.1 PlantVillage

| Élément | Valeur observée | Méthode de vérification |
|---------|----------------|------------------------|
| Existence du dépôt | ✅ Confirmé | https://github.com/spMohanty/PlantVillage-Dataset (200 OK) |
| Statut du dépôt | Public | Page GitHub |
| Nombre total d'images | 54,306 (déclaré dans le README) | README du dépôt |
| Nombre d'espèces | 14 (déclaré dans le README) | README du dépôt |
| Nombre de maladies | 26 (déclaré dans le README) | README du dépôt |
| Papier scientifique | Mohanty et al. (2016), Frontiers in Plant Science, DOI 10.3389/fpls.2016.01419 | README du dépôt |
| Licence | ❌ Non vérifiée | Aucune licence détectée dans le dépôt (API `/license` : 404) |
| Utilisation commerciale | ❌ Non vérifiée | À confirmer auprès des auteurs |
| Structure des données | `raw/` (sous-dossiers `color/`, `grayscale/`, `segmented/`), `leaf_grouping/`, `leaf-map.json`, `scripts/`, `generated_for_paper/` | Exploration du dépôt |
| Fichier de mapping | `leaf-map.json` (ID fichier → classe), 2 429 879 octets | Consulté et analysé en intégralité le 2026-11-24 |
| Classes du mapping `leaf-map.json` | 31 classes comptées ; aucune classe « Cassava » ni « Corn » dans ce mapping (mapping partiel, cf. §2.1.1) | `leaf-map.json` analysé en intégralité |
| Classes Maïs (Corn) dans `raw/` | ✅ Confirmées : 4 classes, cf. §2.1.2 | API GitHub, dossiers `raw/{color,grayscale,segmented}` |
| Classes Manioc (Cassava) | ❌ Absentes de tous les dossiers `raw/` (color, grayscale, segmented) | API GitHub, exploration complète des 38 classes par dossier |
| Splits train/test | 80/20 avec grouping par feuille (anti-fuite) | README du dépôt (via Hugging Face `mohanty/PlantVillage`) |
| Format d'accès recommandé | Hugging Face `datasets` library | README du dépôt |

#### 2.1.1 `leaf-map.json` (fichier racine) — analyse complète du 2026-11-24

- 2 429 879 octets, 4 032 entrées de mapping (l'API GitHub renvoie 2 429 879 octets pour ce fichier).
- **31 classes distinctes** : Apple (Frogeye Spot, Apple_scab, Cedar_apple_rust, healthy), Blueberry (healthy), Cherry (Powdery_mildew, healthy), Grape (Black_rot, Esca, Leaf_blight, healthy), Orange (Haunglongbing), Peach (Bacterial_spot, healthy), Pepper_bell (Bacterial_spot, healthy), Potato (Early_blight, Late_blight, healthy), Raspberry (healthy), Soybean (healthy), Strawberry (Leaf_scorch, healthy), Tomato (Bacterial_spot, Early_blight, Late_blight, Leaf_Mold, Septoria_leaf_spot, Spider_mites, Target_Spot, Yellow_Leaf_Curl_Virus, healthy).
- **Aucune classe « Cassava » ni « Corn » dans ce mapping.** Or le dépôt `raw/` contient bel et bien 4 classes de Maïs (Corn) (cf. §2.1.2) et 2 classes de Tomate (`Tomato_mosaic_virus`, `Tomato_mosaic`) absentes de ce mapping. **Le fichier `leaf-map.json` racine n'est pas exhaustif** : il doit être complété par l'examen des structures `raw/` et des fichiers `leaf_grouping/` pour obtenir la liste définitive des classes.

#### 2.1.2 Classes Maïs (Corn) confirmées dans `raw/` (vérification du 2026-11-24)

Les trois sous-dossiers `raw/color`, `raw/grayscale` et `raw/segmented` contiennent chacun les 38 mêmes classes. Les classes de Maïs sont :

| Classe (nom du dossier) | Nombre d'images (compté via API GitHub, dossier `raw/color`) |
|-------------------------|-------------------------------------------------------------|
| `Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot` | 513 |
| `Corn_(maize)___Common_rust_` | 1000 |
| `Corn_(maize)___Northern_Leaf_Blight` | 985 |
| `Corn_(maize)___healthy` | 1000 |

**Le Maïs est donc présent dans PlantVillage.** Le comptage ci-dessus est limité au dossier `color/` (les autres formats comptent des versions dérivées des mêmes feuilles, pas de nouvelles feuilles). La valeur définitive « par classe entraînante » devra être dérivée du `leaf_grouping` (grouping anti-fuite), pas du simple comptage de fichiers.

#### 2.1.3 Absence de Manioc (Cassava) dans PlantVillage

Aucun dossier « Cassava » n'existe dans `raw/color`, `raw/grayscale` ni `raw/segmented`. **Le manioc n'est pas disponible dans PlantVillage.** La collecte camerounaise (ou une autre source) est requise pour toutes les classes du manioc.

---

### 2.2 PlantDoc

| Élément | Valeur observée | Méthode de vérification |
|---------|----------------|------------------------|
| URL du dépôt | https://github.com/pratikkayal/PlantDoc-Dataset (200 OK) | Page GitHub |
| Existence confirmée | ✅ Confirmé | Page GitHub (déposée à tort comme 404 dans les versions précédentes de cet inventaire ; la bonne URL est `pratikkayal`, non `mpatashnik`) |
| Statut | Public, 474 étoiles, 195 forks | Page GitHub |
| Nombre total d'images | 2,598 (déclaré dans le README) | README du dépôt |
| Nombre d'espèces de cultures | 13 (déclaré dans le README) | README du dépôt |
| Nombre de classes de maladies | Jusqu'à 17 (déclaré dans le README) | README du dépôt |
| Licence | **CC-BY-4.0** (confirmée par l'API GitHub) | Fichier `LICENSE.txt` du dépôt, confirmé par `GET /repos/pratikkayal/PlantDoc-Dataset → license.cc-by-4.0` |
| Papier scientifique | « PlantDoc: A Dataset for Visual Plant Disease Detection », CODS-COMAD 2020 (ACM) | README du dépôt |
| Arxiv | https://arxiv.org/abs/1911.10317 | README du dépôt |
| Structure | Dossiers `train/` (27 sous-dossiers) et `test/` (26 sous-dossiers) | API GitHub |

**Classes Tomate confirmées dans `train/` (9 classes) :**

| Classe PlantDoc | Type |
|-----------------|------|
| Tomato Early blight leaf | Maladie |
| Tomato Septoria leaf spot | Maladie |
| Tomato leaf bacterial spot | Maladie |
| Tomato leaf late blight | Maladie |
| Tomato leaf mosaic virus | Maladie |
| Tomato leaf yellow virus | Maladie |
| Tomato leaf | Plante saine |
| Tomato mold leaf | Maladie |
| Tomato two spotted spider mites leaf | Ravageur (acarien) |

**Classes Maïs confirmées dans `train/` (3 classes) :**

| Classe PlantDoc | Type |
|-----------------|------|
| Corn Gray leaf spot | Maladie |
| Corn leaf blight | Maladie |
| Corn rust leaf | Maladie |

**Le manioc est absent de PlantDoc** (aucun dossier « Cassava » ni « Manioc » dans `train/` ni `test/`).

---

### 2.3 CCMT

| Élément | Valeur observée | Méthode de vérification |
|---------|----------------|------------------------|
| Acronyme | « CCMT » mentionné dans l'issue #15 du dépôt AgriDoc | Mention dans un document interne |
| Nom complet présumé | « Cassava Cloud Monitoring Tool ou équivalent cassava-focused » | Hypothèse non vérifiée |
| Existence confirmée | ❌ Non | Aucune source primaire fiable localisée |
| Dépôt connu | Aucun | Non identifié |

---

## 3. Datasets Non Trouvés ou Non Accessibles

| Source | Raison de non-examen | Conséquence |
|--------|---------------------|-------------|
| CCMT | Source non identifiée, acronyme incertain | Exclue de la planification |
| Autres datasets agricoles | Non recherchés dans le cadre de cette mission | À identifier si nécessaire (cf. recommandation §5, priorité Moyenne) |

*PlantDoc a été confirmé accessible le 2026-11-24 (cf. §2.2) et n'est plus listé ici.*

---

## 4. Données Locales sur la Machine

### 4.1 Dossiers examinés

| Chemin | Résultat |
|--------|----------|
| `C:\Users\Wilfried\Documents\Agridoc\app\src\main\assets/` | Uniquement `.gitkeep` (55 octets) — aucun dataset, aucun modèle `.tflite`, aucun `labels.txt` |
| `C:\Users\Wilfried\Documents\AgriDoc-Collaboratif/` | Dossier vide |
| `C:\Users\Wilfried\Documents\GitHub\TP_CHAP1/` | Non examiné en détail (hors périmètre AgriDoc) |
| `C:\Users\Wilfried\Documents\` | Aucun fichier de dataset agricole identifié |

### 4.2 Conclusion

**Aucun dataset agricole n'est présent localement.** Aucun fichier d'image, aucune annotation, aucun modèle n'a été trouvé sur la machine dans le contexte du projet AgriDoc.

---

## 5. Limites de l'Inventaire

| Limite | Description |
|--------|-------------|
| Aucun téléchargement d'images effectué | Seuls les métadonnées (leaf-map.json, structures de dépôt via API GitHub) ont été consultées |
| Comptage d'images partiel pour PlantVillage | Compté via API GitHub sur le dossier `raw/color` uniquement (513 + 1 000 + 985 + 1 000 = 3 498 images de Maïs) ; le comptage définitif par feuille (pas par fichier) requiert le `leaf_grouping` de PlantVillage, qui sera établi lors du téléchargement réel |
| `leaf-map.json` incomplet | 31 classes dans ce mapping, mais 38 classes dans les dossiers `raw/` ; le mapping doit être complété avant entraînement |
| Licence PlantVillage non vérifiée | Aucune licence détectée dans le dépôt ; l'utilisation commerciale reste à confirmer auprès des auteurs (Mohanty et al., 2016) |
| PlantDoc comptage non réalisé | Le nombre d'images par classe dans PlantDoc n'a pas été compté (seule la liste des 27 dossiers de `train/` a été vérifiée) |
| Manioc absent des deux sources | La collecte camerounaise est la seule source possible pour les classes du manioc |

---

## 6. Recommandations pour la Suite

| Action | Priorité | Commentaire |
|--------|----------|-------------|
| Compléter l'examen de `leaf_grouping/` de PlantVillage pour le Maïs et la Tomate | Haute | Le comptage définitif par classe entraînante doit être dérivé du `leaf_grouping`, pas du simple comptage de fichiers |
| Vérifier la licence d'utilisation commerciale de PlantVillage | Haute | Bloquant pour la distribution de l'application ; aucune licence détectée dans le dépôt |
| Planifier la collecte camerounaise pour le manioc et les classes ravageurs/carences | Haute | Le manioc est absent de PlantVillage et de PlantDoc ; les ravageurs et carences sont absents des deux sources |
| Compléter le comptage d'images par classe de PlantDoc | Moyenne | Seule la liste des 27 dossiers de `train/` a été vérifiée ; le comptage définitif requiert le téléchargement |
| Identifier d'autres sources de données pour les classes manquantes | Moyenne | Si PlantVillage et PlantDoc ne couvrent pas suffisamment les besoins après comptage |
