# Issue #15 : Produire le modèle TFLite et son fichier de labels

- **Assignés** : Keumeka (Lead IA) & Messi (Data / Prétraitement)
- **Branche** : `feature/ia-classification` (Pull Request vers `devop`)
- **Priorité** : Bloquante — l’intégration et l’inférence réelles ne peuvent pas être terminées sans ces artefacts.
- **Dépendances** : Issues #09 (inférence TFLite), #10 (prétraitement) et #02 (intégration des assets par Balawe).

## Contexte

L’Issue #02 attend `plant_disease_model.tflite` et `labels.txt` dans `app/src/main/assets/`, mais ces fichiers ne sont pas encore dans le dépôt. Les issues #09 et #10 décrivent une entrée de 224×224 pixels en RGB. Le modèle et ses labels doivent donc être réellement compatibles avec le contrat utilisé par le code Android.

Cette tâche consiste à sélectionner ou entraîner un modèle de diagnostic, à l’exporter en TFLite quantifié, et à fournir le mapping exact entre ses sorties et les noms de classes. Aucun modèle ou label fictif ne doit être ajouté.

## Responsabilités

- **Keumeka — Lead IA** : choisir ou entraîner le modèle pour les classes de plantes et maladies retenues, puis produire un export TFLite quantifié compatible avec l’exécution Android prévue.
- **Messi — Data / Prétraitement** : confirmer les dimensions, le format et la normalisation des entrées ; préparer le fichier de labels en respectant exactement l’ordre des indices de sortie du modèle.
- **Keumeka et Messi ensemble** : valider que les sorties du modèle, les labels et le prétraitement correspondent. Signaler toute incompatibilité avec le contrat 224×224 RGB avant l’intégration, et convenir des changements nécessaires dans le périmètre IA.

## Livrables à transmettre à Balawe pour l’Issue #02

- Le vrai fichier `plant_disease_model.tflite`, exporté et quantifié.
- Le vrai fichier `labels.txt`, avec un label par classe, dans le même ordre que les indices de sortie.
- Les informations de provenance et de licence du modèle, confirmant que son inclusion dans l’application est autorisée.
- Le contrat d’entrée et de sortie : formes des tenseurs, types de données, disposition des canaux, plage/normalisation des pixels, paramètres de quantification et nature des sorties (logits ou probabilités).
- Une vérification de fumée reproductible sur une image représentative : classe prédite, indice correspondant et score retourné.

Balawe reste responsable de l’intégration des deux fichiers dans `app/src/main/assets/` et de la vérification Gradle décrite dans l’Issue #02. Les livrables doivent être transmis dans la Pull Request IA ou par un moyen approuvé par Balawe ; ne pas créer de fichiers de remplacement dans le dépôt.

## Critères d’acceptation

- [ ] Le fichier TFLite est un modèle réel, quantifié, traçable et licencié pour cette utilisation.
- [ ] Le modèle peut être chargé avec la version TensorFlow Lite déjà déclarée dans le projet, sans ajouter ni modifier de dépendance Gradle.
- [ ] Le contrat du modèle est documenté et indique explicitement si l’entrée 224×224 RGB de l’Issue #09 est respectée.
- [ ] Le nombre de lignes de `labels.txt` correspond au nombre de classes de sortie et chaque ligne correspond à l’indice de sortie indiqué.
- [ ] L’image de vérification produit une sortie valide, un indice de classe dans les limites et un score interprétable.
- [ ] Les deux fichiers et leur contrat sont transmis à Balawe afin qu’il termine l’intégration de l’Issue #02.

## Hors périmètre

Cette issue ne demande pas de modifier les écrans, CameraX, Room/MVVM, les fichiers Gradle ou le manifeste. Toute modification des interfaces de prétraitement ou de classification doit rester dans les fichiers attribués aux rôles IA et être documentée dans la Pull Request.
