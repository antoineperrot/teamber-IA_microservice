import uvicorn
from fastapi import Body, FastAPI

import pandas as pd
from module import solve_problem

app = FastAPI()

@app.get("/")
async def home():
    return {'response':'welcome'}

@app.post("/solve/")
async def main(tasks: str = Body(..., embed=True),
                capacite_utilisateur : str = Body(..., embed=True),
                matrice_competence: str = Body(..., embed=True),
                matrice_projet: str = Body(..., embed=True),
                curseur_politique: float = 1.0):
    tasks = pd.read_json(tasks)
    capacite_utilisateur = pd.read_json(capacite_utilisateur)
    matrice_competence = pd.read_json(matrice_competence)
    matrice_projet = pd.read_json(matrice_projet)

    output = solve_problem(tasks,
    capacite_utilisateur, 
    matrice_competence,
    matrice_projet,
    curseur_politique)

    return output