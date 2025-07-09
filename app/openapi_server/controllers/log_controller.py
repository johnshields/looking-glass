import json
import connexion
from datetime import date
from app.database.db import SessionLocal
from sqlalchemy import text
from uuid import UUID, uuid4

from app.openapi_server.models.daily_log import DailyLog  # noqa: E501


def logs_post(body=None) -> tuple[None, int, dict[str, str]] | str:
    """Create a new daily log"""

    if not connexion.request.is_json:
        return None, 400, {"error": "Request body must be JSON"}

    try:
        data = connexion.request.get_json()

        db = SessionLocal()
        new_id = str(uuid4())

        db.execute(
            text("""
                    INSERT INTO daily_log (id, title, entries, log_date, tags, mood, created_at, updated_at)
                    VALUES (:id, :title, :entries, :log_date, :tags, :mood, NOW(), NOW())
                """),
            {
                "id": new_id,
                "title": data.get("title", ""),
                "entries": data.get("entries", ""),
                "log_date": data.get("log_date", date.today().isoformat()),
                "tags": json.dumps(data.get("tags", [])),
                "mood": data.get("mood", "")
            }
        )

        db.commit()
        return None, 201, {"message": f"Log {new_id} created successfully"}

    except Exception as e:
        return None, 500, {"error": str(e)}

    finally:
        db.close()


def logs_get() -> str:
    """Get all logs"""

    try:
        db = SessionLocal()
        result = db.execute(
            text("SELECT id, title, entries, log_date, tags, mood, created_at, updated_at FROM daily_log"))
        logs = []

        for row in result.fetchall():
            logs.append({
                "id": row.id,
                "title": row.title,
                "entries": row.entries,
                "date": row.log_date.isoformat() if row.log_date else None,
                "tags": row.tags.split(",") if row.tags else [],
                "mood": row.mood,
                "created_at": row.created_at.isoformat(),
                "updated_at": row.updated_at.isoformat()
            })

        return logs, 200

    except Exception as e:
        return None, 500, {"error": str(e)}

    finally:
        db.close()


def logs_id_get(id: str):
    """Get log by ID"""

    try:
        UUID(id, version=4)
    except ValueError:
        return None, 400, {"error": "Invalid UUID format for ID"}

    try:
        db = SessionLocal()
        stmt = text("""
            SELECT id, title, entries, log_date, tags, mood, created_at, updated_at
            FROM daily_log
            WHERE id = :id
            LIMIT 1
        """)
        result = db.execute(stmt, {"id": id}).fetchone()

        if not result:
            return None, 404, {"error": f"No log found for date {id}"}

        log = {
            "id": result.id,
            "title": result.title,
            "entries": result.entries,
            "log_date": result.log_date.isoformat(),
            "tags": result.tags.split(",") if result.tags else [],
            "mood": result.mood,
            "created_at": result.created_at.isoformat(),
            "updated_at": result.updated_at.isoformat()
        }

        return log, 200

    except Exception as e:
        return None, 500, {"error": str(e)}

    finally:
        db.close()


def logs_id_put(id: str, body=None) -> tuple[None, int, dict[str, str]] | str:
    """Update log by ID"""

    try:
        uuid_obj = UUID(id)
    except ValueError as e:
        return None, 400, {"error": f"Invalid UUID format for ID: {id}"}

    if not connexion.request.is_json:
        return None, 400, {"error": "Request body must be JSON"}

    try:
        data = connexion.request.get_json()
        db = SessionLocal()

        print(f"Looking up log with ID: {uuid_obj}")

        result = db.execute(
            text("SELECT id FROM daily_log WHERE id = :id"),
            {"id": str(uuid_obj)}
        ).fetchone()

        if not result:
            return None, 404, {"error": f"No log found with ID {id}"}

        db.execute(
            text("""
                UPDATE daily_log
                SET title = :title,
                    entries = :entries,
                    log_date = :log_date,
                    tags = :tags,
                    mood = :mood,
                    updated_at = NOW()
                WHERE id = :id
            """),
            {
                "id": str(uuid_obj),
                "title": data.get("title", ""),
                "entries": data.get("entries", ""),
                "log_date": data.get("log_date", date.today().isoformat()),
                "tags": json.dumps(data.get("tags", [])),
                "mood": data.get("mood", "")
            }
        )

        db.commit()
        return None, 204, {"message": f"Log {id} updated successfully"}

    except Exception as e:
        return None, 500, {"error": str(e)}

    finally:
        db.close()


def logs_id_delete(id: str) -> tuple[None, int, dict[str, str]] | str:
    """Delete log by ID"""

    try:
        UUID(id, version=4)
    except ValueError:
        return None, 400, {"error": "Invalid UUID format for ID"}

    try:
        db = SessionLocal()
        stmt = text("DELETE FROM daily_log WHERE id = :id")
        result = db.execute(stmt, {"id": id})
        db.commit()

        if result.rowcount == 0:
            return None, 404, {"error": f"No log found for with ID {id}"}

        return None, 204, {"message": f"Log {id} delete successfully"}

    except Exception as e:
        return None, 500, {"error": str(e)}

    finally:
        db.close()
