# Développement d'un microservice IA pour la société TEAMBER



## 1. Développement "task_assigner" en cours

__organisation du service :__

1. le __front__ envoie les données légères à l'__API__ (la liste d'utilisateur, peut-être une date de début et de fin pour mieux sélectionner les tâches dans la BDD ensuite)
2. l'__API__ va chercher les données auprès du __back__
3. l'__API__ assigner les tâches aux utilisateurs de manière optimale
4. <span style="color:red"> l'__API__ retourne les données au __back__ ? A discuter.</span>

__avancée des travaux :__
1. preuve de concept terminée avec des données synthétiques (voir *demo_notebooks/task_assigner.ipynb*)
2. rédaction des requêtes pour aller chercher les données auprès du back en cours. Plus précisément : on peut aller chercher les dispos, la matrice projet, il manque encore la matrice de compétences et la liste des tâches à assigner.


## 2. Développement "planning_optimizer" à venir

__avancée des travaux :__
- dans main.py, l'endpoint *solve* va chercher les données, les prépare, génère une solution mathématique, valide la solution par une batterie de tests, retourne la solution au format JSON formatted string. 
- dans main.py, un endpoint *test_with_random_data* teste la fonction __solve()__ avec des données générées aléatoirement et de manière cohérente (propose un grand panel de possibilitées pour la situation des entreprises: surchargées, sous-effectif, sous-chargées, correctes, peu de projets, bcp de projets ...).

__à faire :__
- endpoint *solve* : manque plus qu'à pouvoir préciser une date de départ et de fin pour ensuite aller chercher les bonnes taches dans le BACK. Le curseur politique aussi.

## Notes

- Faire tourner une RestAPI en local avec __uvicorn__ : dans un terminal PowerShell, lancer la commande :
```
uvicorn main:app --reload
```