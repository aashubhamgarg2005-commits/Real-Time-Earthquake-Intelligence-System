from .ingestion.api_client import EarthquakeWebSocketClient
from .kafka.kafka_client import KafkaClientService
from .config.config import (kafka_bootstrap_server,
                           kafka_topic,
                           emsc_websocket_url)

def main():
    # create kafka client object
        kafka = KafkaClientService(bootstrap_server=kafka_bootstrap_server)
        # create topic if not exists 
        kafka.create_topic(topic=kafka_topic)
        # fetch earthquake strem data
        client = EarthquakeWebSocketClient(emsc_websocket_url=emsc_websocket_url)
        for earthquake in client.stream():
            earthquake_data = earthquake
            # send message to kafka
            kafka.send_message(topic_name=kafka_topic,
                           data=earthquake_data)

if __name__ == "__main__":
      main()