from kafka import KafkaConsumer
import json


def run_consumer(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="localhost:29092",
        auto_offset_reset="latest",
        group_id="g1",
        consumer_timeout_ms=5000,  # 5 seconds
    )

    ret = dict()
    try:
        for msg in consumer:
            serialized = {
                "key": msg.key.decode("utf-8") if msg.key else None,
                "value": msg.value.decode("utf-8") if msg.value else None,
            }
            ret[serialized["key"]] = json.loads(serialized["value"])
    except KeyboardInterrupt:
        print("Consumer interrupted. Exiting...")
    finally:
        consumer.close()

    return ret
