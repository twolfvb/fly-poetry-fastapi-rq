import os


def is_production() -> bool:
    """Check if we are in production."""
    return os.getenv("APP_ENV", "development") == "production"
