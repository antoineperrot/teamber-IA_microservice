# from os import sync
import sqlite3
import uvicorn
from fastapi import Body, FastAPI

import pandas as pd
from modules.task_assigner import solve_problem

import requests
api_url = 'https://development.api.wandeed.com/api/lst/search?offset=0&limit=500'
access_token='eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJydXRUeHJ5dlltOUVZcGhpRjRxak45ajFvTktLNnU4YUhuM1QySFFSUU5FIn0.eyJleHAiOjE2NjIxMjMyODQsImlhdCI6MTY2MjEwNTI4NCwiYXV0aF90aW1lIjoxNjYyMTA1MjgzLCJqdGkiOiJiZTg5N2YzZC1iZDJhLTQ3MDQtOTcyMy01NTgwZmFhOGRkNjIiLCJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LmF1dGgud2FuZGVlZC5jb20vYXV0aC9yZWFsbXMvd2FuZGVlZC1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIzMWZmODY3NC1iOGZhLTQyMmYtYWM3NC02YzFjZGI2YTUwZGUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YW5kZWVkLWNsaWVudCIsIm5vbmNlIjoiY2RmMzc2OTctMjY5Ny00MTE1LWFmNDUtZmQyYzE4MDRlNmI1Iiwic2Vzc2lvbl9zdGF0ZSI6Ijc3NTVjNzZkLWExMDYtNGE4ZS1hNTE5LWM0ZDAwNGExMWJhOCIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8qLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXBpLndhbmRlZWQuY29tLyoiLCIqIiwiaHR0cHM6Ly8qLmFkbWluLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXV0aC53YW5kZWVkLmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy13YW5kZWVkLXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiI3NzU1Yzc2ZC1hMTA2LTRhOGUtYTUxOS1jNGQwMDRhMTFiYTgiLCJ1dGxfc3BrdXRpbGlzYXRldXIiOjEsInV0bF91dGlsaXNhdGV1cl9yb2xlcyI6IlsxXSIsInV0bF9jcHJlbm9tIjoiR2F5bG9yZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1dGxfc2FwcGFydGVuYW5jZSI6WzIsMzhdLCJ1dGxfY25vbSI6IlBldGl0IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwibG9jYWxlIjoiZnIiLCJnaXZlbl9uYW1lIjoiR2F5bG9yZCIsInV0bF9zZmtpbnN0YW5jZSI6MSwidXRsX3NhZG1pbmlzdHJlciI6W10sIm5hbWUiOiJHYXlsb3JkIFBldGl0IiwidXRsX3Nkcm9pdHNhY2NlcyI6WzYwLDMsNCw1LDE1LDI1LDI2LDMzLDM0LDM1LDM2LDM3LDQwLDQxLDQ0LDQ1LDQ2LDQ3XSwiZmFtaWx5X25hbWUiOiJQZXRpdCIsImVtYWlsIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwidXNlcl9ncm91cHMiOlsyLDM4LDYwLDMsNCw1LDE1LDI1LDI2LDMzLDM0LDM1LDM2LDM3LDQwLDQxLDQ0LDQ1LDQ2LDQ3XX0.RxaYUfGqoQU4F2lucmyC2yR2mk4AWniPi8lCpxf70GJv3k8xGbEv0FExXuEv-Kpht9gGC9LKGpEOZ_RMbXQkLOpf0uwE6iQSx5DZL9nA_AP7Vyvvt8-0h5xHsadOtPWgLPzaSi6L3fCpmUVFvnmes_gJcRxHqm2VTM3FqmpXa9PJrPdtiHT95XAKnqbPaayNrSjGQ8xn_HfpYZxRUn9GzckNTBIr4Fo78MbMaLMMQfZsAONiBUUk_4eywwzsOiKtEwPyE_g-44MwzkRqWMLfAakD5nQIjTJbBl-ZGVND81KuTUKun91CSTb8o-nQYxIPDD3fS_9v8s9r6DP0-TAnKA'

headers={'Authorization': f'Bearer {access_token}',
             'Content-Type':'application/json'}

app = FastAPI()

@app.get("/")
async def home():
    return {'response':'welcome'}

@app.get('/get_data_task_assigner/')
def get_data_task_assigner():
    out = {}
    
    sql_querys_dict = {
        "matrice_projet": {"select": ["utl_spkutilisateur","int_sfkprojet"],"from": "lst_vprojet_utilisateur_py"},
        "dispos_utilisateurs": {'select':['utl_spkutilisateur','utl_sdispo'],'from': 'lst_vdispo_py'},
        'matrice_competence':{'select':['emc_sfkutilisateur','emc_sfkarticle','emc_sniveau'],'from': 'lst_vcompetence_PY'},
        "taches":{'select':['evt_spkevenement','evt_sfkprojet','evt_dduree'], 'from': 'lst_vevenement_py'}
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
    out['STATUT_RECUPERATION_DONNEES'] = 'SUCCES' if compteur_succes == 4 else "ECHEC"

    return out

@app.get("/solve/")
def main():
    collect_data = get_data_task_assigner()

    # tasks = pd.read_json(tasks)
    # capacite_utilisateur = pd.read_json(capacite_utilisateur)
    # matrice_competence = pd.read_json(matrice_competence)
    # matrice_projet = pd.read_json(matrice_projet)

    # output = solve_problem(tasks,
    # capacite_utilisateur, 
    # matrice_competence,
    # matrice_projet,
    # curseur_politique)

    return collect_data

