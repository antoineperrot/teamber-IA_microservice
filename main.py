# from os import sync
import sqlite3
import uvicorn
from fastapi import Body, FastAPI
import pandas as pd
import requests
from my_module.task_assigner import *
api_url = 'https://development.api.wandeed.com/api/lst/search?offset=0&limit=500'
access_token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJydXRUeHJ5dlltOUVZcGhpRjRxak45ajFvTktLNnU4YUhuM1QySFFSUU5FIn0.eyJleHAiOjE2NjMxODI2MDgsImlhdCI6MTY2MzE2NDYwOCwiYXV0aF90aW1lIjoxNjYzMTYzODY4LCJqdGkiOiJhMzIwMTBmZC1mZDFjLTQ2OGQtYjNlYy00MDY3ODU2ZWE1ZjkiLCJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LmF1dGgud2FuZGVlZC5jb20vYXV0aC9yZWFsbXMvd2FuZGVlZC1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIzMWZmODY3NC1iOGZhLTQyMmYtYWM3NC02YzFjZGI2YTUwZGUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YW5kZWVkLWNsaWVudCIsIm5vbmNlIjoiMmYzNTI3YzMtZDFkMy00OTgxLTgwY2EtMjdmZjMwMGJlYTgwIiwic2Vzc2lvbl9zdGF0ZSI6IjI1NmYzNWE5LWIzNzUtNDJiMi05NDczLTFhYmNmMjgzNDAxMyIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8qLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXBpLndhbmRlZWQuY29tLyoiLCIqIiwiaHR0cHM6Ly8qLmFkbWluLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXV0aC53YW5kZWVkLmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy13YW5kZWVkLXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiIyNTZmMzVhOS1iMzc1LTQyYjItOTQ3My0xYWJjZjI4MzQwMTMiLCJ1dGxfc3BrdXRpbGlzYXRldXIiOjEsInV0bF91dGlsaXNhdGV1cl9yb2xlcyI6IlsxXSIsInV0bF9jcHJlbm9tIjoiR2F5bG9yZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1dGxfc2FwcGFydGVuYW5jZSI6WzIsMzhdLCJ1dGxfY25vbSI6IlBldGl0IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwibG9jYWxlIjoiZnIiLCJnaXZlbl9uYW1lIjoiR2F5bG9yZCIsInV0bF9zZmtpbnN0YW5jZSI6MSwidXRsX3NhZG1pbmlzdHJlciI6W10sIm5hbWUiOiJHYXlsb3JkIFBldGl0IiwidXRsX3Nkcm9pdHNhY2NlcyI6WzYwLDMsNCw1LDE1LDI1LDI2LDMzLDM0LDM1LDM2LDM3LDQwLDQxLDQ0LDQ1LDQ2LDQ3XSwiZmFtaWx5X25hbWUiOiJQZXRpdCIsImVtYWlsIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwidXNlcl9ncm91cHMiOlsyLDM4LDYwLDMsNCw1LDE1LDI1LDI2LDMzLDM0LDM1LDM2LDM3LDQwLDQxLDQ0LDQ1LDQ2LDQ3XX0.iWQo1pQ2gInMiwaCWUGe5NjM1xGd6se0PrF-SC0PW-DK8QA2T5eT1ZbPR5g8__kUcvlm3LHkpGfNKfz4ZQ51YmeSmZKdj-JGsanv4-LnW8BMenI0OLClg28W73xwu0JGBRHbXc8MvOu-E0uXFHsxovXylLNvyejTKnn1HL0JHpuNKiFAf2Ia_X5aXdnk91DFlq9fJXV2WhWINXslIv5SOEH0fNcL2oZeo62UckqFL0TDb4ci-k9c4vMB0fgMSxDVyYVHMeVicPwT77BkaWi-_5QgVwUOeAc1Cj15pLBVhQAd2i3RAXpCaSO2R-592fa-Ufl1p6YtE0-fqbXSBzC6ag'

headers={'Authorization': f'{access_token}',
             'Content-Type':'application/json'}

app = FastAPI()

@app.get("/")
async def home():
    return {'response':'welcome'}


@app.get("/solve/")
def main():
    dic = get_data_task_assigner()
    
    data = split_data_from_dic(dic)

    return data




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
    out['STATUT_RECUPERATION_DONNEES'] = 'SUCCES' if compteur_succes == 4 else "ECHEC"

    return out