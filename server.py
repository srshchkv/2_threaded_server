import socket 
import threading
#Программа, написанная на семинаре выдавала ошибку при подключении нескольких клиентов,тк поток и функция для обработки подключения имели одинаковое название
#nтеперь возможна работа с несколькими клиентами одновременно
# Создаем сокет для сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(('', 9091))  
server_socket.listen(5)  

print("Эхо-сервер запущен, ожидаем подключений...")

# Функция для обработки подключения клиента в отдельном потоке
def client_threading(conn, addr):
    print(f"Новое подключение: {addr}")
    while True:
         data = conn.recv(1024)
         if not data:
             break
    # Отправляем данные обратно клиенту в верхнем регистре
         conn.send(data.decode().upper().encode())
    # Закрываем подключение при выходе из цикла
    conn.close()
    print(f"Соединение с клиентом {addr} закрыто.")

while True:
     conn, addr = server_socket.accept()
     # Создаем новый поток для обработки подключения
     client_thread = threading.Thread(target=client_threading, args=(conn, addr))
     client_thread.start()
