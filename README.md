# My pet-project to learn FastAPI

## Install

1. clone rep:
```
git clone https://github.com/Muskelo/ToDoAPI.git .
```

2. set config in .env like this (i'm hide .env by git-crypt):
```
#POSTGRES
POSTGRES_PASSWORD=password
PGDATA=/data/postgres

#API
SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://postgres:password@db/postgres"
SECRET_KEY="SECRET_KEY"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINS=30
REFRESH_TOKEN_EXPIRE_DAYS=30
```

3. up
```
docker-compose up -d --build
```

4. migrate in db (in project used alembic)
```
docker-compose exec -it api bash
alembic revision --autogenerate
alembic migrate head
```
