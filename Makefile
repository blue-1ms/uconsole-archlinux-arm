PYTHON ?= python3

.PHONY: help docs-check validate

help:
	@printf '%s\n' \
	  'uConsole Arch Linux ARM control plane' \
	  '' \
	  '  make docs-check  validate local Markdown links' \
	  '  make validate    validate repository structure, policy and docs'

docs-check:
	@$(PYTHON) scripts/validate-repository.py --docs-only

validate:
	@$(PYTHON) scripts/validate-repository.py
