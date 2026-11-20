# Issue #02 : Intégration du Modèle TFLite dans Assets

- **Assigné à** : Balawe (Lead DevOps & Architecte)
- **Branche** : `feature/balawe-devops` (Pull Request vers `devop`)
- **Bloquée par** : Issue #15 — livraison du modèle TFLite réel, des labels et du contrat d’inférence par Keumeka et Messi.
- **Priorité** : Bloquante tant que l’Issue #15 n’est pas terminée.

## 📌 Description
Après réception et validation des artefacts IA de l’Issue #15, intégrer le modèle TensorFlow Lite quantifié (`plant_disease_model.tflite`) et son fichier de labels (`labels.txt`) dans `app/src/main/assets/`. Ne créer aucun fichier de remplacement si les artefacts ne sont pas disponibles.

## 📋 Critères d'Acceptation
- [ ] Modèle `plant_disease_model.tflite` présent dans `app/src/main/assets/`.
- [ ] Fichier `labels.txt` présent dans `app/src/main/assets/`.
- [ ] Règle `aaptOptions { noCompress "tflite" }` validée dans `app/build.gradle`.
