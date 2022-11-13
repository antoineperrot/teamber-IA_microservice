from fastapi import HTTPException


def controller_parameters(
    datein_isoformat,
    dateout_isoformat,
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

    if not isinstance(datein_isoformat, str):
        raise HTTPException(
            status_code=422, detail="'datein_isoformat' doit être de  string."
        )

    if not isinstance(dateout_isoformat, str):
        raise HTTPException(
            status_code=422, detail="'dateout_isoformat' doit être de  string."
        )

    # try :
    #     datetime.datetime.fromisoformat(datein_isoformat)
    # except:
    #     raise HTTPException(status_code=422,
    #                             detail=f"Invalid isoformat string for 'datein_isoformat': {datein_isoformat}")

    # try :
    #     datetime.datetime.fromisoformat(dateout_isoformat)
    # except:
    #     raise HTTPException(status_code=422,
    #                             detail=f"Invalid isoformat string for 'dateout_isoformat': {dateout_isoformat}")

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
