prep:
	brew install python3
	pyvenv venv
	source venv/bin/activate && pip install --upgrade pip 
	source venv/bin/activate && pip install -r etc/requirements.txt
	mkdir var

run:
	source venv/bin/activate && python app/shue.py

build:
	brew install gnu-tar || true
	rm -f shue.tgz
	gtar --create --numeric-owner --owner=0 --group=0 --gzip --file shue.tgz app etc *.sh
