# Développement d'un microservice IA pour la société TEAMBER

## Installer l'environnement de dev:

Lancer le ```setup_venv.bat```

## Faire tourner l'app en local :


Lancer le ```run_app.bat```


## Tests

### Unit tests
Testes les fonctionnalités de l'application

Lancer le ```run_unittest.bat```

## Test d'intégration
Test les interfaces avec le back

1. Ouvrir une invite de commande
2. Se rendre dans le répertoire du projet
3. Obtenir la clé API du back de [Dev Wandeed](https://development.wandeed.com)
4. Lancer les commmandes :
   1. Mettre en place l'environnement virtuel
   ```
   setup_venv.bat
   ```
   
   2. L'activer
   ```
   venv\Scripts\activate
   ```
   
   3. Run les test d'inté de Planning optimizer __Bien mettre les guillemets__

   ``` 
   python api\services\planning_optimizer\tests\integration\test_integration_recuperation_data.py "<api_key>" 
   ```
   4. Run les tests d'inté de Task Assigner __Bien mettre les guillemets__
   ``` 
   python api\services\task_assigner\tests\integration\test_integration_recuperation_data.py "<api_key>" 
   ```





