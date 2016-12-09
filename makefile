run:
	env SECRET_KEY=`python -c 'from os import urandom; from base64 import b64encode as be; print(be(urandom(32)))'` python privacy_app.py
setup:
	pip install -r requirements.txt
