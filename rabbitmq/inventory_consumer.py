import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="inventory-q",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "dlx-exchange"
    }
)

print("Inventory Consumer Started...")

def callback(ch, method, properties, body):
    order = json.loads(body)

    # Simulate failure for Order 5
    if order["order_id"] == "5":
     print("Simulating failure for Order 5")
    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    return
        

    print(f"Inventory Received: {order}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue="inventory-q",
    on_message_callback=callback
)

channel.start_consuming()