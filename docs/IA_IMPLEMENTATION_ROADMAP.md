# IA_IMPLEMENTATION_ROADMAP — Feuille de Route d'Implémentation IA AgriDoc V1

**Version :** 1.1  
**Statut :** Révision consolidée (PlantVillage et PlantDoc confirmés accessibles ; Maïs confirmé dans PlantVillage ; manioc absent de PlantVillage et de PlantDoc ; CCMT non identifié)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi)  
**Dernière révision :** 2026-11-22

---

## 1. Objectif

Définir la stratégie de modélisation IA pour AgriDoc V1 et le plan d'implémentation associé, à partir des données réellement examinées lors de la Mission 3.

---

## 2. Contraintes et Prérequis (État Réel)

| Contrainte | Détail | Statut |
|------------|--------|--------|
| Cultures V1 | Manioc, Tomate, Maïs uniquement | Validé |
| Types de problèmes | Maladies, ravageurs visibles, dégâts visibles, carences, plante saine, inconnu | Validé |
| Périmètre photo | Feuille ou partie identifiable de plante uniquement | Validé |
| Pas de diagnostic garanti | Le résultat est une aide, pas une certitude | Validé |
| Hors-ligne 100% | Inférence locale TFLite, pas de serveur | Validé |
| Java / Android | TFLite 2.14.0, minSdk 24 | Validé |
| Aucun modèle n'existe | Aucun `.tflite`, aucun `labels.txt` dans le dépôt | Confirmé par audit Git |
| Aucun dataset téléchargé | Aucune image locale ; sources vérifiées, comptages préliminaires uniquement | Confirmé par DATASET_AUDIT.md et DATASET_INVENTORY.md |
| PlantVillage confirmé | 54,306 images annoncées, 14 espèces, 26 maladies ; Tomate et Maïs confirmés dans `raw/` ; manioc absent des dossiers consultés | Confirmé par DATASET_AUDIT.md et DATASET_INVENTORY.md |
| PlantDoc confirmé | 2,598 images, 13 espèces, jusqu'à 17 classes ; Tomate et Maïs présents ; manioc absent ; licence CC-BY-4.0 | Confirmé par DATASET_AUDIT.md et DATASET_INVENTORY.md |
| CCMT non identifié | Source non trouvée | Confirmé par DATASET_AUDIT.md |

---

## 3. Stratégies de Modélisation Comparées

### 3.1 Stratégie A — Classification Multi-Classes à Une Étiquette (Single-label)

**Principe :** Chaque image appartient à une seule classe parmi la nomenclature complète. Une seule tête de sortie avec `N` neurones (softmax).

| Aspect | Détail |
|--------|--------|
| Nombre de sorties | Une tête de `N` classes |
| Type de prédiction | Une seule classe prédite par image |
| Exigences d'annotation | Un label principal par image |
| Gestion multi-problèmes | Non gérée nativement (classe principale ou exclusion) |
| Gestion hors domaine | Classe `GLOBAL_INCONNU` / `GLOBAL_NON_EXPLOITABLE` + seuil de confiance |
| Séparation culture / problème | Implicite dans le nom de classe |
| Avantages | Simple à implémenter, annoter et évaluer |
| Limites | Ne peut pas exprimer plusieurs conditions simultanément |

**Verdict :** Recommandée pour V1 compte tenu du dataset limité et de l'absence de données multi-label confirmées.

---

### 3.2 Stratégie B — Classification Multi-Labels (Multi-label)

**Principe :** Plusieurs étiquettes simultanées par image.

| Aspect | Détail |
|--------|--------|
| Avantages | Représente la réalité agricole (plusieurs problèmes possibles) |
| Limites | Plus complexe à annoter et évaluer ; risque de prédictions incohérentes |
| Justification actuelle | Aucune donnée multi-label confirmée dans les sources examinées |

**Verdict :** Non retenue pour V1. À envisager en V2 si le dataset le justifie.

---

### 3.3 Stratégie C — Architecture à Plusieurs Têtes (Multi-Head)

**Principe :** Têtes séparées pour culture, type de problème, problème spécifique.

| Aspect | Détail |
|--------|--------|
| Avantages | Séparation claire des responsabilités |
| Limites | Plus complexe à entraîner ; risque d'incohérence entre têtes ; plus d'annotations requises |
| Justification actuelle | Sur-ingénierie pour V1 avec un dataset limité |

**Verdict :** Non retenue pour V1.

---

## 4. Recommandation d'Architecture pour V1

| Critère | Recommandation | Justification |
|---------|---------------|---------------|
| Stratégie retenue | **Classification multi-classes à une seule étiquette** | Dataset limité, pas de données multi-label confirmées, simplicité d'implémentation |
| Séparation culture / problème | **Implicite dans le nom de classe** (MANIOC_*, TOMATE_*, MAIS_*) | Évite les incohérences inter-têtes |
| Nombre de têtes | Une seule tête de sortie | Simplicité d'entraînement et de déploiement TFLite |
| Gestion hors domaine | Classes `GLOBAL_INCONNU` + `GLOBAL_NON_EXPLOITABLE` + seuil de confiance | Simple et explicite |
| Nombre de classes initial | À déterminer après vérification des datasets | Dépendra des classes dont le nombre d'images a été compté |

---

## 5. Plan d'Implémentation par Étapes

### Étape 0 — Constitution et vérification du dataset (Bloquant)

| Tâche | Objectif | Livrable | Dépendance | Responsable | Critère de validation |
|-------|----------|----------|------------|-------------|----------------------|
| 0.1 | Examiner complètement leaf-map.json de PlantVillage | Liste exhaustive des classes Manioc/Tomate/Maïs avec comptage d'images | Accès au dépôt PlantVillage | Keumeka / Messi | Nombre d'images par classe documenté |
| 0.2 | Confirmer l'absence du manioc et la présence du Maïs dans PlantVillage | Manioc absent des dossiers consultés ; Maïs confirmé (4 classes dans `raw/`) | Résultat 0.1 | Keumeka / Messi | Présence confirmée ou infirmée pour chaque culture, avec comptage définitif à compléter via `leaf_grouping` |
| 0.3 | Vérifier la licence d'utilisation commerciale de PlantVillage | Document de licence | Site de PlantVillage / auteurs | Keumeka / Messi | Licence documentée et compatible |
| 0.4 | Définir la liste finale des classes V1 | Liste validée des classes entraînables | Résultats 0.1 à 0.3 | Keumeka / Messi + référent agronomique | Liste figée, pas de classe fictive |
| 0.5 | Planifier la collecte camerounaise pour les classes manquantes | Plan de collecte (régions, cultures, classes, nombre d'images cibles) | Résultat 0.4 | Keumeka / Messi + référent agronomique | Plan documenté avec zones et calendriers |

**Critère de passage à l'étape 1 :** Au moins une classe par culture (sain + au moins une maladie) a un nombre d'images vérifié > 0.

---

### Étape 1 — Préparation des données et annotations

| Tâche | Objectif | Livrable | Dépendance | Responsable | Critère de validation |
|-------|----------|----------|------------|-------------|----------------------|
| 1.1 | Télécharger les images des classes retenues | Dataset brut organisé par classe | Étape 0.5 | Keumeka / Messi | Images disponibles localement |
| 1.2 | Appliquer la déduplication (pHash + SHA-256) | Dataset sans doublons | 1.1 | Keumeka / Messi | Zéro doublon détecté |
| 1.3 | Séparer train/validation/test | Trois ensembles disjoints | 1.2 | Keumeka / Messi | Aucune image partagée entre ensembles |
| 1.4 | Générer les images négatives (inconnu, non exploitable) | Images de main, ciel, sol, objets | Étape 0.5 | Keumeka / Messi | Au moins 50 images par classe négative |
| 1.5 | Valider les annotations agronomiquement | Dataset avec champ `validation_agronomique = true` | 1.1 à 1.4 | Référent agronomique | 100% des classes ont un valideur identifié |

**Critère de passage à l'étape 2 :** Chaque classe retenue a au moins 20 images dans l'ensemble de test.

---

### Étape 2 — Entraînement et sélection du modèle

| Tâche | Objectif | Livrable | Dépendance | Responsable | Critère de validation |
|-------|----------|----------|------------|-------------|----------------------|
| 2.1 | Entraîner MobileNetV2 (référence) | Modèle Float32 + métriques | Étape 1 | Keumeka | Rapport d'entraînement avec accuracy, macro-F1 |
| 2.2 | Entraîner MobileNetV3-Small | Modèle Float32 + métriques | Étape 1 | Keumeka | Rapport d'entraînement |
| 2.3 | Entraîner EfficientNet-Lite0 | Modèle Float32 + métriques | Étape 1 | Keumeka | Rapport d'entraînement |
| 2.4 | Comparer les trois architectures | Tableau comparatif (taille, latence, précision) | 2.1 à 2.3 | Keumeka | Architecture retenue documentée avec justification |
| 2.5 | Quantifier le modèle retenu en INT8 | Modèle .tflite quantifié | 2.4 | Keumeka | Fichier .tflite généré, dégradation < 3% vs Float32 |
| 2.6 | Produire labels.txt | Fichier de labels dans l'ordre des sorties | 2.4 | Keumeka / Messi | Nombre de lignes == nombre de classes de sortie |
| 2.7 | Générer model_contract.json | Contrat d'entrée/sortie documenté | 2.5, 2.6 | Keumeka / Messi | Valeurs extraites du modèle réel (pas de placeholders) |

**Critère de passage à l'étape 3 :** Le modèle .tflite se charge avec TFLite 2.14.0 sans exception, et `labels.txt` correspond au nombre de classes de sortie.

---

### Étape 3 — Intégration Android (Sous-système IA)

| Tâche | Objectif | Fichiers concernés | Dépendance | Responsable | Critère de validation |
|-------|----------|-------------------|------------|-------------|----------------------|
| 3.1 | Réécrire ClassificationModel.java (Inférence réelle) | `ClassificationModel.java` | Étape 2 | Keumeka | Interpreter instancié, classifyImage retourne une vraie prédiction |
| 3.2 | Ajouter bitmapToByteBuffer dans ImageUtils | `ImageUtils.java` | Étape 2 | Keumeka / Messi | ByteBuffer accepté par interpreter.run() |
| 3.3 | Créer LabelProvider.java | `model/LabelProvider.java` | Étape 2 | Keumeka | Mapping index→label cohérent avec labels.txt |
| 3.4 | Créer TFLiteModelLoader.java (optionnel) | `model/TFLiteModelLoader.java` | Étape 2 | Keumeka | Chargement depuis assets/ sans exception |
| 3.5 | Enrichir Plante.java (champ estReconnu) | `Plante.java` | Étape 2 | Keumeka | Champ estReconnu présent et renseigné |
| 3.6 | Implémenter la gestion du seuil de confiance | `ClassificationModel.java` | 3.1 | Keumeka | Sous seuil → estReconnu = false, maladie = "Non reconnu" |
| 3.7 | Thread de fond pour l'inférence | `ClassificationModel.java` | 3.1 | Keumeka | Aucun blocage du thread UI |

**Critère de passage à l'étape 4 :** `classifyImage(bitmap)` retourne un `Plante` avec des données issues d'une vraie inférence TFLite, pas de hardcodé.

---

### Étape 4 — Intégration avec les autres composants Android

| Tâche | Objectif | Fichiers concernés | Dépendance | Responsable | Critère de validation |
|-------|----------|-------------------|------------|-------------|----------------------|
| 4.1 | Intégrer ClassificationModel dans ResultActivity | `ResultActivity.java` | Étape 3, Moumoun (caméra) | Keumeka / Adoum | Réception de l'image, appel d'inférence, affichage du résultat |
| 4.2 | Sauvegarder dans HistoriqueRepository | `ResultActivity.java` | Étape 3, Sam (repository) | Keumeka / Sam | Diagnostic persisté dans Room |
| 4.3 | Gérer les erreurs (modèle manquant, inférence échouée, non reconnu) | `ResultActivity.java`, `ClassificationModel.java` | Étape 3 | Keumeka | Messages d'erreur clairs, pas de crash |

**Critère de passage à l'étape 5 :** Parcours complet Dashboard → Caméra → photo → inférence → résultat avec score honnête → sauvegarde → retour Dashboard.

---

### Étape 5 — Tests et validation finale

| Tâche | Objectif | Commande / Test | Dépendance | Responsable | Critère de validation |
|-------|----------|-----------------|------------|-------------|----------------------|
| 5.1 | Tests unitaires IA | `./gradlew testDebugUnitTest` | Étape 4 | Keumeka / Sam | Tests ClassificationModel, ImageUtils, LabelProvider passent |
| 5.2 | Tests d'instrumentation | `./gradlew connectedCheck` | Étape 4 | Sam | Espresso : navigation et UI fonctionnent |
| 5.3 | Test d'inférence réelle sur appareil | Test instrumenté | Étape 4 | Keumeka | Prédiction réelle retournée sur appareil |
| 5.4 | Test hors-ligne | Test manuel en mode avion | Étape 4 | Keumeka | Inférence et historique fonctionnent sans réseau |
| 5.5 | Test de latence et mémoire | Mesure sur appareil | Étape 4 | Keumeka | Valeurs mesurées et documentées |
| 5.6 | Test hors domaine | Images de main, ciel, sol | Étape 4 | Keumeka | Score faible ou rejet par le seuil |

**Critère de livraison V1 :** Tous les critères d'acceptation de `ACCEPTANCE_CRITERIA.md` sont vérifiés, la Pull Request `feature/ia-classification` est mergée vers `devop`.

---

## 6. Dépendances Croisées et Points de Synchronisation

| Dépendance | De qui | Impact sur la roadmap IA |
|------------|--------|-------------------------|
| Dataset vérifié (PlantVillage) | Keumeka / Messi | Bloquant pour l'étape 1 |
| Licence commerciale PlantVillage | Keumeka / Messi | Bloquant pour la distribution de l'app |
| Collecte camerounaise (ravageurs, carences) | Référent agronomique + Keumeka | Bloquant pour les classes RAVAGEUR, DEGAT_RAVAGEUR, CARENCE |
| Intégration des assets (.tflite + labels.txt) | Balawe | Requis avant l'étape 3 |
| Contrat de transmission image (CameraActivity → ResultActivity) | Moumoun | Requis pour l'étape 4.1 |
| Sauvegarde historique (Room) | Sam | Requis pour l'étape 4.2 |
| Protection des fichiers de build | Balawe | Aucune modification de build.gradle sans accord |

---

## 7. Blocs Réels et Risques

| Risque | Gravité | Impact | Mitigation |
|--------|---------|--------|------------|
| Aucun dataset téléchargé ; sources vérifiées, comptage définitif incomplet | Bloquant | Impossible d'entraîner un modèle tant que le comptage par feuille n'est pas établi | Télécharger PlantVillage, appliquer `leaf_grouping` et compter les images par classe |
| Aucun modèle .tflite dans assets/ | Bloquant | L'inférence ne peut pas être intégrée | Issue #15 doit être livrée par Keumeka/Messi |
| Licence PlantVillage non vérifiée | Majeur | Risque juridique pour la distribution | Vérifier avant tout entraînement |
| Classes ravageurs/carences non couvertes par PlantVillage | Majeur | 11 classes nécessitent une collecte locale | Planifier la collecte camerounaise tôt |
| CBSD (manioc) principalement racinaire | Majeur | Incompatible avec le périmètre photo-feuille | Exclue de V1 (statut 5) |
| Manioc absent de PlantVillage et de PlantDoc | Majeur | Le manioc ne peut pas être couvert par les sources publiques vérifiées | Collecte camerounaise obligatoire pour toutes les classes du manioc |
| Seuil de confiance non défini | Majeur | Impossible de gérer l'incertitude honnêtement | Déterminer par courbe précision/rappel sur validation |

---

## 8. Décisions à Prendre (Non encore implémentées)

| Décision | Recommandation | Statut |
|----------|---------------|--------|
| Architecture de modélisation | Multi-classes à une seule étiquette (Stratégie A) | ❌ En attente de vérification du dataset |
| Nombre de classes initial | À déterminer après vérification des datasets | ❌ En attente |
| Seuil de confiance | À déterminer expérimentalement | ❌ En attente |
| Quantification INT8 | Recommandée, à confirmer par mesure de dégradation | ❌ En attente |
| Classes ravageurs et carences | Collecte locale obligatoire | ❌ Non commencé |

---

## 9. Livrables Attendus de la Branche `feature/ia-classification`

| Livrable | Description | État |
|----------|-------------|------|
| `ClassificationModel.java` réécrit | Moteur d'inférence TFLite réel | ❌ À implémenter |
| `ImageUtils.java` enrichi | Méthode `bitmapToByteBuffer` ajoutée | ❌ À implémenter |
| `Plante.java` enrichi | Champ `estReconnu` ajouté | ❌ À implémenter |
| `model/LabelProvider.java` | Lecture `labels.txt`, mapping index→libellé | ❌ À créer |
| `model/TFLiteModelLoader.java` | Chargement modèle depuis `assets/` | ❌ À créer (optionnel) |
| `plant_disease_model.tflite` | Modèle réel, quantifié, licencié | ❌ À produire (issue #15) |
| `labels.txt` | Labels dans l'ordre des sorties du modèle | ❌ À produire (issue #15) |
| `model_contract.json` | Contrat d'entrée/sortie avec valeurs réelles | ❌ À créer après entraînement |
| Tests unitaires IA | `ClassificationModelTest`, `ImageUtilsTest`, `LabelProviderTest` | ❌ À créer |

---

## 10. Informations Manquantes pour Démarrer

| Information | Impact | Vérification nécessaire |
|-------------|--------|------------------------|
| Nombre définitif d'images par classe dans PlantVillage | Détermine quelles classes sont entraînables | Télécharger, appliquer `leaf_grouping` et compter par feuille |
| Présence effective du Manioc et du Maïs dans PlantVillage | Manioc absent confirmé ; Maïs confirmé (4 classes) ; comptage définitif à établir | Examen complet de `raw/` et du `leaf_grouping` |
| Licence d'utilisation commerciale des datasets | Impacte la distribution de l'application | Vérifier auprès de chaque source |
| Référent agronomique camerounais disponible | Bloquant pour les classes ravageurs et carences | Recruter |
| Budget et délai de collecte terrain | Impacte le planning | Planifier avec le chef de projet |
