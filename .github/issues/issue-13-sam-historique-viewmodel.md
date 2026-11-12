# Issue #13 : Implémentation MVVM avec `HistoriqueViewModel.java` (Chapitre 9)

- **Assigné à** : Sam (Persistance & QA)
- **Branche** : `feature/data-room-historique`
- **Priorité** : Haute

## 📌 Description
Implémenter le modèle MVVM en créant `HistoriqueViewModel.java` pour isoler la logique de données et conserver l'état lors de la rotation de l'écran.

## 📋 Critères d'Acceptation
- [ ] Extension de `androidx.lifecycle.ViewModel` ou `AndroidViewModel`.
- [ ] Exposition de `LiveData<List<EntityHistorique>>` ou callbacks observés par `HistoriqueActivity`.
- [ ] Persistance des données d'historique lors du changement de configuration (rotation).
