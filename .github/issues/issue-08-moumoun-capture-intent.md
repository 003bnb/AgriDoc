# Issue #08 : Capture d'Image et Transmission par Intent (Chapitre 8)

- **Assigné à** : Moumoun (CameraX & Capture)
- **Branche** : `feature/camera-camerax`
- **Priorité** : Haute

## 📌 Description
Implémenter la prise de vue via `ImageCapture` et transmettre le chemin du fichier image ou l'URI à `ResultActivity` via `Intent.putExtra("image_path", ...)`.

## 📋 Critères d'Acceptation
- [ ] Capture d'image instantanée lors de l'appui sur le bouton de déclenchement.
- [ ] Sauvegarde temporaire du fichier image.
- [ ] Transmission du chemin via `Intent.putExtra("image_path", path)` vers `ResultActivity`.
