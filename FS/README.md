# Fibonacci Server

The Fibonacci Server (FS) acts as a backend service in our demonstration. It serves two main purposes:

1. Register its own DNS record with the Authoritative Server (AS)
2. Respond to user requests for Fibonacci numbers

### 1. Registering with the AS

FS exposes a `PUT` endpoint at `/register`, which accepts requests to register its own DNS record with the AS.

**Request Format:**
```json
{
  "hostname": "fibonacci.com",
  "ip": "172.18.0.2",          // IP address of FS
  "as_ip": "10.9.10.2",        // IP address of AS
  "as_port": "30001"           // Port number of AS
}
```

Based on the provided input, FS constructs the following message and sends it to the AS over UDP:
```
TYPE=A
NAME=fibonacci.com
VALUE=172.18.0.2
TTL=10
```

If registration succeeds, FS responds with HTTP status code `201`.

> **Note:** In a real-world system, exposing a public `/register` endpoint for DNS registration would be a security risk. In this assignment, it exists to simplify testing and give you control over when and how FS registers with AS.

### 2. Responding to Fibonacci Requests

FS provides a `GET` endpoint at `/fibonacci`, which accepts a query parameter `number` and returns the corresponding Fibonacci value.

**Example:**
```
GET /fibonacci?number=5
```

**Response:**
```json
{
  "fibonacci": 3
}
```

If the `number` is missing, non-integer, or non-positive, FS will return an appropriate `400 Bad Request` error with a message.

---

## Testing FS (+AS)

1. Run the AS container
```bash
docker build -t as-app .
docker run --rm -p 53533:53533/udp as-app
```

2. Run the FS container
```bash
docker build -t fs-app .
docker run --rm -p 9090:9090 fs-app
```

3. Open a new terminal window and send requests to FS

* Test DNS Registration
```bash
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"hostname":"fibonacci.com","ip":"172.18.0.2","as_ip":"host.docker.internal","as_port":"53533"}' \
  http://localhost:9090/register
```

* `host.docker.internal` is a special DNS name that allows a Docker container to communicate with the host machine. It’s useful when a container needs to access a service running on the host. In this assignment, since the AS container is bound to `localhost:53533`, FS can use `host.docker.internal:53533` to send registration requests to it.


* Test Fibonacci Result
```bash
curl "http://localhost:9090/fibonacci?number=7"
```