# DATASET_SPECIFICATION — Stratégie de Données AgriDoc V1

**Version :** 1.0  
**Statut :** Proposition (aucune donnée n'est encore collectée ni téléchargée)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi)  
**Dernière révision :** 2026-11-22

---

## 1. Objectif

Définir une stratégie de données complète pour entraîner un modèle de classification des problèmes phytosanitaires sur trois cultures : **Manioc, Tomate, Maïs**. Aucune image, aucune annotation et aucun dataset n'existent actuellement dans le dépôt AgriDoc. Cette spécification décrit ce qui doit être collecté, annoté et validé avant entraînement.

---

## 2. Sources de Données Candidates

### 2.1 PlantVillage

| Élément | Détail |
|---------|--------|
| Cultures disponibles | Tomate et Maïs confirmés dans les données examinées ; manioc absent des dossiers `raw/` consultés |
| Catégories disponibles | Maladies (multiples par plante), plantes saines |
| Pertinence pour AgriDoc | Très élevée pour les maladies de la Tomate et du Maïs ; le manioc n'est pas couvert par cette source |
| Limites | Peu ou pas de catégories "ravageurs" ou "carences nutritionnelles" ; focus sur les maladies fongiques, virales, bactériennes |
| Licence | À vérifier pour un usage commercial (aucune licence détectée dans le dépôt) |
| Risque de fuite | Certaines images peuvent apparaître dans d'autres datasets publics (déduplication nécessaire) |

### 2.2 PlantDoc

| Élément | Détail |
|---------|--------|
| Cultures disponibles | Tomate et Maïs confirmés dans les données examinées ; manioc absent des dossiers `train/` et `test/` consultés |
| Catégories disponibles | Maladies, plantes saines |
| Pertinence pour AgriDoc | Moyenne à élevée pour la Tomate et le Maïs ; le manioc n'est pas couvert par cette source |
| Limites | Couverture inégale selon les cultures ; moins de classes que PlantVillage |
| Licence | CC-BY-4.0 confirmée dans l'audit pour PlantDoc ; les conditions applicables aux images individuelles doivent rester traçables ; ne pas présenter cette licence comme une autorisation commerciale universelle sans vérification |
| Risque de fuite | À évaluer par déduplication |

### 2.3 CCMT (Cassava Cloud Monitoring Tool ou équivalent cassava-focused)

| Élément | Détail |
|---------|--------|
| Cultures disponibles | Aucune donnée vérifiée (source non identifiée) |
| Catégories disponibles | Aucune catégorie vérifiée |
| Pertinence pour AgriDoc | Non établie (source non identifiée) |
| Limites | Source non identifiée ; aucune donnée disponible ; ne pas utiliser comme source planifiée |
| Licence | À vérifier |
| Risque de fuite | À évaluer |

### 2.4 Collecte de Données Agricoles Camerounaises (À planifier)

| Élément | Détail |
|---------|--------|
| Cultures visées | Manioc, Tomate, Maïs cultivés au Cameroun |
| Catégories visées | Maladies locales, ravageurs locaux, carences nutritionnelles observées sur le terrain |
| Pertinence pour AgriDoc | Essentielle pour la représentativité des conditions camerounaises (éclairage, sols, variétés, stades de croissance) |
| Limites | Coût de collecte, nécessité d'un référent agronomique pour la validation, délai |
| Licence | À définir (consentement des agriculteurs, droits d'image) |
| Risque de fuite | N/A (données propriétaires du projet) |

---

## 3. Nomenclature des Classes (V1)

Les classes sont organisées par culture, puis par type de problème. Chaque classe correspond à une sortie distincte du modèle. **Aucune classe fictive n'est créée.**

### 3.1 Structure de nomenclature

```
{CULTURE}_{TYPE}_{NOM}
```

Où :
- `{CULTURE}` ∈ {MANIOC, TOMATE, MAIS}
- `{TYPE}` ∈ {MALADIE, RAVAGEUR, DEGAT_RAVAGEUR, CARENCE, SAIN, INCONNU}
- `{NOM}` = identificateur spécifique

### 3.2 Classes par culture

#### 3.2.1 Manioc (Manihot esculenta)

| Classe | Type | Description | Statut des données |
|--------|------|-------------|-------------------|
| MANIOC_SAIN | Plante saine | Feuille sans symptôme visible | À collecter / valider |
| MANIOC_MALADIE_MOSAIQUE | Maladie | Mosaïque du manioc (Cassava Mosaic Virus) | Collecte camerounaise obligatoire (manioc absent de PlantVillage et de PlantDoc) |
| MANIOC_MALADIE_BRUNISSEMENT | Maladie | Brunissement du manioc (CBSD) | Exclu de V1 (symptômes principalement racinaires) |
| MANIOC_CARENCE | Carence | Carence nutritionnelle (nutriment à spécifier avec un agronome) | À collecter / valider |
| MANIOC_RAVAGEUR | Ravageur | Insecte visible sur la feuille (espèce à préciser) | À collecter / valider |
| MANIOC_DEGAT_RAVAGEUR | Dégâts ravageur | Trous, déformations ou galeries visibles | À collecter / valider |
| MANIOC_INCONNU | Inconnu | Image non exploitable ou hors domaine | À générer (images négatives) |

#### 3.2.2 Tomate (Solanum lycopersicum)

| Classe | Type | Description | Statut des données |
|--------|------|-------------|-------------------|
| TOMATE_SAIN | Plante saine | Feuille sans symptôme visible | À collecter / valider |
| TOMATE_MALADIE_MILDIEU | Maladie | Mildiou (Phytophthora infestans) | Source probable : PlantVillage |
| TOMATE_MALADIE_TACHE_BACTERIENNE | Maladie | Tache bactérienne (Xanthomonas) | Source probable : PlantVillage / PlantDoc |
| TOMATE_MALADIE_SEPTORIA | Maladie | Tache de Septoria | Source probable : PlantVillage / PlantDoc |
| TOMATE_MALADIE_YELLOW_LEAF_CURL | Maladie | Virus de l'enroulement jaune (TYLCV) | Source probable : PlantVillage |
| TOMATE_MALADIE_LEAF_MOLD | Maladie | Moisissure foliaire (Fulvia fulva) | Source probable : PlantVillage |
| TOMATE_MALADIE_TARGET_SPOT | Maladie | Tache cible (Corynespora) | Source probable : PlantVillage |
| TOMATE_MALADIE_EARLY_BLIGHT | Maladie | Alternariose (Alternaria solani) | Source probable : PlantVillage / PlantDoc |
| TOMATE_RAVAGEUR_SPIDER_MITE | Ravageur | Acarien rouge (Tétranyque tisserand) | Source probable : PlantVillage / PlantDoc |
| TOMATE_RAVAGEUR | Ravageur | Autre insecte visible (espèce à préciser) | À collecter / valider |
| TOMATE_DEGAT_RAVAGEUR | Dégâts ravageur | Trous, déformations visibles | À collecter / valider |
| TOMATE_CARENCE | Carence | Carence nutritionnelle | À collecter / valider |
| TOMATE_INCONNU | Inconnu | Image non exploitable ou hors domaine | À générer (images négatives) |

#### 3.2.3 Maïs (Zea mays)

| Classe | Type | Description | Statut des données |
|--------|------|-------------|-------------------|
| MAIS_SAIN | Plante saine | Feuille sans symptôme visible | À collecter / valider |
| MAIS_MALADIE_ROUILLE | Maladie | Rouille du maïs | À collecter / valider |
| MAIS_MALADIE_TACHE_NORD | Maladie | Tache foliaire du nord | À collecter / valider |
| MAIS_RAVAGEUR | Ravageur | Insecte visible sur la feuille | À collecter / valider |
| MAIS_DEGAT_RAVAGEUR | Dégâts ravageur | Trous, galeries visibles | À collecter / valider |
| MAIS_CARENCE | Carence | Carence nutritionnelle | À collecter / valider |
| MAIS_INCONNU | Inconnu | Image non exploitable ou hors domaine | À générer (images négatives) |

### 3.3 Classes globales

| Classe | Type | Description | Statut des données |
|--------|------|-------------|-------------------|
| GLOBAL_INCONNU | Inconnu | Image sans partie identifiable de plante (main, ciel, sol, objet) | À générer (images négatives) |
| GLOBAL_NON_EXPLOITABLE | Inconnu | Image floue, sous-exposée, surexposée | À générer (images négatives) |

### 3.4 Classes exclues de la V1

- Toutes les autres cultures (banane, patate douce, haricot, etc.)
- Maladies non visuelles (requérant une analyse de sol ou de sève)
- Ravageurs non visibles sur la photo (identification par dégâts uniquement quand visible)

---

## 4. Format des Annotations et Métadonnées

### 4.1 Format d'annotation des images

Chaque image d'entraînement doit être accompagnée d'un fichier de métadonnées (JSON ou CSV) contenant :

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `image_id` | String | Oui | Identifiant unique de l'image |
| `source` | String | Oui | Origine (PlantVillage, PlantDoc, CCMT, collecte_camerounaise) |
| `source_url` | String | Non | URL de provenance si applicable |
| `culture` | String | Oui | MANIOC, TOMATE, MAIS, ou GLOBAL |
| `type_probleme` | String | Oui | MALADIE, RAVAGEUR, DEGAT_RAVAGEUR, CARENCE, SAIN, INCONNU |
| `classe` | String | Oui | Nom complet de la classe (ex. MANIOC_MALADIE_MOSAIQUE) |
| `date_capture` | Date | Non | Date de prise de vue |
| `localisation` | String | Non | Région/pays si connue (pour collecte camerounaise ; équivalent aux champs `region` et `localite` du protocole camerounais) |
| `validation_agronomique` | Boolean | Oui | `true` si validé par un référent agronomique |
| `valideur_nom` | String | Non | Nom du référent agronomique |
| `qualite_image` | String | Oui | EXCELLENTE, BONNE, MOYENNE, EXPLOITABLE_DIFFICILE |
| `luminosite` | String | Non | ADEQUATE, INSUFFISANTE, EXCESSIVE |
| `nettete` | String | Non | NETTE, LEGEREMENT_FLOUE, FLOUE |

### 4.2 Règles de validation des labels

1. **Un seul label principal par image** : chaque image appartient à une seule classe.
2. **Validation agronomique obligatoire** : aucune image ne peut être utilisée pour l'entraînement sans validation par un référent agronomique, sauf les images provenant de sources publiques déjà annotées (PlantVillage, etc.) dont la provenance est documentée.
3. **Pas de classe "fourre-tout"** : une image présentant plusieurs problèmes simultanés doit être assignée à la classe la plus significative, ou exclue si l'ambiguïté est trop grande.
4. **Images hors domaine** : les images ne montrant pas une feuille ou une partie identifiable de plante sont assignées à `GLOBAL_INCONNU` ou `GLOBAL_NON_EXPLOITABLE`.

---

## 5. Stratégie de Collecte Camerounaise

### 5.1 Objectif

Collecter des images représentatives des conditions réelles au Cameroun (éclairage, variétés locales, stades de croissance, types de sols, pratiques culturales) pour éviter le biais de domaine des datasets publics (souvent pris en serre ou en conditions idéales).

### 5.2 Zones et cultures visées

| Région camerounaise | Cultures prioritaires | Problèmes visés |
|---------------------|----------------------|-----------------|
| Zone forestière (Sud, Centre, Est) | Manioc, Maïs | Mosaïque du manioc, carences |
| Zone de haute altitude (Ouest, Nord-Ouest) | Tomate, Maïs | Mildiou, ravageurs |
| Zone sahélienne (Extrême-Nord) | Maïs, Tomate | Carences, stress hydrique |

### 5.3 Méthode de collecte

1. Recrutement d'un référent agronomique local.
2. Formation des collecteurs à la prise de vue (feuille bien cadrée, éclairage naturel, plusieurs angles).
3. Capture d'au moins 50 à 100 images par classe visée (à ajuster selon la disponibilité).
4. Validation immédiate sur le terrain par l'agronome.
5. Renommage et stockage avec métadonnées complètes.

---

## 6. Règles de Déduplication et Prévention des Fuites

### 6.1 Déduplication

- **Hachage perceptuel** : calculer un hash perceptuel (pHash) pour chaque image afin de détecter les doublons visuels exacts ou près-exacts.
- **Vérification croisée** : comparer les images collectées au Cameroun avec celles des sources publiques pour éviter qu'une même image apparaisse deux fois sous des noms différents.
- **Suppression des doublons** : ne garder qu'un exemplaire par image unique.

### 6.2 Prévention des fuites de données (Data Leakage)

- **Séparation stricte** : aucune image ne peut apparaître simultanément dans l'entraînement, la validation et le test.
- **Séparation par source** : si une même plante est photographiée sous plusieurs angles, toutes les variantes doivent aller dans le même ensemble (train, validation OU test, jamais réparties).
- **Séparation par collecteur** : si possible, les images d'un même collecteur ou d'une même parcelle ne doivent pas être séparées entre train et test.

---

## 7. Séparation Entraînement / Validation / Test

| Ensemble | Pourcentage | Usage |
|----------|-------------|-------|
| Entraînement | 70% | Apprentissage du modèle |
| Validation | 15% | Ajustement des hyperparamètres, sélection du meilleur modèle |
| Test | 15% | Évaluation finale non biaisée (jamais utilisé pendant l'entraînement) |

### 7.1 Représentativité

- Chaque culture doit être représentée dans chaque ensemble (train/validation/test) dans des proportions similaires.
- Chaque classe doit avoir un nombre minimal d'images dans le test (recommandé : au moins 20 images par classe dans le test).
- Les images camerounaises doivent être représentées dans les trois ensembles pour évaluer la généralisation aux conditions locales.

---

## 8. Exigences de Représentativité des Images

| Critère | Exigence |
|---------|----------|
| Variété d'éclairage | Soleil, ombre, nuageux, matin, après-midi |
| Variété d'appareils | Au moins 3 modèles de smartphones différents |
| Variété de résolution | Plusieurs résolutions (le modèle redimensionnera, mais l'entraînement doit couvrir la variabilité) |
| Orientation | Feuille du dessus, du dessous, en biseau |
| Stade de croissance | Jeune feuille, feuille mature, feuille âgée |
| Santé | Plantes saines et malades dans des proportions équilibrées (éviter le déséquilibre de classes) |

---

## 9. Données Non Disponibles (À collecter)

| Donnée | Raison | Action |
|--------|--------|--------|
| Ravageurs spécifiques camerounais | Peu documentés dans les datasets publics | Collecte terrain obligatoire |
| Carences nutritionnelles visuelles | Rarement annotées dans PlantVillage | Collecte terrain avec agronome |
| Maladies du maïs locales | Couverture inégale dans les sources publiques | Collecte terrain |
| Images d'objets non-plantes (main, ciel, sol) | Nécessaires pour la classe "inconnu" | Génération d'images négatives |

---

## 10. Informations Manquantes

| Information | Impact | Vérification nécessaire |
|-------------|--------|------------------------|
| Nombre exact d'images par classe disponible dans PlantVillage | Impacte la taille du jeu d'entraînement | À vérifier par téléchargement et comptage |
| Licence d'utilisation commerciale de PlantVillage | Impacte la possibilité d'inclure le modèle dans une application distribuée | À vérifier auprès de la source |
| Disponibilité d'un référent agronomique camerounais | Bloquant pour la validation des classes ravageurs et carences | À recruter |
| Budget et délai de collecte terrain | Impacte le planning | À planifier avec le chef de projet |
