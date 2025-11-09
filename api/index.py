from fastapi import FastAPI

# Try common locations for your FastAPI instance. Replace these with your actual import path.
app = None
try:
    # common patterns: "app", "main", "server"
    from app import app as app  # noqa: F401
except Exception:
    try:
        from main import app as app  # noqa: F401
    except Exception:
        try:
            from server import app as app  # noqa: F401
        except Exception:
            # Fallback: minimal app — replace above imports with your real module
            app = FastAPI()

            @app.get("/")
            def _root():
                return {"status": "fallback app - update api/index.py to import your app"}