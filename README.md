# Développement d'un microservice IA pour la société TEAMBER



## 1. Développement "task_assigner" en cours

__organisation du service :__

1. le __front__ envoie les données légères à l'__API__ (la liste d'utilisateur, peut-être une date de début et de fin pour mieux sélectionner les tâches dans la BDD ensuite)
2. l'__API__ va chercher les données auprès du __back__
3. l'__API__ assigner les tâches aux utilisateurs de manière optimale
4. <span style="color:red"> l'__API__ retourne les données au __back__ ? A discuter.</span>

__avancée des travaux :__
1. L'endpoint *task_assigner/* va chercher les données auprès du BACK, les prépare, génère une solution mathématique, valide la solution par une batterie de tests, retourne la solution au format JSON formatted string. 
2. Possibilité de spécifier des préférences d'optimisation via différents paramètres lors de l'appel à l'endpoint *task_assigner/*.
3. L'endpoint *test_task_assigner_with_random_data/* teste la fonction __task_assigner()__ avec des données générées aléatoirement et de manière cohérente (propose un grand panel de possibilitées pour la situation des entreprises: surchargées, sous-effectif, sous-chargées, correctes, peu de projets, bcp de projets ...).
3. Implémentation de réponses HTTP pour les éxceptions, selon les cas de figures, à tous les niveaux du process 
    1. Réception des paramètres front,
    2. Collecte des données auprès du BACK
    3. __Vérification de la cohérence des données (à faire)__
    4. Mise en forme des données
    5. Production d'une solution mathématique

__ensuite:__

1. Voir comment on teste la fonctionnalité. Avec des données aléatoires ? Avec des vraies données provenant du BACK ?
    - __idée__: générérer des triplets (variables_entrees, fonction, variables_sorties_attendues) à différents instants du programme. Les stocker dans un répertoire *synthetic_data_test/*et s'en servir pour tester ensuite chaque fonction du module.





## 2. Développement "planning_optimizer" à venir

__avancée des travaux :__
1. preuve de concept terminée avec des données synthétiques (voir *demo_notebooks/task_assigner.ipynb*)

# Notes

- Faire tourner une RestAPI en local avec __uvicorn__ : dans un terminal PowerShell, lancer la commande :
```
uvicorn main:app --reload
```
- Générer un *requirements.txt* dans le répertoire courant :
```
pipreqs --force .
```

## Docker
1. This will build the Docker image of the Dockerfile, and give the image the tag "myimg"
```
docker build -t myimg .
```    
2. This will run a container corresponding to the Docker image "myimg"  on ports 8000:8000, name it "myctn"
```
docker run -p 8000:8000 --name myctn myimg
```

## Jenkins 

- [Installing Jenkins for WSL (Windows Subsystem Linux 2)](https://dev.to/davidkou/install-jenkins-in-windows-subsystem-for-linux-wsl2-209)
- [Jenkins on OVHcloud Managed Kubernetes](https://docs.ovh.com/ie/en/kubernetes/installing-jenkins/)

##### Starting Jenkins on WSL2 :
1. Open Ubuntu on the start menu of your windows machine

2. Enter command line 
```
sudo service jenkins start
```
3. Go to http://localhost:8080/ on your web browser
4. Enter login and password : _admin f236a8ea59c141e784d241170f18e67e
