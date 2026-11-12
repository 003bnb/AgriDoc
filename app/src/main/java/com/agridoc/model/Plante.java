package com.agridoc.model;

public class Plante {

    private String nom;
    private String maladie;
    private float scoreConfiance;
    private String traitementConseille;

    public Plante() {
    }

    public Plante(String nom, String maladie, float scoreConfiance, String traitementConseille) {
        this.nom = nom;
        this.maladie = maladie;
        this.scoreConfiance = scoreConfiance;
        this.traitementConseille = traitementConseille;
    }

    public String getNom() {
        return nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public String getMaladie() {
        return maladie;
    }

    public void setMaladie(String maladie) {
        this.maladie = maladie;
    }

    public float getScoreConfiance() {
        return scoreConfiance;
    }

    public void setScoreConfiance(float scoreConfiance) {
        this.scoreConfiance = scoreConfiance;
    }

    public String getTraitementConseille() {
        return traitementConseille;
    }

    public void setTraitementConseille(String traitementConseille) {
        this.traitementConseille = traitementConseille;
    }
}
