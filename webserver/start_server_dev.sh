FLASK_APP=../main_flask.py FLASK_ENV=development \
	flask run --host 0.0.0.0 --port 5000 --extra-files "*.py:src/*:../main_flask.py"
