
from .processing.spark_session import spark
from .config.config import minio_bucket
from .processing.kafka_spark_stream import consume_stream_data
from .storage.minio_client import MinioClient
from .processing.data_cleaning import EarthQuakeDataCleaning
from .processing.earthquake_schema import earthquake_schema
from .processing.gold_transformer import GoldTransformer


def main():

    # ==========================================
    # 1. READ RAW EARTHQUAKE DATA FROM KAFKA
    # ==========================================
    earthquake_json = consume_stream_data()

    # ==========================================
    # 2. CREATE MINIO BUCKET IF NOT EXISTS
    # ==========================================
    minio_client = MinioClient()

    if not minio_client.bucket_exists():
        minio_client.create_bucket()

    # ==========================================
    # 3. BRONZE LAYER - WRITE RAW JSON
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
    # 4. CLEAN RAW EARTHQUAKE DATA
    # ==========================================
    earthquake_cleaner = EarthQuakeDataCleaning(
        schema=earthquake_schema
    )

    clean_data = earthquake_cleaner.clean_data(
        df=earthquake_json
    )

    # ==========================================
    # 5. SILVER LAYER - WRITE CLEAN PARQUET
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
    # 6. GOLD LAYER - PROCESS EACH MICRO-BATCH
    # ==========================================
    def process_gold_batch(batch_df, batch_id):

        if batch_df.isEmpty():
            print(f"Gold batch {batch_id} is empty. Skipping.")
            return

        print(f"Processing Gold batch: {batch_id}")

        # Create transformer using the current batch
        gold_transformer = GoldTransformer(df=batch_df)

        # Create dimension tables
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

        # Create fact table using batch DataFrames
        fact_earthquake = (
            gold_transformer.prepare_fact_earthquake(
                dim_location=dim_location,
                dim_time=dim_time,
                dim_event_type=dim_event_type,
                dim_source=dim_source
            )
        )

        # Collect all Gold DataFrames
        gold_dataframes = {
            "dim_location": dim_location,
            "dim_time": dim_time,
            "dim_event_type": dim_event_type,
            "dim_source": dim_source,
            "fact_earthquake": fact_earthquake
        }

        # Write Gold tables to MinIO
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

        print(f"Gold batch {batch_id} completed.")

    # ==========================================
    # 7. START GOLD STREAMING WITH FOREACHBATCH
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

    print("Bronze streaming started.")
    print("Silver streaming started.")
    print("Gold streaming started.")

    # ==========================================
    # 8. KEEP ALL STREAMS RUNNING
    # ==========================================
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
