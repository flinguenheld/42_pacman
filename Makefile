NAME=pac-man.py
UV=UV_SKIP_WHEEL_FILENAME_CHECK=1 uv


install:
	${UV} sync

helix:
	${UV} run hx .

debug:
	${UV} run python ${NAME} test_config.json

clean:
	rm -rf __pycache__ .mypy_cache .venv

lint:
	${UV} run flake8 . --extend-exclude '.venv/'
	${UV} run mypy . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \

.PHONY: install helix debug clean lint
