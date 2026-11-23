# Contrat d'intégration des modules — `com.agridoc.contract`

Ce package contient les interfaces et POJO qui définissent le contrat
entre les quatre modules d'AgriDoc (CameraX, IA, SQLite, UI/UX).

**Règle** : les modules ne se connaissent pas entre eux. Ils dépendent
uniquement de ce package et de `com.agridoc.data.repository`.

## Fichiers

| Fichier | Rôle | Responsable |
|---|---|---|
| `NavigationContract.java` | Clés d'extra Intent et fabriques d'Intent entre les écrans | Architecture (Wilfried) |
| `CameraOutput.java` | POJO : résultat de la capture (chemin, EXIF, timestamp, statut) | Architecture + Caméra (Moumoun) |
| `CameraOutputContract.java` | Interface que `CameraActivity` doit implémenter | Architecture (Wilfried) |
| `Classifier.java` | Interface que `ClassificationModel` doit implémenter | Architecture (Wilfried) |
| `InferenceResult.java` | POJO : résultat de l'inférence (classe, score, statut, conseil) | Architecture + IA (Keumeka/Messi) |

## Flux de données

```
Dashboard ──► Camera ──► Result ──► Historique
              │           │
              │           │
        CameraOutput   InferenceResult
        (Parcelable)   (Parcelable)
```

- `CameraOutput` traverse `Camera → Result` via
  `NavigationContract.cameraToResult`.
- `InferenceResult` traverse `Result → Historique` via
  `NavigationContract.resultToHistorique`.

## Pourquoi ces objets sont Parcelable

Les résultats traversent les frontières d'activités via `Intent`.
`Parcelable` est le format natif d'Android pour cette opération.
`Serializable` serait fonctionnel mais plus lent ; `Parcelable` est
la convention standard pour les données qui passent entre activités.

## Comment implémenter

### Moumoun — Caméra

Implémenter `CameraOutputContract` dans `CameraActivity` :

```java
public class CameraActivity extends AppCompatActivity
        implements CameraOutputContract {

    @Override
    public CameraOutput capture() {
        // 1. Vérifier la permission (PermissionManager)
        // 2. Capturer l'image
        // 3. Écrire le fichier dans filesDir
        // 4. Récupérer l'orientation EXIF
        // 5. Retourner CameraOutput.success(chemin, orientation, timestamp)
        //    ou CameraOutput.error(message)
    }
}
```

### Keumeka / Messi — IA

Implémenter `Classifier` dans `ClassificationModel` :

```java
public class ClassificationModel implements Classifier {

    private Interpreter tflite;  // à charger depuis assets/

    @Override
    public boolean isReady() {
        return tflite != null;
    }

    @Override
    public InferenceResult classify(Bitmap bitmap) {
        // 1. Vérifier isReady()
        // 2. Prétraiter (ImageUtils : 224x224, ByteBuffer)
        // 3. Exécuter tflite
        // 4. Mapper l'indice de sortie sur labels.txt
        // 5. Retourner InferenceResult.success / inconclusive / error
    }
}
```

### Sam — Historique

`HistoriqueRepository` accepte un `InferenceResult` pour le persister :

```java
public void save(InferenceResult result, CameraOutput output,
                 RepositoryCallback<Long> callback) {
    // Construire EntityHistorique à partir de result + output
    // Insérer via DaoHistorique
}
```

## Ce que ce contrat n'est pas

- Ce n'est pas le modèle TFLite. Le modèle reste dans `assets/`.
- Ce n'est pas le prétraitement. `ImageUtils` reste dans `utils/`.
- Ce n'est pas le layout. Les écrans restent dans `ui/`.

Le contrat ne définit que **ce qui traverse les frontières** :
les données et les interfaces. Chaque module garde son implémentation.
