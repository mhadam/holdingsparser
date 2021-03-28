install:
	poetry build && ls -t dist/*.whl | head -n1 | xargs pip install --upgrade --force-reinstall