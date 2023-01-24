# Développement d'un microservice IA pour la société TEAMBER

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




