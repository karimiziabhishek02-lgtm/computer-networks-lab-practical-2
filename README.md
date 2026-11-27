# DNS-Based Client-Server Application Using UDP Sockets

A simple DNS resolver built in Python using UDP socket communication. The client sends a domain name to the server, and the server validates it, checks a local cache, resolves it to an IPv4 address if needed, and sends the result back.

This project was developed as part of the Computer Networks (CN) practical work.

## Features

- **UDP communication** using Python's built-in `socket` module (`SOCK_DGRAM`)
- **Domain validation** with a regular expression (letters, digits and hyphens, labels up to 63 characters, total length up to 253)
- **Local cache** with a 60-second TTL, so repeated queries are answered faster
- **IPv4 resolution** of uncached domains through the system DNS resolver
- **Multi-threaded server**, where each query is handled in its own thread
- **Thread-safe cache** protected with a lock
- **Error handling** for invalid formats, unknown domains and an unreachable server
- **Response time display** on the client in milliseconds

## Tech Stack

| Item | Details |
|---|---|
| Language | Python 3 |
| Protocol | UDP |
| Libraries | `socket`, `threading`, `time`, `re` (all built in) |

No external packages are required.

## Project Structure

```
.
├── server.py    # UDP DNS server (validation, cache, resolution)
├── client.py    # Interactive command-line client
└── README.md
```

## How It Works

1. The client reads a domain name from the user and sends it to the server over UDP.
2. The server cleans the input (trims whitespace, converts to lowercase) and validates the format.
3. If the format is invalid, the server replies with an error.
4. If the domain is in the cache and younger than 60 seconds, the server returns the cached IP.
5. Otherwise, the server resolves the domain with `socket.gethostbyname()`, stores the result in the cache and returns it.
6. The client displays the IP address, the source (DNS lookup or local cache) and the response time.

### Message Format

| Direction | Format | Example |
|---|---|---|
| Client → Server | Plain domain name | `google.com` |
| Server → Client (success) | `OK\|<ip>\|<source>` | `OK\|142.250.77.110\|DNS` |
| Server → Client (error) | `ERROR\|<message>` | `ERROR\|Domain not found` |

`<source>` is either `DNS` (fresh lookup) or `CACHE` (served from the local cache).

## Getting Started

### Prerequisites

- Python 3 installed (check with `python --version`)
- An internet connection (needed to resolve real domains)

### Run the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. Open **two terminals** in the project folder.

3. Start the server in **Terminal 1**:
   ```bash
   python server.py
   ```

4. Start the client in **Terminal 2**:
   ```bash
   python client.py
   ```

5. Enter domain names at the prompt. Type `exit` to close the client, and press `Ctrl + C` in the server terminal to stop the server.

> The server listens on `127.0.0.1:5300`. If this port is already in use, change `PORT` in `server.py` and `SERVER` in `client.py`.

## Test Cases

| Input | Expected Result |
|---|---|
| `google.com` | IP address, source: DNS lookup |
| `google.com` (again within 60 seconds) | Same IP, source: local cache, faster response |
| `thisdomaindoesnotexist123.com` | `Error : Domain not found` |
| `goo gle..com` | `Error : Invalid domain format` |

## Sample Output

**Client**

```
DNS Client (type exit to quit)
Enter domain name (or exit): google.com
Resolved IP   : 142.250.77.110
Source        : DNS lookup
Response time : 141 ms

Enter domain name (or exit): google.com
Resolved IP   : 142.250.77.110
Source        : local cache
Response time : 2 ms

Enter domain name (or exit): thisdomaindoesnotexist123.com
Error : Domain not found

Enter domain name (or exit): goo gle..com
Error : Invalid domain format

Enter domain name (or exit): exit
Client closed.
```

**Server**

```
[SERVER] DNS server started on 127.0.0.1:5300
[SERVER] Waiting for queries... (Press Ctrl+C to stop)
[SERVER] 127.0.0.1:62568 asked 'google.com' -> OK|142.250.77.110|DNS
[SERVER] 127.0.0.1:57760 asked 'google.com' -> OK|142.250.77.110|CACHE
[SERVER] 127.0.0.1:63853 asked 'thisdomaindoesnotexist123.com' -> ERROR|Domain not found
[SERVER] 127.0.0.1:64711 asked 'goo gle..com' -> ERROR|Invalid domain format
```

IP addresses, port numbers and response times will vary depending on your network and DNS resolver.

## Limitations

- Resolves **IPv4 only** (`gethostbyname`)
- The cache is **in memory** and is cleared when the server stops
- Runs on **localhost** by default and is intended for learning, not production use

## Result

The DNS-based client-server application was developed successfully using Python UDP socket communication. The client sends domain name queries to the server, which validates the format, checks its 60-second local cache, resolves uncached domains to IPv4 addresses concurrently using threads, and returns the results or error messages to the client.
