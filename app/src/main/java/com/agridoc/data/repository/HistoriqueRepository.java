package com.agridoc.data.repository;

import android.content.Context;
import com.agridoc.data.local.AppDatabase;
import com.agridoc.data.local.DaoHistorique;
import com.agridoc.data.local.EntityHistorique;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class HistoriqueRepository {

    private final DaoHistorique daoHistorique;
    private final ExecutorService executorService;

    public HistoriqueRepository(Context context) {
        AppDatabase database = AppDatabase.getInstance(context);
        this.daoHistorique = database.daoHistorique();
        this.executorService = Executors.newSingleThreadExecutor();
    }

    public interface RepositoryCallback<T> {
        void onComplete(T result);
    }

    public void insert(EntityHistorique historique, RepositoryCallback<Long> callback) {
        executorService.execute(() -> {
            long id = daoHistorique.insertDiagnostic(historique);
            if (callback != null) {
                callback.onComplete(id);
            }
        });
    }

    public void getAllDiagnostics(RepositoryCallback<List<EntityHistorique>> callback) {
        executorService.execute(() -> {
            List<EntityHistorique> list = daoHistorique.getAllDiagnostics();
            if (callback != null) {
                callback.onComplete(list);
            }
        });
    }
}
