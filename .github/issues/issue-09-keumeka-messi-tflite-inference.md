# Issue #09 : Inférence TFLite (`ClassificationModel.java`)

- **Assigné à** : Keumeka (Lead IA) & Messi (Data)
- **Branche** : `feature/ia-classification`
- **Priorité** : Bloquante

## 📌 Description
Charger le modèle `.tflite` depuis assets/ et exécuter l'inférence réseau de neurones sur un `Bitmap` de feuille.

## 📋 Critères d'Acceptation
- [ ] Chargement du modèle via `Interpreter` TFLite.
- [ ] Traitement du tableau d'entrée float/byte 224x224 RGB.
- [ ] Restitution d'un objet `Plante` avec le nom de maladie, score de confiance et traitement.
