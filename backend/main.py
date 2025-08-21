#!/usr/bin/env python3
import connexion
from flask import jsonify
from datetime import datetime
from flask_cors import CORS
from backend.openapi_server import encoder
from backend.database.db import engine


def create_app() -> connexion.App:
    """Initialise and configure the API."""
    api = connexion.App(__name__, specification_dir='openapi_server/openapi')
    api.app.json_encoder = encoder.JSONEncoder
    CORS(api.app, resources={r"/*": {"origins": "*"}})

    @api.app.route("/")
    def root():
        return jsonify({
            "message": "Looking Glass API is running.",
            "status": 200,
            "date": datetime.now(),
            "type": "about:blank"
        }), 200

    @api.app.route("/api/")
    def api_info():
        return jsonify({
            "name": "LookingGlassAPI",
            "version": "1.0.2",
            "description": "A minimalist daily log tracker. Create, read, update, and delete what you did each day.",
            "status": "OK",
            "date": datetime.now()
        }), 200

    api.add_api('openapi.yaml', strict_validation=True, validate_responses=True)
    return api


# Exported for use in __main__.py
connexion_app = create_app()
app = connexion_app.app
engine = engine
