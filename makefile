format:
	black .
install:
	pip install -r requirements.txt
test:
	pytest ./src/test/
	

