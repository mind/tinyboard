.PHONY: protoc
protoc:
	@protoc -I=tinyboard/proto --python_out=tinyboard/proto tinyboard/proto/*.proto

.PHONY: lint
lint:
	@flake8 tinyboard

.PHONY: clean
clean:
	@find . -type f -name '*.pyc' -delete

.PHONY: bootstrap
bootstrap:
	@pip install -r requirements.txt
	@python setup.py develop

.PHONY: test
test: lint
	py.test --cov-report term-missing --cov=tinyboard tests/
