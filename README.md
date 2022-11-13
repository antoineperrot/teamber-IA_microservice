# Développement d'un microservice IA pour la société TEAMBER

## Organisation du dépôt

- *api/* contient tout ce qui relève des interfaces avec le back et le front Wandeed.
- *api/data_handling/* contient tous les outils permettant le nettoyage des données
fournies par le back.
- *my_module/* contient les fonctionnalités d'optimisation, sensées recevoir des données propres.


## Fonctionnement général du webservice :

1. le __front__ envoie les données légères à l'__API__ (token d'accès BDD, 
date début sprint, date fin sprint, préferences d'optimisation)
2. l'__API__ va chercher les données auprès du __back__ avec en paramètres 
(token d'accès BDD, date début sprint, date fin sprint)
3. l'__API__ vérifier que les données récupérées sont valides, 
sinon retourne une HTTP Exception, status code 422.
3. l'__API__  effectue l'opération d'optimisation. Si la procédure échoue 
retourne une HTTP Exception, status code 422.
4. <span style="color:red"> l'__API__ retourne les données au __back__ ? A discuter.</span>

## 1. Task Assigner

__avancée des travaux :__
1. L'endpoint *task_assigner/* va chercher les données auprès du BACK, les prépare, génère une solution mathématique, valide la solution par une batterie de tests, retourne la solution au format JSON formatted string. 
2. Possibilité de spécifier des préférences d'optimisation via différents paramètres lors de l'appel à l'endpoint *task_assigner/*.
3. L'endpoint *test_task_assigner_with_random_data/* teste la fonction __task_assigner()__ avec des données générées aléatoirement et de manière cohérente (propose un grand panel de possibilitées pour la situation des entreprises: surchargées, sous-effectif, sous-chargées, correctes, peu de projets, bcp de projets ...).
3. Implémentation de réponses HTTP pour les éxceptions, selon les cas de figures, à tous les niveaux du process 
    1. Réception des paramètres front,
    2. Collecte des données auprès du BACK
    3. Vérification de la cohérence des données
    4. Mise en forme des données
    5. Production d'une solution mathématique

__ensuite:__

1. Se construire un jeu de données réelles (provenant des utilisateurs wandeed) 
et le stocker dans un dossier à l'intérieur du micro-service afin de :
    - A) S'assurer qu'elle fonctionne dans un nombre de cas maximal.
    - B) A l'avenir : pouvoir s'assurer de la reproductibilité des résultats fournis par le programme.

2. Auprès de quelle URL aller chercher les données ? Si j'ai bien compris, un client Wandeed = 
une entité à part, une URL? l'URL où aller chercher les données en BDD est donc possiblement 
un paramètre à précisier lors des requêtes auprès de mon API ?



## 2. Planning Optimizer

[__Proof of Concept notebook__](https://github.com/antoineperrot/teamber-IA_microservice/blob/main/demo_notebooks/planning_optimizer.ipynb)
### Avancée des travaux
- [x] Aller chercher les données auprès du Back
- [ ] Gérer les données brutes Wandeed
    - [x] Nettoyage des horaires utilisateurs
    - [ ] Découpage des tâches entre les utilisateurs
    - [ ] Prise en compte des impératifs

...

### Tests

- [x] Fonctionnalités de nettoyages des horaires
- [ ] Prise en compte des impératifs
- [ ] Programme d'optimisation
    - [ ] Tester les fonctions de calcul de potentiel
    - [ ] Tester les fonctions de permutations des tâches

...


### TODO List
- Modifier requête pour avoir les niveaux de priorité des tâches

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


[10:41] Gaylord PETIT

__Obtenir les impératifs :__
{
    "select": [
        "evt_spkevenement",
        "evt_sfkprojet",
        "evt_dduree",
        "lgl_sfkligneparent",
    ],
    "from": "lst_vevenement_py",
    "where": {
        "condition": "and",
        "rules": [
            {
                "label": "evt_xdate_debut",
                "field": "evt_xdate_debut",
                "operator": "greaterthan",
                "type": "date",
                "value": f"{datein_isoformat}"
            },
            {
                "label": "evt_xdate_fin",
                "field": "evt_xdate_fin",
                "operator": "lessthan",
                "type": "date",
                "value": f"{dateout_isoformat}"
            },
            {
                "label": "lgl_sfkligneparent",
                "field": "lgl_sfkligneparent",
                "operator": "isnotnull",
                "type": "integer",
                "value": "none"
            },
            {
                "condition": "and",
                "rules": [
                    {
                        "label": "ecu_bsysteme",
                        "field": "ecu_bsysteme",
                        "operator": "equal",
                        "type": "integer",
                        "value": 1
                    },
                    {
                        "label": "ecu_bsysteme",
                        "field": "ecu_bsysteme",
                        "operator": "equal",
                        "type": "integer",
                        "value": 2
                    }
                ]
            }
        ]
    },
}


__Obtenir les horaires de travail :__
{
    "select": [
        "epu_sfkutilisateur",
        "epl_employe_horaire",
        "epl_xdebutperiode",
        "epl_xfinperiode"
    ],
    "from": "lst_vutilisateur_horaires_py",
    "where": {
        "condition": "and",
        "rules": [
            {
                "label": "epl_xdebutperiode",
                "field": "epl_xdebutperiode",
                "operator": "greaterthan",
                "type": "date",
                "value": f"{datein_isoformat}"
            },
            {
                "label": "epl_xfinperiode",
                "field": "epl_xfinperiode",
                "operator": "lessthan",
                "type": "date",
                "value": f"{dateout_isoformat}"
            }
        ]
    }
}

__Obtenir les tâches non planifiées:__


[10:49] Antoine PERROT
{
    "select": [
        "evt_spkevenement",
        "evt_sfkprojet",
        "evt_dduree",
        "lgl_sfkligneparent",
    ],
    "from": "lst_vevenement_py",
    "where": {
        "condition": "and",
        "rules": [
            {
                "label": "evt_xdate_debut",
                "field": "evt_xdate_debut",
                "operator": "greaterthan",
                "type": "date",
                "value": f"{datein_isoformat}"
            },
            {
                "label": "evt_xdate_fin",
                "field": "evt_xdate_fin",
                "operator": "lessthan",
                "type": "date",
                "value": f"{dateout_isoformat}"
            },
            {
                "label": "lgl_sfkligneparent",
                "field": "lgl_sfkligneparent",
                "operator": "isnotnull",
                "type": "integer",
                "value": "none"
            },
        ]
    },
}



à la place de ecu_bsysteme c'est

ecu_idsystem




