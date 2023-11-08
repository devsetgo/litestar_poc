# Makefile

# Variables
DEV_SERVER = uvicorn src.main:app
PROD_SERVER = uvicorn src.main:app
PORT = 5000
WORKERS = 2
REQUIREMENTS = requirements.txt
TESTS = tests

.PHONY: dev prod install test

dev:
	${DEV_SERVER} --port ${PORT} --reload

prd:
	${PROD_SERVER} --port ${PORT} --workers ${WORKERS}

install:
	pip install -r ${REQUIREMENTS}

test:
	pytest ${TESTS}
