all: liboled test flake8 flake8-complexity

liboled:
	python setup.py build_ext --build-lib .

test:
	python -m pytest tests/

flake8:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

flake8-complexity:
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

init:
	pip install -r requirements-dev.txt -r requirements.txt

clean:
	rm -fv liboled*.so
	rm -rf build
