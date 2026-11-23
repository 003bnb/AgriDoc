package com.agridoc.contract;

import android.graphics.Bitmap;

/**
 * Contrat d'inférence IA.
 *
 * L'équipe IA (Keumeka, Messi — issues #09, #10, #15) implémente cette
 * interface dans {@code model/ClassificationModel.java}.
 *
 * Le reste de l'application ne dépend jamais de
 * {@code ClassificationModel} directement ; il dépend de cette interface.
 * C'est ce qui permet :
 *  - de remplacer le modèle par une autre implémentation (test, mock),
 *  - de faire évoluer le moteur sans toucher aux écrans,
 *  - de connaître l'état du modèle (chargé, absent, en erreur)
 *    avant d'appeler la classification.
 *
 * Cycle de vie attendu :
 *  1. L'écran résultat (Adoum, issue #05) reçoit un
 *     {@code CameraOutput} via {@link NavigationContract#cameraToResult}.
 *  2. Il charge le Bitmap depuis {@code CameraOutput.imagePath}.
 *  3. Il appelle {@link #classify(Bitmap)} sur une instance de
 *     {@link Classifier} (obtenue par DI ou fabrique).
 *  4. Il lit le {@link InferenceResult} et affiche ou enregistre.
 *
 * Exigence : {@link #classify} doit exécuter l'inférence hors du
 * thread UI (voir cahier des charges, §5 « Robustesse »). L'implémentation
 * est libre de faire ce que veut ; le contrat ne prescrit que le
 * comportement observable.
 */
public interface Classifier {

    /**
     * Indique si le modèle est prêt à classer.
     *
     * L'écran de résultat utilise ce drapeau pour afficher un état
     * « modèle indisponible » si {@code false} (F-07 du cahier des
     * charges, « modèle indisponible »).
     *
     * @return {@code true} si un modèle est chargé et opérationnel.
     */
    boolean isReady();

    /**
     * Classe un Bitmap de feuille et retourne le résultat.
     *
     * L'implémentation doit :
     *  - pré-traiter le Bitmap selon le contrat du modèle
     *    (224×224, RGB, normalisation — issue #10),
     *  - exécuter l'inférence TFLite,
     *  - mapper la sortie du réseau sur les labels
     *    (ordre des classes — issue #15),
     *  - retourner un {@link InferenceResult} non nul.
     *
     * En cas d'erreur (modèle absent, image illisible, exception),
     * retourner {@link InferenceResult#error(String)} plutôt que
     * {@code null}. Le score de confiance ne doit jamais être inventé.
     *
     * @param bitmap image de feuille à classifier
     * @return le résultat de l'inférence ; jamais {@code null}.
     */
    InferenceResult classify(Bitmap bitmap);
}
