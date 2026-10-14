from .processing.spark_session import spark
from .config.config import minio_bucket
from .processing.kafka_spark_stream import consume_stream_data
from .storage.minio_client import MinioClient
from .processing.data_cleaning import EarthQuakeDataCleaning
from.processing.earthquake_schema import earthquake_schema

def main():
    # read EarthQuake Raw data from Kafka
    EarthQuake_json = consume_stream_data()
    # create bucket if not exists
    minio_client = MinioClient()
    if not minio_client.bucket_exists():
        minio_client.create_bucket()
    # write raw data to minio
    query = (EarthQuake_json.writeStream\
            .format("json")\
            .outputMode("append")\
            .option(
                "path",
                f"s3a://{minio_bucket}/bronze/"
            )\
            .option(
                "checkpointLocation",
                f"s3a://{minio_bucket}/checkpoints/raw/"
            )\
            .partitionBy("events_date")
            .start()
    )

    # do some cleaning on earthquake data
    earthquake_cleaner = EarthQuakeDataCleaning(schema=earthquake_schema)
    clean_data = earthquake_cleaner.clean_data(df=EarthQuake_json)

    # write clean data into minio storage 
    query2 = (clean_data.writeStream\
                .format("parquet")\
                .outputMode("append")\
                .option(
                    "path",
                    f"s3a://{minio_bucket}/process"
                )\
                .option(
                    "checkpointLocation",
                    f"s3a://{minio_bucket}/checkpoints/process"
                )\
                .start()
    )
    spark.streams.awaitAnyTermination()



if __name__ == "__main__":
    main()