import os 
from dotenv import load_dotenv

# Load .env file 

load_dotenv()

# kafka configuration

kafka_bootstrap_server = os.getenv("KAFKA_BOOTSTRAP_SERVER")
kafka_topic = os.getenv("KAFKA_TOPIC")

# Minio configuration

minio_endpoint = os.getenv("MINIO_ENDPOINT")
minio_access_key = os.getenv("MINIO_ACCESS_KEY")
minio_secret_key = os.getenv("MINIO_SECRET_KEY")
minio_bucket = os.getenv("MINIO_BUCKET")
minio_secure = os.getenv("MINIO_SECURE", "false").strip().lower() == "true"
# postgres configuration

postgres_host = os.getenv("POSTGRESQL_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")

# EMSC Websocket

emsc_websocket_url = os.getenv("EMSC_WEBSOCKET_URL")


# Application

app_env = os.getenv("APP_ENV")
log_level = os.getenv("LOG_LEVEL")