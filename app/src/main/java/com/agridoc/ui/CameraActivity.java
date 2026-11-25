package com.agridoc.ui;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.camera.core.CameraSelector;
import androidx.camera.core.ImageCapture;
import androidx.camera.core.ImageCaptureException;
import androidx.camera.core.Preview;
import androidx.camera.lifecycle.ProcessCameraProvider;
import androidx.camera.view.PreviewView;
import androidx.core.content.ContextCompat;

import com.agridoc.R;
import com.agridoc.utils.PermissionManager;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.common.util.concurrent.ListenableFuture;

import java.io.File;
import java.util.concurrent.ExecutionException;

/**
 * Activité de gestion du flux caméra temps réel (CameraX), de la demande de permission
 * et de la capture de la photo pour le diagnostic des maladies.
 *
 * Développeur : Moumoun (Issues #06, #07, #08)
 */
public class CameraActivity extends AppCompatActivity {

    private static final String TAG = "CameraActivity";

    private PreviewView viewFinder;
    private FloatingActionButton btnCapturePhoto;
    private ImageButton btnBack;
    private LinearLayout layoutPermissionDenied;
    private Button btnGrantPermission;

    private ImageCapture imageCapture;
    private ProcessCameraProvider cameraProvider;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        // Initialisation des vues UI
        initViews();

        // Gestionnaires d'événements
        setupClickListeners();

        // Vérification et demande des permissions caméra (Issue #07)
        checkAndRequestPermissions();
    }

    private void initViews() {
        viewFinder = findViewById(R.id.viewFinder);
        btnCapturePhoto = findViewById(R.id.btnCapturePhoto);
        btnBack = findViewById(R.id.btnBack);
        layoutPermissionDenied = findViewById(R.id.layoutPermissionDenied);
        btnGrantPermission = findViewById(R.id.btnGrantPermission);
    }

    private void setupClickListeners() {
        // Bouton retour
        btnBack.setOnClickListener(v -> finish());

        // Bouton de capture d'image (Issue #08)
        btnCapturePhoto.setOnClickListener(v -> capturePhoto());

        // Bouton de demande de permission en cas de refus
        btnGrantPermission.setOnClickListener(v -> PermissionManager.requestCameraPermission(
                CameraActivity.this,
                PermissionManager.CAMERA_PERMISSION_REQUEST_CODE
        ));
    }

    /**
     * Vérifie si la permission Caméra est accordée (Issue #07).
     */
    private void checkAndRequestPermissions() {
        if (PermissionManager.hasCameraPermission(this)) {
            showCameraUi();
            startCamera();
        } else {
            hideCameraUi();
            PermissionManager.requestCameraPermission(this, PermissionManager.CAMERA_PERMISSION_REQUEST_CODE);
        }
    }

    /**
     * Affichage de l'interface de caméra active.
     */
    private void showCameraUi() {
        layoutPermissionDenied.setVisibility(View.GONE);
        viewFinder.setVisibility(View.VISIBLE);
        btnCapturePhoto.setVisibility(View.VISIBLE);
    }

    /**
     * Masquage de l'interface caméra et affichage de l'écran de refus de permission.
     */
    private void hideCameraUi() {
        layoutPermissionDenied.setVisibility(View.VISIBLE);
        viewFinder.setVisibility(View.GONE);
        btnCapturePhoto.setVisibility(View.GONE);
    }

    /**
     * Traitement de la réponse à la demande de permission runtime (Issue #07).
     */
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PermissionManager.CAMERA_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                showCameraUi();
                startCamera();
            } else {
                hideCameraUi();
                Toast.makeText(this, R.string.camera_permission_denied_message, Toast.LENGTH_LONG).show();
            }
        }
    }

    /**
     * Initialisation et liaison de CameraX avec le cycle de vie de l'activité (Issue #06).
     */
    private void startCamera() {
        ListenableFuture<ProcessCameraProvider> cameraProviderFuture = ProcessCameraProvider.getInstance(this);

        cameraProviderFuture.addListener(() -> {
            try {
                cameraProvider = cameraProviderFuture.get();
                bindCameraUseCases();
            } catch (ExecutionException | InterruptedException e) {
                Log.e(TAG, "Erreur d'initialisation du ProcessCameraProvider: ", e);
                Toast.makeText(this, R.string.camera_capture_error, Toast.LENGTH_SHORT).show();
            }
        }, ContextCompat.getMainExecutor(this));
    }

    /**
     * Configuration des cas d'usage Preview et ImageCapture (Issue #06 & #08).
     */
    private void bindCameraUseCases() {
        if (cameraProvider == null) return;

        // Délier tous les cas d'usage existants
        cameraProvider.unbindAll();

        // 1. Cas d'usage Preview (Aperçu)
        Preview preview = new Preview.Builder().build();
        preview.setSurfaceProvider(viewFinder.getSurfaceProvider());

        // 2. Cas d'usage ImageCapture (Prise de vue)
        imageCapture = new ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build();

        // 3. Sélection de la caméra arrière
        CameraSelector cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA;

        try {
            // Lier les cas d'usage au cycle de vie de l'activité
            cameraProvider.bindToLifecycle(
                    this,
                    cameraSelector,
                    preview,
                    imageCapture
            );
        } catch (Exception e) {
            Log.e(TAG, "Erreur lors de la liaison des cas d'usage CameraX: ", e);
        }
    }

    /**
     * Capture de l'image et sauvegarde temporaire dans le cache local (Issue #08).
     * Transmet le chemin du fichier à ResultActivity via Intent.
     */
    private void capturePhoto() {
        if (imageCapture == null) {
            Log.e(TAG, "ImageCapture n'est pas initialisé.");
            return;
        }

        // Fichier temporaire de sortie dans le répertoire cache de l'application
        File photoFile = new File(getCacheDir(), "agridoc_scan_" + System.currentTimeMillis() + ".jpg");

        ImageCapture.OutputFileOptions outputFileOptions = new ImageCapture.OutputFileOptions.Builder(photoFile).build();

        btnCapturePhoto.setEnabled(false);

        imageCapture.takePicture(
                outputFileOptions,
                ContextCompat.getMainExecutor(this),
                new ImageCapture.OnImageSavedCallback() {
                    @Override
                    public void onImageSaved(@NonNull ImageCapture.OutputFileResults outputFileResults) {
                        btnCapturePhoto.setEnabled(true);
                        Log.d(TAG, "Photo capturée avec succès : " + photoFile.getAbsolutePath());

                        // Transmission de l'image à ResultActivity (Issue #08)
                        Intent intent = new Intent(CameraActivity.this, ResultActivity.class);
                        intent.putExtra("image_path", photoFile.getAbsolutePath());
                        startActivity(intent);
                        finish();
                    }

                    @Override
                    public void onError(@NonNull ImageCaptureException exception) {
                        btnCapturePhoto.setEnabled(true);
                        Log.e(TAG, "Erreur lors de la prise de vue : ", exception);
                        Toast.makeText(CameraActivity.this, R.string.camera_capture_error, Toast.LENGTH_SHORT).show();
                    }
                }
        );
    }
}
