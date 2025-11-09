from fastapi import FastAPI
import os
import sys
import importlib.util
import traceback
from types import ModuleType

def _is_fastapi_app(obj) -> bool:
    try:
        return isinstance(obj, FastAPI)
    except Exception:
        return False

def _discover_app(root_dir: str):
    this_file = os.path.abspath(__file__)
    counter = 0
    ignored_dirs = {"__pycache__", ".venv", "venv", "env", ".git", "node_modules", "site-packages"}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # skip ignored dirs
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            fullpath = os.path.join(dirpath, fname)
            # skip this entrypoint
            if os.path.abspath(fullpath) == this_file:
                continue
            # avoid simple private modules
            if fname.startswith("_"):
                continue
            try:
                module_name = f"_autodiscovered_module_{counter}"
                counter += 1
                spec = importlib.util.spec_from_file_location(module_name, fullpath)
                if spec is None or spec.loader is None:
                    continue
                mod = importlib.util.module_from_spec(spec)
                # prevent side-effects on sys.modules name collisions
                sys.modules[module_name] = mod
                spec.loader.exec_module(mod)  # type: ignore
                # check for attribute "app"
                if hasattr(mod, "app"):
                    candidate = getattr(mod, "app")
                    if _is_fastapi_app(candidate):
                        return candidate
                # also check top-level variables that may be named differently (optional)
                # e.g., variable names like "application"
                if hasattr(mod, "application"):
                    candidate = getattr(mod, "application")
                    if _is_fastapi_app(candidate):
                        return candidate
            except Exception:
                # don't fail fast — continue searching other files
                # (silently consume import errors to avoid noisy builds)
                # If you want debugging info locally, uncomment the next line:
                # traceback.print_exc()
                continue
            finally:
                # cleanup temp module entry
                try:
                    del sys.modules[module_name]
                except Exception:
                    pass
    return None

# Project root is parent directory of this file (adjust if your layout differs)
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = _discover_app(_project_root)

if app is None:
    # Fallback minimal app — replace with explicit import if you prefer
    app = FastAPI()

    @app.get("/")
    def _root():
        return {
            "status": "fallback app - no FastAPI instance autodetected",
            "hint": "Place your FastAPI instance in a top-level module as `app` or update api/index.py to import it explicitly"
        }