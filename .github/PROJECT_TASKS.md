# 📋 AgriDoc - Feuille de Route & Reconstitution des Issues par Rôle

Ce document définit l'attribution précise des tâches, la répartition des rôles et les spécifications techniques pour l'équipe de 6 développeurs (Niveau L3) travaillant sur le projet **AgriDoc** (MVP Android de diagnostic des maladies des plantes par IA).

---

## 👥 Répartition des Rôles et des Branches Git

| Développeur | Rôle / Domaine | Branche Git Assignée | Fichiers Principaux gérés |
| :--- | :--- | :--- | :--- |
| **Balawe** | Lead DevOps & Architecte | `devop` / `main` | Gradle, `AndroidManifest.xml`, Assets TFLite |
| **Adoum** | UI / UX & Dashboard | `feature/ui-dashboard` | `DashboardActivity.java`, `activity_dashboard.xml`, `activity_result.xml` |
| **Moumoun** | Caméra & Capture (CameraX) | `feature/camera-camerax` | `CameraActivity.java`, `activity_camera.xml`, `PermissionManager.java` |
| **Keumeka** | Lead IA (TensorFlow Lite) | `feature/ia-classification` | `ClassificationModel.java`, `Plante.java` |
| **Messi** | Data & Inférence | `feature/ia-classification` | `ImageUtils.java`, Pretraitement Inférence |
| **Sam** | Persistance & QA (Room / MVVM / Tests) | `feature/data-room-historique`, `feature/qa-test-suite` | `AppDatabase.java`, `HistoriqueViewModel.java`, `HistoriqueAdapter.java`, Tests |

---

## 📌 Liste des 14 Issues et Critères d'Acceptation

### 👤 1. Balawe (Lead DevOps & Architecte)
- **Issue #01** : `issue-01-balawe-gitflow-setup.md` - Configuration Gitflow et gestion des branches (`devop` / `main`).
- **Issue #02** : `issue-02-balawe-tflite-assets.md` - Intégration du modèle TFLite (`plant_disease_model.tflite`) et `labels.txt` dans `app/src/main/assets/`.

### 🎨 2. Adoum (UI / UX & Dashboard)
- **Issue #03** : `issue-03-adoum-dashboard-layout.md` - Layout `activity_dashboard.xml` en Material Design 3.
- **Issue #04** : `issue-04-adoum-dashboard-navigation.md` - Navigation `DashboardActivity.java` via `Intent`.
- **Issue #05** : `issue-05-adoum-result-layout.md` - Layout `activity_result.xml` (maladie, score et traitement).

### 📷 3. Moumoun (CameraX & Capture)
- **Issue #06** : `issue-06-moumoun-camerax-preview.md` - Intégration `PreviewView` et CameraX dans `CameraActivity.java`.
- **Issue #07** : `issue-07-moumoun-permissions.md` - Gestion dynamique des permissions caméra (`PermissionManager.java`).
- **Issue #08** : `issue-08-moumoun-capture-intent.md` - Capture d'image et transmission vers `ResultActivity` par `Intent` (Chapitre 8).

### 🧠 4. Keumeka (Lead IA) & Messi (Data)
- **Issue #09** : `issue-09-keumeka-messi-tflite-inference.md` - Moteur d'inférence TFLite dans `ClassificationModel.java`.
- **Issue #10** : `issue-10-keumeka-messi-image-utils.md` - Helper d'image `ImageUtils.java` (redimensionnement 224x224, rotation, ByteBuffer).

### 💾 5. Sam (Persistance, MVVM & QA)
- **Issue #11** : `issue-11-sam-historique-recyclerview.md` - `RecyclerView` dans `activity_historique.xml` et layout `item_historique.xml`.
- **Issue #12** : `issue-12-sam-historique-adapter.md` - Développement de `HistoriqueAdapter.java` connecté à `HistoriqueRepository.java`.
- **Issue #13** : `issue-13-sam-historique-viewmodel.md` - Implémentation du pattern MVVM avec `HistoriqueViewModel.java` (Chapitre 9).
- **Issue #14** : `issue-14-sam-qa-unit-espresso-tests.md` - Suite de tests unitaires JVM et d'instrumentation Espresso (Chapitre 8).
