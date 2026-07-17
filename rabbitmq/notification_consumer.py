import json
import pika

credentials = pika.PlainCredentials("guest", "guest")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=credentials
    )
)

channel = connection.channel()

channel.queue_declare(
    queue="notification-q",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "dlx-exchange"
    }
)

print("Notification Consumer Started...")

def callback(ch, method, properties, body):
    order = json.loads(body)
    print("Notification Sent:", order)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue="notification-q",
    on_message_callback=callback
)

channel.start_consuming()