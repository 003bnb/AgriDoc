# DATASET_SOURCE_VERIFICATION — Vérification des Sources de Données AgriDoc V1

**Version :** 1.0

**Note de version :** la version v1.0 de ce document est supersédée pour les informations actualisées. Les données à jour se trouvent dans `DATASET_AUDIT.md` v1.2 et `DATASET_INVENTORY.md` v1.2. Les sections historiques ci-dessous sont conservées pour la traçabilité.  
**Statut :** Vérification effectuée le 2026-11-22  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi)  

---

## 1. Objectif

Ce document récapitule les sources de données réellement consultées, les URL, les fichiers lus, les preuves observées et les limites identifiées. Aucune donnée n'a été téléchargée.

---

## 2. Sources Consultées

### 2.1 PlantVillage

| Élément | Valeur observée | Preuve |
|---------|----------------|--------|
| URL du dépôt | https://github.com/spMohanty/PlantVillage-Dataset | Page GitHub consultée (200 OK) |
| Statut | Public | Page GitHub |
| Nombre total d'images | 54,306 | README du dépôt |
| Nombre d'espèces de cultures | 14 | README du dépôt |
| Nombre de maladies | 26 | README du dépôt |
| Format des images | JPEG (raw/color, grayscale, segmented) | Arborescence du dépôt |
| Structure des annotations | Organisation par dossier (nom du dossier = classe) | Arborescence du dépôt |
| Fichier de mapping | `leaf-map.json` (ID fichier → classe) | Fichier consulté (25 117 lignes) |
| Licence | ❌ Non vérifiée clairement | Non spécifiée de manière explicite sur la page GitHub |
| Papier scientifique | Mohanty et al. (2016), Frontiers in Plant Science, DOI 10.3389/fpls.2016.01419 | README du dépôt |
| Hugging Face | https://huggingface.co/datasets/mohanty/PlantVillage | Lien dans le README |
| Splits train/test | 80/20, respectent le grouping par feuille (anti-fuite) | README du dépôt |

#### 2.1.1 Classes Tomate confirmées dans leaf-map.json

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

#### 2.1.2 Classes NON confirmées dans l'examen de leaf-map.json

| Élément | Statut | Commentaire |
|---------|--------|-------------|
| Manioc (Cassava) | **Non vérifié** | Le terme "Cassava" n'a pas été trouvé dans les parties du fichier leaf-map.json examinées |
| Maïs (Corn/Maize) | **Non vérifié** | Le terme "Corn" ou "Maize" n'a pas été trouvé dans les parties du fichier leaf-map.json examinées |
| Ravageurs (autres que Spider_mites sur Tomate) | **Non vérifié** | Aucune autre classe ravageur n'a été trouvée dans l'examen |
| Carences nutritionnelles | **Non vérifié** | Aucune classe carence n'a été trouvée dans l'examen |

---

### 2.2 PlantDoc

| Élément | Valeur observée | Preuve |
|---------|----------------|--------|
| URL du dépôt | https://github.com/pratikkayal/PlantDoc-Dataset | Page GitHub consultée (200 OK) |
| Statut | Public | Page GitHub (475 étoiles, 195 forks) |
| Nombre total d'images | 2,598 | README du dépôt |
| Nombre d'espèces de cultures | 13 | README du dépôt |
| Nombre de classes de maladies | Jusqu'à 17 | README du dépôt |
| Format des images | Non spécifié | Arborescence du dépôt |
| Structure des annotations | Organisation par dossier (nom du dossier = classe) | Dossiers `train/` et `test/` |
| Licence | **CC-BY-4.0** | Fichier `LICENSE.txt` lu intégralement ; déclaration dans README |
| Papier scientifique | "PlantDoc: A Dataset for Visual Plant Disease Detection", CODS-COMAD 2020 | README du dépôt |
| Arxiv | https://arxiv.org/abs/1911.10317 | README du dépôt |
| ACM | https://dl.acm.org/doi/10.1145/3371158.3371196 | README du dépôt |
| Auteurs | Davinder Singh, Naman Jain, Pranjali Jain, Pratik Kayal, Sudhakar Kumawat, Nipun Batra | README du dépôt |
| Structure | Dossiers `train/` et `test/` avec sous-dossiers par classe | Arborescence du dépôt |

#### 2.2.1 Classes Tomate confirmées dans PlantDoc (dossier `train/`)

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

#### 2.2.2 Classes Maïs confirmées dans PlantDoc (dossier `train/`)

| Classe PlantDoc | Type | Présent dans `test/` |
|-----------------|------|---------------------|
| Corn Gray leaf spot | Maladie | Oui |
| Corn leaf blight | Maladie | Oui |
| Corn rust leaf | Maladie | Oui |

#### 2.2.3 Classes d'autres cultures (hors périmètre V1) dans PlantDoc

| Classe PlantDoc | Culture | Type |
|-----------------|---------|------|
| Apple Scab Leaf | Pomme | Maladie |
| Apple leaf | Pomme | Plante saine |
| Apple rust leaf | Pomme | Maladie |
| Bell_pepper leaf spot | Poivron | Maladie |
| Bell_pepper leaf | Poivron | Plante saine |
| Blueberry leaf | Myrtille | Plante saine |
| Cherry leaf | Cerise | Plante saine |
| Peach leaf | Pêche | Plante saine |
| Potato leaf early blight | Pomme de terre | Maladie |
| Potato leaf late blight | Pomme de terre | Maladie |
| Raspberry leaf | Framboise | Plante saine |
| Soyabean leaf | Soja | Plante saine |
| Squash Powdery mildew leaf | Courge | Maladie |
| Strawberry leaf | Fraise | Plante saine |
| grape leaf black rot | Raisin | Maladie |
| grape leaf | Raisin | Plante saine |

#### 2.2.4 Absence de Manioc dans PlantDoc

Le manioc n'est **pas présent** dans PlantDoc (aucun dossier "Cassava" ou "Manioc" dans `train/` ni `test/`).

---

### 2.3 CCMT

| Élément | Valeur observée | Statut |
|---------|----------------|--------|
| Acronyme | "CCMT" mentionné dans l'issue #15 du dépôt AgriDoc | Incertain |
| Nom complet présumé | "Cassava Cloud Monitoring Tool ou équivalent cassava-focused" | Hypothèse non vérifiée |
| Existence confirmée | **Non** | Aucune source primaire fiable localisée |
| Dépôt connu | Aucun | Non identifié |

---

### 2.4 Collecte Camerounaise

| Élément | Statut |
|---------|--------|
| Images collectées | 0 |
| Référent agronomique | Non recruté |
| Budget | Non défini |
| Zones visées | Planifiées uniquement |

---

## 3. Synthèse des Sources Vérifiées

| Source | Existence confirmée | Manioc | Tomate | Maïs | Maladies | Ravageurs | Carences | Plante saine | Licence | Données dans le dépôt AgriDoc |
|--------|-------------------|--------|--------|------|----------|-----------|----------|--------------|---------|------------------------------|
| PlantVillage | ✅ Oui | ❌ Non confirmé | ✅ Confirmé | ❌ Non confirmé | ✅ Confirmé (Tomate) | ⚠️ Partiel (Spider_mites Tomate) | ❌ Non | ✅ Confirmé (Tomate) | ❌ Non vérifiée | ❌ Non |
| PlantDoc | ✅ Oui | ❌ Absent | ✅ Confirmé | ✅ Confirmé | ✅ Confirmé | ✅ Confirmé (Spider_mites Tomate, uniquement `train/`) | ❌ Non | ✅ Confirmé | ✅ CC-BY-4.0 | ❌ Non |
| CCMT | ❌ Non identifié | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Collecte camerounaise | ❌ Non commencée | Planifié | Planifié | Planifié | Planifié | Planifié | Planifié | Planifié | ❌ Non définie | ❌ Non |

---

## 4. Limites de la Vérification

| Limite | Description |
|--------|-------------|
| Aucun téléchargement effectué | Les datasets publics n'ont pas été téléchargés (taille, licences non toutes vérifiées) |
| Aucun comptage d'images par classe | Le nombre d'images par classe spécifique n'a pas pu être déterminé |
| Examen partiel de leaf-map.json | Le fichier contient 25 117 lignes ; seules certaines parties ont été parcourues |
| Licence PlantVillage non vérifiée | La licence d'utilisation commerciale de PlantVillage n'a pas été confirmée |
| PlantDoc classes non comptées | Le nombre d'images par classe dans PlantDoc n'a pas pu être déterminé (pas de téléchargement) |
| Manioc dans PlantVillage non confirmé | L'absence de "Cassava" dans les parties examinées ne prouve pas l'absence totale dans le dataset |

---

## 5. Fichiers Consultés

| Source | Fichier | URL | Contenu extrait |
|--------|---------|-----|-----------------|
| PlantVillage | README.md | https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/README.md | 54,306 images, 14 espèces, 26 maladies, DOI, licence à vérifier |
| PlantVillage | leaf-map.json | https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/leaf-map.json | Mapping ID fichier → classe, classes Tomate confirmées |
| PlantVillage | Page GitHub | https://github.com/spMohanty/PlantVillage-Dataset | 1.0k étoiles, 770 forks, structure des dossiers |
| PlantDoc | README.md | https://raw.githubusercontent.com/pratikkayal/PlantDoc-Dataset/master/README.md | 2,598 images, 13 espèces, jusqu'à 17 classes, CC-BY-4.0, auteurs, papier CODS-COMAD 2020 |
| PlantDoc | LICENSE.txt | https://raw.githubusercontent.com/pratikkayal/PlantDoc-Dataset/master/LICENSE.txt | Texte complet de la licence CC-BY-4.0 |
| PlantDoc | Dossier `train/` | https://github.com/pratikkayal/PlantDoc-Dataset/tree/master/train | 27 classes de dossiers, dont 9 Tomate, 3 Maïs |
| PlantDoc | Dossier `test/` | https://github.com/pratikkayal/PlantDoc-Dataset/tree/master/test | 26 classes de dossiers, dont 8 Tomate, 3 Maïs |

---

## 6. Conclusion

**Deux sources publiques sont maintenant confirmées comme réelles et accessibles :** PlantVillage et PlantDoc. PlantDoc apporte notamment des classes Maïs (3) et Tomate (9 dans `train/`, 8 dans `test/`) qui n'étaient pas confirmées dans mon audit précédent. Le manioc n'est présent dans aucune des deux sources vérifiées.

**Aucune donnée n'a été téléchargée.** Aucun comptage d'images par classe n'a été effectué. Les licences d'utilisation commerciale restent à vérifier pour PlantVillage (PlantDoc est sous CC-BY-4.0, ce qui autorise la réutilisation commerciale avec attribution).
