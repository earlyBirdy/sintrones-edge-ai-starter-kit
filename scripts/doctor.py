import sys, os, pathlib
print('Python:', sys.version)
print('CWD:', os.getcwd())
print('Repo root guess:', pathlib.Path(__file__).resolve().parents[1])
print('sys.path head:', sys.path[:5])
try:
    import core.db as db
    print('core.db import: OK')
except Exception as e:
    print('core.db import: FAIL ->', e)