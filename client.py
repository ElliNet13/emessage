import socket

# Define constants for packet type
MESSAGE_PACKET = 0

# Function to send a message packet
def send_message(sock, username, message):
    # Create packet data
    packet_data = f"{username}:{message}"

    # Calculate packet length
    packet_length = len(packet_data)

    # Create header (packet type and packet length)
    header = bytes([MESSAGE_PACKET]) + packet_length.to_bytes(2, byteorder='big')

    # Send packet (header + data)
    sock.sendall(header + packet_data.encode())

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

# Usage example
def main():
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to server
        s.connect(('localhost', 12345))

        # Send a message
        send_message(s, 'user1', 'Hello, world!')

        # Receive a message
        username, message = receive_message(s)
        print(f"Received message from {username}: {message}")

if __name__ == "__main__":
    main()