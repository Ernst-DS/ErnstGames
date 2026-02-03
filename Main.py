import pygame
import socket
import threading
import json

# Stratego, Pente, Catan

pygame.init()
CANVAS = pygame.display.set_mode((1000,1000))
pygame.display.set_caption("Ernst Games")
running = True

while running:
    CANVAS.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

class Connection:
    def __init__(self, sock):
        self.sock = sock
        self.running = True
        self.on_message = None
        self.listener_thread = threading.Thread(target=self._listen, daemon=True)
        self.listener_thread.start()
    def send(self, data: dict):
        try:
            msg = json.dumps(data).encode("utf-8")
            length = len(msg).to_bytes(4, "big")
            self.sock.sendall(length + msg)
        except:
            self.close()
    def _listen(self):
        try:
            while self.running:
                length_bytes = self.sock.recv(4)
                if not length_bytes:
                    break

                length = int.from_bytes(length_bytes, "big")
                data = self.sock.recv(length)

                message = json.loads(data.decode("utf-8"))

                if self.on_message:
                    self.on_message(message)
        except:
            pass
        finally:
            self.close()
    def close(self):
        self.running = False
        self.sock.close()


def host(port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(1)
    print("Waiting for player...")
    client_socket, addr = server.accept()
    print(f"Player connected from {addr}")
    return Connection(client_socket)

def connect(ip, port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print("Connected to host")
    return Connection(sock)
