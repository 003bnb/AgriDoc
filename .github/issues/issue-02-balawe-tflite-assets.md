# Issue #02 : Intégration du Modèle TFLite dans Assets

- **Assigné à** : Balawe (Lead DevOps & Architecte)
- **Branche** : `feature/devops-assets`
- **Priorité** : Moyenne

## 📌 Description
Placer le fichier modèle TensorFlow Lite quantifié (`plant_disease_model.tflite`) ainsi que le fichier d'étiquettes des maladies (`labels.txt`) dans le dossier `app/src/main/assets/`.

## 📋 Critères d'Acceptation
- [ ] Modèle `plant_disease_model.tflite` présent dans `app/src/main/assets/`.
- [ ] Fichier `labels.txt` présent dans `app/src/main/assets/`.
- [ ] Règle `aaptOptions { noCompress "tflite" }` validée dans `app/build.gradle`.
