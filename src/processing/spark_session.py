
from pathlib import Path

from pyspark.sql import SparkSession

from src.config.config import (
    minio_access_key,
    minio_secret_key,
    minio_endpoint,
)


# ==========================================
# Project paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
JARS_DIR = PROJECT_ROOT / "jars"

POSTGRES_JAR = JARS_DIR / "postgresql-42.7.7.jar"


# ==========================================
# Ivy dependency paths
# ==========================================

IVY_CACHE = Path.home() / ".ivy2.5.2" / "cache"


KAFKA_CONNECTOR_JAR = (
    IVY_CACHE
    / "org.apache.spark"
    / "spark-sql-kafka-0-10_2.13"
    / "jars"
    / "spark-sql-kafka-0-10_2.13-4.2.0.jar"
)

KAFKA_TOKEN_PROVIDER_JAR = (
    IVY_CACHE
    / "org.apache.spark"
    / "spark-token-provider-kafka-0-10_2.13"
    / "jars"
    / "spark-token-provider-kafka-0-10_2.13-4.2.0.jar"
)

KAFKA_CLIENTS_JAR = (
    IVY_CACHE
    / "org.apache.kafka"
    / "kafka-clients"
    / "jars"
    / "kafka-clients-3.9.2.jar"
)

COMMONS_POOL_JAR = (
    IVY_CACHE
    / "org.apache.commons"
    / "commons-pool2"
    / "jars"
    / "commons-pool2-2.13.1.jar"
)

HADOOP_AWS_JAR = (
    IVY_CACHE
    / "org.apache.hadoop"
    / "hadoop-aws"
    / "jars"
    / "hadoop-aws-3.4.1.jar"
)

AWS_SDK_JAR = (
    IVY_CACHE
    / "software.amazon.awssdk"
    / "bundle"
    / "jars"
    / "bundle-2.35.4.jar"
)


# ==========================================
# Validate JAR files
# ==========================================

REQUIRED_JARS = [
    POSTGRES_JAR,
    KAFKA_CONNECTOR_JAR,
    KAFKA_TOKEN_PROVIDER_JAR,
    KAFKA_CLIENTS_JAR,
    COMMONS_POOL_JAR,
    HADOOP_AWS_JAR,
    AWS_SDK_JAR,
]

missing_jars = [
    str(jar_path)
    for jar_path in REQUIRED_JARS
    if not jar_path.is_file()
]

if missing_jars:
    raise FileNotFoundError(
        "Required JAR files were not found:\n"
        + "\n".join(missing_jars)
    )


# ==========================================
# Spark Session
# ==========================================

ALL_JARS = ",".join(
    str(jar_path)
    for jar_path in REQUIRED_JARS
)

spark = (
    SparkSession.builder
    .appName("Real-Time-Earthquake-Intelligence-System")
    .master("local[2]")

    # PostgreSQL + Kafka + MinIO dependencies
    .config("spark.jars", ALL_JARS)

    # Hadoop native library
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

    # MinIO / S3A configuration
    .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint)
    .config("spark.hadoop.fs.s3a.access.key", minio_access_key)
    .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key)
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config(
        "spark.hadoop.fs.s3a.impl",
        "org.apache.hadoop.fs.s3a.S3AFileSystem"
    )
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")

    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("SparkSession created successfully")
print("Spark version:", spark.version)
print("MinIO configuration loaded")
print("PostgreSQL JAR loaded:", POSTGRES_JAR.name)
print("Kafka connector JAR loaded:", KAFKA_CONNECTOR_JAR.name)
