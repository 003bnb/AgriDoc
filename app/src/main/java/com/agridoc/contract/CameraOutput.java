package com.agridoc.contract;

import android.os.Parcel;
import android.os.Parcelable;
import android.os.Parcelable.Creator;

/**
 * Contrat de sortie de la capture caméra.
 *
 * Un objet {@code CameraOutput} est produit par l'écran caméra
 * (implémentation de {@link CameraOutputContract}) et transmis à
 * l'écran de résultat via {@link NavigationContract#cameraToResult}.
 *
 * Il décrit :
 *  - le chemin du fichier image capturée,
 *  - l'orientation EXIF à appliquer,
 *  - le timestamp de la capture.
 *
 * Les champs EXIF et le timestamp servent au prétraitement
 * (Moumoun, issue #08) et à la traçabilité de l'observation.
 */
public final class CameraOutput implements Parcelable {

    /** Chemin absolu du fichier image dans le stockage applicatif. */
    public final String imagePath;

    /** Orientation EXIF (degrés, 0 / 90 / 180 / 270) ou -1 si inconnue. */
    public final int exifOrientation;

    /** Timestamp en millisecondes (System.currentTimeMillis). */
    public final long timestamp;

    /** {@code true} si la capture a réussi et l'image est exploitable. */
    public final boolean isValid;

    /** Message d'erreur si {@code isValid == false}. */
    public final String errorMessage;

    public CameraOutput(String imagePath, int exifOrientation, long timestamp,
                        boolean isValid, String errorMessage) {
        this.imagePath = imagePath;
        this.exifOrientation = exifOrientation;
        this.timestamp = timestamp;
        this.isValid = isValid;
        this.errorMessage = errorMessage;
    }

    /** Fabrique : capture réussie. */
    public static CameraOutput success(String imagePath, int exifOrientation,
                                       long timestamp) {
        return new CameraOutput(imagePath, exifOrientation, timestamp, true, null);
    }

    /** Fabrique : capture échouée. */
    public static CameraOutput error(String errorMessage) {
        return new CameraOutput(null, -1, 0L, false, errorMessage);
    }

    public boolean isSuccess() {
        return isValid;
    }

    // ----------------------------------------------------------------
    // Parcelable
    // ----------------------------------------------------------------

    private CameraOutput(Parcel in) {
        this.imagePath = in.readString();
        this.exifOrientation = in.readInt();
        this.timestamp = in.readLong();
        this.isValid = in.readInt() == 1;
        this.errorMessage = in.readString();
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(imagePath);
        dest.writeInt(exifOrientation);
        dest.writeLong(timestamp);
        dest.writeInt(isValid ? 1 : 0);
        dest.writeString(errorMessage);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    public static final Creator<CameraOutput> CREATOR =
            new Creator<CameraOutput>() {
                @Override
                public CameraOutput createFromParcel(Parcel source) {
                    return new CameraOutput(source);
                }

                @Override
                public CameraOutput[] newArray(int size) {
                    return new CameraOutput[size];
                }
            };
}
