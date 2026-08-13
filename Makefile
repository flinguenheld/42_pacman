NAME=pac-man.py
UV=UV_SKIP_WHEEL_FILENAME_CHECK=1 uv
PYINSTALLER-BUILD-NAME=Pac-Man

install:
	${UV} sync

# QUESTION: Should we keep this?
helix:
	${UV} run hx .

run:
	${UV} run python ${NAME} test_config.json

debug:
	${UV} run python -m pdb ${NAME} test_config.json

# QUESTION: Should we add Windows and MacOS support?
build:
	rm -rf dist/${PYINSTALLER-BUILD-NAME} build/${PYINSTALLER-BUILD-NAME}
	${UV} run pyinstaller -F -n ${PYINSTALLER-BUILD-NAME} --add-data=test_config.json:. --add-data=textures:textures bundle_pac-man.py

build-run: build
	./dist/${PYINSTALLER-BUILD-NAME}

clean:
	rm -rf	.venv build dist \
			${PYINSTALLER-BUILD-NAME}.spec \
			.mypy_cache .ruff_cache __pycache__ \
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
			src/views/__pycache__

lint:
	${UV} run flake8 . --extend-exclude '.venv/'
	${UV} run mypy . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \

.PHONY: install helix run debug build build-run clean lint
