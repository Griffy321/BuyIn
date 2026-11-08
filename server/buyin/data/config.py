import dataclasses
import sqlite3
import types
import typing
from pathlib import Path

from buyin.tools import logger
from buyin.tools.paths import desktop_folder

_RESOURCE = "Setup"
_DB_FOLDER = desktop_folder() / "Database"


def _get_db_path(db_name: str) -> Path:
    return _DB_FOLDER / db_name


def _validate_db_name(db_name: str) -> None:
    if not db_name.endswith(".db"):
        logger.warn(body="Database name must end with .db", resource=_RESOURCE, attributes={"dbName": db_name})  # warn you must provide a .db
        raise ValueError("dbName must end with .db")


def column_name(field_name: str) -> str:
    """Python field names are snake_case, database columns are PascalCase: player_first_name -> PlayerFirstName."""
    return "".join(part[:1].upper() + part[1:] for part in field_name.split("_"))


def create_db(db_name: str) -> bool:
    _validate_db_name(db_name)
    db_path = _get_db_path(db_name)
    if not db_path.exists():
        try:
            _DB_FOLDER.mkdir(parents=True, exist_ok=True)  # does nothing if the folder already exists
            db_path.touch()
            logger.info(body="Database file created", resource=_RESOURCE, attributes={"path": str(db_path)})  # file created
            return True
        except Exception as ex:
            logger.error(body="Failed to create database file", resource=_RESOURCE, attributes={"path": str(db_path)}, exception=ex)  # failed to make file
            return False
    else:
        logger.info(body="Database file already exists", resource=_RESOURCE, attributes={"path": str(db_path)})  # file exists
        return True


def create_connection(db_name: str) -> sqlite3.Connection:
    """Opens a connection in autocommit mode. Close it when done, e.g. `with closing(create_connection(...)) as connection:`."""
    _validate_db_name(db_name)
    connection_string = _get_db_path(db_name).as_uri() + "?mode=rw"  # rw errors on a missing file instead of making a new empty one
    logger.info(body="Opening database connection", resource=_RESOURCE, attributes={"connectionString": connection_string})  # making connection
    try:
        connection = sqlite3.connect(connection_string, uri=True, isolation_level=None)
        logger.info(body="Database connection opened", resource=_RESOURCE)  # connection open
        return connection
    except Exception as e:
        logger.error(body="Failed to open database connection", resource=_RESOURCE, attributes={"connectionString": connection_string}, exception=e)  # failed to connect
        raise


def create_table(db_name: str, table_name: str, record_type: type, primary_key: str) -> bool:
    """Builds a table from a dataclass: each field becomes a column. primary_key is the field name."""
    hints = typing.get_type_hints(record_type)

    def column(field: dataclasses.Field) -> str:
        definition = f"{column_name(field.name)} {_get_sql_type(hints[field.name])}"
        return f"{definition} PRIMARY KEY" if field.name == primary_key else definition

    columns = ", ".join(column(field) for field in dataclasses.fields(record_type))

    try:
        connection = create_connection(db_name)
        try:
            connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")  # safe to run every time the app opens
        finally:
            connection.close()
        logger.info(body="Table ready", resource=_RESOURCE, attributes={"dbName": db_name, "tableName": table_name})  # table exists now
        return True
    except Exception as e:
        logger.error(body="Failed to create table", resource=_RESOURCE, attributes={"dbName": db_name, "tableName": table_name}, exception=e)  # failed to make table
        return False


def _get_sql_type(python_type) -> str:
    if typing.get_origin(python_type) in (typing.Union, types.UnionType):  # treats int | None the same as int
        python_type = next(arg for arg in typing.get_args(python_type) if arg is not type(None))
    if python_type in (int, bool):
        return "INTEGER"
    if python_type is float:
        return "REAL"
    return "TEXT"
