package com.agridoc;

import android.content.Context;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.ext.junit.runners.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.assertEquals;

/**
 * Exemple de test d'instrumentation exécuté sur un appareil ou un émulateur Android.
 *
 * @see <a href="http://d.android.com/tools/testing">Documentation de test</a>
 */
@RunWith(AndroidJUnit4.class)
public class ExempleInstrumentedTest {

    @Test
    public void useAppContext() {
        // Contexte de l'application sous test.
        Context appContext = InstrumentationRegistry.getInstrumentation().getTargetContext();
        assertEquals("com.agridoc", appContext.getPackageName());
    }
}
