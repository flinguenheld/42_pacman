# Builds successfully but does not run yet
pyinstaller -F -n Pac-Man --add-data=test_config.json:test_config.json bundle_pac-man.py