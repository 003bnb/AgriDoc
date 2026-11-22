# PHASE B — Architecture du sous-système IA AgriDoc V1

**Version :** 1.0
**Date :** 2026-11-22
**Auteur :** Lead IA / ML / TensorFlow Lite
**Statut :** Choix techniques justifiés à partir des données réellement vérifiées en Phase A. **Aucun modèle entraîné, aucune performance annoncée.**

---

## 1. Décision critique préalable

L'architecture dépend du jeu de données réellement disponible. La Phase A montre que :

- **CCMT** (CC BY 4.0, 24 881 images brutes) est la seule source vérifiée couvrant **les trois cultures V1 et des ravageurs visibles** ;
- il n'existe **aucune image de carence**, **aucune image négative**, **aucune image camerounaise** ;
- PlantVillage est juridiquement non confirmé, PlantDoc a des classes quasi vides (spider mites : 2 images).

**Décision :** retenir une **architecture hiérarchique à deux étages avec rejet explicite**, mais prévoir un **baseline plat unique** comme point de comparaison obligatoire en Phase D. Le choix final se fera sur F1 macro et taux de faux diagnostics positifs, pas sur l'accuracy globale.

---

## 2. Options étudiées

| Option | Avantages | Limites au regard des données V1 | Verdict |
|---|---|---|---|
| **A. Classification plate multi-classes** (1 sortie softmax sur N classes) | Simple à entraîner/export TFLite ; une seule inférence | Mélange culture + symptôme + ravageur ; confusion inter-cultures ; déséquilibre 208–2 614 images ; pas de sortie « culture seule » ni de rejet structuré | ❌ Non retenue comme architecture finale ; ✅ conservée comme **baseline de comparaison** |
| **B. Hiérarchique 2 étages** (culture → diagnostic) | Sépare la culture du symptôme ; permet un seuil par culture ; erreur de culture détectable ; coût d'inférence encore faible (2 petits modèles ou 1 modèle à têtes) | Nécessite des libellés de culture cohérents (OK dans CCMT) et assez d'images par culture (OK : 7 508 / 5 389 / 5 435) | ✅ **Retenu pour V1** |
| **C. Multi-têtes** (culture + catégorie + classe) | Sorties explicites pour chaque dimension | Exige 3 annotations indépendantes par image ; aucun jeu vérifié ne les fournit ; sur-ingénierie | ❌ Reporté V2 |
| **D. Multi-labels** | Représente co-infections | Aucune annotation multi-label vérifiée ; métriques complexes | ❌ Reporté V2 |
| **E. Détection d'objets** (YOLO/SSD TFLite) | Localise le ravageur sur la feuille | Aucune bounding box dans CCMT/PlantDoc/PlantVillage ; modèle lourd ; hors MVP | ❌ Reporté V2 |
| **F. Zéro-shot / vision-langage** | Pas d'entraînement | Incompatible avec contrainte 100 % hors-ligne et TFLite 2.14.0 | ❌ Exclu |

---

## 3. Architecture retenue

```text
Image caméra (Bitmap)
        │
        ▼
┌───────────────────────────────────────────────┐
│  ÉTAGE 0 — Contrôle d'entrée (déterministe)   │
│  taille, netteté, exposition, plante visible  │
│  → ACCEPTÉ | NON_EXPLOITABLE | ENTREE_ERREUR  │
└───────────────────────────────────────────────┘
        │ ACCEPTÉ
        ▼
┌───────────────────────────────────────────────┐
│  ÉTAGE 1 — Classificateur de culture          │
│  MANIOC | TOMATE | MAIS | INCONNU             │
│  + confiance culture + seuil culture          │
└───────────────────────────────────────────────┘
        │ culture acceptée
        ▼
┌───────────────────────────────────────────────┐
│  ÉTAGE 2 — Classificateur diagnostique        │
│  (un modèle léger par culture, ou une tête    │
│   conditionnée par la culture)                │
│  classes : SAIN / MALADIE / RAVAGEUR_VISIBLE  │
│            / DEGAT_RAVAGEUR / CARENCE         │
└───────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────┐
│  ÉTAGE 3 — Fiabilité et décision              │
│  confiance calibrationnée + entropie +        │
│  seuil issu de la validation + hors-domaine  │
│  → FIABLE | INCERTAIN | INCONNU | ERREUR      │
└───────────────────────────────────────────────┘
```

### 3.1 Étape 0 — contrôle d'entrée

Règles déterministes, sans réseau de neurones :

- image décodable, dimensions minimales, canaux RGB ;
- netteté insuffisante (variance du Laplacian ou équivalent sans dépendance lourde) → `NON_EXPLOITABLE` ;
- exposition extrême → `NON_EXPLOITABLE` ;
- absence de partie identifiable de plante → `INCONNU` (à entraîner avec les images négatives de la Phase C).

Cette étape empêche qu'une photo de main ou de ciel reçoive un diagnostic de maladie.

### 3.2 Étape 1 — culture

Classes : `MANIOC`, `TOMATE`, `MAIS`, `INCONNU`.
Justification : CCMT fournit des dossiers par culture avec effectifs suffisants (7 508 / 5 389 / 5 435), ce qui rend l'apprentissage de cette distinction réaliste. Le seuil de la classe `INCONNU` est calibré sur la validation (Phase E).

### 3.3 Étape 2 — diagnostic par culture

Le classifieur ne reçoit que les classes de la culture détectée. Cela réduit le nombre de classes simultanées et les confusions inter-cultures.

**Règle absolue pour les ravageurs :**

- une classe `RAVAGEUR_VISIBLE` n'est retournée **que si l'insecte lui-même est visible sur l'image** ;
- si seuls des trous, galeries ou déformations sont visibles, la sortie est `DEGAT_RAVAGEUR` avec mention explicite **« espèce non identifiée »** ;
- **aucune espèce n'est déduite d'un dégât non spécifique** ;
- si l'image ne montre ni insecte ni dégât interprétable, le modèle retourne `INCERTAIN`, pas un ravageur.

Conséquence sur CCMT : les classes `Fall armyworm`, `Grasshopper`, `Leaf beetle`, `Green mite` doivent être **auditées à l'image** (Phase C). Celles où seul le dégât est visible seront réétiquetées `DEGAT_RAVAGEUR` par culture, pas `RAVAGEUR_VISIBLE`.

---

## 4. Contrat d'entrée/sortie indépendant d'Android

Ce contrat est **proposé** ; il sera figé après export du modèle réel (Phase F). Aucune valeur n'est à coder en dur dans l'application avant cette validation.

### 4.1 Entrée

| Paramètre | Valeur proposée | Statut |
|---|---|---|
| Type tenseur | `float32` | À confirmer par le modèle réel |
| Forme | `[1, H, W, 3]` | H/W à confirmer (224×224 est une **hypothèse**, pas un acquis) |
| Ordre canaux | RGB | À confirmer |
| Plage pixels | `[0, 1]` ou `[-1, 1]` ou INT8 quantifié | À confirmer par le contrat d'export |
| Prétraitement | resize, rotation EXIF, conversion RGB, normalisation | Implémenté côté IA ; l'intégration Android reste à Balawe |

### 4.2 Sortie (structure logique, pas une classe Java)

```json
{
  "statut": "FIABLE | INCERTAIN | INCONNU | ENTREE_ERREUR | INFERENCE_ERREUR",
  "culture": "MANIOC | TOMATE | MAIS | null",
  "categorie": "SAIN | MALADIE | RAVAGEUR_VISIBLE | DEGAT_RAVAGEUR | CARENCE | INCONNU | NON_EXPLOITABLE | null",
  "classe": "-identifiant de la nomenclature-",
  "confiance": 0.0,
  "incertitude": 0.0,
  "seuil_utilise": 0.0,
  "justification": "texte court, ex. 'insecte non visible, degat seul'",
  "modele": {"nom": "...", "version": "...", "contrat": "..."}
}
```

Règles d'interprétation :

- `confiance` est une **estimation calibrationnée**, jamais une probabilité de vérité agronomique ;
- un score de 0,95 **ne signifie pas** « diagnostic certain à 95 % » ; l'UI devra l'afficher comme indicateur de fiabilité relative ;
- `INCERTAIN` et `INCONNU` sont des résultats normaux, pas des erreurs ;
- `ENTREE_ERREUR` / `INFERENCE_ERREUR` sont distincts de `INCONNU` (image exploitable mais hors périmètre).

---

## 5. Incertitude — principes (détail opérationnel en Phase E)

1. **Seuils par culture et par catégorie** calculés sur un jeu de validation séparé, pas choisis à la main.
2. **Calibration** : température ou isotonique selon la taille du jeu de validation.
3. **Détection hors-domaine** : combinaison confiance maximale + entropie + écart à la distribution de validation ; les images négatives (`GLOBAL_INCONNU`) servent de référence.
4. **Aucun seuil par défaut** : tant que la Phase E n'a pas produit de courbes précision/rappel, le système doit refuser de conclure.

---

## 6. Contraintes d'implémentation et responsabilités

| Contrainte | Décision |
|---|---|
| Hors-ligne | Tous les modèles embarqués, aucune requête réseau |
| Dépendances Gradle | **Aucune modification** : TFLite 2.14.0 + support 0.4.4 déjà déclarés suffisent |
| Taille | Modèles quantifiés INT8 visés ; à mesurer en Phase F |
| Latence | Inférence hors thread UI ; cible à mesurer sur appareil, pas à inventer |
| Frontière d'équipe | Le sous-système IA livre `.tflite`, `labels.txt`, `model_contract.json` et la documentation ; **Balawe intègre dans `app/src/main/assets/`** (issue #02). Aucun fichier Android modifié ici. |

---

## 7. Risques identifiés

| Risque | Mitigation |
|---|---|
| CCMT « augmented » provoque des fuites train/test | N'utiliser que le jeu **brut** ; regrouper par image source |
| Classes CCMT mêlant insecte et dégât | Audit visuel obligatoire avant mapping (Phase C) |
| Aucune donnée camerounaise | Jeu de test local dédié, minimum 20 images/classe |
| Carences absentes | Ne pas créer la classe tant que l'agronome n'a pas précisé le nutriment |
| Seuil arbitraire | Calibration sur validation + courbes (Phase E) |
| PlantVillage non licencié | Exclusion tant que l'accord écrit n'est pas obtenu |

---

## 8. Prochaine étape

Phase C : pipeline reproductible d'import, nettoyage, déduplication, séparation anti-fuite, augmentations réalistes et génération des labels — sans téléchargement ni entraînement tant que l'autorisation n'est pas donnée.
