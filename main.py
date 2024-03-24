import socket
import threading

# Define constants for packet type
MESSAGE_PACKET = 0

# Specify the port number
PORT = 12345

# Function to handle client connections
def handle_client(client_socket, clients, addresses):
    # Receive messages from the client and broadcast them
    while True:
        try:
            # Receive a message packet
            username, message = receive_message(client_socket)

            # Broadcast the message to all clients
            broadcast_message(username, message, clients)

        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove client from the list if found
    try:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        client_socket.close()
        print(f"Connection with {addresses[index]} closed.")
    except ValueError:
        pass  # Do nothing if client is not found in the list

# Function to receive a message packet
def receive_message(sock):
    # Receive header (packet type and packet length)
    header = sock.recv(3)

    # Extract packet type and packet length from header
    packet_type = header[0]
    packet_length = int.from_bytes(header[1:], byteorder='big')

    # Receive data payload
    data = sock.recv(packet_length).decode()

    # Extract username and message from data
    username, message = data.split(':', 1)

    return username, message

# Function to broadcast a message to all clients
def broadcast_message(username, message, clients):
    # Create packet data
    packet_data = f"{username}:{message}"

    # Calculate packet length
    packet_length = len(packet_data)

    # Create header (packet type and packet length)
    header = bytes([MESSAGE_PACKET]) + packet_length.to_bytes(2, byteorder='big')

    # Send packet (header + data) to all clients
    for client in clients:
        try:
            client.sendall(header + packet_data.encode())
        except:
            # If sending fails, remove the client
            clients.remove(client)

# Main function to start the server
def main():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind(('localhost', PORT))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server is listening for connections on port {PORT}...")

    # Lists to keep track of clients and their addresses
    clients = []
    addresses = []

    # Accept incoming connections and handle them in separate threads
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        clients.append(client_socket)
        addresses.append(client_address)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients, addresses))
        client_thread.start()

if __name__ == "__main__":
    main()