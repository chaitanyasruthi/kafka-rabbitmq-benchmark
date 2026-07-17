import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    group_id="inventory-cg",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Inventory Consumer Started...")

for message in consumer:
    order = message.value

    print(f"Inventory Processing: {order}")

    # Business Logic Here

    consumer.commit()