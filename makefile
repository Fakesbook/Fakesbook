run:
	env SECRET_KEY=`python -c 'from os import urandom; from base64 import b64encode as be; print(be(urandom(32)))'` python privacy_app.py
clean:
	python3 reset_db.py app.db
