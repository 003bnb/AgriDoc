# AGRI_DOC V1 — Spécification Technique Complète

**Version :** 1.0  
**Statut :** Proposition de spécification (non encore implémentée)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Branche de référence au moment du snapshot :** `devop` (HEAD : `a74307c`, 2026-11-22)  
**Statut du document :** snapshot historique. L'état du dépôt a évolué depuis : la PR #11 a fusionné les commits de Balawe dans `devop` (`578c6e0`), dont le retrait de la permission `INTERNET` ; aucune justification technique supplémentaire n'est documentée dans le corps de cette PR. Les branches `feature/android-architecture` et `feature/camera-camerax` existent désormais.  
**Auteur :** Équipe AgriDoc — Spécification IA (Keumeka, Messi)  
**Dernière révision :** 2026-11-22

---

## 1. Contexte et Périmètre Fonctionnel Validé

### 1.1 Objectif du produit

AgriDoc est une application Android MVP de reconnaissance des problèmes phytosanitaires à partir de photographies de feuilles. L'application fonctionne **100% hors-ligne** : capture, prétraitement, inférence TensorFlow Lite locale, affichage du résultat et persistance Room se font sans connexion Internet.

### 1.2 Cultures prises en charge (V1)

| Culture | Statut V1 | Note |
|---------|-----------|------|
| Manioc | ✅ Prise en charge | Objectif principal |
| Tomate | ✅ Prise en charge | Objectif principal |
| Maïs | ✅ Prise en charge | Objectif principal |
| Autres cultures camerounaises | ❌ Exclu de la V1 | Réservé à une version ultérieure |

### 1.3 Types de problèmes à reconnaître

| Catégorie | Exemples (illustratifs, à confirmer par données) | Statut |
|-----------|---------------------------------------------------|--------|
| Maladies | Mosaïque du manioc, brûlure bactérienne, etc. | ✅ Reconnaissance visuelle |
| Ravageurs | Insectes visibles sur la feuille | ✅ Uniquement si l'espèce est suffisamment visible |
| Dégâts associés aux ravageurs | Trous, galeries, déformations visibles | ✅ Quand visibles |
| Carences nutritionnelles | Jaunissement, nécrose, décoloration | ✅ Reconnaissance visuelle |
| Plante saine | Aucun symptôme visible | ✅ Classe "saine" par culture |
| Inconnu / non exploitable | Image sans partie identifiable de plante | ✅ Rejet ou signalement |

### 1.4 Règles relatives aux photographies

- Seules les photos d'une **feuille ou d'une partie identifiable de la plante** sont acceptées.
- Les photos de **parcelles entières** ne font pas partie du périmètre garanti.
- Les images doivent être **suffisamment nettes et exploitables**.
- Les images ne contenant **pas une partie identifiable de la plante** doivent être rejetées ou signalées comme non exploitables.
- La sélection d'image depuis la galerie n'est pas confirmée pour le MVP (décision à valider).

### 1.5 Règles de reconnaissance des ravageurs

- Reconnaître les **dégâts visibles compatibles** avec des ravageurs.
- Identifier un ravageur **uniquement lorsqu'il est suffisamment visible**.
- Ne **jamais** prétendre identifier une espèce sur la seule base de dégâts non spécifiques.

### 1.6 Limite du diagnostic

Le résultat du modèle est une **aide au diagnostic**, jamais une certitude agronomique. L'application doit afficher explicitement les incertitudes et recommander de consulter un technicien agricole en cas de doute.

---

## 2. État Réel du Dépôt (Audit au 2026-11-22)

### 2.1 Git et branches

| Élément | Valeur observée | Vérifié |
|---------|----------------|---------|
| Branche active | `devop` | ✅ `git status` |
| Dernier commit | `a74307c` — docs: ajout README, 14 issues par rôle, strings.xml enrichi et corrections audit | ✅ `git log --oneline -1` |
| Remote | `https://github.com/003bnb/AgriDoc.git` | ✅ `git remote -v` |
| Working tree | Propre | ✅ `git status` |
| Branches locales | `devop`, `feature/balawe-devops`, `main` | ✅ `git branch -a` |
| Branches de feature existantes | `feature/balawe-devops`, `feature/android-architecture`, `feature/camera-camerax`, `feature/ia-classification` | ✅ `git branch -a` |
| Branches de feature encore absentes | `feature/ui-dashboard`, `feature/data-room-historique`, `feature/qa-test-suite` | ✅ `git branch -a` |
| Auteurs des commits | Uniquement `BALAWE NDIKWA BIENVENU` et `003BNB` (initial) | ✅ `git log --all --format="%an"` |

### 2.2 Fichiers source présents

| Fichier | État | Fonctionnel ? |
|---------|------|---------------|
| `ClassificationModel.java` | Squelette avec `TODO`, résultat hardcodé (`0.95f`) | ❌ Non |
| `Plante.java` | POJO complet (nom, maladie, scoreConfiance, traitementConseille) | ⚠️ Partiel (pas de champ `estReconnu`) |
| `ImageUtils.java` | `resizeBitmap`, `rotateBitmap` présents ; `bitmapToByteBuffer` **absent** | ⚠️ Partiel |
| `EntityHistorique.java` | Entité Room complète | ✅ Oui |
| `DaoHistorique.java` | DAO Room complet | ✅ Oui |
| `AppDatabase.java` | Singleton Room | ✅ Oui |
| `HistoriqueRepository.java` | Repository asynchrone avec callbacks | ✅ Oui |
| `PermissionManager.java` | Classe utilitaire (hasPermission, requestPermission, requestPermissions) | ⚠️ Non intégrée dans les activités |
| `MainActivity.java` | Redirection vers DashboardActivity | ✅ Présent |
| `DashboardActivity.java` | Squelette (`setContentView` uniquement) | ❌ Non |
| `CameraActivity.java` | Squelette (`setContentView` uniquement) | ❌ Non |
| `ResultActivity.java` | Squelette (`setContentView` uniquement) | ❌ Non |
| `HistoriqueActivity.java` | Squelette (`setContentView` uniquement) | ❌ Non |
| Tous les layouts XML | ConstraintLayout racine vide | ❌ Vide |
| `app/src/main/assets/` | Vide (uniquement `.gitkeep`) | ❌ Pas de `.tflite`, pas de `labels.txt` |
| Tests | Uniquement exemples par défaut Android Studio | ⚠️ Pas de tests réels |

### 2.3 Dépendances déclarées (`app/build.gradle`)

| Dépendance | Version | Statut |
|------------|---------|--------|
| Android Gradle Plugin | 8.2.2 | Déclaré |
| Gradle | 8.2 | Déclaré |
| Java | 17 | Déclaré |
| minSdk / targetSdk | 24 / 34 | Déclaré |
| CameraX | 1.3.1 | Déclaré |
| TensorFlow Lite | 2.14.0 | Déclaré |
| TensorFlow Lite Support | 0.4.4 | Déclaré |
| Room | 2.6.1 | Déclaré |
| Material Components | 1.11.0 | Déclaré |
| ConstraintLayout | 2.1.4 | Déclaré |
| RecyclerView | 1.3.2 | Déclaré |
| JUnit | 4.13.2 | Déclaré |
| Espresso | 3.5.1 | Déclaré |
| `aaptOptions { noCompress "tflite" }` | Présent | ✅ Correct |

### 2.4 Documents existants

| Document | Emplacement | État |
|----------|-------------|------|
| README.md | Racine | Présent, décrit l'architecture cible comme "amorcée" |
| PROJECT_TASKS.md | `.github/` | Présent, 14 issues réparties sur 6 rôles |
| 14 issues individuelles | `.github/issues/` | Présentes, critères d'acceptation définis |
| Issue #15 (modèle TFLite et labels) | `feature/balawe-devops` uniquement | Présente, bloquante |
| CAHIER_DES_CHARGES.md | `feature/balawe-devops` uniquement | Présent, 156 lignes |

### 2.5 Contradictions identifiées

| # | Contradiction | Détails | Impact |
|---|---------------|---------|--------|
| C1 | `224×224 RGB` présenté comme acquis | Les issues #09/#10 et le README supposent 224×224, mais le CAHIER_DES_CHARGES et l'issue #15 disent que c'est une "entrée candidate" à confirmer par le modèle retenu | Risque d'incompatibilité entre le prétraitement et le modèle |
| C2 | `issue-02` attribuée à Balawe pour fournir le modèle | L'issue #15 précise que Keumeka et Messi doivent produire le modèle et les labels ; Balawe ne fait que les intégrer | Confusion sur les responsabilités |
| C3 | Permission `INTERNET` déclarée au snapshot `a74307c` | `AndroidManifest.xml` déclarait `android.permission.INTERNET` au snapshot ; cette permission a ensuite été retirée par la PR #11 (`578c6e0`). Aucune justification technique supplémentaire n'est documentée dans le corps de la PR | Point historique, déjà corrigé dans `devop` |
| C4 | Branches de feature annoncées mais inexistantes | Le README et PROJECT_TASKS.md annoncent 6 branches de feature ; seules `devop`, `main` et `feature/balawe-devops` existent | Les autres développeurs n'ont pas de branche de travail |

### 2.6 Responsabilités par rôle (d'après documents)

| Développeur | Rôle officiel | Fichiers responsables | État réel de sa contribution |
|-------------|--------------|----------------------|------------------------------|
| Balawe | Lead DevOps & Architecte | Gradle, Manifest, assets TFLite | ✅ Infrastructure livrée |
| Keumeka | Lead IA (TFLite) | `ClassificationModel.java`, `Plante.java` | ❌ Squelettes uniquement |
| Messi | Data & Inférence | `ImageUtils.java`, prétraitement | ⚠️ Partiel (pas de `bitmapToByteBuffer`) |
| Adoum | UI / UX & Dashboard | Dashboard, Result layouts + activités | ❌ Squelettes/vides |
| Moumoun | Caméra & Capture | CameraActivity, layout caméra, PermissionManager | ❌ Squelette/vide |
| Sam | Persistance, MVVM & QA | Room, Repository, ViewModel, Adapter, Tests | ✅ Repository livré ; ViewModel/Adapter/Tests absents |

---

## 3. Architecture Cible (Recommandée)

### 3.1 Organisation des packages (existante, à conserver)

```
com.agridoc/
├── MainActivity.java
├── data/
│   ├── local/          # Room : AppDatabase, DaoHistorique, EntityHistorique
│   └── repository/     # HistoriqueRepository (asynchrone, callbacks)
├── model/
│   ├── ClassificationModel.java   # Moteur d'inférence TFLite (à réécrire)
│   ├── Plante.java                # POJO métier (à enrichir)
│   ├── LabelProvider.java         # NOUVEAU : lecture labels.txt, mapping index→libellé
│   └── TFLiteModelLoader.java     # NOUVEAU : chargement modèle depuis assets/
├── ui/
│   ├── DashboardActivity.java
│   ├── CameraActivity.java
│   ├── ResultActivity.java
│   └── HistoriqueActivity.java
└── utils/
    ├── ImageUtils.java            # À enrichir : bitmapToByteBuffer
    └── PermissionManager.java     # Existant, à intégrer
```

### 3.2 Principe d'architecture

- **Clean Architecture / MVVM** (déclarée dans le README, partiellement implémentée).
- Les activités **ne contiennent pas** la logique d'inférence ni les requêtes Room directement.
- L'inférence TFLite s'exécute **hors thread UI** (ExecutorService).
- Le Repository est le point d'accès unique aux données Room.
- `ClassificationModel` est un service métier appelé par `ResultActivity`.

### 3.3 Contrats entre composants (à formaliser dans ANDROID_MODEL_CONTRACT.md)

| Composant A | Composant B | Donnée échangée | Responsabilité |
|-------------|-------------|-----------------|----------------|
| `CameraActivity` | `ResultActivity` | Chemin fichier image (`Intent.putExtra("image_path", String)`) | Transmission de la photo capturée |
| `ResultActivity` | `ClassificationModel` | `Bitmap` → `Plante` | Appel d'inférence |
| `ClassificationModel` | `assets/` | `plant_disease_model.tflite`, `labels.txt` | Chargement modèle et labels |
| `ClassificationModel` | `ImageUtils` | `Bitmap` → `ByteBuffer` | Prétraitement tensor |
| `ResultActivity` | `HistoriqueRepository` | `EntityHistorique` → `long` (id) | Persistance du diagnostic |
| `HistoriqueRepository` | `Room` | `EntityHistorique` | Insertion/lecture en base |
| `HistoriqueViewModel` | `HistoriqueActivity` | `LiveData<List<EntityHistorique>>` | Observation de l'historique |

---

## 4. Limites du Système (V1)

| Limite | Description | Justification |
|--------|-------------|---------------|
| Pas de modèle TFLite fourni | Aucun fichier `.tflite` ni `labels.txt` dans le dépôt | Issue #15 bloquante, à livrer par Keumeka/Messi |
| Pas d'entraînement effectué | Aucun dataset, aucune annotation, aucun modèle n'existe dans le dépôt | À créer hors dépôt, puis livré via issue #15 |
| Pas de galerie d'images | La sélection depuis la galerie n'est pas confirmée pour le MVP | Périmètre caméra uniquement |
| Pas de compte utilisateur | Aucune authentification, aucune synchronisation | Contrainte hors-ligne |
| Pas de diagnostic garanti | Le résultat est une aide, pas une certitude agronomique | Exigence produit |
| Pas de cultures hors V1 | Uniquement Manioc, Tomate, Maïs | Périmètre fonctionnel validé |
| Pas de seuil de confiance défini | Aucun seuil n'est configuré dans le code actuel | À déterminer expérimentalement |

---

## 5. Règles de Collaboration Git (Existantes)

| Règle | Source |
|-------|--------|
| `devop` = branche d'intégration principale | README, PROJECT_TASKS.md |
| Aucun commit direct sur `main` | README |
| PR de `feature/*` vers `devop` avant revue et merge | README |
| `strings.xml` : ajouter les nouvelles clés à la fin | README |
| Fichiers de build protégés (accord de Balawe requis) | README |
| Branche de travail pour l'IA : `feature/ia-classification` | README, PROJECT_TASKS.md, issue #15 |

---

## 6. Décisions Techniques Recommandées (Non encore implémentées)

| Décision | Recommandation | Statut |
|----------|---------------|--------|
| Langage | Java 100% (pas de Kotlin) | ✅ Déjà validé |
| UI | XML + ConstraintLayout + Material Design 3 | ✅ Déjà validé |
| Modèle IA | À choisir entre MobileNetV2, MobileNetV3-Small, EfficientNet-Lite0 | ❌ En attente de comparaison expérimentale |
| Quantification | INT8 post-training (recommandé pour mobile) | ❌ À confirmer |
| Dimensions d'entrée | À déterminer par le modèle retenu (pas de 224×224 par défaut) | ❌ Hypothèse non vérifiée |
| Seuil de confiance | À déterminer expérimentalement (pas de 0,60 par défaut) | ❌ À définir |
| Thread d'inférence | ExecutorService (hors thread UI) | ❌ À implémenter |
| Gestion d'erreur | État "non reconnu" dans `Plante`, pas de résultat fictif | ❌ À implémenter |

---

## 7. Documents Spécifications Associés

| Document | Contenu |
|----------|---------|
| `docs/DATASET_SPECIFICATION.md` | Stratégie de données, sources, nomenclature des classes, annotations, collecte, nettoyage, séparation |
| `docs/MODEL_SPECIFICATION.md` | Architectures candidates, stratégie d'entraînement, évaluation, export TFLite, quantification |
| `docs/ANDROID_MODEL_CONTRACT.md` | Contrat IA/Android, prétraitement, entrées/sorties, gestion des erreurs, structures de résultats |
| `docs/ACCEPTANCE_CRITERIA.md` | Critères de validation vérifiables, conditions de livraison, tests obligatoires |

---

## 8. Informations Manquantes

| Information | Impact | Vérification nécessaire |
|-------------|--------|------------------------|
| Fichier `plant_disease_model.tflite` réel | Bloquant pour l'inférence | Issue #15, à livrer par Keumeka/Messi |
| Fichier `labels.txt` réel | Bloquant pour le mapping des classes | Issue #15, à livrer par Keumeka/Messi |
| Contrat d'entrée du modèle (dimensions, type, normalisation) | Bloquant pour `bitmapToByteBuffer` | À documenter par Keumeka/Messi |
| Seuil de confiance acceptable | Impacte la gestion de l'incertitude | À définir par l'équipe IA |
| Liste finale des maladies/ravageurs/carences par culture | Impacte les strings, layouts, historique | À valider avec référent agronomique |
| Format de transmission image (chemin vs URI) | Impacte CameraActivity ↔ ResultActivity | À définir avec Moumoun |
