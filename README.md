# 🌱 AgriDoc - MVP Android de Diagnostic des Maladies des Plantes par IA

## 📌 Présentation du Projet

**AgriDoc** est une application mobile Android MVP (Minimum Viable Product) conçue pour aider les agriculteurs et producteurs agricoles à diagnostiquer instantanément les maladies des plantes à partir d'une simple prise de vue photographique des feuilles touchées.

### 🎯 Public Cible & Contraintes Principales
- **Public cible** : Agriculteurs, exploitants agricoles et techniciens de terrain.
- **Contrainte Majeure** : **100% Hors-Ligne (Offline First)**. L'application exécute l'inférence IA directement sur le processeur du smartphone sans nécessiter de connexion Internet, garantissant une utilisation optimale même dans les zones rurales reculées.

---

## 🛠️ Stack Technique

- **Langage de programmation** : Java (Standards du cours, 100% Java, pas de Kotlin).
- **Interface Utilisateur (UI)** : XML / Layouts Android standards (pas de Jetpack Compose).
- **Environnement de Build** : Android Studio avec **AGP 8.2.2** et **Gradle 8.2** (Configuration Groovy).
- **Capture Caméra** : Jetpack CameraX 1.3.1 (`camera-core`, `camera-camera2`, `camera-lifecycle`, `camera-view`).
- **Intelligence Artificielle On-Device** : TensorFlow Lite 2.14.0 & TFLite Support Library.
- **Base de Données Locale** : Room Database 2.6.1 / SQLite.
- **Design System** : Material Design 3 (Theme.Material3.DayNight.NoActionBar) & ConstraintLayout.

---

## 📂 Architecture du Projet

Le projet suit une architecture moderne en couches (Clean Architecture / MVVM) répartie dans les packages suivants sous `com.agridoc` :

```text
com.agridoc/
├── MainActivity.java                <-- Activité d'entrée (redirection vers le Dashboard)
├── data/
│   ├── local/                      <-- Base de données Room (AppDatabase, DaoHistorique, EntityHistorique)
│   └── repository/                 <-- Gestionnaire de données asynchrones (HistoriqueRepository)
├── model/
│   ├── ClassificationModel.java    <-- Moteur d'inférence TensorFlow Lite (.tflite)
│   └── Plante.java                 <-- Objet Métier POJO (Nom, Maladie, Score, Traitement)
├── ui/
│   ├── DashboardActivity.java      <-- Écran d'accueil principal
│   ├── CameraActivity.java         <-- Prise de vue temps réel avec CameraX
│   ├── ResultActivity.java         <-- Affichage des résultats du diagnostic
│   └── HistoriqueActivity.java     <-- Consultation de l'historique des scannages
└── utils/
    ├── ImageUtils.java             <-- Traitement et prétraitement des images (224x224, rotation)
    └── PermissionManager.java      <-- Gestion dynamique des permissions (Caméra, Stockage)
```

---

## 👥 Répartition des Rôles dans l'Équipe

| Développeur | Rôle / Domaine | Branche Git Assignée | Responsabilités Principales |
| :--- | :--- | :--- | :--- |
| **Balawe** | Lead DevOps & Architecte | `devop` / `main` | Architecture globale, configuration Gradle/Gitflow, intégration du modèle `.tflite`. |
| **Keumeka** | Lead IA | `feature/ia-classification` | Réseau de neurones TFLite, inférence et classification dans `ClassificationModel.java`. |
| **Messi** | Data & Inférence | `feature/ia-classification` | Prétraitement d'images 224x224, conversion Bitmap/ByteBuffer dans `ImageUtils.java`. |
| **Adoum** | UI / UX & Dashboard | `feature/ui-dashboard` | Conception des interfaces `activity_dashboard.xml`, `activity_result.xml` et navigation. |
| **Moumoun** | Caméra & Capture | `feature/camera-camerax` | Flux temps réel CameraX, prise de vue et transmission par `Intent` (`CameraActivity.java`). |
| **Sam** | Persistance, MVVM & QA | `feature/data-room-historique`, `feature/qa-test-suite` | `RecyclerView`, `HistoriqueViewModel.java` (MVVM), suite de tests unitaires et Espresso. |

---

## 🚀 Instructions de Démarrage

### 1. Cloner le projet
```bash
git clone https://github.com/votre-compte/AgriDoc.git
cd AgriDoc
```

### 2. Se placer sur la branche d'intégration `devop`
```bash
git checkout devop
git pull origin devop
```

### 3. Créer sa branche de fonctionnalité individuelle
```bash
# Exemple pour le développeur travaillant sur la caméra :
git checkout -b feature/camera-camerax
```

---

## 📜 Règles de Collaboration et Gitflow

1. **Branche d'Intégration** : La branche **`devop`** est la branche d'intégration principale. Aucun commit direct ne doit être fait sur `main`.
2. **Règle sur `res/values/strings.xml`** : Pour éviter tout conflit Git lors des fusions, ajoutez impérativement vos nouvelles clés de texte **à la fin du fichier**, sous le bloc de commentaires prévu à cet effet.
3. **Fichiers de Build Strictement Protégés** : Il est **strictement interdit** de modifier les fichiers `build.gradle` (racine et module) ou `gradle-wrapper.properties` sans l'accord préalable de **Balawe (Lead DevOps)**.
4. **Pull Requests** : Toute fonctionnalité finalisée doit faire l'objet d'une Pull Request de `feature/votre-fonctionnalite` vers `devop` avant revue et merge.
