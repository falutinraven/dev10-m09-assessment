import json
from kafka import KafkaProducer


def run_producer(topic, items):
    producer = KafkaProducer(
        bootstrap_servers="localhost:29092",
        allow_auto_create_topics=True,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
    )

    for key, value in items.items():
        print(key)
        print(value)
        future = producer.send(topic, key=key, value=value)
        result = future.get(timeout=60)
        print(f"Sent: {value} with result: {result}")

    producer.flush()
    producer.close()


if __name__ == "__main__":
    items = {
        'A1': {'name': 'Nerds Gummy Clusters', 'price': 3.95, 'inventory': 10},
        'B2': {'name': 'Dove Dark Chocolate', 'price': 5.75, 'inventory': 5},
        'C3': {'name': 'Quest Protein Chips', 'price': 4.50, 'inventory': 0}
    }
    run_producer("inventory", items)
