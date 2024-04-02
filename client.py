import socket
#Создаем сокет для клиента
client_socket = socket.socket()
client_socket.connect(('localhost', 9091)) 

while True:
# Получаем сообщение от пользователя
     message = input("Введите сообщение ('quit'): ")
     if message.lower() == 'quit':
         break
# Отправляем сообщение серверу
     client_socket.send(message.encode())
# Получаем ответ от сервера
     response = client_socket.recv(1024)
     print(f"Ответ сервера: {response.decode()}")

#Закрываем соединение с сервером
client_socket.close()
