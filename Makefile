PYTHON ?= python

export PYTHONPATH = $(shell echo "$$PYTHONPATH"):./cups_fab

.PHONY: all check clean clean-pyc clean-patchfiles pylint reindent test

all: clean-pyc check test

check:
	@$(PYTHON) utils/check_sources.py -i tests/path.py -i tests/coverage.py .

clean: clean-pyc clean-patchfiles

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-patchfiles:
	find . -name '*.orig' -exec rm -f {} +
	find . -name '*.rej' -exec rm -f {} +

pylint:
	@pylint --rcfile utils/pylintrc cups_fab

reindent:
	@$(PYTHON) utils/reindent.py -r -B .

test:
	@cd tests; $(PYTHON) run.py -d -m '^[tT]est' $(TEST)

covertest:
	@cd tests; $(PYTHON) run.py -d -m '^[tT]est' --with-coverage --cover-package=cups_fab $(TEST)
