# Issue #12 : Intégration de Room & Repository dans l'Historique

- **Assigné à** : Développeur 6 (Room & Persistance)
- **Branche** : `feature/data-room-historique`
- **Priorité** : Haute

## 📌 Description
Connecter `HistoriqueActivity.java` à `HistoriqueRepository.java` pour charger asynchronement les diagnostics stockés en base SQLite via Room.

## 📋 Critères d'Acceptation
- [ ] Lecture asynchrone des diagnostics enregistrés dans la table `historique_diagnostic`.
- [ ] Sauvegarde automatique d'un nouveau diagnostic lors de la validation sur `ResultActivity`.
- [ ] Mise à jour dynamique de la liste dans l'UI.
