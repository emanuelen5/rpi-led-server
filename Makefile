all: liboled test

liboled:
	python setup.py build_ext --build-lib .

test:
	python -m pytest tests/
