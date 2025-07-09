#!/usr/bin/env python3

import connexion
from flask import jsonify
from datetime import datetime
from flask_cors import CORS
from app.openapi_server import encoder
from app.database.db import engine


def create_app() -> connexion.App:
    """Initialize and configure the API application."""
    app = connexion.App(__name__, specification_dir='openapi_server/openapi')
    app.app.json_encoder = encoder.JSONEncoder

    CORS(app.app, resources={r"/*": {"origins": "*"}})

    # Health check endpoint
    @app.app.route("/")
    def root():
        return jsonify({
            "message": "Looking Glass API is running.",
            "status": 200,
            "date": datetime.utcnow(),
            "type": "about:blank"
        }), 200

    # API metadata endpoint
    @app.app.route("/api/")
    def api_info():
        return jsonify({
            "name": "LookingGlassAPI",
            "version": "1.0.2",
            "description": "A minimalist daily log tracker. Create, read, update, and delete what you did each day.",
            "status": "OK",
            "date": datetime.utcnow()
        }), 200

    # Add OpenAPI spec
    app.add_api('openapi.yaml', strict_validation=True, validate_responses=True)
    return app


def main():
    """Run the Looking Glass API server."""
    try:
        with engine.connect() as conn:
            print("Successfully connected to MySQL")
    except Exception as e:
        print("MySQL connection failed:", e)

    app = create_app()
    app.run(port=8080)


if __name__ == '__main__':
    main()
