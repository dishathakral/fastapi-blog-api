from fastapi import FastAPI

# Try common locations for the user's FastAPI app. Replace these with your real import if needed.
application = None
try:
    from app import app as application
except Exception:
    try:
        from main import app as application
    except Exception:
        try:
            from server import app as application
        except Exception:
            # Fallback minimal app — replace import above with your real path.
            application = FastAPI()

            @application.get("/")
            def _root():
                return {"status": "fallback app - change import in api/index.py to your app"}

# Wrap for Vercel using vercel-asgi adapter if available; otherwise expose app directly.
try:
    from vercel_asgi import VercelAsgi

    handler = VercelAsgi(application)
except Exception:
    # Vercel Python builder may accept `app` directly; export both names to be safe.
    app = application
    handler = None