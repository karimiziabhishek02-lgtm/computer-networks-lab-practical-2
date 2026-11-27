import socket
import threading
import time
import re

HOST, PORT = '127.0.0.1', 5300
CACHE_TTL = 60                 # Seconds a cached IP stays valid
cache = {}                     # {domain: (ip, time_saved)}
lock = threading.Lock()        # Protects cache across threads

# Validate domain format (letters, digits, hyphens; labels up to 63 chars)
DOMAIN_RE = re.compile(
    r'^(?!-)[a-z0-9-]{1,63}(?<!-)([.](?!-)[a-z0-9-]{1,63}(?<!-))*$'
)


def resolve(domain):
    now = time.time()
    with lock:
        if domain in cache and now - cache[domain][1] < CACHE_TTL:
            return cache[domain][0], 'CACHE'
    ip = socket.gethostbyname(domain)
    with lock:
        cache[domain] = (ip, now)
    return ip, 'DNS'


def handle_request(data, addr, sock):
    domain = data.decode(errors='ignore').strip().lower()
    if len(domain) > 253 or not DOMAIN_RE.match(domain):
        reply = 'ERROR|Invalid domain format'
    else:
        try:
            ip, source = resolve(domain)
            reply = f'OK|{ip}|{source}'
        except socket.gaierror:
            reply = 'ERROR|Domain not found'
    sock.sendto(reply.encode(), addr)
    print(f'[SERVER] {addr[0]}:{addr[1]} asked {domain!r} -> {reply}')


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    sock.settimeout(1.0)       # Allows clean Ctrl+C exit on Windows
    print(f'[SERVER] DNS server started on {HOST}:{PORT}')
    print('[SERVER] Waiting for queries... (Press Ctrl+C to stop)')
    try:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
            except (socket.timeout, ConnectionResetError):
                continue
            threading.Thread(
                target=handle_request, args=(data, addr, sock), daemon=True
            ).start()
    except KeyboardInterrupt:
        print('\n[SERVER] Server stopped by user.')
    finally:
        sock.close()


if __name__ == '__main__':
    main()
