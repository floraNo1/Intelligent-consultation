"""Development entry point for the course prototype."""

import os

from medical_agent import create_app


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
