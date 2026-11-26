# ACCEPTANCE_CRITERIA — Critères d'Acceptation AgriDoc V1

**Version :** 1.0  
**Statut :** Proposition (aucun test n'a encore été exécuté)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe AgriDoc (Keumeka, Messi, Sam, Balawe)  
**Dernière révision :** 2026-11-22

---

## 1. Objectif

Définir des critères de validation vérifiables pour le dataset, le modèle, le déploiement et l'application. Chaque critère doit être mesurableobjectivement. **Aucun objectif numérique (précision 95 %, seuil 0,60, etc.) n'est fixé arbitrairement : tous les objectifs doivent être justifiés par les données et les risques.**

---

## 2. Critères A — Dataset

### 2.1 Traçabilité des images

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| A-01 | Chaque image d'entraînement possède un `image_id` unique | Vérification du fichier de métadonnées (CSV/JSON) | 100% des images ont un ID unique |
| A-02 | Chaque image possède une `source` documentée (PlantVillage, PlantDoc, CCMT, collecte_camerounaise) | Vérification du fichier de métadonnées | 100% des images ont une source |
| A-03 | Chaque image possède un champ `validation_agronomique` | Vérification du fichier de métadonnées | 100% des images ont ce champ renseigné |
| A-04 | Les images provenant de sources publiques ont une `source_url` quand disponible | Vérification du fichier de métadonnées | 100% des images publiques ont une URL |

### 2.2 Qualité des annotations

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| A-05 | Chaque image est assignée à une seule classe de la nomenclature V1 | Vérification du fichier de métadonnées | 100% des images ont une classe valide |
| A-06 | Les classes utilisées sont exclusivement celles définies dans `DATASET_SPECIFICATION.md` | Vérification du fichier de métadonnées | 100% des classes sont dans la nomenclature |
| A-07 | Aucune classe fictive n'est créée pour combler des données manquantes | Revue manuelle de la nomenclature | Zéro classe fictive |
| A-08 | Les classes non suffisamment représentées sont explicitement marquées comme "collecte nécessaire" | Revue manuelle de `DATASET_SPECIFICATION.md` | Toutes les classes insuffisantes sont identifiées |

### 2.3 Absence de doublons et fuites

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| A-09 | Aucun doublon visuel exact entre les ensembles (train/validation/test) | Hachage perceptuel (pHash) sur toutes les images | Zéro doublon entre ensembles |
| A-10 | Aucune image n'apparaît simultanément dans train, validation et test | Vérification des `image_id` par ensemble | Zéro image partagée entre ensembles |
| A-11 | Les variantes d'une même plante (même parcelle, angles différents) sont dans un seul ensemble | Vérification par métadonnées de localisation/date | 100% des variantes sont cohérentes |

### 2.4 Validation agronomique

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| A-12 | Un référent agronomique a validé chaque classe de maladie, ravageur et carence | Signature/nom du valideur dans les métadonnées | 100% des classes ont un valideur identifié |
| A-13 | Les classes ravageurs ne contiennent que des ravageurs suffisamment visibles sur la photo | Revue manuelle des annotations | Zéro identification de ravageur sur dégâts non spécifiques |

### 2.5 Représentativité des données camerounaises

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| A-14 | Au moins X% des images proviennent de la collecte camerounaise (X à définir selon la disponibilité) | Comptage des images par source | À définir après collecte |
| A-15 | Les trois cultures (Manioc, Tomate, Maïs) sont représentées dans chaque ensemble (train/validation/test) | Comptage par culture par ensemble | ≥ 10 images par culture par ensemble |
| A-16 | La collecte couvre plusieurs conditions d'éclairage, d'appareils et de stades de croissance | Revue des métadonnées `qualite_image`, `luminosite` | Couverture variée documentée |

---

## 3. Critères B — Modèle

### 3.1 Entraînement reproductible

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| B-01 | Le code d'entraînement est versionné et documenté | Revue du dépôt de code d'entraînement (hors dépôt AgriDoc) | Code disponible et documenté |
| B-02 | Une graine aléatoire (random seed) est fixée pour l'entraînement | Vérification du code d'entraînement | Graine fixée et documentée |
| B-03 | Relancer l'entraînement avec les mêmes paramètres produit le même modèle | Deuxième entraînement + comparaison des poids | Résultats identiques |

### 3.2 Rapport d'évaluation

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| B-04 | Un rapport d'évaluation est produit avec accuracy, macro-F1, rappel par classe, précision par classe | Rapport écrit (PDF/Markdown) | Toutes les métriques présentes |
| B-05 | Une matrice de confusion est générée et analysée | Fichier de la matrice de confusion | Matrice présente et interprétée |
| B-06 | Le macro-F1 est mesuré sur le jeu de test (jamais utilisé pendant l'entraînement) | Calcul sur le jeu de test | Valeur numérique documentée |

### 3.3 Performance par classe

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| B-07 | Le rappel par classe est mesuré pour chaque classe de la nomenclature | Calcul sur le jeu de test | Valeur par classe documentée |
| B-08 | Les classes rares (peu d'images) sont identifiées et leur performance est rapportée séparément | Analyse du jeu de test | Classes rares listées avec leur performance |

### 3.4 Tests hors domaine

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| B-09 | Le modèle est testé sur des images ne montrant pas de plante (mains, ciel, sol, objets) | Jeu de test hors domaine dédié | Score de confiance faible ou rejet par le seuil |
| B-10 | Le modèle ne force pas une image de tomate vers une classe de manioc, et inversement | Test croisé inter-cultures | Zéro confusion inter-culture sur le jeu de test |

### 3.5 Gestion des résultats incertains

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| B-11 | Un seuil de confiance est déterminé expérimentalement à partir de la courbe précision/rappel | Analyse du jeu de validation | Seuil documenté avec justification |
| B-12 | Le seuil n'est pas fixé arbitrairement à 0,60 (ou toute autre valeur sans justification) | Revue de la documentation | Justification expérimentale présente |

---

## 4. Critères C — Déploiement

### 4.1 Export TensorFlow Lite

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| C-01 | Le fichier `plant_disease_model.tflite` est un modèle réel, quantifié, traçable et licencié | Vérification du fichier et des documents de provenance | Fichier présent, licence documentée |
| C-02 | Le modèle se charge avec TensorFlow Lite 2.14.0 sans ajouter de dépendance Gradle | Test de chargement sur Android | Chargement sans exception |
| C-03 | Le fichier `labels.txt` est présent avec un label par classe, dans l'ordre des indices de sortie | Comptage des lignes vs nombre de classes de sortie | Nombre de lignes == nombre de classes |
| C-04 | La règle `aaptOptions { noCompress "tflite" }` est présente dans `app/build.gradle` | Vérification du fichier build.gradle | Règle présente |

### 4.2 Vérification des tenseurs

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| C-05 | Les dimensions du tenseur d'entrée sont lues depuis le modèle (pas de valeur en dur) | `interpreter.getInputTensor(0).shape()` | Valeurs cohérentes avec le prétraitement |
| C-06 | Le type numérique d'entrée est lu depuis le modèle (UINT8 ou FLOAT32) | `interpreter.getInputTensor(0).dataType()` | Cohérent avec `bitmapToByteBuffer` |
| C-07 | Le nombre de classes de sortie correspond au nombre de lignes dans `labels.txt` | `interpreter.getOutputTensor(0).shape()` vs `labels.txt` | Correspondance exacte |

### 4.3 Comparaison Float32 / INT8

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| C-08 | Une version Float32 et une version INT8 sont évaluées sur le jeu de test | Évaluation des deux versions | Les deux versions disponibles |
| C-09 | La dégradation d'accuracy entre Float32 et INT8 est mesurée | Comparaison des deux versions | Dégradation < 3% (à justifier) |

### 4.4 Tests sur Android

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| C-10 | L'inférence s'exécute sur un appareil Android réel (ou émulateur) | Test instrumenté | Inférence réussie sans crash |
| C-11 | La latence d'inférence est mesurée sur l'appareil cible | Chronométrage sur appareil | Valeur mesurée et documentée |
| C-12 | La consommation mémoire est mesurée pendant l'inférence | Surveillance RAM sur appareil | Valeur mesurée et documentée |

### 4.5 Absence de prédictions fictives

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| C-13 | Aucun score de confiance n'est hardcodé (ex. 0.95f) | Recherche de valeurs littérales suspects dans le code Java | Zéro score hardcodé |
| C-14 | `ClassificationModel.classifyImage()` retourne une vraie prédiction TFLite | Test unitaire avec modèle réel | Résultat issu du modèle, pas simulé |
| C-15 | Si le score est sous le seuil, le résultat indique un état "non reconnu" | Test avec image à faible confiance | `estReconnu = false` |

---

## 5. Critères D — Application

### 5.1 Respect du périmètre photographique

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| D-01 | L'application accepte les photos de feuille ou de partie identifiable de plante | Test manuel avec plusieurs photos valides | Les photos valides sont acceptées |
| D-02 | Les photos de parcelles entières ne sont pas garanties (message approprié si détecté) | Test manuel avec photo de parcelle | Message d'avertissement ou rejet |
| D-03 | Les images floues ou non exploitables sont détectées | Test avec image floue | Message "Image non exploitable" |

### 5.2 Gestion des images non exploitables

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| D-04 | Une image sans partie identifiable de plante produit un état compréhensible | Test avec image de main, ciel, sol | Message "Image non reconnue" ou similaire |
| D-05 | L'utilisateur peut réessayer après un échec | Test du bouton "Réessayer" | Bouton fonctionnel, nouvel essai possible |

### 5.3 Gestion des cultures non prises en charge

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| D-06 | Une image de culture hors V1 (banane, patate douce) n'est pas forcée vers une classe des trois cultures | Test avec image de bananier | Résultat "Non reconnu" ou message approprié |
| D-07 | L'application n'affirme jamais une maladie sur une culture non supportée | Test avec image de culture inconnue | Pas de prédiction forcée |

### 5.4 Affichage explicite des incertitudes

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| D-08 | L'écran résultat affiche le nom de classe, le score et le conseil | Test manuel | Tous les éléments affichés |
| D-09 | Un message indique que le résultat n'est pas un diagnostic agronomique certain | Test manuel sur l'écran résultat | Mention présente |
| D-10 | En cas de score sous seuil, un message conseille de consulter un technicien agricole | Test manuel avec image incertaine | Message de conseil présent |

### 5.5 Historique et persistance

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| D-11 | Un diagnostic réussi est enregistré dans Room avec plante, maladie, score, date, chemin image | Test de bout en bout + vérification de la base | Entrée présente dans la base |
| D-12 | L'historique survit à la rotation de l'écran | Test de rotation d'écran | Données conservées |
| D-13 | L'écran historique affiche un état vide quand aucun diagnostic n'est enregistré | Test avec base vide | État vide affiché |

### 5.6 Hors-ligne

| ID | Critère | Méthode de vérification | Seuil de succès |
|----|---------|------------------------|-----------------|
| D-14 | L'inférence fonctionne sans connexion Internet | Test en mode avion | Inférence réussie hors-ligne |
| D-15 | L'historique fonctionne sans connexion Internet | Test en mode avion | Lecture/écriture Room réussie |

---

## 6. Objectifs Numériques de Performance

### 6.1 Principe

**Aucun objectif numérique de précision (ex. 95%) n'est fixé arbitrairement.** Les objectifs doivent être définis après :
1. Constitution du dataset et connaissance du nombre de classes.
2. Entraînement initial et mesure de référence.
3. Analyse des confusions entre classes similaires.
4. Évaluation des risques (faux positif sur une maladie grave vs faux négatif).

### 6.2 Cibles indicatives (À confirmer après mesure)

| Indicateur | Valeur indicative | À confirmer par |
|------------|-------------------|-----------------|
| Macro-F1 sur le jeu de test | À mesurer | Rapport d'évaluation |
| Rappel par classe principale | À mesurer | Rapport d'évaluation |
| Taille modèle INT8 | < 5 Mo (indicative) | Mesure sur le fichier exporté |
| Latence inférence | < 500 ms (indicative) | Mesure sur appareil |
| Dégradation Float32 → INT8 | < 3% (indicative) | Comparaison des deux versions |

**Note sur les seuils** : les valeurs `< 5 Mo`, `< 500 ms` et `< 3 %` sont des cibles indicatives à confirmer par mesure. Elles ne constituent pas des objectifs arbitraires imposés sans justification. Les seuils statistiques et de confiance doivent être déterminés expérimentalement.

---

## 7. Conditions de Livraison

Une fonctionnalité est considérée comme livrable uniquement si :

1. Tous les critères de sa catégorie (A, B, C ou D) sont vérifiés.
2. Les tests unitaires et d'instrumentation passent (`./gradlew testDebugUnitTest` et `./gradlew connectedCheck`).
3. Le code est revue et mergé via Pull Request vers `devop` (pas de commit direct).
4. La documentation du contrat (`model_contract.json` ou équivalent) est à jour avec les valeurs réelles du modèle.
5. Aucun résultat fictif ou hardcodé ne subsiste dans le code.

---

## 8. Tests Obligatoires

| Type | Commande | Objectif |
|------|----------|----------|
| Tests unitaires JVM | `./gradlew testDebugUnitTest` | Tests sur `ClassificationModel`, `ImageUtils`, `LabelProvider`, entités Room |
| Tests d'instrumentation | `./gradlew connectedCheck` | Tests Espresso sur la navigation et l'UI |
| Test de chargement du modèle | Test manuel ou instrumenté | Vérifier que le `.tflite` se charge sans exception |
| Test d'inférence réelle | Test instrumenté sur appareil | Vérifier qu'une prédiction réelle est retournée |
| Test hors-ligne | Test manuel en mode avion | Vérifier que l'inférence et l'historique fonctionnent sans réseau |

---

## 9. Informations Manquantes

| Information | Impact | Vérification nécessaire |
|-------------|--------|------------------------|
| Nombre total de classes (définit la taille de la couche de sortie) | Impacte B-07, C-03, C-07 | À confirmer après validation de la nomenclature |
| Dataset d'entraînement constitué | Bloquant pour B-01 à B-12 | À constituer (voir DATASET_SPECIFICATION.md) |
| Seuil de confiance optimal | Impacte B-11, D-08, D-09, D-10 | À déterminer par courbe précision/rappel |
| Appareils de test pour la latence | Impacte C-10, C-11, C-12 | À planifier avec l'équipe QA |
| Licence des données et du modèle | Impacte C-01 | À vérifier pour chaque source |
