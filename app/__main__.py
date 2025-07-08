#!/usr/bin/env python3

import connexion
from flask import jsonify
from datetime import datetime
from app.openapi_server import encoder
from app.database.db import engine

def main():
    try:
        with engine.connect() as conn:
            print("Successfully connected to MySQL")
    except Exception as e:
        print("MySQL connection failed:", e)

    app = connexion.App(__name__, specification_dir='openapi_server/openapi')
    app.app.json_encoder = encoder.JSONEncoder

    @app.app.route("/")
    def root():
        return jsonify({
            "message": "Looking Glass API is running.",
            "status": 200,
            "date": datetime.utcnow(),
            "type": "about:blank"
        }), 200

    @app.app.route("/api/")
    def api_info():
        return jsonify({
            "name": "Looking Glass API",
            "version": "1.0.1",
            "description": "A minimalist daily log tracker. Create, read, update, and delete what you did each day.",
            "date": datetime.utcnow(),
            "status": "OK"
        }), 200

    app.add_api('openapi.yaml', strict_validation=True, validate_responses=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()