#!/usr/bin/make

.PHONY: docs
default: build

build:
	pandoc --from=markdown --to=rst --output=README.rst README.md
	python setup.py sdist
	python setup.py bdist_wheel

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
	rm -rf build
	rm -rf dist
	rm -rf rafter.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -f README.rst
	make -C docs clean
	find ./ -type f -name '*.pyc' -delete
	find ./ -type d -name __pycache__ -delete
