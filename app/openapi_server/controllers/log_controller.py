import connexion
from typing import Dict, Tuple, Union
from datetime import datetime
from app.database.db import SessionLocal
from sqlalchemy import text

from app.openapi_server.models.daily_log import DailyLog  # noqa: E501


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


def logs_date_get(date: str):
    """Get log by date"""
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return None, 400, {"error": "Invalid date format, expected YYYY-MM-DD"}

    try:
        db = SessionLocal()
        stmt = text("""
            SELECT id, title, entries, log_date, tags, mood, created_at, updated_at
            FROM daily_log
            WHERE log_date = :log_date
            LIMIT 1
        """)
        result = db.execute(stmt, {"log_date": parsed_date}).fetchone()

        if not result:
            return None, 404, {"error": f"No log found for date {date}"}

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


def logs_date_delete(_date: str) -> tuple[None, int, dict[str, str]] | str:
    """Delete log by date

    :param _date: The date of the log to delete
    :type _date: str
    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]]
    """
    try:
        parsed_date = datetime.strptime(_date, "%Y-%m-%d").date()
    except ValueError:
        return None, 400, {"error": "Invalid date format, expected YYYY-MM-DD"}

    # TODO: implement deletion logic
    return 'do some magic!'


def logs_date_put(_date: str, body=None) -> tuple[None, int, dict[str, str]] | str:
    """Update log by date

    :param _date: The date of the log to update
    :type _date: str
    :param body: The updated log data
    :type body: dict | bytes
    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]]
    """
    try:
        parsed_date = datetime.strptime(_date, "%Y-%m-%d").date()
    except ValueError:
        return None, 400, {"error": "Invalid date format, expected YYYY-MM-DD"}

    if connexion.request.is_json:
        daily_log = DailyLog.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return None, 400, {"error": "Request body must be JSON"}

    # TODO: implement update logic
    return 'do some magic!'


def logs_post(body=None) -> tuple[None, int, dict[str, str]] | str:
    """Create a new daily log

    :param body: The new log to create
    :type body: dict | bytes
    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]]
    """
    if connexion.request.is_json:
        daily_log = DailyLog.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return None, 400, {"error": "Request body must be JSON"}

    # TODO: implement creation logic
    return 'do some magic!'
