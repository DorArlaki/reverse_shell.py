import socket
import logging

logging.basicConfig(level=logging.DEBUG)

def run_client():
    try:
        ip_address = input("Enter the server's IP address: ")
        port = int(input("Enter the server's port number: "))
        s = socket.socket()
        s.connect((ip_address, port))
        while True:
            print("CMD> ", end = "")
            command = input()
            if "exit" in command.lower():
                s.send("exit".encode())
                logging.debug("Received exit command from client. Closing connection.")
                s.close()
                break
            else:
                logging.debug(f"Received command from client: {command}")
                s.send(command.encode())
                data = s.recv(2048).decode()
                print(data)
    except socket.error as e:
        logging.error(f"Error occurred while running client: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    run_client()
