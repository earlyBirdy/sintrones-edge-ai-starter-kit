# Robust initializer that finds repo root automatically
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.db import migrate, connect
migrate(connect())
print('SQLite schema initialized at data/edge.db (root=%s)' % ROOT)