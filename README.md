### Description

The service for basic banking operations for internal bank employees:
- **Customers**
  - create
  - get
  - get all bank accounts
- **Bank accounts**
  - create
  - get
  - get balance
  - get all transactions
- **Transactions**
  - create (deposit, withdrawal, transfer)
  - get
  - get all current transaction types (deposit, withdrawal, transfer)

### Local running

- Copy env file into home directory `cp .env-defaults .env`
- Create venv with requirements (preferable python v 3.9) 
`python -m venv venv` + `source venv/bin/activate` + `pip install -r requirements.txt`
- Setup Postgres DB (preferable v 13.0) 
`docker run --name pg-13 -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=database -d postgres:13`
- Run alembic migrations from **src** directory `cd src/` + `alembic upgrade head`
- Create internal user for API `python manage.py create-user username password`
- Run server `python manage.py runserver` at http://127.0.0.1:8000

### Production running

- Use docker-compose file

### Local tests running

- Setup separate Postgres DB (preferable v 13.0) with **test** postfix
`docker run --name pg-13 -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=database_test -d postgres:13`
- Run pytest from **src** directory `cd src/` + `pytest -v` 
  - if you meet ModuleNotFoundError make `export PYTHONPATH=$(pwd)` from **src** directory

### Swagger and OpenAPI schemas

- After running server you can use:
  - http://127.0.0.1:8000/api/docs
  - http://127.0.0.1:8000/api/docs/openapi.json
  - http://127.0.0.1:8000/api/redocs