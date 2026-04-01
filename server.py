import grpc
from concurrent import futures
import email_pb2
import email_pb2_grpc

class EmailService(email_pb2_grpc.EmailServiceServicer):

    def SendEmail(self, request, context):
        print("Получено письмо:")
        print("Кому:", request.to)
        print("Тема:", request.subject)
        print("Текст:", request.body)

        return email_pb2.EmailResponse(
            status="Письмо успешно отправлено"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    email_pb2_grpc.add_EmailServiceServicer_to_server(EmailService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()