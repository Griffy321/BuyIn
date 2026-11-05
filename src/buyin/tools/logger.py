import json
import traceback
from datetime import datetime, timezone

from buyin.tools.paths import desktop_folder
from buyin.tools.random_string import generate_uid

_FILE_PATH = desktop_folder() / "BuyInLogs.txt"


def info(body: str, resource: str | None = None, attributes: dict | None = None, exception: BaseException | None = None) -> None:
    _write("Info", body, resource, attributes, exception)


def warn(body: str, resource: str | None = None, attributes: dict | None = None, exception: BaseException | None = None) -> None:
    _write("Warning", body, resource, attributes, exception)


def error(body: str, resource: str | None = None, attributes: dict | None = None, exception: BaseException | None = None) -> None:
    _write("Error", body, resource, attributes, exception)


def _write(level: str, body: str, resource: str | None, attributes: dict | None, exception: BaseException | None) -> None:
    now = datetime.now(timezone.utc)
    log = {
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z",  # utc time, ISO 8601
        "traceID": generate_uid(),  # distinct log id
        "level": level,  # log level
        "body": body,  # human readable text saying what's up
    }
    if resource is not None:
        log["resource"] = resource  # the thing that made the log, e.g. the name of the class that makes the object
    if attributes is not None:
        log["attributes"] = attributes  # details relating to the object like the playerID, written as a nested JSON object
    if exception is not None:
        log["exception"] = "".join(traceback.format_exception(exception)).rstrip()  # any exceptions go here

    try:
        line = json.dumps(log, separators=(",", ":"), default=str)
        with open(_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(line + "\n")
    except Exception as ex:
        print("Failed to write log: " + str(ex))
        print(" ".join(str(value) for value in log.values()))
