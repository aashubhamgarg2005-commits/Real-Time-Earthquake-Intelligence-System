
from pyspark.sql.functions import (
    col,
    to_date,
    current_timestamp,
)

from src.processing.spark_session import spark
from src.config.config import (
    kafka_bootstrap_server,
    kafka_topic,
)


def consume_stream_data():
    # Read stream from Kafka
    earthquake = (
        spark.readStream
        .format("kafka")
        .option(
            "kafka.bootstrap.servers",
            kafka_bootstrap_server,
        )
        .option("subscribe", kafka_topic)
        .option("startingOffsets", "latest")
        .option("failOnDataLoss", "false")
        .load()
    )

    # Convert Kafka value from binary to string
    earthquake_json = earthquake.select(
        col("value").cast("string").alias("json_data"),
        col("timestamp").alias("kafka_timestamp"),
    )

    # Create partition date using Kafka timestamp
    earthquake_json = earthquake_json.withColumn(
        "events_date",
        to_date(col("kafka_timestamp")),
    )

    return earthquake_json
