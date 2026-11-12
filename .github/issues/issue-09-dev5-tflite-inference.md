# Issue #09 : Moteur d'Inférence TFLite (`ClassificationModel.java`)

- **Assigné à** : Développeur 5 (IA & Inférence)
- **Branche** : `feature/ia-classification`
- **Priorité** : Bloquante

## 📌 Description
Implémenter la logique d'analyse de l'image de la plante avec TensorFlow Lite dans `ClassificationModel.java`.

## 📋 Critères d'Acceptation
- [ ] Chargement du modèle `.tflite` depuis les assets.
- [ ] Exécution de l'inférence sur un `Bitmap` de 224x224 pixels.
- [ ] Retour du résultat sous forme d'un objet `Plante` (maladie, score de confiance, recommandation).
