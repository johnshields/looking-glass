#!/usr/bin/env python3

import connexion
from flask import jsonify
from datetime import datetime
from flask_cors import CORS

# Project-specific imports
from backend.openapi_server import encoder  # Custom JSON encoder for consistent API output
from backend.database.db import engine  # SQLAlchemy engine for DB connectivity


def create_app() -> connexion.App:
    """Initialize and configure the API application."""

    # Create the Connexion app with OpenAPI specification directory
    app = connexion.App(__name__, specification_dir='openapi_server/openapi')

    # Use custom JSON encoder to handle datetime and UUID objects properly
    app.app.json_encoder = encoder.JSONEncoder

    # Enable Cross-Origin Resource Sharing (CORS) for all routes
    CORS(app.app, resources={r"/*": {"origins": "*"}})

    # ----------------------- ROUTES -----------------------

    # Health check route — confirms the API is up
    @app.app.route("/")
    def root():
        return jsonify({
            "message": "Looking Glass API is running.",
            "status": 200,
            "date": datetime.utcnow(),
            "type": "about:blank"
        }), 200

    # API info/metadata route — provides version and description
    @app.app.route("/api/")
    def api_info():
        return jsonify({
            "name": "LookingGlassAPI",
            "version": "1.0.2",
            "description": "A minimalist daily log tracker. Create, read, update, and delete what you did each day.",
            "status": "OK",
            "date": datetime.utcnow()
        }), 200

    # Attach the OpenAPI spec to enable auto-routing and validation
    app.add_api('openapi.yaml', strict_validation=True, validate_responses=True)

    return app


# Instantiate the Connexion app
connexion_app = create_app()
app = connexion_app.app  # The underlying Flask app for WSGI or deployment


def main():
    """Run the Looking Glass API server."""

    # Test database connectivity on startup
    try:
        with engine.connect() as conn:
            print("Successfully connected to MySQL")
    except Exception as e:
        print("MySQL connection failed:", e)

    # Start the app on port 8080
    connexion_app.run(port=8080)


# Entry point
if __name__ == '__main__':
    main()
