#!/usr/bin/make

.PHONY: docs
default: build

build:
	python setup.py sdist

lint:
	flake8 ./setup.py ./rafter ./tests ./examples

test: lint
	python setup.py test

docs:
	pip install -q -r docs/requirements/docs.txt
	make -C docs html

upload: clean test build
	twine upload dist/*

clean:
	rm -rf .eggs
	rm -rf dist
	rm -rf rafter.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	make -C docs clean
	find ./ -type f -name '*.pyc' -delete
	find ./ -type d -name __pycache__ -delete
