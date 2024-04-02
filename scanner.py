import socket
import threading
from queue import Queue
from tqdm import tqdm

# Функция для сканирования порта
def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    try:
        sock.connect((host, port))
        open_ports.put(port)
    except:
        pass
    finally:
        sock.close()

# Функция для параллельного сканирования портов
def scan_ports(host, start_port, end_port, num_threads):
    threads = []
    open_ports.queue.clear()
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(host, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return list(open_ports.queue)

# Функция для вывода открытых портов
def print_open_ports(open_ports):
    if not open_ports:
        print("Открытые порты не найдены.")
    else:
        print("Открытые порты:")
        for port in sorted(open_ports):
            print(f"Порт {port} открыт")

#
# Получаем хост/IP-адрес от пользователя
host = input("Введите имя хоста или IP-адрес: ")

# Получаем диапазон портов от пользователя
start_port = int(input("Введите начальный порт: "))
end_port = int(input("Введите конечный порт: "))
num_threads = int(input("Введите количество потоков: "))

open_ports = Queue()

# Сканируем порты и выводим прогресс
print("Сканирование портов...")
total_ports = end_port - start_port + 1
with tqdm(total=total_ports, unit="port") as pbar:
    open_ports_list = scan_ports(host, start_port, end_port, num_threads)
    pbar.update(total_ports)

# Выводим открытые порты
print_open_ports(open_ports_list)

'''
 Функция для обработки подключения клиента в отдельном потоке
def client_threading(conn, addr):
    print(f"Новое подключение: {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.send(data.upper())
    conn.close()
    print(f"Соединение с клиентом {addr} закрыто.")
# Функция для запуска эхо-сервера
def start_echo_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 9091))
    server_socket.listen(5)
    print("Эхо-сервер запущен, ожидаем подключений...")
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=client_threading, args=(conn, addr))
        client_thread.start()
start_echo_server()
