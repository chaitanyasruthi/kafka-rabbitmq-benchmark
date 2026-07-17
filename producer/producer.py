import json
import time
from kafka import KafkaProducer
import pika
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("ORDER_TOPIC_NAME")

RABBIT_HOST = os.getenv("RABBITMQ_HOST")
RABBIT_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBIT_USER = os.getenv("RABBITMQ_USER")
RABBIT_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
EXCHANGE = os.getenv("ORDER_EXCHANGE_NAME")

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: str(k).encode("utf-8")
)

# RabbitMQ Connection
credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        credentials=credentials
    )
)

channel = connection.channel()

channel.exchange_declare(
    exchange=EXCHANGE,
    exchange_type="direct",
    durable=True
)

for i in range(1, 11):

    order = {
        "order_id": str(i),
        "user_id": f"user{i}",
        "product_id": f"product{i}",
        "amount": 100.50 + i,
        "timestamp": int(time.time())
    }

    # Kafka
    producer.send(
        TOPIC,
        key=order["order_id"],
        value=order
    )

    # RabbitMQ
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key="order.created",
        body=json.dumps(order)
    )

    print(f"Sent Order {i}")

producer.flush()

connection.close()

print("All Orders Sent Successfully")