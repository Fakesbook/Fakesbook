run:
	python3 fakesbook.py
test:
	python3 fakesbook.py debug
clean:
	python3 reset_db.py app.db
