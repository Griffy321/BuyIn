import dataclasses
from contextlib import closing

from buyin.data import config
from buyin.tools import logger

_RESOURCE = "Insert"


def get_metadata(record) -> dict[str, object]:
    """Maps each dataclass field to its database column name and value."""
    return {config.column_name(field.name): getattr(record, field.name) for field in dataclasses.fields(record)}


def write_record(db_name: str, table_name: str, record) -> bool:
    column_values = get_metadata(record)
    column_names = ", ".join(column_values)
    placeholders = ", ".join(":" + key for key in column_values)
    try:
        with closing(config.create_connection(db_name)) as connection:
            connection.execute(
                f"""
                insert into {table_name} ({column_names})
                values ({placeholders})
                """,
                column_values,
            )
        return True
    except Exception as e:
        logger.warn(body="Failed to write record", resource=_RESOURCE, attributes={"tableName": table_name}, exception=e)
        return False
