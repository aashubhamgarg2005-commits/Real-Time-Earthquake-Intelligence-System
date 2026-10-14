from pyspark.sql import SparkSession
from src.config.config import (
    minio_access_key,
    minio_secret_key,
    minio_endpoint,
)


KAFKA_CONNECTOR_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.spark"
    r"\spark-sql-kafka-0-10_2.13\jars"
    r"\spark-sql-kafka-0-10_2.13-4.2.0.jar"
)

KAFKA_TOKEN_PROVIDER_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.spark"
    r"\spark-token-provider-kafka-0-10_2.13\jars"
    r"\spark-token-provider-kafka-0-10_2.13-4.2.0.jar"
)

KAFKA_CLIENTS_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.kafka"
    r"\kafka-clients\jars"
    r"\kafka-clients-3.9.2.jar"
)

COMMONS_POOL_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.commons"
    r"\commons-pool2\jars"
    r"\commons-pool2-2.13.1.jar"
)

HADOOP_AWS_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\org.apache.hadoop"
    r"\hadoop-aws\jars"
    r"\hadoop-aws-3.4.1.jar"
)

AWS_SDK_JAR = (
    r"C:\Users\HP\.ivy2.5.2\cache\software.amazon.awssdk"
    r"\bundle\jars"
    r"\bundle-2.35.4.jar"
)


spark = (
    SparkSession.builder
    .appName("Real-Time-EarthQuake-Intelligence-System")
    .master("local[2]")

    .config(
        "spark.jars",
        ",".join([
            KAFKA_CONNECTOR_JAR,
            KAFKA_TOKEN_PROVIDER_JAR,
            KAFKA_CLIENTS_JAR,
            COMMONS_POOL_JAR,
            HADOOP_AWS_JAR,
            AWS_SDK_JAR
        ])
    )

    .config(
        "spark.driver.extraJavaOptions",
        "-Djava.library.path=C:/hadoop/bin"
    )

    .config(
        "spark.executor.extraJavaOptions",
        "-Djava.library.path=C:/hadoop/bin"
    )

    .config("spark.hadoop.native.lib", "true")
    .config("spark.hadoop.io.native.lib.available", "true")
    .config("spark.hadoop.home.dir", r"C:\hadoop")
    .config("spark.hadoop.native.lib.path", r"C:\hadoop\bin")
    .config("spark.hadoop.fs.s3a.endpoint",minio_endpoint)
    .config("spark.hadoop.fs.s3a.access.key",minio_access_key)
    .config("spark.hadoop.fs.s3a.secret.key",minio_secret_key)
    .config("spark.hadoop.fs.s3a.path.style.access","true")
    .config("spark.hadoop.fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled","false")

    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")
print("SparkSession created successfully")
print("Spark version:", spark.version)
print("MinIO configuration loaded")