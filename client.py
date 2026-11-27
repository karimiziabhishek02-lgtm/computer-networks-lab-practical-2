import socket
import time

SERVER = ('127.0.0.1', 5300)


def query(domain):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(3)        # Wait at most 3 seconds for a reply
        start = time.time()
        s.sendto(domain.encode(), SERVER)
        data, _ = s.recvfrom(1024)
        ms = (time.time() - start) * 1000
        return data.decode(), ms


def main():
    print('DNS Client (type exit to quit)')
    while True:
        domain = input('Enter domain name (or exit): ').strip()
        if domain.lower() == 'exit':
            break
        if not domain:
            continue
        try:
            reply, ms = query(domain)
        except (socket.timeout, ConnectionResetError):
            print('Error : Could not reach server (is it running?)\n')
            continue
        parts = reply.split('|')
        if parts[0] == 'OK':
            src = 'local cache' if parts[2] == 'CACHE' else 'DNS lookup'
            print(f'Resolved IP   : {parts[1]}')
            print(f'Source        : {src}')
            print(f'Response time : {ms:.0f} ms')
        else:
            print(f'Error : {parts[1]}')
        print()
    print('Client closed.')


if __name__ == '__main__':
    main()
