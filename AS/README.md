# Authoritative Server

An Authoritative Server is a DNS server that stores and serves DNS records.

Our AS has two responsibilities:

1. Register new DNS records
2. Handle DNS queries for registered records

The AS listens for UDP messages on port `53533`. We use Python’s built-in `socket` library to process UDP messages.

Our AS stores DNS records in a local file called `records.txt`.

## Testing AS Standalone (Without US or FS)

### Build Docker image
```bash
docker build -t as-app .
```

### Run Docker container
```bash
docker run --rm -e PYTHONUNBUFFERED=1 -p 53533:53533/udp as-app
```
* `--rm` automatically deletes the container after it exits (e.g., when you press `Ctrl+C`)
* `PYTHONUNBUFFERED=1` ensures Python logs appear immediately (no buffering)

### Open a new terminal and send requests to AS

Install netcat if not already installed.
```bash
# macOS
brew install netcat
```

Test record registration
```bash
echo -e "TYPE=A\nNAME=fibonacci.com\nVALUE=172.18.0.2\nTTL=10" | nc -u -w1 localhost 53533
```

Test DNS query
```bash
echo -e "TYPE=A\nNAME=fibonacci.com" | nc -u -w1 localhost 53533
```