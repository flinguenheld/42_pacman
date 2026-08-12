# Builds successfully but does not run yet
rm -rf dist/Pac-Man build/Pac-Man && \
pyinstaller -F -n Pac-Man --add-data=test_config.json:. --add-data=textures:textures bundle_pac-man.py