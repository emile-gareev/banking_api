# Requirements
requirements:
	python -m pip install --upgrade pip setuptools wheel && python -m pip install -r requirements.txt


# Run in Docker
start:
	docker-compose up --build -d

stop:
	docker-compose down

start-app:
	docker-compose up --build -d app

stop-app:
	docker-compose stop app

start-db:
	docker-compose up db

stop-db:
	docker-compose stop db


# DB Migration in Docker
migration:
	docker-compose up -d app && docker-compose exec app alembic revision --autogenerate -m "$(name)"

upgrade:
	docker-compose up -d app && docker-compose exec app alembic upgrade head

downgrade:
	docker-compose up -d app && docker-compose exec app alembic downgrade -1


# Run in local OS
start-local:
	cd src && export PYTHONPATH=. && python manage.py runserver


# Testing
test:
	cd src && \
	export PYTHONPATH=. && \
	pytest -sv --cov=app --cov-report term-missing --cov-report xml:../coverage.xml . -W ignore::DeprecationWarning --junitxml=../report.xml


# DB Migration in local
migration-local:
	cd src && alembic revision --autogenerate -m "$(name)"

upgrade-local:
	cd src && alembic upgrade head

downgrade-local:
	cd src && alembic upgrade downgrade -1


# Formatting
isort:
	cd src && isort $(arg1) .

black:
	cd src && black $(arg1) .

format: isort black

# Linting
flake8:
	cd src && flake8 .

mypy:
	cd src && mypy --namespace-packages --explicit-package-bases --exclude 'alembic' .

bandit:
	cd src && bandit -q -r -x /venv,/tests .

lint: flake8 mypy bandit


check: format lint test
