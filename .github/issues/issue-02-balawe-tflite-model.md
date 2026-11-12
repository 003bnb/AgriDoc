# Issue #02 : Intégration du Modèle TensorFlow Lite dans Assets

- **Assigné à** : Balawe (Lead DevOps & Architecte)
- **Branche** : `feature/devops-assets`
- **Priorité** : Moyenne

## 📌 Description
Placer le fichier modèle TensorFlow Lite quantifié (`plant_disease_model.tflite`) ainsi que le fichier d'étiquettes des maladies (`labels.txt`) dans le dossier `app/src/main/assets/`.

## 📋 Critères d'Acceptation
- [ ] Le fichier `.tflite` et `labels.txt` sont présents dans `app/src/main/assets/`.
- [ ] Le bloc `aaptOptions { noCompress "tflite" }` empêche la compression lors du build.
