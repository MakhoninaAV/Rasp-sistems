import grpc
from concurrent import futures
import sys
import os
from datetime import datetime

# Добавляем путь к сгенерированным файлам
sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))

import lab13_pb2
import lab13_pb2_grpc

class TaskServiceServicer(lab13_pb2_grpc.TaskServiceServicer):
    
    # Задание 1: Генерация токена сброса пароля
    def GenerateResetToken(self, request, context):
        email = request.email
        # Имитируем токен
        token = f"reset_token_{email.replace('@', '_at_')}"
        result = f"Ссылка для сброса отправлена на {email}. Токен: {token}"
        return lab13_pb2.TokenResponse(message=result)
    
    # Задание 2: Расчет возраста
    def CalculateAge(self, request, context):
        birth_date_str = request.birth_date
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth_date.year
            # Если день рождения еще не был в этом году
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
            return lab13_pb2.AgeResponse(age=age)
        except:
            return lab13_pb2.AgeResponse(age=-1)  # ошибка
    
    # Задание 3: Сортировка слов
    def SortWords(self, request, context):
        text = request.text
        words = text.split()
        words.sort()
        sorted_text = " ".join(words)
        return lab13_pb2.WordsResponse(sorted_text=sorted_text)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab13_pb2_grpc.add_TaskServiceServicer_to_server(TaskServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC сервер запущен на порту 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()