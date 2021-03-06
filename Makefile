all: liboled test

liboled:
	python setup.py build_ext --build-lib .

test:
	python -m pytest tests/

init:
	pip install -r requirements-dev.txt -r requirements.txt

clean:
	rm -fv liboled*.so
	rm -rf build
