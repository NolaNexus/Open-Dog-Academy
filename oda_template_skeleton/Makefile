gen:
	python scripts/generate_cards.py

check:
	python scripts/run_checks.py

serve: gen
	mkdocs serve

build: gen
	mkdocs build --strict
