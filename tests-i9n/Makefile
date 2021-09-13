test: test-examples test-parse

export PYTHONPATH = $(shell pwd)/../src

test-examples:
	env | grep PY
	python3 examples_test.py

test-parse:
	python3 parse_test.py
