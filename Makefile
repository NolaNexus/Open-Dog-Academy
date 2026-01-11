.PHONY: help check fast index path report-core10 perms-check perms-fix status-normalize size prune catalog verify-catalog catalog-rebuild

help:
	@echo "ODA helpers"
	@echo "  make fast             # run quick checks (no mkdocs build)"
	@echo "  make check            # run full checks (incl mkdocs build)"
	@echo "  make index            # regenerate indexes"
	@echo "  make path             # regenerate learning paths"
	@echo "  make report-core10     # write core10 report"
	@echo "  make perms-check       # check permissions policy (exec bits)"
	@echo "  make perms-fix         # fix permissions policy (exec bits)"
	@echo "  make status-normalize  # normalize legacy status strings"
	@echo "  make size             # show a size audit (top files + by-ext)"
	@echo "  make prune            # delete Python cache artifacts (__pycache__, *.pyc)"
	@echo "  make catalog          # generate docs/reference/catalog.md from SQLite"
	@echo "  make verify-catalog   # verify docs/ against artifacts/oda_catalog.sqlite"
	@echo "  make catalog-rebuild  # rebuild artifacts/oda_catalog.sqlite from docs/"
	@echo "  make catalog-rebuild  # rebuild artifacts/oda_catalog.sqlite from docs/ (authoritative index)"

fast:
	python3 scripts/oda.py check --fast

check:
	python3 scripts/oda.py check

index:
	python3 scripts/oda.py index

path:
	python3 scripts/oda.py path

report-core10:
	python3 scripts/oda.py report core10 --write

perms-check:
	python3 scripts/oda.py perms check

perms-fix:
	python3 scripts/oda.py perms fix

status-normalize:
	python3 scripts/oda.py status normalize

size:
	python3 scripts/size_audit.py .

prune:
	bash scripts/prune_pycache.sh .

catalog:
	python3 scripts/sqlite_to_catalog_md.py

verify-catalog:
	python3 scripts/verify_catalog_sqlite.py

catalog-rebuild:
	python3 scripts/rebuild_catalog_sqlite.py
