package com.agridoc.model;

import android.content.Context;
import android.graphics.Bitmap;

public class ClassificationModel {

    private Context context;
    private boolean isLoaded = false;

    public ClassificationModel(Context context) {
        this.context = context;
    }

    public void loadModel() {
        // TODO: Charger le modèle TensorFlow Lite (.tflite) depuis assets/
        this.isLoaded = true;
    }

    public Plante classifyImage(Bitmap bitmap) {
        // TODO: Prétraiter l'image bitmap et exécuter l'inférence TFLite
        if (!isLoaded) {
            loadModel();
        }
        // Retourne un objet Plante avec le résultat simulé
        return new Plante("Plante Détectée", "Saine / Maladie Détectée", 0.95f, "Description et traitement préventif");
    }

    public void close() {
        // Libérer les ressources TFLite
        this.isLoaded = false;
    }
}
