# Issue #10 : Helper de Prétraitement d'Images (`ImageUtils.java`)

- **Assigné à** : Keumeka (Lead IA) & Messi (Data)
- **Branche** : `feature/ia-classification`
- **Priorité** : Moyenne

## 📌 Description
Développer les fonctions utilitaires dans `ImageUtils.java` pour redimensionner (224x224), pivoter et convertir les Bitmaps en `ByteBuffer` pour TFLite.

## 📋 Critères d'Acceptation
- [ ] Méthode `resizeBitmap(Bitmap original, 224, 224)`.
- [ ] Méthode `rotateBitmap(Bitmap original, float degrees)`.
- [ ] Méthode `bitmapToByteBuffer(Bitmap bitmap)`.
