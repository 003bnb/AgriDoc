# CAMEROON_DATA_COLLECTION_PROTOCOL — Protocole de Collecte Camerounaise AgriDoc V1

**Version :** 1.0  
**Statut :** Proposition (aucune collecte n'a été effectuée à ce jour)  
**Dépôt :** https://github.com/003bnb/AgriDoc  
**Auteur :** Équipe IA (Keumeka, Messi) avec référent agronomique (à recruter)  
**Dernière révision :** 2026-11-22

---

## 1. Objectif

Définir un protocole de collecte d'images agricoles au Cameroun pour alimenter le dataset d'entraînement du modèle AgriDoc V1. Ce protocole s'applique aux classes non couvertes par les sources publiques (ravageurs, carences, et complément pour les maladies avec représentation locale insuffisante).

**Aucune donnée camerounaise n'a été collectée à ce jour.** Ce document prépare la collecte future.

---

## 2. Cultures Ciblées

| Culture | Nom scientifique | Statut V1 |
|---------|-----------------|-----------|
| Manioc | Manihot esculenta | ✅ Prise en charge |
| Tomate | Solanum lycopersicum | ✅ Prise en charge |
| Maïs | Zea mays | ✅ Prise en charge |

**Autres cultures :** strictement exclues de la V1 (réservé à V2).

---

## 3. Types de Symptômes Recherchés

### 3.1 Maladies (visibles sur feuille)

Pour chaque culture, les symptômes foliaires suivants doivent être recherchés et documentés :

| Culture | Symptômes visuels recherchés | Exemple de maladie (à valider par agronome) |
|---------|-----------------------------|---------------------------------------------|
| Manioc | Marbrures, déformations, jaunissement, nécroses foliaires | Mosaïque du manioc |
| Tomate | Taches nécrotiques, duvet, enroulement, jaunissement, flétrissement | Mildiou, tache bactérienne, virus |
| Maïs | Pustules, taches longues, nécroses, jaunissement | Rouille, tache foliaire |

### 3.2 Ravageurs (uniquement si l'espèce est suffisamment visible)

| Élément | Règle |
|---------|-------|
| Identification d'espèce | **Uniquement si le ravageur est clairement visible sur la photo** |
| Dégâts visibles | Trous de mastication, galeries, déformations, présence d'insecte |
| Dégâts non spécifiques | Ne doivent **jamais** être présentés comme l'identification certaine d'une espèce |
| Ravageur non visible | Ne pas créer de classe "ravageur" sur la seule base de dégâts non spécifiques |

### 3.3 Carences nutritionnelles

| Élément | Règle |
|---------|-------|
| Nutriment | **Doit être spécifié** (azote, phosphore, potassium, magnésium, etc.) |
| Validation | Uniquement par un référent agronomique ayant observé sur le terrain |
| Symptômes visuels | Jaunissement, nécrose, décoloration spécifiques au nutriment |

### 3.4 Plante saine

| Élément | Règle |
|---------|-------|
| Critère | Feuille sans aucun symptôme visible |
| Validation | Confirmation par le référent agronomique |

---

## 4. Conditions de Prise de Vue

### 4.1 Vues acceptées

| Type de vue | Accepté ? | Commentaire |
|-------------|-----------|-------------|
| Feuille entière (dessus) | ✅ Oui | Vue principale recommandée |
| Feuille entière (dessous) | ✅ Oui | Utile pour certains ravageurs et moisissures |
| Feuille en biseau / angle | ✅ Oui | À inclure pour la robustesse |
| Partie identifiable de feuille | ✅ Oui | Si l'organe est reconnaissable |
| Parcelle entière | ❌ Non | Hors périmètre V1 |
| Plusieurs plantes sans cadrage feuille | ❌ Non | Hors périmètre V1 |
| Main, ciel, sol, objet non végétal | ❌ Non | Classe "inconnu" uniquement (à générer séparément) |

### 4.2 Qualité technique minimale

| Critère | Exigence |
|---------|----------|
| Netteté | La feuille doit être suffisamment nette pour distinguer les symptômes |
| Éclairage | Lumière naturelle suffisante, éviter les zones d'ombre marquée sur le sujet |
| Résolution | Suffisante pour voir les détails symptomatiques (pas de minimum strict, mais éviter les images trop petites) |
| Cadrage | La feuille ou la partie identifiable doit占据 une part significative de l'image |

### 4.3 Conditions environnementales recommandées

- Éclairage : soleil, ombre, nuageux, matin, après-midi (variété pour la robustesse)
- Stade de croissance : jeune feuille, feuille mature, feuille âgée
- Orientation : dessus, dessous, en biseau
- Appareils : au moins 3 modèles de smartphones différents (pour couvrir la variabilité des capteurs)

---

## 5. Métadonnées à Enregistrer

Pour chaque image capturée, les métadonnées suivantes doivent être enregistrées dans un fichier CSV ou JSON associé :

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `image_id` | String | Oui | Identifiant unique (ex. CM_20261122_001) |
| `source` | String | Oui | Valeur fixe : "collecte_camerounaise" |
| `culture` | String | Oui | MANIOC, TOMATE, ou MAIS |
| `type_probleme` | String | Oui | MALADIE, RAVAGEUR, DEGAT_RAVAGEUR, CARENCE, SAIN |
| `classe` | String | Oui | Nom complet de la classe (ex. MANIOC_MALADIE_MOSAIQUE) |
| `region` | String | Oui | Région du Cameroun (ex. Centre, Ouest, Extrême-Nord) |
| `localite` | String | Oui | Localité ou village précis |
| `date_capture` | Date | Oui | Date de prise de vue |
| `stade_developpement` | String | Non | Jeune, mature, âgé (si connu) |
| `variete` | String | Non | Variété cultivée (si connue) |
| `organe_photographie` | String | Oui | Feuille_dessus, Feuille_dessous, Partie_feuille |
| `symptomes_observes` | String | Oui | Description des symptômes vus sur le terrain |
| `diagnostic_confirme` | Boolean | Oui | `true` si validé par l'agronome, `false` sinon |
| `validation_agronomique` | Boolean | Oui | `true` si le label a été validé par le référent |
| `valideur_id` | String | Non | Identifiant du référent agronomique (pas de nom complet pour protéger les données personnelles) |
| `role_valideur` | String | Non | Rôle (ex. "Agronome", "Technicien agricole") |
| `qualite_image` | String | Oui | EXCELLENTE, BONNE, MOYENNE, EXPLOITABLE_DIFFICILE |
| `luminosite` | String | Non | ADEQUATE, INSUFFISANTE, EXCESSIVE |
| `nettete` | String | Non | NETTE, LEGEREMENT_FLOUE, FLOUE |
| `appareil` | String | Non | Modèle de smartphone utilisé |
| `consentement_agriculteur` | Boolean | Oui | `true` si l'agriculteur a consenti à la prise de vue et à l'utilisation des images |

---

## 6. Système d'Annotation

### 6.1 Un seul label principal par image

Chaque image appartient à une seule classe. Si plusieurs problèmes sont présents sur une même feuille :
- Assigner à la classe la plus significative (la plus sévère ou la plus caractéristique)
- Ou exclure l'image si l'ambiguïté est trop grande

### 6.2 Validation par référent agronomique

| Étape | Responsable | Action |
|-------|-------------|--------|
| 1 | Collecteur | Prend la photo et enregistre les métadonnées de terrain |
| 2 | Référent agronomique | Examine la photo et les métadonnées, valide ou corrige le label |
| 3 | Référent agronomique | Renseigne `diagnostic_confirme` et `validation_agronomique` |
| 4 | Équipe IA | Intègre l'image dans le dataset uniquement si `validation_agronomique = true` |

### 6.3 Cas ambigus

| Situation | Procédure |
|-----------|-----------|
| Symptômes non clairs | L'image est marquée comme "à réexaminer" et soumise à un second avis |
| Plusieurs problèmes simultanés | Assigner à la classe la plus significative ou exclure |
| Ravageur non visible | Ne pas créer de label "ravageur" ; classer sous "dégât" ou exclure |
| Carence sans nutriment identifié | Ne pas créer de label "carence" ; exclure jusqu'à identification du nutriment |
| Culture hors V1 | Exclure immédiatement, ne pas intégrer au dataset |

---

## 7. Consentement et Protection des Données

**Note :** les modalités de consentement doivent être validées juridiquement et par les responsables de la collecte avant toute collecte réelle. Ce document prépare la collecte future ; il ne constitue pas un avis juridique.

| Règle | Description |
|-------|-------------|
| Consentement de l'agriculteur | Obtenu et consigné avant chaque prise de vue, selon des modalités qui devront être validées juridiquement et par les responsables de la collecte avant toute collecte réelle ; enregistré dans `consentement_agriculteur` |
| Données personnelles du valideur | Seul l'identifiant et le rôle sont enregistrés (pas de nom complet, pas de contact) |
| Localisation | Niveau localité/village uniquement (pas de coordonnées GPS précises si l'agriculteur s'y oppose) |
| Droit d'image | Les images restent la propriété du projet AgriDoc ; l'agriculteur est informé de l'usage (application mobile, entraînement d'IA) |
| Stockage | Images stockées localement, accès restreint à l'équipe projet |

---

## 8. Règles de Qualité

| Règle | Description |
|-------|-------------|
| Une image = une seule feuille (ou partie identifiable) | Éviter les images avec plusieurs feuilles superposées de plantes différentes |
| Pas de filtre lourd | Éviter les filtres qui modifient les couleurs symptomatiques |
| Pas de retouche | Ne pas modifier l'image pour cacher ou accentuer des symptômes |
| Vérification immédiate | Le collecteur vérifie sur place que l'image est exploitable avant de passer à la suivante |
| Sauvegarde immédiate | Les images et métadonnées sont sauvegardées dès la fin de la session de collecte |

---

## 9. Procédure pour les Cas Ambigus

```
1. Le collecteur prend la photo et note ses observations
2. Le collecteur signale l'ambiguïté dans `symptomes_observes`
3. Le référent agronomique examine la photo dans les 48 heures
4. Si le diagnostic est confirmé → l'image est intégrée avec le label validé
5. Si le diagnostic est incertain → l'image est marquée "à réexaminer" et soumise à un second avis
6. Si le second avis est également incertain → l'image est exclue du dataset d'entraînement
```

---

## 10. Nombre d'Images Cibles (à ajuster)

| Type de classe | Nombre cible par classe | Commentaire |
|----------------|------------------------|-------------|
| Maladies confirmées (ex. mosaïque manioc, mildiou tomate) | 50-100 images | À ajuster selon la disponibilité sur le terrain |
| Plante saine | 50-100 images par culture | Nécessaire pour l'équilibre des classes |
| Ravageurs (espèce visible) | 30-50 images | Plus difficile à collecter |
| Dégâts de ravageurs | 30-50 images | Plus facile à collecter que l'insecte lui-même |
| Carences (nutriment spécifié) | 30-50 images | Nécessite un agronome pour l'identification |
| Inconnu / non exploitable | 50-100 images | Images négatives générées |

**Ces chiffres sont indicatifs et doivent être ajustés selon la disponibilité réelle sur le terrain.**

---

## 11. Zones et Calendrier (à planifier)

| Région du Cameroun | Cultures prioritaires | Période de collecte suggérée |
|--------------------|----------------------|------------------------------|
| Zone forestière (Sud, Centre, Est) | Manioc, Maïs | Saison des pluies (symptômes plus visibles) |
| Zone de haute altitude (Ouest, Nord-Ouest) | Tomate, Maïs | Saison culturale principale |
| Zone sahélienne (Extrême-Nord) | Maïs, Tomate | Période d'irrigation |

**Le calendrier définitif doit être établi avec le référent agronomique recruté.**

---

## 12. Informations Manquantes

| Information | Impact | Vérification nécessaire |
|-------------|--------|------------------------|
| Référent agronomique recruté | Bloquant pour la validation des labels | À recruter avant le début de la collecte |
| Budget de collecte | Détermine l'ampleur de la collecte | À définir avec le chef de projet |
| Délai de collecte | Détermine le planning d'entraînement | À planifier |
| Appareils de collecte disponibles | Impacte la variété des capteurs | À inventorier |
