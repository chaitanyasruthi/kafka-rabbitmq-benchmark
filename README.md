# Kafka vs RabbitMQ Order Processing Benchmark

## Project Overview

This project implements a dual messaging system using Apache Kafka and RabbitMQ for processing customer orders. The same order is published to both Kafka and RabbitMQ so that their processing mechanisms can be compared.

The project demonstrates:

- Apache Kafka Producer and Consumers
- RabbitMQ Producer and Consumers
- Dead Letter Queue (DLQ)
- Message Routing
- Fault Handling
- Benchmark Comparison

---

# Architecture

Producer
   │
   ├────────────► Kafka Topic (orders)
   │                  │
   │                  ├── Inventory Consumer
   │                  ├── Notification Consumer
   │                  └── Analytics Consumer
   │
   └────────────► RabbitMQ Exchange (order-exchange)
                      │
                      ├── inventory-q
                      ├── notification-q
                      └── analytics-q
                               │
                               ▼
                        failed-orders-q (DLQ)

---

# Technologies Used

- Python 3.x
- Apache Kafka
- RabbitMQ
- Docker
- Docker Compose
- kafka-python
- pika
- python-dotenv

---

# Project Structure

```
kafka-rabbitmq-benchmark/
│
├── kafka/
│   ├── inventory_consumer.py
│   ├── notification_consumer.py
│   └── analytics_consumer.py
│
├── rabbitmq/
│   ├── inventory_consumer.py
│   ├── notification_consumer.py
│   ├── analytics_consumer.py
│   ├── setup_rabbitmq.py
│   └── setup_dlx.py
│
├── producer/
│   └── producer.py
│
├── docker-compose.yml
├── .env
├── .env.example
└── README.md
```

---

# Setup Instructions

## Clone Project

```bash
git clone <repository-url>
cd kafka-rabbitmq-benchmark
```

## Create Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate
```

## Install Dependencies

```bash
pip install kafka-python pika python-dotenv
```

## Start Docker

```bash
docker compose up -d
```

## Create Kafka Topic

```bash
docker exec -it kafka bash

kafka-topics --create \
--topic orders \
--bootstrap-server localhost:9092 \
--partitions 3 \
--replication-factor 1
```

## Create RabbitMQ Queues

```bash
python rabbitmq/setup_dlx.py

python rabbitmq/setup_rabbitmq.py
```

---

# Running the Project

Start Kafka Consumers

```bash
python kafka/inventory_consumer.py

python kafka/notification_consumer.py

python kafka/analytics_consumer.py
```

Start RabbitMQ Consumers

```bash
python rabbitmq/inventory_consumer.py

python rabbitmq/notification_consumer.py

python rabbitmq/analytics_consumer.py
```

Run Producer

```bash
python producer/producer.py
```

---

# Dead Letter Queue (DLQ)

The Inventory Consumer intentionally rejects Order 5 using:

```python
ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```

RabbitMQ routes the failed message to:

```
failed-orders-q
```

This verifies successful Dead Letter Queue implementation.

---

# Benchmark Results

| Metric | Result |
|---------|---------|
| Total Orders Sent | 10 |
| Kafka Consumers | 3 |
| RabbitMQ Consumers | 3 |
| Kafka Topic | orders |
| RabbitMQ Exchange | order-exchange |
| RabbitMQ Queues | 3 |
| Dead Letter Queue | failed-orders-q |
| Failed Orders Routed to DLQ | Yes |
| Docker Containers | Kafka, ZooKeeper, RabbitMQ |
| Producer Status | Success |
| Consumer Status | Success |

---

# Test Results

✔ Successfully published orders to Kafka

✔ Successfully published orders to RabbitMQ

✔ Kafka consumers processed all messages.

✔ RabbitMQ consumers processed all messages.

✔ Dead Letter Queue received failed messages.

✔ Docker containers executed successfully.

---

# Screenshots

Add screenshots here:

- Docker Containers
- Kafka Consumers
- RabbitMQ Consumers
- RabbitMQ Queues
- Dead Letter Queue
- Producer Output

---

# Conclusion

This project successfully demonstrates the implementation and comparison of Apache Kafka and RabbitMQ for distributed message processing. It also validates message routing, multiple consumers, and Dead Letter Queue (DLQ) handling using RabbitMQ.