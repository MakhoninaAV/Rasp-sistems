import pika
import grpc
import sys
import os
from datetime import datetime

# Добавляем путь к сгенерированным файлам gRPC
sys.path.append(os.path.join(os.path.dirname(__file__), '../grpc_part/generated'))
import lab13_pb2
import lab13_pb2_grpc

def call_grpc(method, data):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = lab13_pb2_grpc.TaskServiceStub(channel)
        if method == 'reset':
            response = stub.GenerateResetToken(lab13_pb2.EmailRequest(email=data))
            return response.message
        elif method == 'age':
            response = stub.CalculateAge(lab13_pb2.BirthDateRequest(birth_date=data))
            return f"Возраст: {response.age} лет"
        elif method == 'sort':
            response = stub.SortWords(lab13_pb2.WordsRequest(text=data))
            return f"Отсортировано: {response.sorted_text}"
        else:
            return f"Неизвестный метод: {method}"

def callback(ch, method, properties, body):
    message = body.decode()
    print(f"Получено сообщение: {message}")
    
    if ':' not in message:
        print("Неверный формат сообщения")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    
    cmd, data = message.split(':', 1)
    
    print(f"Вызываю gRPC метод: {cmd} с данными: {data}")
    result = call_grpc(cmd, data)
    print(f"Результат: {result}")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Подключение к RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print("Consumer запущен, жду сообщений...")
channel.start_consuming()