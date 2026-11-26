# ANDROID_MODEL_CONTRACT — Contrat IA / Android AgriDoc V1

**Version :** 1.0  
**Statut :** Proposition (aucun modèle n'est encore entraîné, les valeurs techniques doivent être extraites du modèle réel)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi) avec l'équipe Android  
**Dernière révision :** 2026-11-22

---

## 1. Objectif

Définir précisément le contrat technique entre le sous-système IA (TensorFlow Lite) et l'application Android. Ce contrat spécifie les entrées, les sorties, les formats de données, la gestion des erreurs et les responsabilités de chaque composant. **Aucune valeur (dimensions, dtype, seuil) n'est fixée arbitrairement : elles devront être extraites du modèle effectivement entraîné et exporté.**

---

## 2. Principes Généraux

| Principe | Description |
|----------|-------------|
| Aucune valeur en dur | Les dimensions, le type numérique, la normalisation et la quantification doivent être lues depuis le modèle TFLite au chargement, pas codées en dur |
| Inférence hors thread UI | L'inférence TFLite ne doit jamais bloquer le thread principal Android |
| Résultat honnête | Pas de score fictif, pas de "0.95f" hardcodé. Le score est une valeur réelle issue du modèle |
| Gestion de l'incertitude | Un seuil de confiance sépare une prédiction fiable d'un état "non reconnu" |
| Pas de diagnostic garanti | Le résultat est une aide, jamais une certitude agronomique |

---

## 3. Contrat d'Entrée (Image → Modèle)

### 3.1 Format d'entrée (À déterminer à partir du modèle réel)

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| Dimensions du tenseur | **À extraire du modèle** (ex. [1, H, W, C]) | `interpreter.getInputTensor(0).shape()` |
| Type numérique | **À extraire du modèle** (UINT8 ou FLOAT32) | `interpreter.getInputTensor(0).dataType()` |
| Ordre des canaux | **À extraire du modèle** (RGB ou BGR) | Documenté par l'équipe IA |
| Plage de pixels | **À extraire du modèle** (0-255, 0-1, ou -1 à 1) | Documenté par l'équipe IA |
| Normalisation | **À extraire du modèle** (mean/std ou none) | Documenté par l'équipe IA |
| Quantification | **À extraire du modèle** (scale, zero point si quantifié) | `interpreter.getInputTensor(0).quantizationParams()` |

**Hypothèse à ne PAS retenir sans vérification :** 224×224 RGB. Cette valeur est une entrée candidate mentionnée dans les issues #09/#10, mais le CAHIER_DES_CHARGES et l'issue #15 indiquent qu'elle doit être confirmée par le modèle retenu.

### 3.2 Pipeline de prétraitement (ImageUtils)

| Étape | Opération | Responsabilité |
|-------|-----------|----------------|
| 1 | Chargement du fichier image depuis le chemin transmis par `CameraActivity` | `ResultActivity` (via `BitmapFactory.decodeFile`) |
| 2 | Correction de l'orientation EXIF si nécessaire | `ImageUtils.rotateBitmap` (existant) |
| 3 | Redimensionnement aux dimensions du modèle | `ImageUtils.resizeBitmap` (existant, dimensions à lire du modèle) |
| 4 | Conversion `Bitmap` → `ByteBuffer` | `ImageUtils.bitmapToByteBuffer` (à créer, dimensions/type/normalisation du modèle) |
| 5 | Alignement de l'ordre des octets (`ByteOrder.nativeOrder()`) | `ImageUtils.bitmapToByteBuffer` |

### 3.3 Contrat ImageUtils

```java
// Méthode à créer dans ImageUtils.java
public static ByteBuffer bitmapToByteBuffer(Bitmap bitmap)
```

- **Entrée :** `Bitmap` non nul, toute taille, toute orientation (après rotation EXIF).
- **Sortie :** `ByteBuffer` de taille égale au tenseur d'entrée du modèle, ordre des octets natif.
- **Traitement interne :** Redimensionnement, conversion couleur (RGB→BGR si nécessaire), normalisation selon le contrat du modèle.
- **Erreur :** Retourne `null` ou lève `IllegalArgumentException` si le bitmap est inutilisable.

---

## 4. Contrat de Sortie (Modèle → Plante)

### 4.1 Sortie brute du TFLite Interpreter

| Paramètre | Valeur | Source |
|-----------|--------|--------|
| Forme du tenseur de sortie | **À extraire du modèle** (ex. [1, N] où N = nombre de classes) | `interpreter.getOutputTensor(0).shape()` |
| Type numérique | **À extraire du modèle** (FLOAT32 ou UINT8) | `interpreter.getOutputTensor(0).dataType()` |
| Nature de la sortie | **À documenter** (logits bruts ou probabilités après softmax) | Documenté par l'équipe IA |
| Ordre des classes | **À documenter** (correspond à l'ordre des lignes dans `labels.txt`) | Documenté par l'équipe IA |

### 4.2 Mapping vers l'objet `Plante`

Le `Plante` retourné par `ClassificationModel.classifyImage()` doit contenir :

| Champ | Type | Source | Description |
|-------|------|--------|-------------|
| `nom` | String | Nom de la culture (ex. "Manioc") | Extrait de la classe prédite |
| `maladie` | String | Libellé de la classe (issu de `labels.txt`) | Ou "Non reconnu" si sous seuil |
| `scoreConfiance` | float | Score de la classe prédite (0.0 à 1.0) | Valeur réelle du modèle, pas de hardcodé |
| `traitementConseille` | String | Recommandation associée à la classe | Ou conseil de consulter un technicien si non reconnu |
| `estReconnu` | boolean (à ajouter) | `true` si score >= seuil, `false` sinon | Champ nouveau à ajouter à `Plante` |

### 4.3 Gestion du seuil de confiance

| Condition | Comportement |
|-----------|-------------|
| `scoreMax >= seuil` | `estReconnu = true`, `maladie` = libellé de la classe prédite |
| `scoreMax < seuil` | `estReconnu = false`, `maladie` = "Non reconnu", `traitementConseille` = conseil de consulter un technicien |
| Modèle non chargé | État d'erreur, `estReconnu = false` |
| Inférence échoue | État d'erreur, `estReconnu = false` |

**Le seuil de confiance n'est pas fixé à 0,60 par défaut.** Il doit être déterminé expérimentalement à partir de la courbe précision/rappel sur le jeu de validation (voir `ACCEPTANCE_CRITERIA.md`).

---

## 5. Contrats entre Composants Android

### 5.1 CameraActivity → ResultActivity (avec Moumoun)

| Élément | Spécification |
|---------|---------------|
| Donnée transmise | Chemin absolu du fichier image temporaire |
| Mécanisme | `Intent.putExtra("image_path", String)` |
| Clé de l'extra | `"image_path"` |
| Format du chemin | Chemin absolu lisible par `BitmapFactory.decodeFile()` |
| Responsabilité | `CameraActivity` sauvegarde l'image capturée, transmet le chemin ; `ResultActivity` charge le bitmap depuis ce chemin |

### 5.2 ResultActivity → ClassificationModel (avec Keumeka)

| Élément | Spécification |
|---------|---------------|
| Méthode appelée | `classifyImage(Bitmap bitmap)` |
| Entrée | `Bitmap` issu de la photo capturée |
| Sortie | `Plante` (avec `estReconnu`, score réel) |
| Threading | L'inférence s'exécute sur un thread de fond (ExecutorService) |
| Callback | Résultat retourné de manière asynchrone à `ResultActivity` |

### 5.3 ResultActivity → HistoriqueRepository (avec Sam)

| Élément | Spécification |
|---------|---------------|
| Donnée transmise | `EntityHistorique(nomPlante, nomMaladie, scoreConfiance, imagePath, dateTimestamp)` |
| Condition d'enregistrement | Uniquement si classification réussie (`estReconnu = true`) — ou enregistrement avec mention "non reconnu" selon décision produit |
| Méthode | `HistoriqueRepository.insert(EntityHistorique, RepositoryCallback<Long>)` |
| Threading | Asynchrone (déjà implémenté dans `HistoriqueRepository`) |

### 5.4 HistoriqueViewModel → HistoriqueActivity (avec Sam)

| Élément | Spécification |
|---------|---------------|
| Donnée observée | `LiveData<List<EntityHistorique>>` |
| Responsabilité | `HistoriqueViewModel` expose les données, `HistoriqueActivity` les observe |
| Survie à la rotation | Le `ViewModel` conserve l'état lors de la rotation d'écran |

---

## 6. Classes et Interfaces Recommandées (À créer, non implémentées)

### 6.1 `model/LabelProvider.java`

```java
public class LabelProvider {
    // Lecture de labels.txt depuis assets/
    // Mapping index → libellé
    // Vérification : nombre de lignes == nombre de classes de sortie
    public String getLabel(int index);
    public int getLabelCount();
    public boolean isValid();
}
```

**Responsabilité :** Lecture du fichier `labels.txt`, alignement avec les indices de sortie du modèle, détection d'incohérence.

### 6.2 `model/TFLiteModelLoader.java` (ou intégration dans ClassificationModel)

```java
public class TFLiteModelLoader {
    // Ouverture du .tflite depuis assets/ via MappedByteBuffer
    // Instanciation de l'Interpreter TFLite
    // Lecture des dimensions d'entrée/sortie
    // Vérification de compatibilité avec le contrat
}
```

**Responsabilité :** Chargement du modèle, instanciation de l'Interpreter, lecture des métadonnées des tenseurs.

### 6.3 `model/ClassificationCallback.java` (optionnel)

```java
public interface ClassificationCallback {
    void onResult(Plante result);
    void onError(Throwable throwable);
}
```

**Responsabilité :** Retour asynchrone du résultat d'inférence vers `ResultActivity`.

### 6.4 Modification de `model/Plante.java`

Ajout du champ :
```java
private boolean estReconnu;
```
Avec getter/setter, et constructeur mis à jour.

### 6.5 Modification de `utils/ImageUtils.java`

Ajout de la méthode :
```java
public static ByteBuffer bitmapToByteBuffer(Bitmap bitmap);
```

---

## 7. États d'Erreur et Gestion

| Situation | Détection | Comportement Android |
|-----------|-----------|---------------------|
| Modèle `.tflite` absent de `assets/` | Exception au chargement de l'Interpreter | Afficher "Modèle IA indisponible" |
| `labels.txt` absent ou incohérent | `LabelProvider.isValid() == false` | Afficher "Configuration IA incomplète" |
| Bitmap inutilisable (null, trop petit) | `bitmapToByteBuffer` retourne null | Afficher "Image non exploitable" |
| Inférence TFLite lève une exception | try/catch autour de `interpreter.run()` | Afficher "Erreur de classification, réessayer" |
| Score max < seuil de confiance | Comparaison après softmax | Afficher "Plante non reconnue avec certitude" |
| Permission caméra refusée | `PermissionManager.hasPermission() == false` | Afficher demande de permission ou message d'impossibilité |
| Caméra indisponible | Exception CameraX | Afficher "Caméra non disponible" |

---

## 8. Modèle de Fichier `model_contract.json`

Un fichier JSON doit être généré avec le modèle pour documenter le contrat. Il est **à créer après l'entraînement du modèle**, pas avant.

```json
{
  "model": {
    "name": "plant_disease_model",
    "version": "1.0",
    "framework": "TensorFlow Lite",
    "tflite_version": "2.14.0",
    "quantization": "À renseigner",
    "file": "plant_disease_model.tflite",
    "license": "À renseigner",
    "source": "À renseigner"
  },
  "input": {
    "tensor_name": "À renseigner",
    "shape": [1, "H", "W", "C"],
    "data_type": "À renseigner (UINT8 ou FLOAT32)",
    "channel_order": "À renseigner (RGB ou BGR)",
    "pixel_range": "À renseigner",
    "normalization": {
      "type": "À renseigner",
      "mean": null,
      "std": null
    },
    "quantization_params": {
      "scale": "À renseigner",
      "zero_point": "À renseigner"
    }
  },
  "output": {
    "tensor_name": "À renseigner",
    "shape": [1, "N"],
    "data_type": "À renseigner (FLOAT32 ou UINT8)",
    "nature": "À renseigner (logits ou probabilités après softmax)",
    "num_classes": "N (à renseigner)"
  },
  "labels_file": "labels.txt",
  "label_count": "N (à renseigner)",
  "confidence_threshold": "À renseigner (à déterminer expérimentalement)",
  "preprocessing": {
    "resize_method": "À renseigner",
    "exif_rotation": true,
    "byte_order": "NATIVE"
  }
}
```

**Toutes les valeurs ci-dessus sont des PLACEHOLDERS.** Elles doivent être remplacées par les valeurs réelles extraites du modèle entraîné et exporté. Aucune valeur (dimensions, dtype, seuil, nombre de classes) n'est fixée dans ce contrat avant l'obtention du modèle réel.

---

## 8.5 Note collective sur les contrats de résultat

Le présent contrat propose un objet métier `Plante` avec le champ `estReconnu`. Le commit `305652e` introduit également `com.agridoc.contract.InferenceResult`. **Le choix entre ces deux modèles de résultat doit être arbitré collectivement par l'équipe Android avant implémentation.** Ce document reste une proposition documentaire : il n'est pas encore intégré dans l'application et aucune classe Java correspondante n'a été modifiée par cette consolidation.

---

## 9. Responsabilités des Composants Existants

| Composant | Rôle dans le contrat | Modifications requises |
|-----------|---------------------|----------------------|
| `ClassificationModel.java` | Moteur d'inférence TFLite réel, chargement depuis `assets/`, appel à `ImageUtils.bitmapToByteBuffer`, mapping vers `Plante`, gestion du seuil et du cas "non reconnu", `close()` réel | Réécriture complète |
| `Plante.java` | Objet métier retourné par l'inférence | Ajout du champ `estReconnu` |
| `ImageUtils.java` | Prétraitement : resize, rotate, conversion `Bitmap → ByteBuffer` | Ajout de `bitmapToByteBuffer` |
| `ResultActivity.java` | Réception de l'image, appel à `ClassificationModel`, affichage du résultat, sauvegarde en historique | Implémentation complète |
| `HistoriqueRepository.java` | Persistance du diagnostic dans Room | Aucune modification (déjà fonctionnel) |

---

## 10. Informations Manquantes (À obtenir après entraînement)

| Information | Quand | Comment |
|-------------|-------|---------|
| Dimensions d'entrée du modèle (H, W, C) | Après export TFLite | `interpreter.getInputTensor(0).shape()` |
| Type numérique d'entrée (UINT8/FLOAT32) | Après export TFLite | `interpreter.getInputTensor(0).dataType()` |
| Ordre des canaux (RGB/BGR) | Après documentation du modèle | Documenté par Keumeka/Messi |
| Plage de pixels et normalisation | Après documentation du modèle | Documenté par Keumeka/Messi |
| Nombre de classes et ordre des labels | Après entraînement | Nombre de lignes dans `labels.txt` |
| Seuil de confiance optimal | Après évaluation sur jeu de validation | Courbe précision/rappel |
| License du modèle | Après sélection du modèle | Documentée par Keumeka/Messi |
