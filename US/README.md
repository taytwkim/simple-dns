# User Server

The User Server (US) is responsible for client-side logic. In a real-world system, this logic would typically reside in a browser or client application. However, for the purpose of this assignment, US simulates the client behavior and allows us to explicitly control how the client interacts with the DNS system.

The US exposes a single HTTP GET endpoint at `/fibonacci`, which takes several query parameters—`hostname`, `fs_port`, `number`, `as_ip`, and `as_port`. 

It first queries the Authoritative Server (AS) to resolve the given hostname into an IP address. 

Once resolved, it forwards the Fibonacci request to the Fibonacci Server (FS) using the resolved IP. The response from FS is then returned to the user.

## Testing US (+ AS and FS)

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

3. Register FS to AS
```bash
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"hostname":"fibonacci.com","ip":"host.docker.internal","as_ip":"host.docker.internal","as_port":"53533"}' \
  http://localhost:9090/register
```

4. Run the US container
```bash
docker build -t us-app .
docker run --rm -p 8080:8080 us-app
```

5. Send request to US
```bash
curl "http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=7&as_ip=host.docker.internal&as_port=53533"
```

* `host.docker.internal` is a special DNS name that allows Docker containers to access services running on the host machine. It's used here so that the FS and US containers can communicate with AS running on the host. When using `docker-compose`, this is no longer necessary since all services run in the same Docker network and can refer to each other by container name.