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

# Dead Letter Exchange
channel.exchange_declare(
    exchange="dlx-exchange",
    exchange_type="fanout",
    durable=True
)

# Failed Queue
channel.queue_declare(
    queue="failed-orders-q",
    durable=True
)

channel.queue_bind(
    exchange="dlx-exchange",
    queue="failed-orders-q"
)

print("Dead Letter Queue Created Successfully")

connection.close()