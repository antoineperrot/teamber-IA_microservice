from fastapi import HTTPException


def controller_parameters(
    date_start,
    date_end,
    curseur,
    contrainte_etre_sur_projet,
    avantage_projet,
):
    """
    Vérifie que les valeurs des paramètres sont correctes.
    """
    if not isinstance(curseur, float):
        raise HTTPException(
            status_code=422,
            detail="'curseur' doit être un nombre flottant.",
        )

    if not (0.0 <= curseur and curseur <= 1.0):
        raise HTTPException(
            status_code=422,
            detail=f"Le paramètre 'curseur' est incorrect. Valeur spécifiée par l'utilisateur:  {curseur}.\n 'curseur' est un flottant compris entre 0 et 1.",
        )

    if not isinstance(date_start, str):
        raise HTTPException(
            status_code=422, detail="'date_start' doit être de  string."
        )

    if not isinstance(date_end, str):
        raise HTTPException(status_code=422, detail="'date_end' doit être de  string.")

    # try :
    #     datetime.datetime.fromisoformat(date_start)
    # except:
    #     raise HTTPException(status_code=422,
    #                             detail=f"Invalid isoformat string for 'date_start': {date_start}")

    # try :
    #     datetime.datetime.fromisoformat(date_end)
    # except:
    #     raise HTTPException(status_code=422,
    #                             detail=f"Invalid isoformat string for 'date_end': {date_end}")

    if not isinstance(contrainte_etre_sur_projet, str):
        raise HTTPException(
            status_code=422,
            detail=f"'contrainte_etre_sur_projet' doit être de type string. Valeur spécifiée par l'utilisateur: {contrainte_etre_sur_projet}.",
        )

    authorized_values = ["oui", "de_preference", "non"]
    if not contrainte_etre_sur_projet in authorized_values:
        raise HTTPException(
            status_code=422,
            detail=f"Valeur incorrecte fournie pour 'contrainte_etre_sur_projet': {contrainte_etre_sur_projet}. Valeurs possibles: {authorized_values}.",
        )

    if not isinstance(avantage_projet, float):
        raise HTTPException(
            status_code=422, detail="'avantage_projet' doit être de type float."
        )
