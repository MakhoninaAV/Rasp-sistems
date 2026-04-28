import pika
import sys

# Для локального RabbitMQ используем guest/guest
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

if len(sys.argv) < 2:
    print("Использование: python3 producer.py <команда:данные>")
    print("Примеры:")
    print("  python3 producer.py reset:user@example.com")
    print("  python3 producer.py age:2000-01-01")
    print("  python3 producer.py sort:яблоко банан апельсин")
    sys.exit(1)

message = sys.argv[1]

channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)
)

print(f"Отправлено: {message}")
connection.close()