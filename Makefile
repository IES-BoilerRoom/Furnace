.PHONY: check ci
check:
	python3 ci_suite/run_furnace_gate.py

ci:
	python3 ci_suite/run_furnace_gate.py --strict-ci
