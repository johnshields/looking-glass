#!/usr/bin/env python3

import connexion
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
    app.add_api('openapi.yaml', strict_validation=True, validate_responses=True)
    app.run(port=8080)

if __name__ == '__main__':
    main()
