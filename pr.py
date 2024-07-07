import socket
import threading

class ProxyServer:
    def __init__(self, port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", port))
        self.server_socket.listen(5)

    def handle_request(self, client_socket, client_address):
        request = client_socket.recv(1024)
        if not request:
            client_socket.close()
            return

        # Parse the request
        headers = request.decode().split("\r\n")
        method, url, protocol = headers[0].split()
        url_components = url.split("//")[-1].split("/")
        host = url_components[0]
        port = 80
        if ":" in host:
            host, port = host.split(":")
            port = int(port)

        # Create a socket to the target server
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((host, port))

        # Send the request to the target server
        target_socket.sendall(request)

        # Receive the response from the target server
        response = b""
        while True:
            data = target_socket.recv(1024)
            if not data:
                break
            response += data

        # Send the response back to the client
        client_socket.sendall(response)

        # Close the sockets
        target_socket.close()
        client_socket.close()

    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_request, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    proxy_server = ProxyServer(9097)
    print("Proxy server started on port 9097")
    proxy_server.run()