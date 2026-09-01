"""Flask application factory."""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def create_app():
    load_dotenv(PROJECT_ROOT / ".env")
    app = Flask(
        __name__,
        template_folder=str(PROJECT_ROOT / "templates"),
        static_folder=str(PROJECT_ROOT / "static"),
    )
    app.config.update(
        QIANFAN_MODEL=os.getenv("QIANFAN_MODEL", "ERNIE-Tiny-8K"),
        BOOKING_AUTOMATION_ENABLED=(
            os.getenv("BOOKING_AUTOMATION_ENABLED", "false").lower() == "true"
        ),
        BOOKING_SEARCH_URL=os.getenv("BOOKING_SEARCH_URL", ""),
    )

    from .routes import bp

    app.register_blueprint(bp)
    return app
