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

# Main Exchange
channel.exchange_declare(
    exchange="order-exchange",
    exchange_type="direct",
    durable=True
)

# Queues
queues = [
    "inventory-q",
    "notification-q",
    "analytics-q"
]

for q in queues:
    channel.queue_declare(
    queue=q,
    durable=True,
    arguments={
        "x-dead-letter-exchange": "dlx-exchange"
    }
)

    channel.queue_bind(
        exchange="order-exchange",
        queue=q,
        routing_key="order.created"
    )

print("RabbitMQ Exchange and Queues Created Successfully")

connection.close()