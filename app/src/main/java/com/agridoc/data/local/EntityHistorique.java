package com.agridoc.data.local;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "historique_diagnostic")
public class EntityHistorique {

    @PrimaryKey(autoGenerate = true)
    private int id;

    private String nomPlante;
    private String nomMaladie;
    private float scoreConfiance;
    private String imagePath;
    private long dateTimestamp;

    public EntityHistorique(String nomPlante, String nomMaladie, float scoreConfiance, String imagePath, long dateTimestamp) {
        this.nomPlante = nomPlante;
        this.nomMaladie = nomMaladie;
        this.scoreConfiance = scoreConfiance;
        this.imagePath = imagePath;
        this.dateTimestamp = dateTimestamp;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNomPlante() {
        return nomPlante;
    }

    public void setNomPlante(String nomPlante) {
        this.nomPlante = nomPlante;
    }

    public String getNomMaladie() {
        return nomMaladie;
    }

    public void setNomMaladie(String nomMaladie) {
        this.nomMaladie = nomMaladie;
    }

    public float getScoreConfiance() {
        return scoreConfiance;
    }

    public void setScoreConfiance(float scoreConfiance) {
        this.scoreConfiance = scoreConfiance;
    }

    public String getImagePath() {
        return imagePath;
    }

    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
    }

    public long getDateTimestamp() {
        return dateTimestamp;
    }

    public void setDateTimestamp(long dateTimestamp) {
        this.dateTimestamp = dateTimestamp;
    }
}
