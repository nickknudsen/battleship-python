clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

lint:
	pre-commit run -av

pip-install:
	pip install -r requirements-dev.txt

pip-dev:
	pip install -r requirements-dev.txt

trans:
	@xgettext -d battleship -o locale/pt_BR/LC_MESSAGES/battleship.pot -j battleship/main.py
	@cd locale/pt_BR/LC_MESSAGES/; msginit --no-translator --input=battleship.pot --locale=pt_BR.UTF-8 --output-file battleship.po
	@cd locale/pt_BR/LC_MESSAGES/; msgfmt -o battleship.mo battleship.pot

build:
	python setup.py sdist
	python setup.py bdist_wheel

release: clean build
	git tag `python setup.py -q version`
	git push origin `python setup.py -q version`
	twine upload dist/*
