from pyspark.sql.functions import *

class GoldTransformer:
    def __init__(self,df):
        self.df = df

    
    def prepare_dim_location(self):
        df = self.df.withColumn(
            "location_id",
            xxhash64(
                concat_ws(
                    "|",
                    col("latitude").cast("string"),
                    col("longitude").cast("string"),
                    col("region")
                )
            )
        )

        return (
            df.select(
                "location_id",
                "latitude",
                "longitude",
                "region"
            )
            .dropDuplicates(["location_id"])
        )


    def prepare_dim_time(self):
        df = (self.df.withColumn(
            "time_id",
            xxhash64(
                col("event_time").cast("string")
            )
        )
        )\
        .withColumn("year",year("event_time"))\
        .withColumn("month",month("event_time"))\
        .withColumn("day",dayofmonth("event_time"))\
        .withColumn("hour",hour("event_time"))\
        .withColumn("minute",minute("event_time"))\
        .withColumn("second",second("event_time"))\
        .withColumn("day_of_weak",dayofweek("event_time"))\
        .withColumn("day_of_year",dayofyear("event_time"))

        return (
            df.select(
                col("time_id"),
                col("event_time"),
                col("year"),
                col("month"),
                col("day"),
                col("hour"),
                col("minute"),
                col("second"),
                col("day_of_weak"),
                col("day_of_year")
            )
            .dropDuplicates(["time_id"])
        )

    def prepare_dim_event_type(self):
        df = self.df.withColumn(
            "event_type_id",
            xxhash64(
                col("event_type")
            )
        )

        return (
            df.select(
                col("event_type_id"),
                col("event_type"),
                col("magnitude_type")
            )
            .dropDuplicates(["event_type_id"])
        )

    def prepare_dim_source(self):
        df = self.df.withColumn(
            "source_key",
            xxhash64(
                concat_ws(
                    "|",
                    col("source_catalog"),
                    col("author")
                )
            )
        )

        return (
            df.select(
                col("source_key"),
                col("source_id"),
                col("source_catalog"),
                col("author")
            )
            .dropDuplicates(["source_key"])
        )

    def prepare_fact_earthquake(self,dim_location,
                                dim_time,
                                dim_event_type,
                                dim_source):
        df = self.df.alias("s")

        # join dim location
        df = df.join(
            dim_location.select(
                "location_id","latitude","longitude","region"
            ).alias("l"),
            (col("s.latitude") == col("l.latitude")) &
            (col("s.longitude") == col("l.longitude")) &
            (col("s.region") == col("l.region")),
            "left"
        )

        # join dim time

        df = df.join(
            dim_time.select(
                "time_id","event_time"
            ).alias("t"),
            col("s.event_time") == col("t.event_time"),
            "left"
        )

        # join dim event type

        df = df.join(
            dim_event_type.select(
                "event_type_id",
                "event_type",
                "magnitude_type"
            ).alias("et"),
            (col("s.event_type") == col("et.event_type")) &
            (col("s.magnitude_type") == col("et.magnitude_type")),
            "left"
        )

        # join dim source type

        df = df.join(
            dim_source.select(
                "source_key",
                "source_catalog",
                "author"
            ).alias("src"),
            (col("s.source_catalog") == col("src.source_catalog")) &
            (col("s.author") == col("src.author")),
            "left"
        )

        # select final fact table

        fact_df = df.select(
            col("s.event_id"),
            col("l.location_id"),
            col("t.time_id"),
            col("et.event_type_id"),
            col("src.source_key"),
            col("s.magnitude"),
            col("s.depth_km"),
            col("s.lastupdate").alias("last_update"),
            col("s.event_action")
        )

        fact_df = fact_df.withColumn(
            "magnitude_category",
            when(col("magnitude") < 4.0, "Low")
            .when(col("magnitude") < 6.0, "Medium")
            .otherwise("High")
        )

        fact_df = fact_df.withColumn(
            "depth_category",
            when(col("depth_km") < 70, "Shallow")
            .when(col("depth_km") <= 300, "Intermediate")
            .otherwise("deep")
        )

        return fact_df

    

    
        