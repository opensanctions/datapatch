
typecheck:
	mypy --strict datapatch

test:
	pytest --cov=datapatch tests/