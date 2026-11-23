package com.agridoc.contract;

/**
 * Contrat d'exposition de la capture caméra.
 *
 * L'écran caméra (Moumoun, issues #06–#08) implémente cette interface
 * pour produire un {@link CameraOutput} exploitable par l'écran de
 * résultat (Adoum, issue #05).
 *
 * Le reste de l'application ne doit jamais dépendre de
 * {@code CameraActivity} directement ; il dépend de ce contrat.
 *
 * Cycle de vie attendu :
 *  1. L'écran Dashboard lance {@link NavigationContract#dashboardToCamera}.
 *  2. CameraActivity capture l'image et construit un {@link CameraOutput}.
 *  3. CameraActivity transmet {@code CameraOutput} via
 *     {@link NavigationContract#cameraToResult}.
 *
 * Cette interface est un point de convergence : si Moumoun change sa
 * méthode de capture (galerie, webcam, file), le contrat reste identique
 * et le reste de l'application n'est pas impacté.
 */
public interface CameraOutputContract {

    /**
     * Capture l'image courante et retourne le résultat.
     *
     * L'implémentation doit :
     *  - demander la permission caméra si nécessaire
     *    ({@code PermissionManager}, issue #07),
     *  - exécuter la capture,
     *  - appliquer la correction EXIF si disponible,
     *  - écrire le fichier dans le stockage applicatif privé,
     *  - retourner {@link CameraOutput#success} ou
     *    {@link CameraOutput#error}.
     *
     * @return le résultat de la capture ; jamais {@code null}.
     */
    CameraOutput capture();
}
