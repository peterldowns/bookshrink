# Makefile

.PHONY: clean

default: server

server: venv/bin/activate
	. venv/bin/activate && nohup ./runserver.py script args >stdout.log 2>stderr.log&

venv venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv --no-site-packages
	. venv/bin/activate && pip install -r requirements.txt

clean:
	find . -type f -name "*.pyc" -delete

