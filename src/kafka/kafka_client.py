from kafka.admin import KafkaAdminClient,NewTopic
from kafka import KafkaProducer
import json

class KafkaClientService:
    def __init__(self,bootstrap_server):
        self.bootstrap_server = bootstrap_server
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_server,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        
    def create_topic(self,topic):
        admin = KafkaAdminClient(
            bootstrap_servers=self.bootstrap_server,
            client_id="earthquake_admin"
        )

        topic = NewTopic(
            name=topic,
            replication_factor=1,
            num_partitions=1
        )

        try:
            admin.create_topics(new_topics=[topic])
            print(f"Topic {topic} Create Successfully")
        except Exception as e:
            print(f"Topic may already exist: {e}")
        finally:
            admin.close()

    def send_message(self,topic_name,data):
        self.producer.send(topic=topic_name,
                           value=data)
        self.producer.flush()
        print(f"Message send to : {topic_name}")