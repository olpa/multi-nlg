all: lint test

lint:
	flake8

test_makefiles=$(shell find ./tests -name Makefile)

test:
	set -o errexit
	for mf in $(test_makefiles) ; do \
	  make -C $$(dirname $${mf}) || exit 1 ; \
	  done
