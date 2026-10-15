
from .processing.spark_session import spark
from .config.config import minio_bucket
from .processing.kafka_spark_stream import consume_stream_data
from .storage.minio_client import MinioClient
from .processing.data_cleaning import EarthQuakeDataCleaning
from .processing.earthquake_schema import earthquake_schema
from .processing.gold_transformer import GoldTransformer

from sql.postgres_writer import write_to_postgres


def main():
    # ==========================================
    # 1. Read real-time data from Kafka
    # ==========================================
    earthquake_json = consume_stream_data()

    # ==========================================
    # 2. Initialize MinIO bucket
    # ==========================================
    minio_client = MinioClient()

    if not minio_client.bucket_exists():
        minio_client.create_bucket()

    # ==========================================
    # 3. BRONZE: Store raw JSON in MinIO
    # ==========================================
    bronze_query = (
        earthquake_json.writeStream
        .format("json")
        .outputMode("append")
        .option(
            "path",
            f"s3a://{minio_bucket}/bronze/"
        )
        .option(
            "checkpointLocation",
            f"s3a://{minio_bucket}/checkpoints/raw/"
        )
        .partitionBy("events_date")
        .start()
    )

    # ==========================================
    # 4. Clean incoming earthquake data
    # ==========================================
    earthquake_cleaner = EarthQuakeDataCleaning(
        schema=earthquake_schema
    )

    clean_data = earthquake_cleaner.clean_data(
        df=earthquake_json
    )

    # ==========================================
    # 5. SILVER: Store cleaned data in MinIO
    # ==========================================
    silver_query = (
        clean_data.writeStream
        .format("parquet")
        .outputMode("append")
        .option(
            "path",
            f"s3a://{minio_bucket}/silver/"
        )
        .option(
            "checkpointLocation",
            f"s3a://{minio_bucket}/checkpoints/silver/"
        )
        .start()
    )

    # ==========================================
    # 6. GOLD: Transform and write each microbatch
    # ==========================================
    def process_gold_batch(batch_df, batch_id):

        if batch_df.isEmpty():
            print(f"Gold batch {batch_id} is empty. Skipping.")
            return

        print(f"Processing Gold batch: {batch_id}")

        # ------------------------------------------
        # Create Gold Transformer
        # ------------------------------------------
        gold_transformer = GoldTransformer(
            df=batch_df
        )

        # ------------------------------------------
        # Prepare dimension tables
        # ------------------------------------------
        dim_location = (
            gold_transformer.prepare_dim_location()
        )

        dim_time = (
            gold_transformer.prepare_dim_time()
        )

        dim_event_type = (
            gold_transformer.prepare_dim_event_type()
        )

        dim_source = (
            gold_transformer.prepare_dim_source()
        )

        # ------------------------------------------
        # Prepare fact table
        # ------------------------------------------
        fact_earthquake = (
            gold_transformer.prepare_fact_earthquake(
                dim_location=dim_location,
                dim_time=dim_time,
                dim_event_type=dim_event_type,
                dim_source=dim_source
            )
        )

        # ------------------------------------------
        # Write Gold DataFrames to MinIO
        # ------------------------------------------
        gold_dataframes = {
            "dim_location": dim_location,
            "dim_time": dim_time,
            "dim_event_type": dim_event_type,
            "dim_source": dim_source,
            "fact_earthquake": fact_earthquake
        }

        for table_name, table_df in gold_dataframes.items():

            output_path = (
                f"s3a://{minio_bucket}/gold/{table_name}/"
            )

            (
                table_df.write
                .mode("append")
                .parquet(output_path)
            )

            print(
                f"Batch {batch_id}: "
                f"{table_name} written to MinIO"
            )

        # ------------------------------------------
        # Write dimensions to PostgreSQL first
        # ------------------------------------------
        write_to_postgres(
            dim_location,
            "dim_location",
            ["location_id"]
        )

        write_to_postgres(
            dim_time,
            "dim_time",
            ["time_id"]
        )

        # The PostgreSQL table name is event_type,
        # even though the Spark DataFrame is dim_event_type.
        write_to_postgres(
            dim_event_type,
            "dim_event_type",
            ["event_type_id"]
        )

        write_to_postgres(
            dim_source,
            "dim_source",
            ["source_key"]
        )

        print(
            f"Batch {batch_id}: "
            "dimension tables written to PostgreSQL"
        )

        # ------------------------------------------
        # Write fact table after dimension tables
        # ------------------------------------------
        write_to_postgres(
            fact_earthquake,
            "fact_earthquake",
            ["event_id"],
            update_columns=[
                "location_id",
                "time_id",
                "event_type_id",
                "source_key",
                "magnitude",
                "depth_km",
                "last_update",
                "event_action",
                "magnitude_category",
                "depth_category"
            ]
        )

        print(
            f"Gold batch {batch_id} completed successfully."
        )

    # ==========================================
    # 7. Start Gold streaming query
    # ==========================================
    gold_query = (
        clean_data.writeStream
        .foreachBatch(process_gold_batch)
        .option(
            "checkpointLocation",
            f"s3a://{minio_bucket}/checkpoints/gold/"
        )
        .start()
    )

    # ==========================================
    # 8. Pipeline status
    # ==========================================
    print("Bronze streaming started.")
    print("Silver streaming started.")
    print("Gold streaming started.")
    print("PostgreSQL writes enabled.")

    # Keep streaming queries running
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
