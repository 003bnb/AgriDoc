package com.agridoc.contract;

import android.os.Parcel;
import android.os.Parcelable;
import android.os.Parcelable.Creator;

/**
 * Contrat de résultat d'inférence.
 *
 * Un objet {@code InferenceResult} est produit par une implémentation
 * de {@link Classifier} et consommé par l'écran de résultat (Adoum,
 * issue #05) et par le dépôt en historique (Sam, issue #11).
 *
 * Il décrit :
 *  - la classe prédite (index dans {@code labels.txt}),
 *  - le nom de la classe (texte affiché),
 *  - le score de confiance du réseau,
 *  - l'état de l'opération (succès, inconclusif, erreur),
 *  - un conseil de traitement lié à la classe
 *    (issue #05, {@code strings.xml}).
 *
 * La distinction {@link Status#INCONCLUSIVE} est importante : elle
 * couvre le cas où le réseau renvoie un indice mais avec un score
 * en dessous du seuil de confiance. L'application ne doit pas
 * présenter ce résultat comme un diagnostic fiable (cahier des
 * charges, §4 « Le résultat doit distinguer clairement la classe »).
 */
public final class InferenceResult implements Parcelable {

    public enum Status {
        /** Classification fiable, score au-dessus du seuil. */
        SUCCESS,
        /** Classe prédite mais score insuffisant pour conclure. */
        INCONCLUSIVE,
        /** Erreur technique (modèle absent, image illisible, etc.). */
        ERROR
    }

    /** Index de la classe prédite dans le fichier {@code labels.txt}. */
    public final int classIndex;

    /** Nom de la classe prédite, tel qu'il figure dans {@code labels.txt}. */
    public final String classLabel;

    /** Score de confiance tel que renvoyé par le réseau (0.0 – 1.0). */
    public final float confidence;

    /** État de l'opération. */
    public final Status status;

    /**
     * Conseil de traitement associé à la classe, ou {@code null} si
     * non disponible. Le texte est chargé depuis {@code strings.xml}
     * par l'écran de résultat, pas par l'implémentation du modèle.
     */
    public final String treatmentAdvice;

    /** Message d'erreur si {@code status == ERROR}. */
    public final String errorMessage;

    public InferenceResult(int classIndex, String classLabel, float confidence,
                           Status status, String treatmentAdvice,
                           String errorMessage) {
        this.classIndex = classIndex;
        this.classLabel = classLabel;
        this.confidence = confidence;
        this.status = status;
        this.treatmentAdvice = treatmentAdvice;
        this.errorMessage = errorMessage;
    }

    // ----------------------------------------------------------------
    // Fabriques
    // ----------------------------------------------------------------

    /** Classification réussie, score fiable. */
    public static InferenceResult success(int classIndex, String classLabel,
                                          float confidence,
                                          String treatmentAdvice) {
        return new InferenceResult(classIndex, classLabel, confidence,
                Status.SUCCESS, treatmentAdvice, null);
    }

    /** Classe prédite mais score sous le seuil. */
    public static InferenceResult inconclusive(int classIndex,
                                               String classLabel,
                                               float confidence) {
        return new InferenceResult(classIndex, classLabel, confidence,
                Status.INCONCLUSIVE, null, null);
    }

    /** Erreur technique, aucun résultat exploitable. */
    public static InferenceResult error(String errorMessage) {
        return new InferenceResult(-1, null, 0f,
                Status.ERROR, null, errorMessage);
    }

    public boolean isSuccess() {
        return status == Status.SUCCESS;
    }

    // ----------------------------------------------------------------
    // Parcelable
    // ----------------------------------------------------------------

    private InferenceResult(Parcel in) {
        this.classIndex = in.readInt();
        this.classLabel = in.readString();
        this.confidence = in.readFloat();
        this.status = Status.values()[in.readInt()];
        this.treatmentAdvice = in.readString();
        this.errorMessage = in.readString();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(classIndex);
        dest.writeString(classLabel);
        dest.writeFloat(confidence);
        dest.writeInt(status.ordinal());
        dest.writeString(treatmentAdvice);
        dest.writeString(errorMessage);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    public static final Creator<InferenceResult> CREATOR =
            new Creator<InferenceResult>() {
                @Override
                public InferenceResult createFromParcel(Parcel source) {
                    return new InferenceResult(source);
                }

                @Override
                public InferenceResult[] newArray(int size) {
                    return new InferenceResult[size];
                }
            };
}
