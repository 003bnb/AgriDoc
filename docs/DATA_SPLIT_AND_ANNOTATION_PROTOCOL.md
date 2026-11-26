# DATA_SPLIT_AND_ANNOTATION_PROTOCOL — Format d'Annotation et Séparation des Données AgriDoc V1

**Version :** 1.0  
**Statut :** Proposition (aucun dataset n'a été constitué à ce jour)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi)  
**Dernière révision :** 2026-11-22

---

## 1. Objectif

Définir le format d'annotation, les règles de qualité et le protocole de séparation des données pour l'entraînement du modèle AgriDoc V1. **Aucune donnée n'a été constituée à ce jour.** Ce document prépare la préparation future des données.

---

## 2. Format d'Annotation

### 2.1 Fichier de métadonnées principal

Chaque image d'entraînement doit être accompagnée d'une entrée dans un fichier de métadonnées centralisé (CSV ou JSONL). Un exemple de structure JSONL :

```jsonl
{"image_id": "CM_20261122_001", "source": "collecte_camerounaise", "culture": "MANIOC", "type_probleme": "MALADIE", "classe": "MANIOC_MALADIE_MOSAIQUE", "region": "Centre", "localite": "Mbalmayo", "date_capture": "2026-11-22", "stade_developpement": "mature", "variete": null, "organe_photographie": "Feuille_dessus", "symptomes_observes": "Marbrures vert clair sur la feuille", "diagnostic_confirme": true, "validation_agronomique": true, "valideur_id": "AGR_001", "role_valideur": "Agronome", "qualite_image": "BONNE", "luminosite": "ADEQUATE", "nettete": "NETTE", "appareil": "Samsung Galaxy A52", "consentement_agriculteur": true, "ensemble": "train", "fichier_image": "CM_20261122_001.jpg"}
```

Pour les images provenant de sources publiques (PlantVillage), les champs spécifiques à la collecte camerounaise (`region`, `localite`, `consentement_agriculteur`, etc.) peuvent être laissés à null ou renseignés avec la provenance publique.

### 2.2 Champs obligatoires et optionnels

| Champ | Type | Obligatoire | Source publique | Collecte camerounaise |
|-------|------|-------------|-----------------|----------------------|
| `image_id` | String | Oui | Oui | Oui |
| `source` | String | Oui | Oui | Oui |
| `source_url` | String | Non | Oui (si disponible) | Non |
| `culture` | String | Oui | Oui | Oui |
| `type_probleme` | String | Oui | Oui | Oui |
| `classe` | String | Oui | Oui | Oui |
| `date_capture` | Date | Non | Non | Oui |
| `localisation` | String | Non | Non | Oui |
| `validation_agronomique` | Boolean | Oui | Oui (si déjà annoté) | Oui |
| `valideur_id` | String | Non | Non | Oui |
| `role_valideur` | String | Non | Non | Oui |
| `qualite_image` | String | Oui | Oui | Oui |
| `luminosite` | String | Non | Non | Oui |
| `nettete` | String | Non | Non | Oui |
| `ensemble` | String | Oui | Oui | Oui |

### 2.3 Valeurs autorisées

| Champ | Valeurs autorisées |
|-------|-------------------|
| `source` | `PlantVillage`, `PlantDoc`, `collecte_camerounaise` |
| `culture` | `MANIOC`, `TOMATE`, `MAIS`, `GLOBAL` |
| `type_probleme` | `MALADIE`, `RAVAGEUR`, `DEGAT_RAVAGEUR`, `CARENCE`, `SAIN`, `INCONNU` |
| `qualite_image` | `EXCELLENTE`, `BONNE`, `MOYENNE`, `EXPLOITABLE_DIFFICILE` |
| `luminosite` | `ADEQUATE`, `INSUFFISANTE`, `EXCESSIVE` |
| `nettete` | `NETTE`, `LEGEREMENT_FLOUE`, `FLOUE` |
| `ensemble` | `train`, `validation`, `test` |
| `diagnostic_confirme` | `true`, `false` |
| `validation_agronomique` | `true`, `false` |
| `consentement_agriculteur` | `true`, `false` |

### 2.4 Format des noms de fichiers images

Convention de nommage recommandée :
```
{CODE_SOURCE}_{DATE}_{NUMERO}.jpg
```

Exemple : `PV_20261122_001.jpg` (PlantVillage), `CM_20261122_001.jpg` (collecte camerounaise).

Les extensions acceptées : `.jpg`, `.jpeg`, `.png`.

---

## 3. Règles de Qualité des Annotations

### 3.1 Règle d'un seul label principal

Chaque image doit être assignée à **une seule classe**. Si plusieurs problèmes sont présents sur une même image :
- Assigner à la classe la plus significative (la plus sévère ou la plus caractéristique pour le diagnostic)
- Ou exclure l'image si l'ambiguïté est trop grande

### 3.2 Validation agronomique

- **Aucune image ne peut être utilisée pour l'entraînement sans `validation_agronomique = true`**, sauf les images provenant de sources publiques déjà annotées (PlantVillage) dont la provenance est documentée.
- Pour la collecte camerounaise, le référent agronomique doit valider chaque label avant intégration.

### 3.3 Pas de classe "fourre-tout"

Une image présentant plusieurs problèmes simultanés doit être assignée à la classe la plus significative, ou exclue si l'ambiguïté est trop grande. Il n'existe pas de classe "multiple_problemes" dans la nomenclature V1.

### 3.4 Images hors domaine

Les images ne montrant pas une feuille ou une partie identifiable de plante sont assignées à `GLOBAL_INCONNU` ou `GLOBAL_NON_EXPLOITABLE`, jamais à une classe de maladie spécifique.

### 3.5 Qualité minimale

Les images avec `qualite_image = EXPLOITABLE_DIFFICILE` ou `nettete = FLOUE` doivent être examinées au cas par cas avant inclusion. Une image trop floue pour distinguer les symptômes ne doit pas être intégrée.

---

## 4. Protocole de Séparation des Données

### 4.1 Principe général

La séparation entre entraînement, validation et test doit prévenir toute fuite de données. Une fuite se produit lorsque des informations du jeu de test influencent l'entraînement, directement ou indirectement.

### 4.2 Unités de séparation (par ordre de priorité)

| Niveau | Description | Règle |
|--------|-------------|-------|
| 1. Plante | Toutes les images d'une même plante individuelle | Doivent être dans le même ensemble |
| 2. Parcelle | Toutes les images d'une même parcelle | Doivent être dans le même ensemble |
| 3. Exploitation | Toutes les images d'une même exploitation agricole | Doivent être dans le même ensemble |
| 4. Session de prise de vue | Toutes les images prises lors d'une même session | Doivent être dans le même ensemble |
| 5. Source | Toutes les images d'une même source publique | Recommandé de garder dans le même ensemble pour éviter les biais de source |

**Règle d'or :** Si deux images proviennent de la même plante, elles ne peuvent pas être séparées entre train et test.

### 4.3 Proportions (à ajuster selon les effectifs)

| Ensemble | Pourcentage indicatif | Usage |
|----------|----------------------|-------|
| Entraînement | 70% | Apprentissage du modèle |
| Validation | 15% | Ajustement des hyperparamètres, sélection du meilleur modèle |
| Test | 15% | Évaluation finale non biaisée |

**Ces proportions sont indicatives.** Si une classe contient peu d'images (moins de 50), une autre stratégie (validation croisée k-fold) peut être préférée.

### 4.4 Représentativité dans chaque ensemble

| Exigence | Description |
|----------|-------------|
| Chaque culture représentée | Manioc, Tomate, Maïs doivent être présents dans train, validation et test |
| Chaque classe représentée | Chaque classe doit avoir au moins 5 images dans le test (idéalement 20+) |
| Images camerounaises dans tous les ensembles | Si collecte camerounaise effectuée, ses images doivent être réparties dans train, validation et test |
| Variété d'éclairage et d'appareils | Répartie dans tous les ensembles |

### 4.5 Prévention des quasi-doublons

Les images presque identiques (même plante, angles très proches, même session) ne doivent pas se retrouver dans des ensembles différents. Elles doivent être assignées au même ensemble.

---

## 5. Déduplication

### 5.1 Doublons exacts

- Utiliser une empreinte cryptographique (SHA-256 ou MD5) sur le contenu du fichier pour détecter les doublons exacts.
- Ne garder qu'un exemplaire par image unique.

### 5.2 Quasi-doublons

- Utiliser un hachage perceptuel (pHash) pour détecter les images visuellement similaires mais pas identiques.
- Les quasi-doublons détectés doivent être assignés au même ensemble (train, validation OU test).

### 5.3 Vérification croisée entre sources

- Comparer les images collectées au Cameroun avec celles des sources publiques pour éviter qu'une même image apparaisse deux fois.
- Utiliser pHash pour cette vérification croisée.

---

## 6. Ensemble de Test Camerounais Indépendant

Si la collecte camerounaise est effectuée, un **ensemble de test camerounais indépendant** doit être constitué. Cet ensemble :
- Ne contient que des images collectées au Cameroun
- N'est jamais utilisé pendant l'entraînement ni la validation
- Sert à évaluer la généralisation du modèle aux conditions réelles camerounaises
- Doit contenir au moins 20 images par classe retenue (si possible)

---

## 7. Format d'Export pour l'Entraînement

À la fin de la préparation, le dataset doit être organisé comme suit :

```
dataset/
├── train/
│   ├── MANIOC_SAIN/
│   ├── MANIOC_MALADIE_MOSAIQUE/
│   ├── TOMATE_SAIN/
│   ├── ...
│   └── GLOBAL_INCONNU/
├── validation/
│   ├── (même structure)
│   └── ...
└── test/
    ├── (même structure)
    └── ...
metadata.csv  # ou metadata.jsonl
```

---

## 8. Contrôle Qualité Avant Entraînement

Avant de lancer l'entraînement, les vérifications suivantes doivent être effectuées :

| Vérification | Méthode | Critère de succès |
|--------------|---------|-------------------|
| Aucun doublon entre ensembles | Comparer les empreintes SHA-256 | Zéro doublon entre train/validation/test |
| Aucune image partagée | Vérifier les `image_id` par ensemble | Zéro image présente dans deux ensembles |
| Chaque classe a des images en test | Compter par classe dans test | ≥ 20 images par classe pour une validation statistique ; ≥ 5 images minimum pour un calcul non vide, avec évaluation prudente ou validation croisée |
| Validation agronomique | Vérifier le champ `validation_agronomique` | 100% des images d'entraînement ont ce champ = true |
| Licence documentée | Vérifier le champ `source` et `source_url` | 100% des images ont une source documentée |
| Pas de classe fictive | Revue de la nomenclature | Toutes les classes appartiennent à la nomenclature V1 validée |

---

## 9. Informations Manquantes

| Information | Impact | Vérification nécessaire |
|-------------|--------|------------------------|
| Nombre total d'images disponibles | Détermine si les proportions 70/15/15 sont pertinentes | À vérifier après constitution du dataset |
| Nombre d'images par classe | Détermine si certaines classes doivent être exclues | À vérifier après constitution du dataset |
| Disponibilité d'outils de pHash | Nécessaire pour la déduplication | À vérifier dans l'environnement d'entraînement |
