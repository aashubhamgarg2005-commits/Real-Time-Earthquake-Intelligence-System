
from uuid import uuid4

from pyspark.sql import DataFrame

from src.config.config import (
    postgres_url,
    postgres_user,
    postgres_password
)


def write_to_postgres(
    df: DataFrame,
    table_name: str,
    key_columns: list[str],
    update_columns: list[str] | None = None
):
    if df.isEmpty():
        print(f"{table_name}: empty batch, skipped")
        return

    if not key_columns:
        raise ValueError("key_columns cannot be empty")

    # Remove duplicate keys inside this batch.
    df = df.dropDuplicates(key_columns)

    # Create a unique staging table for this batch.
    staging_table = f"stg_{table_name}_{uuid4().hex[:12]}"

    # PostgreSQL JDBC configuration.
    properties = {
        "user": postgres_user,
        "password": postgres_password,
        "driver": "org.postgresql.Driver"
    }

    # 1. Write batch into staging table.
    (
        df.write
        .format("jdbc")
        .option("url", postgres_url)
        .option("dbtable", staging_table)
        .option("user", properties["user"])
        .option("password", properties["password"])
        .option("driver", properties["driver"])
        .mode("errorifexists")
        .save()
    )

    def quote(name):
        return '"' + name.replace('"', '""') + '"'

    columns = df.columns

    column_sql = ", ".join(quote(c) for c in columns)
    timestamp_columns = {
    "event_time",
    "last_update",
    "lastupdate_timestamp"
}

    select_sql = ", ".join(
    f"CAST({quote(c)} AS TIMESTAMPTZ) AS {quote(c)}"
    if c in timestamp_columns
    else quote(c)
    for c in columns
)
    key_sql = ", ".join(quote(c) for c in key_columns)

    if update_columns is None:
        update_columns = [
            c for c in columns
            if c not in key_columns
        ]

    if update_columns:
        updates_sql = ", ".join(
            f"{quote(c)} = EXCLUDED.{quote(c)}"
            for c in update_columns
        )
        conflict_sql = f"DO UPDATE SET {updates_sql}"
    else:
        conflict_sql = "DO NOTHING"

    # 2. Upsert into the target table.

    sql = f"""
        INSERT INTO {quote(table_name)} ({column_sql})
        SELECT {select_sql}
        FROM {quote(staging_table)}
        ON CONFLICT ({key_sql})
        {conflict_sql}
    """


    jvm = df.sparkSession.sparkContext._jvm
    connection = None
    statement = None

    try:
        connection = jvm.java.sql.DriverManager.getConnection(
            postgres_url,
            postgres_user,
            postgres_password
        )

        connection.setAutoCommit(False)
        statement = connection.createStatement()

        statement.executeUpdate(sql)
        statement.executeUpdate(
            f"DROP TABLE {quote(staging_table)}"
        )

        connection.commit()

        print(
            f"{table_name}: PostgreSQL UPSERT successful"
        )

    except Exception:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if statement is not None:
            statement.close()

        if connection is not None:
            connection.close()
