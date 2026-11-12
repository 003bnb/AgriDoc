package com.agridoc.data.local;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;

import java.util.List;

@Dao
public interface DaoHistorique {

    @Insert
    long insertDiagnostic(EntityHistorique historique);

    @Query("SELECT * FROM historique_diagnostic ORDER BY dateTimestamp DESC")
    List<EntityHistorique> getAllDiagnostics();

    @Query("SELECT * FROM historique_diagnostic WHERE id = :id LIMIT 1")
    EntityHistorique getDiagnosticById(int id);

    @Delete
    void deleteDiagnostic(EntityHistorique historique);

    @Query("DELETE FROM historique_diagnostic")
    void deleteAllDiagnostics();
}
