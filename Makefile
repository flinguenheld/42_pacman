NAME=pac-man.py
UV=UV_SKIP_WHEEL_FILENAME_CHECK=1 uv


install:
	${UV} sync

helix:
	${UV} run hx .

run:
	${UV} run python ${NAME} test_config.json

clean:
	rm -rf	.mypy_cache .venv \
			__pycache__ src/__pycache__ \
			src/config/__pycache__ src/maze/__pycache__ \
			src/utils/__pycache__ src/visual/__pycache__ \
			src/visual/entities/__pycache__ \
			src/visual/sprites/__pycache__ \

lint:
	${UV} run flake8 . --extend-exclude '.venv/'
	${UV} run mypy . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \

.PHONY: install helix run clean lint
