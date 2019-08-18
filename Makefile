default:
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make wheel      build wheel'
	@echo '    make clean      cleanup all temporary files'
	@echo

wheel:
	python setup.py bdist_wheel

clean:
	@rm -Rf *.egg .cache .coverage .tox build dist docs/build htmlcov *.egg-info
	@find -depth -type d -name __pycache__ -exec rm -Rf {} \;
	@find -type f -name '*.pyc' -delete

.PHONY: default wheel clean
