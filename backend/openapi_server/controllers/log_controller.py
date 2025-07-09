import json
import connexion
from datetime import date
from uuid import UUID, uuid4
from sqlalchemy import text
from backend.database.db import SessionLocal


# ----------------- Helper Functions ----------------- #

def _validate_uuid(id: str):
    try:
        return UUID(id, version=4)
    except ValueError:
        return None


def _get_json_body():
    if not connexion.request.is_json:
        return None, {"error": "Request body must be JSON"}
    return connexion.request.get_json(), None


# ----------------- Routes ----------------- #

def logs_post(body=None):
    """Create a new daily log"""
    data, error = _get_json_body()
    if error:
        return None, 400, error

    db = SessionLocal()
    try:
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


def logs_get():
    """Get all logs"""
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT id, title, entries, log_date, tags, mood, created_at, updated_at FROM daily_log ORDER BY log_date DESC;
        """))

        logs = [{
            "id": row.id,
            "title": row.title,
            "entries": row.entries,
            "log_date": row.log_date.isoformat() if row.log_date else None,
            "tags": row.tags.split(",") if row.tags else [],
            "mood": row.mood,
            "created_at": row.created_at.isoformat(),
            "updated_at": row.updated_at.isoformat()
        } for row in result.fetchall()]

        return logs, 200
    except Exception as e:
        return None, 500, {"error": str(e)}
    finally:
        db.close()


def logs_id_get(id: str):
    """Get log by ID"""
    if not _validate_uuid(id):
        return None, 400, {"error": "Invalid UUID format for ID"}

    db = SessionLocal()
    try:
        result = db.execute(
            text("""
                SELECT id, title, entries, log_date, tags, mood, created_at, updated_at
                FROM daily_log WHERE id = :id LIMIT 1
            """),
            {"id": id}
        ).fetchone()

        if not result:
            return None, 404, {"error": f"No log found for ID {id}"}

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


def logs_id_put(id: str, body=None):
    """Update log by ID"""
    if not _validate_uuid(id):
        return None, 400, {"error": f"Invalid UUID format for ID: {id}"}

    data, error = _get_json_body()
    if error:
        return None, 400, error

    db = SessionLocal()
    try:
        exists = db.execute(
            text("SELECT id FROM daily_log WHERE id = :id"),
            {"id": id}
        ).fetchone()

        if not exists:
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
                "id": id,
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


def logs_id_delete(id: str):
    """Delete log by ID"""
    if not _validate_uuid(id):
        return None, 400, {"error": "Invalid UUID format for ID"}

    db = SessionLocal()
    try:
        result = db.execute(
            text("DELETE FROM daily_log WHERE id = :id"),
            {"id": id}
        )
        db.commit()

        if result.rowcount == 0:
            return None, 404, {"error": f"No log found with ID {id}"}

        return None, 204, {"message": f"Log {id} deleted successfully"}
    except Exception as e:
        return None, 500, {"error": str(e)}
    finally:
        db.close()
