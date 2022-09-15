# from os import sync
#from curses.ascii import HT
import sqlite3
import uvicorn
from fastapi import Body, FastAPI
import pandas as pd
import requests
from my_module.task_assigner.sub_functions import *
from my_module.task_assigner.test import *
from my_module.task_assigner.data_mocker import *

import simplejson

api_url = 'https://development.api.wandeed.com/api/lst/search?offset=0&limit=500'
access_token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJydXRUeHJ5dlltOUVZcGhpRjRxak45ajFvTktLNnU4YUhuM1QySFFSUU5FIn0.eyJleHAiOjE2NjMyNTAyNjgsImlhdCI6MTY2MzI0ODc5NywiYXV0aF90aW1lIjoxNjYzMTYzODY4LCJqdGkiOiJjMjBkMTY1NS1hM2U4LTRjMTMtODc0MS00ODcyN2M2MGE3YzIiLCJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LmF1dGgud2FuZGVlZC5jb20vYXV0aC9yZWFsbXMvd2FuZGVlZC1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIzMWZmODY3NC1iOGZhLTQyMmYtYWM3NC02YzFjZGI2YTUwZGUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YW5kZWVkLWNsaWVudCIsIm5vbmNlIjoiZTBhMmNmYzgtMTExYi00YzA3LWI1YzctYWM0ZDU3ZDU3MWU1Iiwic2Vzc2lvbl9zdGF0ZSI6IjI1NmYzNWE5LWIzNzUtNDJiMi05NDczLTFhYmNmMjgzNDAxMyIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8qLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXBpLndhbmRlZWQuY29tLyoiLCIqIiwiaHR0cHM6Ly8qLmFkbWluLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXV0aC53YW5kZWVkLmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy13YW5kZWVkLXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiIyNTZmMzVhOS1iMzc1LTQyYjItOTQ3My0xYWJjZjI4MzQwMTMiLCJ1dGxfc3BrdXRpbGlzYXRldXIiOjEsInV0bF91dGlsaXNhdGV1cl9yb2xlcyI6IlsxXSIsInV0bF9jcHJlbm9tIjoiR2F5bG9yZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1dGxfc2FwcGFydGVuYW5jZSI6WzIsMzhdLCJ1dGxfY25vbSI6IlBldGl0IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwibG9jYWxlIjoiZnIiLCJnaXZlbl9uYW1lIjoiR2F5bG9yZCIsInV0bF9zZmtpbnN0YW5jZSI6MSwidXRsX3NhZG1pbmlzdHJlciI6W10sIm5hbWUiOiJHYXlsb3JkIFBldGl0IiwidXRsX3Nkcm9pdHNhY2NlcyI6WzYwLDMsNCw1LDE1LDI1LDI2LDMzLDM0LDM1LDM2LDM3LDQwLDQxLDQ0LDQ1LDQ2LDQ3XSwiZmFtaWx5X25hbWUiOiJQZXRpdCIsImVtYWlsIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwidXNlcl9ncm91cHMiOlsyLDM4LDYwLDMsNCw1LDE1LDI1LDI2LDMzLDM0LDM1LDM2LDM3LDQwLDQxLDQ0LDQ1LDQ2LDQ3XX0.Gu2VvwNwYjqAT03L5GGiM-etdziSko0b9Qx0K02W2mJTOinTJgrZ8KPaYSA-gCRoKdeE-78OvNTLiqEJrhpviRAS-KTA5Fx046XEoJoGsgDC5JTeJA3VV140vmhYa08uh1sKzvm_EjaSrq9gm1255j_YDkEBQFT4aihE9H9YCEMNYALnVodXOgnEDhwUX9v4HLaYPogb5F0SjV6YyTgi1tG39_WeS5-sxCXFyDc1vXH-hIr9AYM4vuMVfkL8P2RTsU7B73bOMj6skyX-yftzXPPAlPDyYNSaTx28z2ZblZL0jTy8Nf8qSDxuDfNFuqLBWTw6HNq9PfbSWTvhSMSP7Q'

headers={'Authorization': f'{access_token}',
             'Content-Type':'application/json'}

app = FastAPI()

# standard json encoder fails to encode np.NaN. This function replaces NaNs with "null", and returns a JSON formatted string.
def _return_json(OUT):
    return simplejson.dumps(OUT, ignore_nan=True)

@app.get("/task_assigner/")
def task_assigner(datein_isoformat : str, dateout_isoformat :str ,
    curseur:float = 0.0, contrainte_etre_sur_projet: str = 'de_preference', avantage_projet : float = 1.0):
    """
    récupère les données (taches, matrices_competence, dispo_utilisateurs, liste_des_participants par projet)
    dans le BACK-END Wandeed pour les dates indiquées et fournie une solution de répartition optimale des tâches entre les utilisateurs.

    :datein_isoformat:  date de début au format ISO du sprint pour la sélection des tâches auprès du BACK
    
    :dateout_isoformat: date de fin au format ISO du sprint pour la sélection des tâches auprès du BACK
    
    :curseur: float compris entre 0 et 1 (valeur par défaut 0). Pour une valeur de 0, l'algorithme tente de maximiser le niveau de compétence auquel est réalisé une heure de travail; à 1 il cherche à affecter la tâche à une personne "qui ne sait faire que cette tâche".
    
    :contrainte_etre_sur_projet: str = "de_preference". Valeurs possibles {"oui","de_preference","non"} Si "oui", les tâches peuvent être affectées uniquement à des utilisateurs participants au projet auquel se réfère la tâche.
    Si "de_preference", l'agorithme préférera assigner la tache à quelqu'un qui est sur le projet par rapport à quelqu'un qui ne l'est pas, tout en ne l'interdisant pas.
    Sachant que l'utilité maximale d'assignation d'une tache à quelqu'un de parfaitement compétent est de 3 points, le paramètre "avantage_projet" fixé à 1 mais réglable permet d'influencer la solution.
    Si "non", une personne n'étant par sur un projet ne peut se voir attribuer des tâches de ce même projet.

    :avantage_projet : float = 1.0: voir explication pour le paramètre contrainte_etre_sur_projet.

    """
    HTTPException_check_parameters(datein_isoformat, dateout_isoformat, curseur, contrainte_etre_sur_projet, avantage_projet)

    data = get_data_task_assigner(datein_isoformat, dateout_isoformat)
    df_prj, df_cmp, df_tsk, df_dsp = split_data(data)
    ## verification cohérence/qualité données ??
    solution = solve(df_prj, df_cmp, df_tsk, df_dsp,
                    curseur, contrainte_etre_sur_projet, avantage_projet)
    out = {
        "validite_solution" : test_solution(solution),
        'solution':solution
    }
    
    return _return_json(out)


@app.get("/test_task_assigner_with_random_data/")
def test_task_assigner_with_random_data(curseur:float = 0.0, contrainte_etre_sur_projet: str = 'de_preference', avantage_projet : float = 1.0):
    """
    teste la fonction task_assigner(...) avec des données générées aléatoirement et de manière cohérente (propose un grand panel de possibilitées pour la situation des entreprises: surchargées, sous-effectif, sous-chargées, correctes, peu de projets, bcp de projets ...).
    """
    df_prj, df_cmp, df_tsk, df_dsp = mock_coherent_data()
    ## verification cohérence/qualité données ??
    solution = solve(df_prj, df_cmp, df_tsk, df_dsp,
                    curseur, contrainte_etre_sur_projet, avantage_projet)
    out = {
        "validite_solution" : test_solution(solution),
        'solution':solution 
    }
    return _return_json(out)


#@app.get('/get_data_task_assigner/')
def get_data_task_assigner(datein_isoformat:str , dateout_isoformat:str):
    data = {}
    sql_querys_dict = {
        "matrice_projet": {"select": ["utl_spkutilisateur","int_sfkprojet"],"from": "lst_vprojet_utilisateur_py"},
        "dispos_utilisateurs": {'select':['utl_spkutilisateur','utl_sdispo'],'from': 'lst_vdispo_py'},
        'matrice_competence':{'select':['emc_sfkutilisateur','emc_sfkarticle','emc_sniveau'], 'from': 'lst_vcompetence_py'},
        "taches":{
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
                        "value": datein_isoformat
                    },
                    {
                        "label": "evt_xdate_fin",
                        "field": "evt_xdate_fin",
                        "operator": "lessthan",
                        "type": "date",
                        "value": dateout_isoformat
                    },
                    {
                        "label": "lgl_sfkligneparent",
                        "field": "lgl_sfkligneparent",
                        "operator": "isnotnull",
                        "type": "integer",
                        "value": "none"
                        
                    }
                ]
            },
        }
    }
    
    for key, sql_query  in sql_querys_dict.items(): 
        request = requests.post(api_url, headers=headers, json = sql_query)    
        if request.status_code != 200 :
            raise HTTPException(
                status_code=424,
                detail=f"Erreur lors de la récupération des données auprès du BACK: {key}.",
                headers= {"status_code_BACK":str(request.status_code),
                    "sql_query_to_BACK":_return_json(sql_query)},
            )
        else: 
            data[key] = request.json()['result']
    return data