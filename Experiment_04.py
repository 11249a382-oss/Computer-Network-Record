Echo Server (echo_server.py):
import socket

def echo_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 65432))
        server_socket.listen(5)

        print("Server listening on port 65432...")

        while True:
            connection, client_address = server_socket.accept()
            print(f"Connected by {client_address}")

            while True:
                data = connection.recv(1024)
                if not data:
                    break

                message = data.decode()
                print(f"Received: {message}")
                connection.sendall(data)

            connection.close()
            print("Client disconnected\n")

    except KeyboardInterrupt:
        print("\nServer stopped manually.")
    except Exception as e:
        print("Error:", e)
    finally:
        server_socket.close()

if __name__ == '__main__':
    echo_server()



Echo Client (echo_client.py):
import socket

def echo_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    while True:
        message = input("Enter a message: ")
        client_socket.sendall(message.encode())

        data = client_socket.recv(1024)
        print(f"Echoed from server: {data.decode()}")

        if message.lower() == 'exit':
            break

    client_socket.close()

if __name__ == '__main__':
    echo_client()
