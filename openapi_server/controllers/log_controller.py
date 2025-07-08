import connexion
from typing import Dict, Tuple, Union
from datetime import datetime

from openapi_server.models.daily_log import DailyLog  # noqa: E501


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


def logs_date_get(_date: str) -> tuple[None, int, dict[str, str]] | str:
    """Get log by date

    :param _date: The date of the log to retrieve
    :type _date: str
    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]]
    """
    try:
        parsed_date = datetime.strptime(_date, "%Y-%m-%d").date()
    except ValueError:
        return None, 400, {"error": "Invalid date format, expected YYYY-MM-DD"}

    # TODO: implement retrieval logic
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


def logs_get() -> str:
    """Get all logs

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]]
    """
    # TODO: implement logic to return all logs
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
