from backend.main import connexion_app, engine
from sqlalchemy.exc import SQLAlchemyError


def main():
    """Run the Looking Glass API server."""
    try:
        with engine.connect():
            print("Successfully connected to MySQL")
    except SQLAlchemyError as e:
        print("MySQL connection failed:", e)

    # Run FastAPI via Uvicorn
    connexion_app.run(port=8080)


if __name__ == '__main__':
    main()
