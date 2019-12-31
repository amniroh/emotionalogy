virtualenv:
	( \
		virtualenv env --python=/usr/bin/python3; \
		. env/bin/activate; \
		pip install -U pip; \
		pip install -U setuptools; \
		pip install -r requirements.txt; \
	)
clean:
	rm -rf env
