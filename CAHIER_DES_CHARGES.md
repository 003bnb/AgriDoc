# Cahier des charges — AgriDoc

- **Version :** 1.0 — document de cadrage pour l’équipe
- **État :** proposition MVP, avec décisions IA encore ouvertes
- **Dépôt :** [003bnb/AgriDoc](https://github.com/003bnb/AgriDoc)
- **Références du projet :** [feuille de route](.github/PROJECT_TASKS.md), [issue #15 — modèle TFLite et labels](.github/issues/issue-15-keumeka-messi-model-tflite.md)

## 1. Présentation

AgriDoc est une application Android destinée aux agriculteurs, exploitants et techniciens de terrain. Elle doit aider à repérer des maladies de plantes à partir d’une photo de feuille et présenter une recommandation associée.

La contrainte centrale est le fonctionnement **hors ligne** : la capture, la classification et la consultation de l’historique doivent fonctionner sans serveur ni connexion Internet. Le résultat est une aide au diagnostic ; l’application ne doit pas présenter une prédiction comme une certitude agronomique.

Ce cahier décrit le MVP attendu. Les classes couvertes par le modèle, son seuil de confiance et les conseils agronomiques doivent être confirmés par l’équipe avant d’être considérés comme définitifs.

## 2. Objectifs du MVP

1. Permettre de lancer un diagnostic depuis l’écran d’accueil.
2. Capturer une photo de feuille avec CameraX.
3. Préparer l’image selon le contrat réel du modèle IA.
4. Exécuter l’inférence localement avec TensorFlow Lite.
5. Présenter la classe prédite, son score et une recommandation validée.
6. Enregistrer et consulter les diagnostics sur l’appareil avec Room.

## 3. Utilisateurs et parcours principal

### Utilisateurs visés

- Agriculteurs et producteurs agricoles.
- Techniciens agricoles intervenant sur le terrain.

### Parcours nominal

1. L’utilisateur ouvre le tableau de bord et choisit **Scanner une plante**.
2. L’application demande la permission caméra au moment où elle est nécessaire.
3. L’utilisateur cadre une feuille et prend une photo.
4. L’application corrige l’orientation et prépare l’image selon le contrat documenté du modèle.
5. Le modèle TFLite s’exécute sur l’appareil, sans requête réseau.
6. L’écran résultat affiche la plante ou la classe reconnue, le diagnostic, le score et le conseil associé.
7. Le diagnostic est enregistré dans l’historique local.
8. L’utilisateur peut consulter l’historique ou revenir au tableau de bord.

Le parcours de sélection d’une image dans la galerie n’est pas confirmé pour le MVP. Il doit être décidé avant de conserver des permissions de lecture d’images qui ne seraient pas nécessaires au parcours caméra.

## 4. Exigences fonctionnelles

| ID | Exigence |
|---|---|
| F-01 | Le tableau de bord propose l’accès au scan et à l’historique. |
| F-02 | L’écran caméra affiche l’aperçu CameraX et gère l’autorisation caméra, son refus et son absence. |
| F-03 | Une photo capturée est transmise à l’étape résultat par un contrat documenté entre les rôles caméra et IA. |
| F-04 | Le prétraitement respecte les dimensions, le format couleur, la normalisation et la quantification attendus par le modèle. |
| F-05 | La classification fonctionne localement et associe chaque indice de sortie à la ligne correspondante de `labels.txt`. |
| F-06 | Le résultat présente le nom de classe, le score de confiance et un conseil associé à cette classe. |
| F-07 | Un échec de capture, un modèle indisponible ou une entrée non exploitable produit un état compréhensible et une possibilité de réessayer. |
| F-08 | Chaque diagnostic réussi est enregistré dans Room avec la plante, la maladie/classe, le score, la date et le chemin d’image si une image est conservée. |
| F-09 | L’écran historique affiche les diagnostics enregistrés et un état vide lorsqu’il n’y en a aucun. |
| F-10 | Aucun parcours nominal ne dépend d’Internet, d’un compte ou d’un service distant. |

### Contrat de diagnostic

Les issues IA actuelles prévoient une entrée candidate de **224×224 pixels RGB**. Cette valeur ne suffit pas à définir le tenseur : le modèle doit aussi documenter son type de données, sa disposition de canaux, sa plage de pixels et sa quantification.

L’issue #15 demande à Keumeka et Messi de confirmer ce contrat. Si le modèle retenu diffère, les responsables IA doivent documenter les changements nécessaires avant l’intégration. La liste de maladies et les textes actuellement présents dans `strings.xml` sont des éléments de départ ; ils ne constituent pas encore un catalogue de classes approuvé.

## 5. Exigences non fonctionnelles

- **Hors ligne :** aucune connexion réseau n’est requise pour scanner, inférer ou consulter l’historique.
- **Confidentialité :** les photos et diagnostics restent sur l’appareil dans le MVP ; aucun envoi distant n’est prévu.
- **Robustesse :** l’application doit gérer le refus de permission, les erreurs de caméra, les images illisibles et les erreurs de chargement du modèle.
- **Lisibilité :** le résultat doit distinguer clairement la classe, le score et le conseil ; les états d’erreur doivent proposer une action.
- **Traçabilité IA :** provenance, licence, contrat d’entrée/sortie et ordre des classes doivent être documentés avec le modèle.
- **Compatibilité :** respecter le socle Android déclaré dans Gradle jusqu’à approbation explicite d’un changement de configuration.

## 6. Socle technique de référence

Les versions déclarées dans le projet servent de référence pour ce MVP :

- Java 17, Android XML et Activities AndroidX.
- Android : minSdk 24, compileSdk 34, targetSdk 34.
- Android Gradle Plugin 8.2.2 et Gradle 8.2.
- CameraX 1.3.1.
- TensorFlow Lite 2.14.0 et TFLite Support 0.4.4.
- Room 2.6.1, SQLite, RecyclerView.
- Material Components 1.11.0 et ConstraintLayout 2.1.4.

Les fichiers Gradle et `gradle-wrapper.properties` sont protégés par les consignes du dépôt : toute modification doit être examinée et autorisée par Balawe avant d’être faite. Le modèle quantifié, s’il est livré, doit être inclus comme asset non compressé conformément au réglage déjà présent.

## 7. Architecture cible et responsabilités

| Membre | Responsabilité principale | Résultat attendu |
|---|---|---|
| **Balawe — Lead DevOps & Architecte** | Gitflow, cohérence de l’architecture, audit du manifeste/build, intégration des assets IA disponibles et coordination de l’intégration. | Branches et PR cohérentes, intégration du modèle vérifiable. |
| **Adoum — UI/UX & Dashboard** | Tableau de bord, interfaces résultat et navigation selon les issues #03 à #05. | Écrans utilisables et navigation vers scan, résultat et historique. |
| **Moumoun — Caméra & capture** | CameraX, cycle de vie de l’aperçu, permissions caméra et transfert de la photo selon les issues #06 à #08. | Capture fiable et contrat de transmission défini avec l’équipe IA. |
| **Keumeka — Lead IA** | Choix ou entraînement du modèle, export TFLite, chargement et inférence selon les issues #09 et #15. | Modèle réel, contrat documenté et prédictions exploitables. |
| **Messi — Data & prétraitement** | Prétraitement image/tensor, ordre des classes et fichier de labels selon les issues #10 et #15. | Entrées conformes au modèle et labels alignés sur ses sorties. |
| **Sam — Persistance, MVVM & QA** | Room, repository, ViewModel, historique et vérifications attribuées aux issues #11 à #14. | Diagnostics locaux persistés et parcours historique vérifié. |

### Organisation du code

- `com.agridoc.ui` : écrans et navigation.
- `com.agridoc.model` : modèle métier et classification IA.
- `com.agridoc.utils` : prétraitement d’images et utilitaires.
- `com.agridoc.data.local` : entité, DAO et base Room.
- `com.agridoc.data.repository` : accès aux données et coordination des opérations.

Les activités ne doivent pas contenir la logique d’inférence ni les requêtes Room directement. Les contrats entre caméra, classification, résultat et historique doivent être convenus avant leur intégration.

## 8. Répartition Git et intégration

- `main` reste la branche de référence publiée ; `devop` est la branche d’intégration du projet.
- Chaque rôle travaille sur sa branche de fonctionnalité issue de `devop`.
- Les changements arrivent dans `devop` par Pull Request avec description, périmètre et vérifications.
- Aucun commit direct sur `main` ou `devop`.
- Les changements de chaque PR restent limités au rôle et aux fichiers concernés.
- Les protections GitHub ne sont pas modifiées sans autorisation.

## 9. Critères d’acceptation du MVP

Le MVP est acceptable lorsque les points suivants sont vérifiés :

- [ ] Le projet compile avec le JDK et le SDK Android compatibles avec la configuration déclarée.
- [ ] L’application démarre et permet d’accéder au scan et à l’historique.
- [ ] Le refus de la permission caméra est géré sans plantage.
- [ ] Une capture peut être préparée et classifiée sans réseau.
- [ ] Le contrat du modèle et le fichier de labels correspondent exactement aux tenseurs et indices de sortie.
- [ ] L’écran résultat affiche le diagnostic et le score sans inventer de classe en cas d’erreur.
- [ ] Une recommandation validée est associée à la classe affichée.
- [ ] Le résultat est conservé localement et apparaît dans l’historique après redémarrage.
- [ ] Un historique vide et les erreurs de capture ou de modèle ont un état d’interface explicite.
- [ ] Les vérifications prévues par les issues QA sont passées et les limites connues sont consignées.

## 10. Décisions à confirmer avant la livraison

| Décision | Responsable à consulter | État |
|---|---|---|
| Liste finale des plantes et maladies couvertes par le modèle | Keumeka, Messi, Balawe | À confirmer |
| Source, licence et disponibilité du modèle TFLite réel | Keumeka | Bloquant — issue #15 |
| Forme, type, normalisation et quantification des entrées/sorties | Keumeka et Messi | Bloquant — issue #15 |
| Seuil de confiance et comportement en cas de prédiction incertaine | Keumeka, Adoum | À définir |
| Source et validation agronomique des conseils par classe | Équipe IA et référent agronomique | À valider |
| Conservation de l’image et utilité de l’accès à la galerie | Moumoun, Sam, Balawe | À confirmer |
| Appareils et versions Android utilisés pour la recette finale | Sam, équipe | À planifier |

## 11. Hors périmètre du MVP

Sauf décision ultérieure de l’équipe, le MVP ne comprend pas :

- serveur, compte utilisateur, synchronisation ou inférence cloud ;
- version iOS ou interface web ;
- diagnostic garanti ou remplacement d’un avis agronomique professionnel ;
- galerie d’images comme source d’entrée ;
- catalogue de traitements présenté comme validé sans source agronomique.

Toute extension de périmètre doit être ajoutée à la feuille de route avec un responsable et des critères d’acceptation.
