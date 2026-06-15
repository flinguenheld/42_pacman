NAME="pac-man.py"

install:
	uv sync

helix:
	uv run hx .

debug:
	uv run python ${NAME}

clean:
	uv cache clean
	rm -rf __pycache__ .mypy_cache .venv

lint:
	uv run flake8 . --extend-exclude '.venv/'
	uv run mypy . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \

.PHONY: install helix debug clean lint
