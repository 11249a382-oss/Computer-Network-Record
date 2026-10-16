Chat Server (chat_server.py):
import socket
import threading

clients = []

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"Received from {client_address}: {message}")

            for client in clients:
                if client != client_socket:
                    client.sendall(message.encode())

        except Exception as e:
            print(f"Error with {client_address}: {e}")
            break

    if client_socket in clients:
        clients.remove(client_socket)

    client_socket.close()
    print(f"{client_address} disconnected")


def chat_server():
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server_socket.bind(('localhost', 55555))
    server_socket.listen(5)

    print("Server listening on port 55555...")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )

        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    chat_server()



Chat Client (chat_client.py):
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                print("Disconnected from server.")
                break

            print(message)

        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def chat_client():
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        client_socket.connect(('localhost', 55555))
        print("Connected to chat server.")

    except Exception as e:
        print(f"Unable to connect: {e}")
        return

    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )

    receive_thread.start()

    while True:
        try:
            message = input()

            if message.lower() == "exit":
                break

            client_socket.sendall(message.encode())

        except Exception as e:
            print(f"Error sending message: {e}")
            break

    client_socket.close()


if __name__ == '__main__':
    chat_client()
