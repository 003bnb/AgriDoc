package com.example.agridoc;

import android.graphics.Bitmap;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/**
 * Utilaire de prétraitement d'images pour le modèle d'inférence et de classification IA.
 * Permet de redimensionner les images au format 224x224 et de les convertir en ByteBuffer
 * pour les modèles TensorFlow Lite / LiteRT.
 */
public class ImageUtils {

    public static final int INPUT_IMAGE_WIDTH = 224;
    public static final int INPUT_IMAGE_HEIGHT = 224;
    public static final int CHANNEL_SIZE = 3; // RGB

    /**
     * Redimensionne une image Bitmap au format 224x224 requis par le modèle d'IA.
     *
     * @param originalBitmap Le Bitmap d'origine.
     * @return Le Bitmap redimensionné en 224x224 pixels.
     */
    public static Bitmap resizeTo224x224(Bitmap originalBitmap) {
        if (originalBitmap == null) {
            return null;
        }
        return Bitmap.createScaledBitmap(originalBitmap, INPUT_IMAGE_WIDTH, INPUT_IMAGE_HEIGHT, true);
    }

    /**
     * Redimensionne une image Bitmap à des dimensions cibles spécifiques.
     *
     * @param originalBitmap Le Bitmap d'origine.
     * @param targetWidth Largeur cible.
     * @param targetHeight Hauteur cible.
     * @return Le Bitmap redimensionné.
     */
    public static Bitmap resizeBitmap(Bitmap originalBitmap, int targetWidth, int targetHeight) {
        if (originalBitmap == null) {
            return null;
        }
        return Bitmap.createScaledBitmap(originalBitmap, targetWidth, targetHeight, true);
    }

    /**
     * Convertit un Bitmap en ByteBuffer Float (Float32) avec des valeurs de pixels normalisées entre 0.0f et 1.0f.
     *
     * @param bitmap Le Bitmap d'entrée.
     * @return Le ByteBuffer prêt pour l'inférence.
     */
    public static ByteBuffer convertBitmapToByteBufferFloat(Bitmap bitmap) {
        return convertBitmapToByteBufferFloat(bitmap, 0.0f, 255.0f);
    }

    /**
     * Convertit un Bitmap en ByteBuffer Float (Float32) avec une normalisation personnalisée (mean et std).
     * Formule : (pixel - mean) / std
     *
     * @param bitmap Le Bitmap d'entrée.
     * @param mean Valeur moyenne à soustraire (ex: 0.0f ou 127.5f).
     * @param std Écart-type pour la division (ex: 255.0f ou 127.5f).
     * @return Le ByteBuffer Float32 ordonné pour le modèle.
     */
    public static ByteBuffer convertBitmapToByteBufferFloat(Bitmap bitmap, float mean, float std) {
        if (bitmap == null) {
            return null;
        }

        Bitmap scaledBitmap = (bitmap.getWidth() == INPUT_IMAGE_WIDTH && bitmap.getHeight() == INPUT_IMAGE_HEIGHT)
                ? bitmap
                : resizeTo224x224(bitmap);

        // Allocation de 4 octets par float (224 x 224 x 3 x 4)
        ByteBuffer byteBuffer = ByteBuffer.allocateDirect(4 * INPUT_IMAGE_WIDTH * INPUT_IMAGE_HEIGHT * CHANNEL_SIZE);
        byteBuffer.order(ByteOrder.nativeOrder());

        int[] intValues = new int[INPUT_IMAGE_WIDTH * INPUT_IMAGE_HEIGHT];
        scaledBitmap.getPixels(intValues, 0, scaledBitmap.getWidth(), 0, 0, scaledBitmap.getWidth(), scaledBitmap.getHeight());

        int pixelIndex = 0;
        for (int i = 0; i < INPUT_IMAGE_HEIGHT; ++i) {
            for (int j = 0; j < INPUT_IMAGE_WIDTH; ++j) {
                final int val = intValues[pixelIndex++];

                // Extraction des composantes RGB
                float r = ((val >> 16) & 0xFF);
                float g = ((val >> 8) & 0xFF);
                float b = (val & 0xFF);

                // Normalisation et écriture dans le buffer
                byteBuffer.putFloat((r - mean) / std);
                byteBuffer.putFloat((g - mean) / std);
                byteBuffer.putFloat((b - mean) / std);
            }
        }

        byteBuffer.rewind();
        return byteBuffer;
    }

    /**
     * Convertit un Bitmap en ByteBuffer quantifié (Uint8 / 1 octet par canal par pixel).
     *
     * @param bitmap Le Bitmap d'entrée.
     * @return Le ByteBuffer Uint8.
     */
    public static ByteBuffer convertBitmapToByteBufferQuantized(Bitmap bitmap) {
        if (bitmap == null) {
            return null;
        }

        Bitmap scaledBitmap = (bitmap.getWidth() == INPUT_IMAGE_WIDTH && bitmap.getHeight() == INPUT_IMAGE_HEIGHT)
                ? bitmap
                : resizeTo224x224(bitmap);

        // Allocation de 1 octet par valeur (224 x 224 x 3)
        ByteBuffer byteBuffer = ByteBuffer.allocateDirect(INPUT_IMAGE_WIDTH * INPUT_IMAGE_HEIGHT * CHANNEL_SIZE);
        byteBuffer.order(ByteOrder.nativeOrder());

        int[] intValues = new int[INPUT_IMAGE_WIDTH * INPUT_IMAGE_HEIGHT];
        scaledBitmap.getPixels(intValues, 0, scaledBitmap.getWidth(), 0, 0, scaledBitmap.getWidth(), scaledBitmap.getHeight());

        int pixelIndex = 0;
        for (int i = 0; i < INPUT_IMAGE_HEIGHT; ++i) {
            for (int j = 0; j < INPUT_IMAGE_WIDTH; ++j) {
                final int val = intValues[pixelIndex++];

                byteBuffer.put((byte) ((val >> 16) & 0xFF));
                byteBuffer.put((byte) ((val >> 8) & 0xFF));
                byteBuffer.put((byte) (val & 0xFF));
            }
        }

        byteBuffer.rewind();
        return byteBuffer;
    }
}
