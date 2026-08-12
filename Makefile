NAME=pac-man.py
UV=UV_SKIP_WHEEL_FILENAME_CHECK=1 uv


install:
	${UV} sync

helix:
	${UV} run hx .

run:
	${UV} run python ${NAME} test_config.json

build:
	sh build_standalone_exe.sh

build-run: build
	./dist/Pac-Man

clean:
	rm -rf	.mypy_cache .venv \ __pycache__ \
			src/__pycache__ \
			src/config/__pycache__ \
			src/data/__pycache__ \
			src/entities/__pycache__ \
			src/gui/__pycache__ \
			src/gui/titles/__pycache__ \
			src/high_scores/__pycache__ \
			src/maze/__pycache__ \
			src/pathfinding/__pycache__ \
			src/sprites/__pycache__ \
			src/utils/__pycache__ \
			src/views/__pycache__ \
			build dist

lint:
	${UV} run flake8 . --extend-exclude '.venv/'
	${UV} run mypy . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \

.PHONY: install helix run build build-run clean lint
