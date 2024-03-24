# TEST technique : commandes pour lancer le test

## Docker

Lancez le docker:

```bash
docker-compose up -d --build
```

On peut maintenant envoyer des données avec par exemple la requête:

```bash
curl -X POST http://localhost:8000/event -H "Content-Type: application/json" -d '{
  "resourceType": "pneu",
  "resourceId": 1,
  "eventType": "resourceHasBeenCreated",
  "triggeredAt": "2024-03-23T10:30:00Z",
  "triggeredBy": "server-1"
}'
```

Pour lancer les tests

```bash
python -m unittest tests.py #utiliser 'python3' si 'python' n'existe pas
```

On peut maintenant verifier dans la DB ou le fichier de log pour voir que les données ont bien été traitrés.
On peut aussi regarder les dockers dans dockerdesktop pour voir les erreurs specifiques et status de retours.

J'ai choisis de faire la vérification d'erreur du coté db_server car on pourrait supposer qu'avoir les logs des données envoyées mais mal formattées puisse etre interressant.
