package com.agridoc.contract;

import android.content.Context;
import android.content.Intent;
import com.agridoc.ui.CameraActivity;
import com.agridoc.ui.HistoriqueActivity;
import com.agridoc.ui.ResultActivity;

/**
 * Contrat de navigation entre les activités d'AgriDoc.
 *
 * Ce fichier centralise les clés d'extra Intent et les fabriques d'Intent
 * pour que chaque écran sache comment passer la main au suivant.
 *
 * Flux attendu :
 *   Dashboard ──► Camera ──► Result ──► Dashboard
 *       └────────► Historique
 *
 * Règle : aucun écran ne construit un Intent avec des extra bruts ;
 * il utilise les fabriques de cette classe. C'est ici que le contrat
 * entre les écrans est défini, et c'est ici que seule la couche
 * d'architecture intervient.
 */
public final class NavigationContract {

    private NavigationContract() {
        throw new UnsupportedOperationException("Utilisation non autorisée.");
    }

    // ----------------------------------------------------------------
    // Clés d'extra Intent
    // ----------------------------------------------------------------

    /** Extra transmis de Camera à Result : résultat de la capture. */
    public static final String EXTRA_CAMERA_OUTPUT = "com.agridoc.extra.CAMERA_OUTPUT";

    /** Extra transmis de Result à Dashboard : résultat de l'inférence. */
    public static final String EXTRA_INFERENCE_RESULT = "com.agridoc.extra.INFERENCE_RESULT";

    /** Extra transmis de Result à Historique : résultat à enregistrer. */
    public static final String EXTRA_INFERENCE_RESULT_FOR_SAVE =
            "com.agridoc.extra.INFERENCE_RESULT_FOR_SAVE";

    // ----------------------------------------------------------------
    // Fabriques d'Intent
    // ----------------------------------------------------------------

    /** Dashboard → Camera : lance l'écran de capture. */
    public static Intent dashboardToCamera(Context context) {
        return new Intent(context, CameraActivity.class);
    }

    /** Dashboard → Historique : lance l'écran d'historique. */
    public static Intent dashboardToHistorique(Context context) {
        return new Intent(context, HistoriqueActivity.class);
    }

    /**
     * Camera → Result : transmet le résultat de la capture.
     *
     * @param context contexte d'envoi
     * @param output  {@link CameraOutput} produit par l'écran caméra
     */
    public static Intent cameraToResult(Context context, CameraOutput output) {
        Intent intent = new Intent(context, ResultActivity.class);
        intent.putExtra(EXTRA_CAMERA_OUTPUT, output);
        return intent;
    }

    /** Result → Dashboard : retour simple, pas d'extra requis. */
    public static Intent resultToDashboard(Context context) {
        return new Intent(context, com.agridoc.ui.DashboardActivity.class);
    }

    /**
     * Result → Historique : transmet le résultat à enregistrer.
     *
     * @param context contexte d'envoi
     * @param result  {@link InferenceResult} à persister
     */
    public static Intent resultToHistorique(Context context, InferenceResult result) {
        Intent intent = new Intent(context, HistoriqueActivity.class);
        intent.putExtra(EXTRA_INFERENCE_RESULT_FOR_SAVE, result);
        return intent;
    }
}
