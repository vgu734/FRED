# FRED

### For local deploy:
Bring up app
```
docker compose up --build
```

Exec into db
```
docker exec -it fred-postgres psql -U postgres -d fred
```

Hitting endpoint
```
curl -X POST http://127.0.0.1:8000/jobs/run-fred -H "Content-Type: application/json"
```