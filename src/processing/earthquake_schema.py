from pyspark.sql.types import *

earthquake_schema = StructType([
    StructField("action",StringType(),True),
    StructField("data",StructType([
        StructField("type",StringType(),True),
        StructField("geometry",StructType([
            StructField("type",StringType(),True),
            StructField("coordinates",ArrayType(DoubleType()),True)
        ]),True),
        StructField("id",StringType(),True),
        StructField("properties",StructType([
             StructField("source_id", StringType(), True),
            StructField("source_catalog", StringType(), True),
            StructField("lastupdate", StringType(), True),
            StructField("time", StringType(), True),
            StructField("flynn_region", StringType(), True),
            StructField("lat", DoubleType(), True),
            StructField("lon", DoubleType(), True),
            StructField("depth", DoubleType(), True),
            StructField("evtype", StringType(), True),
            StructField("auth", StringType(), True),
            StructField("mag", DoubleType(), True),
            StructField("magtype", StringType(), True),
            StructField("unid", StringType(), True)
        ]), True)
    ]), True)
])
