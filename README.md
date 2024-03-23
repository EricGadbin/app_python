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
  "triggeredAt": "2024-03-21T10:00:00Z",
  "triggeredBy": "server-42"
}'
```

on peut maintenant verifier dans la DB ou le fichier de log pour voir que les données ont bien été traitrés
