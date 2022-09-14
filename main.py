# from os import sync
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
access_token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJydXRUeHJ5dlltOUVZcGhpRjRxak45ajFvTktLNnU4YUhuM1QySFFSUU5FIn0.eyJleHAiOjE2NjMyMDI3MTMsImlhdCI6MTY2MzE4NDcxMywiYXV0aF90aW1lIjoxNjYzMTYzODY4LCJqdGkiOiIxZDk3YTA2OS00MDVmLTQ0ZWQtOTcyOS05ZDQ2NzJmMDAxMjkiLCJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LmF1dGgud2FuZGVlZC5jb20vYXV0aC9yZWFsbXMvd2FuZGVlZC1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIzMWZmODY3NC1iOGZhLTQyMmYtYWM3NC02YzFjZGI2YTUwZGUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YW5kZWVkLWNsaWVudCIsIm5vbmNlIjoiMjE1OTU5Y2MtMTQxNC00YTIxLTljN2YtZjUyYzFjMjEzZmEzIiwic2Vzc2lvbl9zdGF0ZSI6IjI1NmYzNWE5LWIzNzUtNDJiMi05NDczLTFhYmNmMjgzNDAxMyIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8qLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXBpLndhbmRlZWQuY29tLyoiLCIqIiwiaHR0cHM6Ly8qLmFkbWluLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXV0aC53YW5kZWVkLmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy13YW5kZWVkLXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiIyNTZmMzVhOS1iMzc1LTQyYjItOTQ3My0xYWJjZjI4MzQwMTMiLCJ1dGxfc3BrdXRpbGlzYXRldXIiOjEsInV0bF91dGlsaXNhdGV1cl9yb2xlcyI6IlsxXSIsInV0bF9jcHJlbm9tIjoiR2F5bG9yZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1dGxfc2FwcGFydGVuYW5jZSI6WzIsMzhdLCJ1dGxfY25vbSI6IlBldGl0IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwibG9jYWxlIjoiZnIiLCJnaXZlbl9uYW1lIjoiR2F5bG9yZCIsInV0bF9zZmtpbnN0YW5jZSI6MSwidXRsX3NhZG1pbmlzdHJlciI6W10sIm5hbWUiOiJHYXlsb3JkIFBldGl0IiwidXRsX3Nkcm9pdHNhY2NlcyI6WzYwLDMsNCw1LDE1LDI1LDI2LDMzLDM0LDM1LDM2LDM3LDQwLDQxLDQ0LDQ1LDQ2LDQ3XSwiZmFtaWx5X25hbWUiOiJQZXRpdCIsImVtYWlsIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwidXNlcl9ncm91cHMiOlsyLDM4LDYwLDMsNCw1LDE1LDI1LDI2LDMzLDM0LDM1LDM2LDM3LDQwLDQxLDQ0LDQ1LDQ2LDQ3XX0.pkg95AD1BYDvI5bfWug-91LKDqg_z-vTQGvyfpSnEfGQ_Yi9Ld0OK6OVp4KBAD5MEx_296H1SQdrfDjpqQkKEx9pOXdSAYOSATltdVeJ5ISe53M97wx8NSULHbqK-M99B8h2zXDXHhv9q2T1u1vJ-5Q7b6rPEBj7f9X2gUQZ2gUNl-1XlgB8NuwwVAdlG-A7viRHe9jC0vxFrkV6SK5jMxjQ6ZtA1O2fiIJ_6rNt-Lfz-t4_YtTMVU39oywFsrowQlKFn6bSPjHqp7rzTOrtOVRlmG2az8UN2t0UzPKZYpJQqAVsOMIemZxo_yqP26t2Jz3d-a_1FslLi3ZZeNXRxA'

headers={'Authorization': f'{access_token}',
             'Content-Type':'application/json'}

app = FastAPI()

# standard json encoder fails to encode np.NaN. This function replaces NaNs with "null", and returns a JSON formatted string.
def _return_json(OUT):
    return simplejson.dumps(OUT, ignore_nan=True)

@app.get("/")
async def home():
    return {'response':'welcome'}


@app.get("/solve/")
def main():
    OUT = {key:ans for key,ans in zip(['SUCCES_RECUPERATION_DONNEES','SUCCES_SOLVEUR','VALIDITE_SOLUTION','SUCCES_GLOBAL'],[np.nan]*3+[False])}
    
    dic = get_data_task_assigner()
    OUT["SUCCES_RECUPERATION_DONNEES"] = dic['SUCCES_RECUPERATION_DONNEES']
    if not OUT["SUCCES_RECUPERATION_DONNEES"]: 
        return _return_json(OUT)
    df_prj, df_cmp, df_tsk, df_dsp = split_data_from_dic(dic)
    
    solution = solve(df_prj, df_cmp, df_tsk, df_dsp)
    OUT['SUCCES_SOLVEUR'] = solution['SUCCES_SOLVEUR']
    
    if not solution['SUCCES_SOLVEUR']: return _return_json(OUT)
    OUT["VALIDITE_SOLUTION"] = test_solution(solution)
    OUT["SUCCES_GLOBAL"] = OUT["VALIDITE_SOLUTION"]
    OUT['solution'] = solution
    return _return_json(OUT)


@app.get("/test_with_random_data/")
def test_with_random_data():
    OUT = {key:ans for key,ans in zip(['SUCCES_SOLVEUR','VALIDITE_SOLUTION','SUCCES_GLOBAL'],[np.nan]*2+[False])}
    OUT["SUCCES_RECUPERATION_DONNEES"] = "Les données sont générées de manière aléatoire et cohérente."
    df_prj, df_cmp, df_tsk, df_dsp = mock_coherent_data()

    solution = solve(df_prj, df_cmp, df_tsk, df_dsp)
    OUT['SUCCES_SOLVEUR'] = solution['SUCCES_SOLVEUR']
    
    if not solution['SUCCES_SOLVEUR']: return _return_json(OUT)
    OUT["VALIDITE_SOLUTION"] = test_solution(solution)
    OUT["SUCCES_GLOBAL"] = OUT["VALIDITE_SOLUTION"]
    OUT['solution'] = solution
    return _return_json(OUT)

    




@app.get('/get_data_task_assigner/')
def get_data_task_assigner():
    out = {}
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
                        "value": "2022-09-06T00:00:00.000Z"
                    },
                    {
                        "label": "evt_xdate_fin",
                        "field": "evt_xdate_fin",
                        "operator": "lessthan",
                        "type": "date",
                        "value": "2022-10-06T00:00:00.000Z"
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
    
    compteur_succes = 0
    for key, sql_query  in sql_querys_dict.items(): 
        request = requests.post(api_url, headers=headers, json = sql_query)    
        if request.status_code != 200 :
            out[key] = {'data':None,
                        'status_code':request.status_code,
                        'commentaire':'erreur récupération données sur le serveur.'}
        else: 
            compteur_succes+=1
            out[key] = {'data':request.json(),
                            'status_code':request.status_code,
                            'commentaire':'données récupérées sur le serveur avec succès.'}
    out['SUCCES_RECUPERATION_DONNEES'] =  compteur_succes == 4

    return out