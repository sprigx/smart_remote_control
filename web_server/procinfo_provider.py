import socket
import psutil
import pickle
import netifaces

PORT = 50000
SERVER_IP_ADDR = '127.0.0.1'
TARGET = 'python'

ip_addr = socket.gethostbyname(socket.gethostname())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP_ADDR, PORT))
    s.listen()
    while True:
        (connection, addr) = s.accept()
        try:
            procs = [
                proc
                .as_dict(['username', 'pid', 'create_time',
                          'cpu_percent', 'memory_percent', 'status'])
                for proc in psutil.process_iter()
                if TARGET in proc.exe()
            ]
            data = {
                "total_cpu_percent": psutil.cpu_percent(),
                "total_memory_percent": psutil.virtual_memory().percent,
                "process_info": procs
            }
            connection.send(pickle.dumps(data))
        finally:
            connection.close()
