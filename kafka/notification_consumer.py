import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    group_id="notification-cg",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Notification Consumer Started...")

for message in consumer:
    order = message.value

    print(f"Notification Sent: {order}")

    consumer.commit()