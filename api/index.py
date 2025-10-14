# Vercel Python Function entrypoint for Flask (WSGI)
# Exposes `app` so Vercel can detect and serve it at /api

import os
import sys

# Ensure project root is on sys.path to import app.py
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app as app  # noqa: E402,F401
