from kafka import KafkaProducer


def create_kafka_producer(bootstrap_servers) -> KafkaProducer:
    return KafkaProducer(bootstrap_servers=bootstrap_servers, api_version=(0, 10))
