# CLASS_FEASIBILITY_MATRIX — Matrice de Faisabilité des Classes AgriDoc V1

**Version :** 1.2  
**Statut :** Révision basée sur l'audit réel des sources (PlantVillage et PlantDoc confirmés accessibles, CCMT non identifié ; Maïs confirmé dans PlantVillage le 2026-11-24)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi)  
**Dernière révision :** 2026-11-24

---

## 1. Objectif et Statuts

Cette matrice recense chaque classe candidate pour l'entraînement du modèle V1 et évalue sa faisabilité réelle en fonction des données **réellement examinées**.

**Statuts utilisés :**

| Statut | Signification |
|--------|---------------|
| **1. VALIDÉE POUR EXPÉRIMENTATION** | Classe dont la présence a été confirmée dans une source accessible (PlantVillage leaf-map.json examiné). Ne signifie pas que la classe est prête pour la production, seulement qu'elle peut entrer dans un premier entraînement après vérification du nombre d'images. |
| **2. DONNÉES INSUFFISANTES** | Classe dont la source est identifiée mais dont le nombre d'images n'a pas pu être vérifié (pas de téléchargement, pas de comptage). |
| **3. COLLECTE LOCALE OBLIGATOIRE** | Classe absente des sources publiques vérifiées ; nécessite une collecte terrain au Cameroun avec référent agronomique. |
| **4. CLASSE À REDÉFINIR** | Classe dont la définition est trop ambiguë (ravageur sans espèce, carence sans nutriment) pour une classification fiable. |
| **5. EXCLUE DE V1** | Classe incompatible avec le périmètre V1 (culture hors V1, symptôme non foliaire, etc.) |

---

## 2. Nomenclature et Statut par Classe

### 2.1 Manioc (Manihot esculenta)

| ID Classe | Culture | Catégorie | Nom de la classe | Description agronomique | Source de données identifiée | Nombre d'images vérifiées | Qualité des annotations | Compatibilité photos acceptées | Risques de confusion | Besoin de collecte camerounaise | Statut final recommandé |
|-----------|---------|-----------|------------------|------------------------|------------------------------|--------------------------|------------------------|-------------------------------|----------------------|-------------------------------|------------------------|
| MANIOC_SAIN | Manioc | Plante saine | Feuille sans symptôme visible | Feuille de manioc sans aucun symptôme visible | Aucune source publique vérifiée (PlantVillage : absent, PlantDoc : absent) | Non vérifié | N/A | Oui (feuille) | Confusion avec feuilles jeunes ou carences légères | **Obligatoire** (validation conditions camerounaises) | 3. COLLECTE LOCALE OBLIGATOIRE |
| MANIOC_MALADIE_MOSAIQUE | Manioc | Maladie | Mosaïque du manioc (Cassava Mosaic Virus) | Marbrures vert clair/foncé sur la feuille, déformation | Aucune source publique vérifiée (PlantVillage : absent, PlantDoc : absent) | Non vérifié | N/A | Oui (feuille) | Confusion avec carences ou dommages mécaniques | **Obligatoire** (validation agronomique locale) | 3. COLLECTE LOCALE OBLIGATOIRE |
| MANIOC_MALADIE_BRUNISSEMENT | Manioc | Maladie | Brunissement du manioc (CBSD) | Symptômes principalement sur les racines, nécroses foliaires possibles | CCMT (non identifié) | Non vérifié | N/A | **Partielle** (symptômes foliaires limités) | Confusion avec autres nécroses foliaires | Oui | 5. EXCLUE DE V1 |
| MANIOC_CARENCE | Manioc | Carence | Carence nutritionnelle (nutriment non spécifié) | Jaunissement, nécrose, décoloration selon le nutriment | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Confusion avec maladies ou stress hydrique | **Obligatoire** (nutriment à préciser avec agronome) | 3. COLLECTE LOCALE OBLIGATOIRE |
| MANIOC_RAVAGEUR | Manioc | Ravageur | Insecte visible sur la feuille (espèce non spécifiée) | Insecte suffisamment visible pour identification | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Confusion entre espèces de ravageurs | **Obligatoire** (espèce à préciser) | 3. COLLECTE LOCALE OBLIGATOIRE |
| MANIOC_DEGAT_RAVAGEUR | Manioc | Dégât ravageur | Trous, déformations visibles sur la feuille | Dégâts de mastication, galeries, déformations | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Dégâts non spécifiques, risque de confusion avec maladies | **Obligatoire** (type de dégât à préciser) | 3. COLLECTE LOCALE OBLIGATOIRE |
| MANIOC_INCONNU | Manioc | Inconnu | Image non exploitable ou hors domaine | Image sans partie identifiable de plante de manioc | À générer (images négatives) | Non vérifié | N/A | N/A | N/A | Oui | 2. DONNÉES INSUFFISANTES |

### 2.2 Tomate (Solanum lycopersicum)

| ID Classe | Culture | Catégorie | Nom de la classe | Description agronomique | Source de données identifiée | Nombre d'images vérifiées | Qualité des annotations | Compatibilité photos acceptées | Risques de confusion | Besoin de collecte camerounaise | Statut final recommandé |
|-----------|---------|-----------|------------------|------------------------|------------------------------|--------------------------|------------------------|-------------------------------|----------------------|-------------------------------|------------------------|
| TOMATE_SAIN | Tomate | Plante saine | Feuille sans symptôme visible | Feuille de tomate sans aucun symptôme visible | PlantVillage (confirmé dans leaf-map.json) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec feuilles jeunes | Oui (validation conditions camerounaises) | 2. DONNÉES INSUFFISANTES |
| TOMATE_MALADIE_MILDIEU | Tomate | Maladie | Mildiou (Phytophthora infestans) | Taches foliaires nécrotiques, duvet blanchâtre sous la feuille | PlantVillage (confirmé : Tomato___Late_blight) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec brûlure bactérienne | Oui (validation agronomique locale) | 2. DONNÉES INSUFFISANTES |
| TOMATE_MALADIE_TACHE_BACTERIENNE | Tomate | Maladie | Tache bactérienne (Xanthomonas) | Taches nécrotiques avec auréole jaune | PlantVillage (confirmé : Tomato___Bacterial_spot) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec mildiou ou tache fongique | Oui (validation agronomique locale) | 2. DONNÉES INSUFFISANTES |
| TOMATE_MALADIE_SEPTORIA | Tomate | Maladie | Tache de Septoria | Taches circulaires brunes avec centre grisâtre | PlantVillage (confirmé : Tomato___Septoria_leaf_spot) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec autres taches foliaires | Oui (validation agronomique locale) | 2. DONNÉES INSUFFISANTES |
| TOMATE_MALADIE_YELLOW_LEAF_CURL | Tomate | Maladie | Virus de l'enroulement jaune (TYLCV) | Enroulement des feuilles, jaunissement, nainisme | PlantVillage (confirmé : Tomato___Tomato_Yellow_Leaf_Curl_Virus) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec carences ou stress hydrique | Oui (validation agronomique locale) | 2. DONNÉES INSUFFISANTES |
| TOMATE_MALADIE_LEAF_MOLD | Tomate | Maladie | Moisissure foliaire (Fulvia fulva) | Taches jaunâtres dessus, spores olive dessous | PlantVillage (confirmé : Tomato___Leaf_Mold) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec autres moisissures | Oui (validation agronomique locale) | 2. DONNÉES INSUFFISANTES |
| TOMATE_MALADIE_TARGET_SPOT | Tomate | Maladie | Tache cible (Corynespora) | Taches concentriques avec anneaux | PlantVillage (confirmé : Tomato___Target_Spot) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec autres taches foliaires | Oui (validation agronomique locale) | 2. DONNÉES INSUFFISANTES |
| TOMATE_MALADIE_EARLY_BLIGHT | Tomate | Maladie | Alternariose (Alternaria solani) | Taches concentriques en cible sur feuilles âgées | PlantVillage (confirmé : Tomato___Early_blight) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec tache cible | Oui (validation agronomique locale) | 2. DONNÉES INSUFFISANTES |
| TOMATE_RAVAGEUR_SPIDER_MITE | Tomate | Ravageur | Acarien rouge (Tétranyque tisserand) | Acarien visible, toiles, jaunissement bronzé | PlantVillage (confirmé : Tomato___Spider_mites) | Non vérifié | À vérifier | Oui (feuille) | Confusion avec autres acariens ou carences | Oui (validation agronomique locale) | 2. DONNÉES INSUFFISANTES |
| TOMATE_RAVAGEUR | Tomate | Ravageur | Autre insecte visible (espèce non spécifiée) | Insecte autre que l'acarien, suffisamment visible | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Confusion entre espèces | **Obligatoire** (espèce à préciser) | 3. COLLECTE LOCALE OBLIGATOIRE |
| TOMATE_DEGAT_RAVAGEUR | Tomate | Dégât ravageur | Trous, déformations visibles | Dégâts de mastication, galeries | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Dégâts non spécifiques | **Obligatoire** (type à préciser) | 3. COLLECTE LOCALE OBLIGATOIRE |
| TOMATE_CARENCE | Tomate | Carence | Carence nutritionnelle (nutriment non spécifié) | Jaunissement, nécrose selon le nutriment | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Confusion avec maladies | **Obligatoire** (nutriment à préciser) | 3. COLLECTE LOCALE OBLIGATOIRE |
| TOMATE_INCONNU | Tomate | Inconnu | Image non exploitable ou hors domaine | Image sans partie identifiable de plante de tomate | À générer (images négatives) | Non vérifié | N/A | N/A | N/A | Oui | 2. DONNÉES INSUFFISANTES |

### 2.3 Maïs (Zea mays)

| ID Classe | Culture | Catégorie | Nom de la classe | Description agronomique | Source de données identifiée | Nombre d'images vérifiées | Qualité des annotations | Compatibilité photos acceptées | Risques de confusion | Besoin de collecte camerounaise | Statut final recommandé |
|-----------|---------|-----------|------------------|------------------------|------------------------------|--------------------------|------------------------|-------------------------------|----------------------|-------------------------------|------------------------|
| MAIS_SAIN | Maïs | Plante saine | Feuille sans symptôme visible | Feuille de maïs sans aucun symptôme visible | PlantVillage (confirmé : `Corn_(maize)___healthy`, 1000 images dans `raw/color`) + PlantDoc (`Corn leaf`, saine) | 1000 (fichiers, `raw/color`) | À vérifier | Oui (feuille) | Confusion avec feuilles jeunes | Oui (validation conditions camerounaises) | 1. VALIDÉE POUR EXPÉRIMENTATION |
| MAIS_MALADIE_ROUILLE | Maïs | Maladie | Rouille du maïs | Pustules orange-brun sur la feuille | PlantVillage (confirmé : `Corn_(maize)___Common_rust_`, 1000 images dans `raw/color`) + PlantDoc (`Corn rust leaf`) | 1000 (fichiers, `raw/color`) | À vérifier | Oui (feuille) | Confusion avec autres pustules | Oui | 1. VALIDÉE POUR EXPÉRIMENTATION |
| MAIS_MALADIE_TACHE_NORD | Maïs | Maladie | Tache foliaire du nord (Northern Leaf Blight) | Taches longues, nécroses, couleurs brunes | PlantVillage (confirmé : `Corn_(maize)___Northern_Leaf_Blight`, 985 images dans `raw/color`) + PlantDoc (`Corn leaf blight`) | 985 (fichiers, `raw/color`) | À vérifier | Oui (feuille) | Confusion avec autres taches | Oui | 1. VALIDÉE POUR EXPÉRIMENTATION |
| MAIS_RAVAGEUR | Maïs | Ravageur | Insecte visible sur la feuille (espèce non spécifiée) | Insecte suffisamment visible | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Confusion entre espèces | **Obligatoire** | 3. COLLECTE LOCALE OBLIGATOIRE |
| MAIS_DEGAT_RAVAGEUR | Maïs | Dégât ravageur | Trous, galeries visibles | Dégâts de mastication, galeries foliaires | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Dégâts non spécifiques | **Obligatoire** | 3. COLLECTE LOCALE OBLIGATOIRE |
| MAIS_CARENCE | Maïs | Carence | Carence nutritionnelle (nutriment non spécifié) | Jaunissement, nécrose selon le nutriment | Aucune source publique identifiée | Non vérifié | N/A | Oui (feuille) | Confusion avec maladies | **Obligatoire** | 3. COLLECTE LOCALE OBLIGATOIRE |
| MAIS_INCONNU | Maïs | Inconnu | Image non exploitable ou hors domaine | Image sans partie identifiable de plante de maïs | À générer (images négatives) | Non vérifié | N/A | N/A | N/A | Oui | 2. DONNÉES INSUFFISANTES |

### 2.4 Classes globales (hors culture spécifique)

| ID Classe | Culture | Catégorie | Nom de la classe | Description agronomique | Source de données identifiée | Nombre d'images vérifiées | Qualité des annotations | Compatibilité photos acceptées | Risques de confusion | Besoin de collecte camerounaise | Statut final recommandé |
|-----------|---------|-----------|------------------|------------------------|------------------------------|--------------------------|------------------------|-------------------------------|----------------------|-------------------------------|------------------------|
| GLOBAL_INCONNU | Global | Inconnu | Image sans partie identifiable de plante | Main, ciel, sol, objet non végétal | À générer (images négatives) | Non vérifié | N/A | N/A | Confusion avec feuillage non ciblé | Oui | 2. DONNÉES INSUFFISANTES |
| GLOBAL_NON_EXPLOITABLE | Global | Inconnu | Image floue, sous-exposée, surexposée | Image techniquement inutilisable | À générer (images négatives) | Non vérifié | N/A | N/A | N/A | Oui | 2. DONNÉES INSUFFISANTES |

---

## 3. Synthèse des Statuts

| Statut | Nombre de classes | Classes concernées | Action requise |
|--------|------------------|--------------------|----------------|
| **1. VALIDÉE POUR EXPÉRIMENTATION** | 3 | MAIS_SAIN, MAIS_MALADIE_ROUILLE, MAIS_MALADIE_TACHE_NORD (confirmées dans PlantVillage `raw/` le 2026-11-24, cf. §2.3 et §4.1) | Télécharger et valider le comptage définitif via le `leaf_grouping` de PlantVillage avant entraînement |
| **2. DONNÉES INSUFFISANTES** | 14 | MANIOC_INCONNU ; les classes Tomate confirmées dans PlantVillage/PlantDoc mais dont le comptage par feuille n'est pas finalisé (TOMATE_SAIN, TOMATE_MALADIE_MILDIEU, TOMATE_MALADIE_TACHE_BACTERIENNE, TOMATE_MALADIE_SEPTORIA, TOMATE_MALADIE_YELLOW_LEAF_CURL, TOMATE_MALADIE_LEAF_MOLD, TOMATE_MALADIE_TARGET_SPOT, TOMATE_MALADIE_EARLY_BLIGHT, TOMATE_RAVAGEUR_SPIDER_MITE, TOMATE_INCONNU) ; MAIS_INCONNU ; GLOBAL_INCONNU ; GLOBAL_NON_EXPLOITABLE | Télécharger, compter et valider les images dans PlantVillage et PlantDoc |
| **3. COLLECTE LOCALE OBLIGATOIRE** | 11 | MANIOC_SAIN, MANIOC_MALADIE_MOSAIQUE, MANIOC_CARENCE, MANIOC_RAVAGEUR, MANIOC_DEGAT_RAVAGEUR, TOMATE_RAVAGEUR, TOMATE_DEGAT_RAVAGEUR, TOMATE_CARENCE, MAIS_RAVAGEUR, MAIS_DEGAT_RAVAGEUR, MAIS_CARENCE | Collecte terrain obligatoire avec référent agronomique (le manioc est absent de toutes les sources publiques vérifiées ; les ravageurs et carences ne sont pas documentés) |
| **4. CLASSE À REDÉFINIR** | 0 | — | Aucune classe ambiguë n'est conservée sans redéfinition ou exclusion |
| **5. EXCLUE DE V1** | 1 | MANIOC_MALADIE_BRUNISSEMENT (CBSD) | Symptômes principalement racinaires, incompatibles avec le périmètre photo-feuille |

**Total des classes répertoriées :** 29  
**Classes validées pour expérimentation (Maïs, cf. §4.1) :** 3  
**Classes avec données insuffisantes ou à vérifier :** 14  
**Classes nécessitant collecte locale obligatoire :** 11  
**Classes exclues de V1 :** 1  
*Note : les comptages d'images sont préliminaires (comptage de fichiers dans `raw/color` pour PlantVillage). Le comptage définitif par feuille/plante doit être établi via le `leaf_grouping` de PlantVillage avant tout entraînement.*

---

## 4. Classes validées pour expérimentation et classes candidates (relecture le 2026-11-24)

### 4.1 Classes Maïs — validées pour expérimentation (3 classes)

La présence des classes Maïs dans PlantVillage a été **confirmée le 2026-11-24** dans le dossier `raw/` (color, grayscale, segmented) :

| Classe AgriDoc | Classe PlantVillage | Nombre d'images (`raw/color`) | Condition de validation finale |
|----------------|---------------------|-------------------------------|-------------------------------|
| MAIS_SAIN | `Corn_(maize)___healthy` | 1000 | Comptage définitif via le `leaf_grouping` de PlantVillage (grouping anti-fuite par feuille) |
| MAIS_MALADIE_ROUILLE | `Corn_(maize)___Common_rust_` | 1000 | Idem |
| MAIS_MALADIE_TACHE_NORD | `Corn_(maize)___Northern_Leaf_Blight` | 985 | Idem |

*Ces classes sont disponibles en complément sous licence CC-BY-4.0 dans PlantDoc (`Corn leaf`, `Corn rust leaf`, `Corn leaf blight`).*

### 4.2 Classes Tomate — candidates (comptage non finalisé)

Les classes Tomate restent candidates car le comptage d'images par classe n'a pas encore été effectué (les classes sont confirmées présentes dans `leaf-map.json` et dans `raw/`, mais le nombre d'images par classe n'a pas été établi définitivement) :

| Classe candidate | Raison de probabilité | Condition de vérification |
|-----------------|----------------------|--------------------------|
| TOMATE_SAIN | Confirmé dans `leaf-map.json` et `raw/color` | Télécharger et compter les images |
| TOMATE_MALADIE_MILDIEU | Confirmé dans `leaf-map.json` et `raw/color` (`Tomato___Late_blight`) | Télécharger et compter les images |
| TOMATE_MALADIE_TACHE_BACTERIENNE | Confirmé dans `leaf-map.json` et `raw/color` (`Tomato___Bacterial_spot`) | Télécharger et compter les images |
| TOMATE_MALADIE_SEPTORIA | Confirmé dans `leaf-map.json` et `raw/color` (`Tomato___Septoria_leaf_spot`) | Télécharger et compter les images |
| TOMATE_MALADIE_YELLOW_LEAF_CURL | Confirmé dans `leaf-map.json` et `raw/color` | Télécharger et compter les images |
| TOMATE_MALADIE_LEAF_MOLD | Confirmé dans `leaf-map.json` et `raw/color` (`Tomato___Leaf_Mold`) | Télécharger et compter les images |
| TOMATE_MALADIE_TARGET_SPOT | Confirmé dans `leaf-map.json` et `raw/color` (`Tomato___Target_Spot`) | Télécharger et compter les images |
| TOMATE_MALADIE_EARLY_BLIGHT | Confirmé dans `leaf-map.json` et `raw/color` (`Tomato___Early_blight`) | Télécharger et compter les images |
| TOMATE_RAVAGEUR_SPIDER_MITE | Confirmé dans `leaf-map.json` et `raw/color` (`Tomato___Spider_mites`) | Télécharger et compter les images |

*Plusieurs de ces classes sont aussi disponibles sous licence CC-BY-4.0 dans PlantDoc (cf. DATASET_INVENTORY.md §2.2).*

### 4.3 Classes Manioc — aucune source publique disponible

**Le manioc est absent de PlantVillage et de PlantDoc** (vérification complète du 2026-11-24 : aucun dossier « Cassava » dans les trois dossiers `raw/` de PlantVillage, ni dans `train/`/`test/` de PlantDoc). Toutes les classes du manioc (MANIOC_SAIN, MANIOC_MALADIE_MOSAIQUE, MANIOC_CARENCE, MANIOC_RAVAGEUR, MANIOC_DEGAT_RAVAGEUR, MANIOC_INCONNU) nécessitent une **collecte locale camerounaise obligatoire**.

---

## 5. Classes nécessitant une collecte locale obligatoire (détail)

| Classe | Motif de la collecte obligatoire | Informations à collecter avec l'agronome |
|--------|----------------------------------|------------------------------------------|
| MANIOC_SAIN | Manioc absent de PlantVillage et de PlantDoc (vérifié le 2026-11-24) | Validation des conditions de culture camerounaises, feuille saine représentative |
| MANIOC_MALADIE_MOSAIQUE | Manioc absent de PlantVillage et de PlantDoc (vérifié le 2026-11-24) | Mosaïque du manioc (CMV) confirmée sur le terrain par l'agronome |
| MANIOC_CARENCE | Aucune source publique ne documente les carences du manioc | Nutriment concerné, symptômes visuels sur feuille, localisation |
| MANIOC_RAVAGEUR | Aucun dataset public ne couvre les ravageurs visibles du manioc | Espèce du ravageur, visibilité sur la photo, dégâts associés |
| MANIOC_DEGAT_RAVAGEUR | Aucun dataset public ne documente les dégâts de ravageurs sur manioc | Type de dégât, visibilité sur la photo, corrélation avec le ravageur |
| TOMATE_RAVAGEUR | Seul l'acarien (Spider_mites) est couvert par PlantVillage et PlantDoc ; autres insectes non documentés | Espèce du ravageur, visibilité sur la photo |
| TOMATE_DEGAT_RAVAGEUR | Aucun dataset public ne documente les dégâts de ravageurs sur tomate | Type de dégât, visibilité sur la photo |
| TOMATE_CARENCE | Aucune source publique ne documente les carences de la tomate | Nutriment concerné, symptômes visuels sur feuille |
| MAIS_RAVAGEUR | Aucun dataset public ne couvre les ravageurs visibles du maïs | Espèce du ravageur, visibilité sur la photo |
| MAIS_DEGAT_RAVAGEUR | Aucun dataset public ne documente les dégâts de ravageurs sur maïs | Type de dégât, visibilité sur la photo |
| MAIS_CARENCE | Aucune source publique ne documente les carences du maïs | Nutriment concerné, symptômes visuels sur feuille |

---

## 6. Classes exclues ou problématiques

| Classe | Motif d'exclusion ou de problème | Décision |
|--------|----------------------------------|----------|
| MANIOC_MALADIE_BRUNISSEMENT (CBSD) | Le CBSD se manifeste principalement sur les racines. Les symptômes foliaires sont limités et peu spécifiques. Le périmètre AgriDoc V1 est limité aux photos de feuilles. | **EXCLUE DE V1** (statut 5) |
| Classes ravageurs sans espèce identifiée (version antérieure) | "Insecte visible sur la feuille" est trop vague pour une classification fiable | **REDÉFINIES** en TOMATE_RAVAGEUR_SPIDER_MITE (confirmé) et classes à collecter (autres espèces) |
| Classes carences sans nutriment spécifié (version antérieure) | "Carence nutritionnelle" est trop vague pour une classification fiable | **REDÉFINIES** en classes à collecter avec précision du nutriment par un agronome |

---

## 7. Informations Manquantes

| Information | Impact | Vérification nécessaire |
|-------------|--------|------------------------|
| Nombre exact d'images par classe dans PlantVillage (via `leaf_grouping`, pas le simple comptage de fichiers `raw/color`) | Détermine quelles classes peuvent être entraînées immédiatement | Télécharger et compter via le `leaf_grouping` de PlantVillage |
| Présence effective de Manioc dans les sources publiques | Détermine si le manioc peut être couvert par des données publiques | **Répondu le 2026-11-24 : le manioc est absent de PlantVillage et de PlantDoc ; la collecte camerounaise est obligatoire pour toutes les classes du manioc.** |
| Licence d'utilisation commerciale de PlantVillage | Détermine si le modèle peut être distribué dans une application | Vérifier auprès des auteurs (Mohanty et al., 2016) — aucune licence détectée dans le dépôt |
| Disponibilité d'un référent agronomique camerounais | Bloquant pour les classes ravageurs, carences et toutes les classes du manioc | Recruter |
| Budget et délai de collecte terrain | Impacte le planning | Planifier avec le chef de projet |
