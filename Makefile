# Makefile

.PHONY: clean

default: dev-server

dev-server: venv/bin/activate
	. venv/bin/activate && ./runserver.py

server: venv/bin/activate
	. venv/bin/activate && nohup ./runserver.py script args >stdout.log 2>stderr.log&

venv venv/bin/activate: requirements.txt clean
	test -d venv || virtualenv venv --no-site-packages
	. venv/bin/activate && pip install -r requirements.txt

clean:
	find . -type f -name "*.pyc" -delete

