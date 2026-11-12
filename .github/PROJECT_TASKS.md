# 📋 AgriDoc - Feuille de Route & Reconstitution des Issues par Rôle

Ce document définit l'attribution précise des tâches, la répartition des rôles et les spécifications techniques pour l'équipe de 6 développeurs (Niveau L3) travaillant sur le projet **AgriDoc** (MVP Android de diagnostic des maladies des plantes par IA).

---

## 👥 Répartition des Rôles et des Branches Git

| Développeur | Rôle / Domaine | Branche Git Assignée | Fichiers Principaux gérés |
| :--- | :--- | :--- | :--- |
| **Balawe** | Lead DevOps & Architecte | `develop` / `main` | Gradle, `AndroidManifest.xml`, Assets TFLite |
| **Sam** | QA & Automation (Tests) | `feature/qa-test-suite` | `test/`, `androidTest/` |
| **Dev 3** | UI / UX & Dashboard | `feature/ui-dashboard` | `DashboardActivity.java`, `activity_dashboard.xml` |
| **Dev 4** | Caméra & Capture (CameraX) | `feature/camera-camerax` | `CameraActivity.java`, `activity_camera.xml`, `PermissionManager.java` |
| **Dev 5** | IA & Inférence (TFLite & Images) | `feature/ia-classification` | `ClassificationModel.java`, `ImageUtils.java`, `Plante.java` |
| **Dev 6** | Données & Historique (Room DB) | `feature/data-room-historique` | `AppDatabase.java`, `EntityHistorique.java`, `DaoHistorique.java`, `HistoriqueActivity.java` |

---

## 📌 Liste des Issues et Critères d'Acceptation

### 👤 1. Balawe (Lead DevOps & Architecte)

#### **Issue #01 : Configuration Gitflow et Gestion du Dépôt**
* **Branche** : `develop`
* **Objectif** : Vérifier la structure du dépôt, s'assurer que `.gitignore` exclut les fichiers temporaires, et créer la branche `develop`.
* **Critères d'acceptation** :
  * Branche `develop` initialisée et poussée sur le dépôt distant.
  * Aucun fichier `.idea/`, `.gradle/` ou `build/` dans le suivi Git.

#### **Issue #02 : Intégration du Modèle TensorFlow Lite (`plant_disease_model.tflite`)**
* **Branche** : `feature/devops-assets` (issue de `develop`)
* **Objectif** : Déposer le fichier de modèle quantifié `.tflite` et `labels.txt` dans le dossier `app/src/main/assets/`.
* **Critères d'acceptation** :
  * Le modèle `.tflite` est placé dans `app/src/main/assets/`.
  * La règle `aaptOptions { noCompress "tflite" }` dans `app/build.gradle` est préservée.

---

### 🧪 2. Sam (QA & Automation)

#### **Issue #03 : Suite de Tests Unitaires (`ExempleUnitTest.java`)**
* **Branche** : `feature/qa-test-suite`
* **Objectif** : Implémenter des tests unitaires validant la création des POJO (`Plante`), la transformation d'images et la logique métier de l'historique.
* **Critères d'acceptation** :
  * Test d'instanciation et getters/setters de `PlanteTest.java`.
  * Exécution réussie via `./gradlew testDebugUnitTest`.

#### **Issue #04 : Tests d'Instrumentation Espresso (`ExempleInstrumentedTest.java`)**
* **Branche** : `feature/qa-test-suite`
* **Objectif** : Valider le lancement de `MainActivity` et la redirection automatique vers `DashboardActivity`.
* **Critères d'acceptation** :
  * Test Espresso vérifiant que l'écran `DashboardActivity` s'affiche au démarrage.
  * Exécution réussie sur émulateur ou appareil de test.

---

### 🎨 3. Développeur 3 (UI / UX & Dashboard)

#### **Issue #05 : Conception Layout Dashboard (`activity_dashboard.xml`)**
* **Branche** : `feature/ui-dashboard`
* **Objectif** : Concevoir une interface moderne et intuitive en Material Design 3.
* **Critères d'acceptation** :
  * Utilisation de `ConstraintLayout`.
  * Présence de deux boutons principaux : "Diagnostic Caméra" et "Voir l'Historique".
  * Respect des couleurs définies dans `colors.xml` (`green_primary`).

#### **Issue #06 : Logique de Navigation (`DashboardActivity.java`)**
* **Branche** : `feature/ui-dashboard`
* **Objectif** : Connecter les boutons du Dashboard aux activités `CameraActivity` et `HistoriqueActivity` via des `Intent`.
* **Critères d'acceptation** :
  * Clic sur "Scanner" ouvre `CameraActivity`.
  * Clic sur "Historique" ouvre `HistoriqueActivity`.

---

### 📷 4. Développeur 4 (Caméra & Capture - CameraX)

#### **Issue #07 : Intégration CameraX et Prévisualisation (`activity_camera.xml` & `CameraActivity.java`)**
* **Branche** : `feature/camera-camerax`
* **Objectif** : Afficher le flux vidéo de la caméra arrière en plein écran avec un bouton de prise de vue.
* **Critères d'acceptation** :
  * `PreviewView` intégré dans `activity_camera.xml`.
  * Démarrage du `ProcessCameraProvider` lié au lifecycle de l'activité.
  * Capture d'image fonctionnelle et transfert vers `ResultActivity` via `Intent` (URI ou byte array).

#### **Issue #08 : Gestion Dynamique des Permissions (`PermissionManager.java`)**
* **Branche** : `feature/camera-camerax`
* **Objectif** : Vérifier et demander la permission `android.permission.CAMERA` au runtime.
* **Critères d'acceptation** :
  * Appel de `PermissionManager.hasPermission()` avant l'ouverture de la caméra.
  * Demande de permission si non accordée avec message explicatif en cas de refus.

---

### 🧠 5. Développeur 5 (IA & Traitement d'Image - TFLite)

#### **Issue #09 : Moteur d'Inférence TFLite (`ClassificationModel.java`)**
* **Branche** : `feature/ia-classification`
* **Objectif** : Charger le modèle `.tflite` depuis les assets et exécuter l'inférence sur le Bitmap d'une feuille.
* **Critères d'acceptation** :
  * Chargement du fichier modèle via `ByteBuffer` ou `FileUtil`.
  * Entrée : Bitmap 224x224 RGB.
  * Sortie : Instance de `Plante` contenant le nom de la maladie, le score de confiance et le traitement conseillé.

#### **Issue #10 : Helpers d'Images (`ImageUtils.java`)**
* **Branche** : `feature/ia-classification`
* **Objectif** : Fournir les méthodes utilitaires pour redimensionner, pivoter et convertir les bitmaps.
* **Critères d'acceptation** :
  * Méthode `resizeBitmap(Bitmap original, 224, 224)`.
  * Méthode `rotateBitmap(Bitmap original, float degrees)`.

---

### 💾 6. Développeur 6 (Persistance & Historique - Room DB)

#### **Issue #11 : Interface de l'Historique (`activity_historique.xml` & `HistoriqueAdapter.java`)**
* **Branche** : `feature/data-room-historique`
* **Objectif** : Afficher la liste des diagnostics enregistrés dans un `RecyclerView`.
* **Critères d'acceptation** :
  * `RecyclerView` configuré dans `activity_historique.xml`.
  * Item layout `item_historique.xml` affichant la vignette, la date, le nom de la plante et le résultat.

#### **Issue #12 : Intégration Room & Repository (`HistoriqueActivity.java`)**
* **Branche** : `feature/data-room-historique`
* **Objectif** : Charger les données asynchrones via `HistoriqueRepository` et mettre à jour l'adaptateur.
* **Critères d'acceptation** :
  * Récupération des enregistrements via `HistoriqueRepository.getAllDiagnostics()`.
  * Insertion automatique d'un nouveau diagnostic lors de la validation sur `ResultActivity`.
