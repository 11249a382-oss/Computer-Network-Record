Server (file_transfer_server.py):
import socket

def file_transfer_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 12345))
        server_socket.listen(1)

        print("Server listening on port 12345...")

        connection, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        filename = connection.recv(1024).decode()
        print(f"Receiving file: {filename}")

        with open(f"received_{filename}", 'wb') as file:
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                file.write(data)

        print(f"File saved as received_{filename}")
        connection.close()

    except Exception as e:
        print("Error:", e)

    finally:
        server_socket.close()


if __name__ == '__main__':
    file_transfer_server()



Client (file_transfer_client.py):
import socket
import os

def file_transfer_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 12345))

        filename = input("Enter the filename to send: ")

        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            client_socket.close()
            return

        client_socket.sendall(filename.encode())

        with open(filename, 'rb') as file:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                client_socket.sendall(chunk)

        print(f"File '{filename}' sent successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()


if __name__ == '__main__':
    file_transfer_client()
