# DATASET_AUDIT — Audit Réel des Sources de Données AgriDoc V1

**Version :** 1.2  
**Statut :** Audit partiellement réalisé (sources publiques examinées, aucun dataset téléchargé)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi)  
**Dernière révision :** 2026-11-24 (correction PlantDoc et confirmation Maïs dans PlantVillage)

---

## 1. Objectif et Méthode

Cet audit recense les sources de données candidates pour l'entraînement du modèle AgriDoc V1 (Manioc, Tomate, Maïs). **Aucune donnée n'a été téléchargée, aucun fichier d'annotation n'a été ouvert, aucun compte d'images n'a été vérifié directement sur les fichiers bruts.** Les informations ci-dessous sont basées sur l'examen direct des dépôts GitHub et des pages Hugging Face accessibles.

---

## 2. PlantVillage — Vérifié (Existence confirmée)

### 2.1 Informations vérifiées

| Élément | Valeur observée | Source de vérification |
|---------|----------------|------------------------|
| Dépôt GitHub | https://github.com/spMohanty/PlantVillage-Dataset | Page GitHub consultée (200 OK) |
| Statut | Public, 1.0k étoiles, 770 forks | Page GitHub |
| Nombre total d'images | 54,306 | README du dépôt |
| Nombre d'espèces de cultures | 14 | README du dépôt |
| Nombre de maladies | 26 | README du dépôt |
| Format des images | JPEG (raw/color, grayscale, segmented) | Structure du dépôt (dossiers raw/) |
| Structure des annotations | Organisation par dossier (nom du dossier = classe) | Structure du dépôt |
| Fichier de mapping | leaf-map.json (ID fichier → classe) | Fichier consulté dans le dépôt |
| Licence | À vérifier (papier Frontiers in Plant Science, DOI 10.3389/fpls.2016.01419) | Citation dans le README |
| Papier scientifique | Mohanty et al. (2016), Frontiers in Plant Science | README du dépôt |
| Hugging Face | https://huggingface.co/datasets/mohanty/PlantVillage | Lien dans le README |
| Splits train/test | 80/20, respectent le grouping par feuille (anti-fuite) | README du dépôt |

### 2.2 Classes Tomate confirmées dans leaf-map.json

Les classes suivantes ont été **visuellement confirmées** dans le fichier `leaf-map.json` du dépôt PlantVillage :

| ID de classe PlantVillage | Libellé complet | Type |
|--------------------------|-----------------|------|
| Tomato___Bacterial_spot | Tache bactérienne de la tomate | Maladie |
| Tomato___Early_blight | Alternariose de la tomate | Maladie |
| Tomato___Late_blight | Mildiou de la tomate | Maladie |
| Tomato___Leaf_Mold | Moisiure foliaire de la tomate | Maladie |
| Tomato___Septoria_leaf_spot | Tache de Septoria de la tomate | Maladie |
| Tomato___Target_Spot | Tache cible de la tomate | Maladie |
| Tomato___Tomato_Yellow_Leaf_Curl_Virus | Virus de l'enroulement jaune de la tomate | Maladie |
| Tomato___Spider_mites Two-spotted_spider_mite | Acarien rouge (Tétranyque tisserand) | Ravageur |
| Tomato___healthy | Tomate saine | Plante saine |

### 2.3 Classes NON confirmées ou absentes dans l'examen réalisé

| Élément | Statut | Commentaire |
|---------|--------|-------------|
| Manioc (Cassava) | **❌ Absent** | Aucun dossier « Cassava » dans `raw/color`, `raw/grayscale` ni `raw/segmented` (vérification complète du 2026-11-24). La collecte camerounaise est la seule source possible. |
| Maïs (Corn/Maize) | **✅ Confirmé dans `raw/`** | 4 classes présentes dans les 3 dossiers `raw/` (color, grayscale, segmented) : `Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot` (513), `Corn_(maize)___Common_rust_` (1000), `Corn_(maize)___Northern_Leaf_Blight` (985), `Corn_(maize)___healthy` (1000). **Absentes de `leaf-map.json`** (mapping incomplet, cf. §2.1) : le comptage définitif par feuille devra être établi via le `leaf_grouping` lors du téléchargement. |
| Ravageurs (autres que Spider_mites sur Tomate) | **Non vérifié** | Aucune autre classe ravageur n'a été trouvée dans l'examen. |
| Carences nutritionnelles | **Non vérifié** | Aucune classe carence n'a été trouvée dans l'examen. |

### 2.4 Limites identifiées pour AgriDoc V1

| Limite | Impact sur le périmètre V1 |
|--------|---------------------------|
| Peu ou pas de catégories "ravageurs" (insectes visibles) | Les classes RAVAGEUR et DEGAT_RAVAGEUR ne peuvent pas être couvertes par PlantVillage (sauf Spider_mites sur Tomate, confirmé) |
| Peu ou pas de catégories "carences nutritionnelles" | Les classes CARENCE ne peuvent pas être couvertes par PlantVillage |
| Images principalement en serre/conditions contrôlées | Biais de domaine par rapport aux conditions réelles camerounaises |
| Risque de doublons avec d'autres datasets publics | Déduplication nécessaire avant entraînement |
| Manioc et Maïs non confirmés dans cet examen (note historique) | Au moment de cet examen, la couverture de ces deux cultures cibles par PlantVillage restait à prouver. Le Maïs a ensuite été confirmé dans `raw/` lors de la vérification du 2026-11-24 ; le manioc reste absent des sources publiques vérifiées. |

### 2.5 Licence

La licence exacte d'utilisation commerciale n'a pas pu être vérifiée à partir du README du dépôt. Le papier scientifique est publié sous DOI 10.3389/fpls.2016.01419 (Frontiers in Plant Science, accès ouvert). La licence de réutilisation des images pour une application mobile distribuée doit être confirmée auprès des auteurs.

---

## 3. PlantDoc — Confirmé accessible (vérification du 2026-11-24)

> **Note de correction :** La version 1.0 de cet audit listait PlantDoc comme « Non trouvé (404) ». La vérification du 2026-11-24 a confirmé que le dépôt existe bel et bien à l'URL `https://github.com/pratikkayal/PlantDoc-Dataset` (200 OK, CC-BY-4.0). L'erreur de la version 1.0 provenait d'un test avec l'URL incorrecte `mpatashnik/PlantDoc-Dataset` (cf. DATASET_INVENTORY.md v1.0).

### 3.1 Résultat de la vérification

| Élément | Valeur observée | Statut |
|---------|----------------|--------|
| URL du dépôt | https://github.com/pratikkayal/PlantDoc-Dataset | Page GitHub consultée (200 OK) |
| Statut | Public (475 étoiles, 195 forks) | Page GitHub |
| Nombre total d'images | 2,598 | README du dépôt |
| Nombre d'espèces de cultures | 13 | README du dépôt |
| Nombre de classes de maladies | Jusqu'à 17 | README du dépôt |
| Licence | **CC-BY-4.0** | Fichier `LICENSE.txt` lu intégralement |
| Papier scientifique | "PlantDoc: A Dataset for Visual Plant Disease Detection", CODS-COMAD 2020 | README du dépôt |

### 3.2 Classes Tomate confirmées dans PlantDoc (dossier `train/`)

Les classes suivantes ont été **visuellement confirmées** dans le dossier `train/` de PlantDoc :

| Classe PlantDoc | Type | Présent dans `test/` |
|-----------------|------|---------------------|
| Tomato Early blight leaf | Maladie | Oui |
| Tomato Septoria leaf spot | Maladie | Oui |
| Tomato leaf bacterial spot | Maladie | Oui |
| Tomato leaf late blight | Maladie | Oui |
| Tomato leaf mosaic virus | Maladie | Oui |
| Tomato leaf yellow virus | Maladie | Oui |
| Tomato leaf | Plante saine | Oui |
| Tomato mold leaf | Maladie | Oui |
| Tomato two spotted spider mites leaf | Ravageur (acarien) | **Non** (uniquement dans `train/`)

### 3.3 Classes Maïs confirmées dans PlantDoc (dossier `train/`)

| Classe PlantDoc | Type | Présent dans `test/` |
|-----------------|------|---------------------|
| Corn Gray leaf spot | Maladie | Oui |
| Corn leaf blight | Maladie | Oui |
| Corn rust leaf | Maladie | Oui |

### 3.4 Absence de Manioc dans PlantDoc

Le manioc n'est **pas présent** dans PlantDoc (aucun dossier "Cassava" ou "Manioc" dans `train/` ni `test/`).

### 3.5 Conséquence

PlantDoc est une source réelle et accessible pour AgriDoc V1. Elle couvre Tomate (9 classes dans `train/`, 8 dans `test/`) et Maïs (3 classes). Elle ne couvre pas le Manioc. La licence CC-BY-4.0 autorise la réutilisation commerciale avec attribution.

---

## 4. CCMT — Source non identifiée

### 4.1 Résultat de la vérification

| Élément | Valeur observée | Statut |
|---------|----------------|--------|
| Acronyme | "CCMT" mentionné dans l'issue #15 | **Incertain — non clairement identifié** |
| Nom complet | "Cassava Cloud Monitoring Tool ou équivalent cassava-focused" | Hypothèse non vérifiée |
| Dépôt connu | Aucun | Aucune source primaire fiable localisée |
| Existence confirmée | **Non** | L'existence même de ce dataset sous ce nom n'est pas prouvée |

### 4.2 Conséquence

CCMT ne peut pas être considéré comme une source de données pour AgriDoc V1. Cette source est exclue de la planification actuelle.

---

## 5. Collecte Camerounaise — Non commencée

| Élément | Statut | Commentaire |
|---------|--------|-------------|
| Images collectées | 0 | Aucune image n'a été collectée |
| Référent agronomique | Non recruté | Validation des labels impossible actuellement |
| Budget | Non défini | Planning incertain |
| Zones visées | Planifiées (Sud/Centre/Est, Ouest/Nord-Ouest, Extrême-Nord) | Non exécuté |

---

## 6. Synthèse des Limites par Source

| Source | Existence confirmée | Manioc | Tomate | Maïs | Maladies | Ravageurs | Carences | Plante saine | Licence vérifiée ? | Données dans le dépôt ? |
|--------|-------------------|--------|--------|------|----------|-----------|----------|--------------|-------------------|------------------------|
| PlantVillage | ✅ Oui | ❌ Absent (vérifié 2026-11-24) | ✅ Confirmé | ✅ Confirmé (4 classes, cf. §2.3) | ✅ Confirmé (Tomate + Maïs) | ⚠️ Partiel (Spider_mites Tomate) | ❌ Non | ✅ Confirmé (Tomate + Maïs) | ❌ Non | ❌ Non |
| PlantDoc | ✅ Oui (vérifié 2026-11-24) | ❌ Absent | ✅ Confirmé (9 classes train) | ✅ Confirmé (3 classes train) | ✅ Confirmé | ✅ Confirmé (Spider_mites Tomate) | ❌ Non | ✅ Confirmé | ✅ CC-BY-4.0 (confirmée par l'API GitHub) | ❌ Non |
| CCMT | ❌ Non identifié | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Collecte camerounaise | ❌ Non commencée | Planifié | Planifié | Planifié | Planifié | Planifié | Planifié | Planifié | ❌ Non définie | ❌ Non |

---

## 7. Risques de Doublons et Fuites

| Risque | Description | Mesure d'atténuation |
|--------|-------------|---------------------|
| Doublons entre sources publiques | Certaines images peuvent apparaître dans plusieurs datasets publics | Hachage perceptuel (pHash) avant fusion |
| Fuites train/validation/test | Variantes d'une même plante réparties sur plusieurs ensembles | Séparation par plante/parcelle, pas par image individuelle |
| Biais de domaine | Images de serre vs conditions réelles camerounaises | Sur-représentation des images camerounaises dans le test |

---

## 8. Conclusion de l'Audit

**Deux sources publiques sont confirmées réelles et accessibles :** PlantVillage et PlantDoc. PlantVillage couvre la Tomate et le Maïs (4 classes, vérifié le 2026-11-24), mais pas le Manioc. PlantDoc couvre la Tomate (9 classes dans `train/`) et le Maïs (3 classes dans `train/`) sous licence CC-BY-4.0, mais pas le Manioc. CCMT n'a pas pu être identifié. Aucune donnée n'a été téléchargée.

**Recommandation :** Avant tout entraînement, il est nécessaire de :
1. Compléter le comptage d'images par classe de PlantVillage (Maïs et Tomate) et de PlantDoc via le téléchargement et le `leaf_grouping`
2. Confirmer la licence d'utilisation commerciale de PlantVillage (aucune licence détectée dans le dépôt ; PlantDoc est sous CC-BY-4.0, ce qui autorise la réutilisation commerciale avec attribution)
3. Prévoir une collecte camerounaise pour le Manioc et les classes ravageurs et carences, qui sont absentes de toutes les sources publiques vérifiées
