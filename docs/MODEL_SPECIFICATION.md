# MODEL_SPECIFICATION — Spécification du Modèle IA AgriDoc V1

**Version :** 1.0  
**Statut :** Proposition (aucun modèle n'est encore entraîné ni exporté)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi)  
**Dernière révision :** 2026-11-22

---

## 1. Objectif

Définir le choix, l'entraînement et l'export du modèle TensorFlow Lite pour la classification des problèmes phytosanitaires sur Manioc, Tomate et Maïs. Aucun modèle n'existe actuellement dans le dépôt. Le modèle doit être réel, quantifié, traçable et licencié (issue #15).

---

## 2. Architectures Candidates

Trois architectures sont étudiées. **Aucune n'est déclarée définitivement meilleure sans comparaison expérimentale.**

### 2.1 MobileNetV2

| Critère | Détail |
|---------|--------|
| Type | CNN légère basée sur des inverted residuals et des convolutions séparables en profondeur |
| Taille approximative (Float32) | ~14 Mo |
| Taille approximative (INT8 quantifié) | ~3,5 Mo |
| Vitesse d'inférence (CPU mobile) | Rapide, bien optimisée pour TFLite |
| Consommation mémoire | Faible à modérée |
| Compatibilité TFLite | Excellente (modèle de référence TFLite) |
| Quantification INT8 | Supportée nativement, bonne rétention de précision |
| Points forts | Bon compromis précision/taille, largement documentée, support communauté important |
| Points faibles | Moins précise que EfficientNet sur des classes fines |

### 2.2 MobileNetV3-Small

| Critère | Détail |
|---------|--------|
| Type | Version optimisée de MobileNetV3, encore plus légère |
| Taille approximative (Float32) | ~5 Mo |
| Taille approximative (INT8 quantifié) | ~1,3 Mo |
| Vitesse d'inférence (CPU mobile) | Très rapide |
| Consommation mémoire | Très faible |
| Compatibilité TFLite | Excellente |
| Quantification INT8 | Supportée |
| Points forts | Plus petite et plus rapide que MobileNetV2 |
| Points faibles | Précision potentiellement inférieure sur des classes visuellement similaires |

### 2.3 EfficientNet-Lite0

| Critère | Détail |
|---------|--------|
| Type | Version "Lite" d'EfficientNet, optimisée pour mobile |
| Taille approximative (Float32) | ~19 Mo |
| Taille approximative (INT8 quantifié) | ~4,8 Mo |
| Vitesse d'inférence (CPU mobile) | Rapide, légèrement plus lente que MobileNetV2 |
| Consommation mémoire | Modérée |
| Compatibilité TFLite | Excellente (conçu pour TFLite) |
| Quantification INT8 | Supportée |
| Points forts | Meilleure précision globale que MobileNetV2 sur de nombreux benchmarks |
| Points faibles | Plus grande, légèrement plus lente, consommation mémoire supérieure |

---

## 3. Critères de Comparaison Expérimentale

Le choix final doit reposer sur des mesures réelles, pas sur des présomptions. Les critères suivants doivent être mesurés pour chaque architecture :

| Critère | Mesure | Objectif |
|---------|--------|----------|
| Précision globale (accuracy) | Pourcentage de bonnes prédictions sur le jeu de test | À mesurer |
| Macro-F1 | Moyenne non pondérée des F1 par classe | À mesurer |
| Rappel par classe | Pourcentage de vrais positifs par classe | À mesurer, surtout pour les classes rares |
| Taille du modèle (INT8) | Mo sur disque | À mesurer |
| Latence d'inférence | Millisecondes par image sur un smartphone représentatif | À mesurer |
| Mémoire RAM pic | Mo consommés pendant l'inférence | À mesurer |
| Dégradation précision Float32 → INT8 | Différence d'accuracy entre les deux versions | À mesurer, doit être < 2-3% |

**Recommandation :** Commencer par MobileNetV2 comme référence initiale (bon compromis documenté), puis comparer avec MobileNetV3-Small et EfficientNet-Lite0 sur le jeu de validation. L'architecture retenue doit être celle offrant le meilleur compromis précision/taille/latence pour les classes cibles.

---

## 4. Stratégie d'Entraînement

### 4.1 Type de classification

**Classification multiclasse à une étiquette par image.** Chaque image appartient à une seule classe parmi la nomenclature définie dans `DATASET_SPECIFICATION.md`.

### 4.2 Gestion des conditions simultanées

Le modèle V1 ne gère pas nativement la reconnaissance de plusieurs conditions simultanées sur une même image. Si une image présente plusieurs problèmes, elle est assignée à la classe la plus significative ou exclue si l'ambiguïté est trop grande. Une évolution future pourra utiliser le multi-label ou la détection d'objets.

### 4.3 Gestion des résultats incertains et hors domaine

Le modèle doit produire un score de confiance par classe. Le système Android appliquera un seuil :
- Si le score max >= seuil → classe prédite affichée.
- Si le score max < seuil → état "non reconnu" ou "incertain".
- Si l'image est hors domaine (pas de plante) → rejet avec message approprié.

Le seuil de confiance n'est **pas fixé arbitrairement** à 0,60. Il doit être déterminé expérimentalement à partir de la courbe précision/rappel sur le jeu de validation.

### 4.4 Cultures non prises en charge

Les images de cultures hors V1 (banane, patate douce, etc.) doivent être classées dans une classe "inconnu" ou rejetées, jamais forcées vers une classe des trois cultures cibles.

---

## 5. Évaluation du Modèle

### 5.1 Métriques obligatoires

| Métrique | Définition | Usage |
|----------|------------|-------|
| Accuracy | (Vrais positifs + Vrais négatifs) / Total | Performance globale |
| Macro-F1 | Moyenne arithmétique des F1-scores par classe | Performance équilibrée entre classes |
| Rappel par classe | TP / (TP + FN) pour chaque classe | Détection des cas positifs par classe |
| Précision par classe | TP / (TP + FP) pour chaque classe | Fiabilité des prédictions par classe |
| Matrice de confusion | Tableau des prédictions vs réalités | Analyse des confusions entre classes similaires |
| Courbe précision-rappel | Trade-off selon le seuil de confiance | Détermination du seuil optimal |

### 5.2 Tests obligatoires

1. **Test hors domaine** : évaluer le modèle sur des images ne montrant pas de plante (mains, ciel, sol, objets). Le modèle doit produire un score faible ou être rejeté par le seuil.
2. **Test multi-culture** : vérifier qu'une image de tomate n'est pas forcée vers une classe de manioc, et inversement.
3. **Test de robustesse** : évaluer sur des images floues, sous-exposées, surexposées.
4. **Test de reproductibilité** : relancer l'entraînement avec la même graine aléatoire et vérifier que les résultats sont identiques.

---

## 6. Export TensorFlow Lite

### 6.1 Format

- Format : **TensorFlow Lite (.tflite)**.
- Quantification : **INT8 post-training** (recommandé pour réduire la taille et accélérer l'inférence sur CPU mobile).
- Alternative : Float32 si la dégradation de précision par quantification est trop importante.

### 6.2 Contraintes du projet

- Le modèle doit être chargeable avec **TensorFlow Lite 2.14.0** déjà déclarée dans `app/build.gradle`.
- Aucune dépendance Gradle supplémentaire ne doit être ajoutée sans accord de Balawe.
- Le fichier `.tflite` doit être placé dans `app/src/main/assets/` avec la règle `aaptOptions { noCompress "tflite" }` déjà présente.
- Le fichier `labels.txt` doit accompagner le modèle, avec un label par ligne, dans l'ordre exact des indices de sortie du modèle.

### 6.3 Vérification de l'export

| Vérification | Méthode | Critère de succès |
|--------------|---------|-------------------|
| Chargement du modèle | `Interpreter.createFromFile()` ou `MappedByteBuffer` | Aucune exception |
| Vérification des tenseurs d'entrée | `interpreter.getInputTensor(0)` | Shape et type correspondent au contrat |
| Vérification des tenseurs de sortie | `interpreter.getOutputTensor(0)` | Shape et type correspondent au nombre de classes |
| Inférence de test | `interpreter.run()` sur une image de test | Sortie valide, indices dans les limites |
| Comparaison Float32 vs INT8 | Évaluer les deux versions sur le jeu de test | Dégradation < 2-3% d'accuracy |

---

## 7. Quantification

### 7.1 INT8 Post-Training Quantification

- Convertir le modèle entraîné (Float32) en TFLite INT8 à l'aide du TFLite Converter.
- Utiliser un jeu de calibration représentatif (subset du jeu d'entraînement ou de validation).
- Vérifier que la précision ne se dégrade pas de plus de 2-3% par rapport à la version Float32.

### 7.2 Alternative : Quantification aware training

Si la post-training quantification dégrade trop la précision, envisager le "quantization aware training" (QAT) pendant l'entraînement. Cela nécessite plus de temps d'entraînement mais peut préserver la précision.

---

## 8. Consommation et Performance Cibles (À confirmer par mesure)

| Indicateur | Valeur cible indicative | À mesurer |
|------------|------------------------|-----------|
| Taille modèle INT8 | < 5 Mo | Mesurer sur le modèle exporté |
| Latence inférence (smartphone milieu de gamme) | < 500 ms | Mesurer sur appareil réel |
| Mémoire RAM pic | < 100 Mo | Mesurer sur appareil réel |
| Dégradation précision Float32 → INT8 | < 3% | Mesurer sur jeu de test |

**Ces valeurs sont indicatives et doivent être confirmées par des mesures réelles sur le modèle entraîné.**

---

## 9. Informations Manquantes

| Information | Impact | Vérification nécessaire |
|-------------|--------|------------------------|
| Nombre total de classes (dépend de la nomenclature validée) | Détermine la taille de la couche de sortie | À confirmer après validation agronomique |
| Dataset d'entraînement réel | Bloquant pour l'entraînement | À constituer (voir DATASET_SPECIFICATION.md) |
| Seuil de confiance optimal | Détermine le comportement "non reconnu" | À déterminer par courbe précision/rappel |
| Appareils de test pour la latence | Détermine les cibles de performance | À planifier avec l'équipe QA |
| Licence des données d'entraînement | Impacte la distribution de l'application | À vérifier pour chaque source |

---

## 10. Décisions à Prendre (Non encore implémentées)

| Décision | Recommandation | Statut |
|----------|---------------|--------|
| Architecture retenue | À choisir après comparaison expérimentale (MobileNetV2 de référence initiale) | ❌ En attente |
| Dimensions d'entrée | À déterminer par le modèle retenu | ❌ Hypothèse 224×224 non vérifiée |
| Type d'entrée (float32 vs uint8) | Dépend de la quantification choisie | ❌ À confirmer |
| Normalisation | Dépend du modèle (0-1, -1 à 1, ou mean/std) | ❌ À documenter |
| Seuil de confiance | À déterminer expérimentalement | ❌ À définir |
| Quantification INT8 | Recommandée, à confirmer par mesure de dégradation | ❌ À confirmer |
| Nombre de threads d'inférence | À tester (1, 2, 4 ou availableProcessors) | ❌ À optimiser |
