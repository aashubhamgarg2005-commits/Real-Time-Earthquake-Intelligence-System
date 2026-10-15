
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col,
    from_json,
    when,
    trim,
    lit,
    to_timestamp
)


class EarthQuakeDataCleaning:

    def __init__(self, schema):
        self.schema = schema

    # 1. Parse nested JSON data
    def parse_json(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            "parsed_data",
            from_json(col("json_data"), self.schema)
        )

    # 2. Flatten nested JSON data
    def flatten_nested_json(self, parsed_df: DataFrame) -> DataFrame:
        return parsed_df.select(
            col("parsed_data.action").alias("event_action"),
            col("parsed_data.data.id").alias("event_id"),
            col("parsed_data.data.type").alias("feature_type"),
            col("parsed_data.data.geometry.type").alias("geometry_type"),

            col("parsed_data.data.geometry.coordinates")
                .getItem(0).alias("coordinate_lon"),
            col("parsed_data.data.geometry.coordinates")
                .getItem(1).alias("coordinate_lat"),
            col("parsed_data.data.geometry.coordinates")
                .getItem(2).alias("coordinate_depth"),

            col("parsed_data.data.properties.source_id").alias("source_id"),
            col("parsed_data.data.properties.source_catalog").alias("source_catalog"),
            col("parsed_data.data.properties.lastupdate").alias("lastupdate"),
            col("parsed_data.data.properties.time").alias("event_time"),
            col("parsed_data.data.properties.flynn_region").alias("region"),
            col("parsed_data.data.properties.lat").alias("latitude"),
            col("parsed_data.data.properties.lon").alias("longitude"),
            col("parsed_data.data.properties.depth").alias("depth_km"),
            col("parsed_data.data.properties.evtype").alias("event_type"),
            col("parsed_data.data.properties.auth").alias("author"),
            col("parsed_data.data.properties.mag").alias("magnitude"),
            col("parsed_data.data.properties.magtype").alias("magnitude_type"),
            col("parsed_data.data.properties.unid").alias("unid")
        )

    # 3. Fix missing and blank values
    def handle_missing_values(self, df: DataFrame) -> DataFrame:
        string_columns = [
            "event_action", "event_id", "feature_type",
            "geometry_type", "source_id", "source_catalog",
            "region", "event_type", "author",
            "magnitude_type", "unid"
        ]

        for column in string_columns:
            df = df.withColumn(
                column,
                when(
                    trim(col(column)) == "",
                    lit(None).cast("string")
                ).otherwise(col(column))
            )

        # Event ID is required
        return df.filter(
            col("event_id").isNotNull() &
            (trim(col("event_id")) != "")
        )

    # 4. Fix data types and timestamps
    def fix_data_types(self, df: DataFrame) -> DataFrame:
        numeric_columns = [
            "latitude", "longitude", "depth_km", "magnitude",
            "coordinate_lon", "coordinate_lat", "coordinate_depth"
        ]

        for column in numeric_columns:
            df = df.withColumn(
                column,
                col(column).cast("double")
            )

        return (
            df
            .withColumn("event_time", to_timestamp("event_time"))
            .withColumn(
                "lastupdate_timestamp",
                to_timestamp("lastupdate")
            )
        )

    # 5. Validate earthquake records
    def validate_data(self, df: DataFrame) -> DataFrame:
        return df.filter(
            col("latitude").between(-90, 90) &
            col("longitude").between(-180, 180) &
            col("magnitude").isNotNull() &
            col("event_time").isNotNull()
        )

    # 6. Remove duplicates (batch DataFrames)
    def remove_duplicates(self, df: DataFrame) -> DataFrame:
        return df.dropDuplicates(["event_id"])

    # 7. Complete cleaning pipeline
    def clean_data(self, df: DataFrame) -> DataFrame:
        df = self.parse_json(df)
        df = df.filter(col("parsed_data").isNotNull())

        df = self.flatten_nested_json(df)
        df = self.handle_missing_values(df)
        df = self.fix_data_types(df)
        df = self.validate_data(df)

        # Batch deduplication only
        if not df.isStreaming:
            df = self.remove_duplicates(df)

        return df
