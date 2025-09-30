import socket, sys

HOST, PORT = "localhost", 9999

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        def recv_line():
            data = b""
            while True:
                bch = client.recv(1)
                if not bch:
                    break
                if bch == b"\n":
                    break
                data += bch
            return data.decode().strip()

        def send_line(s):
            client.sendall((s + "\n").encode())

        prompt = recv_line()
        send_line(input(prompt + " ").strip())
        prompt = recv_line()
        send_line(input(prompt + " ").strip())
        print(recv_line())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
