import grpc
import email_pb2
import email_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = email_pb2_grpc.EmailServiceStub(channel)

    print("Отправка письма")
    to = input("Кому: ")
    subject = input("Тема: ")
    body = input("Текст письма: ")

    response = stub.SendEmail(
        email_pb2.EmailMessage(
            to=to,
            subject=subject,
            body=body
        )
    )

    print("Ответ сервера:", response.status)

if __name__ == '__main__':
    run()