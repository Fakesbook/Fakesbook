run:
	env SECRET_KEY=`python -c 'from os import urandom; print(urandom(32))'` python privacy_app.py
setup:
	pip install -r requirements.txt
