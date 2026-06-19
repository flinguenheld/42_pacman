NAME=pac-man.py

install:
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv sync

helix:
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv run hx .

debug:
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv run python ${NAME} test_config.json

clean:
	rm -rf __pycache__ .mypy_cache .venv

lint:
	uv run flake8 . --extend-exclude '.venv/'
	uv run mypy . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \

.PHONY: install helix debug clean lint
