from socket import *
import logging

AS_HOST = "0.0.0.0"

# 0.0.0.0 is a special IP address that means "listen on all available network interfaces."
# When using Docker, we don't know the exact IP the container will get, so binding to 0.0.0.0 ensures this server can receive requests

AS_PORT = 53533
FILE_NAME = "records.txt"   # file in local directory to store DNS records

records_map = {}            # maps domain name to (value, _type, ttl)

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def load_records():
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                record = line.strip().split(',')
                name, value, _type, ttl = record
                records_map[name] = (value, _type, ttl)
        logging.info(f"Loaded {len(records_map)} records from {FILE_NAME}")
    except FileNotFoundError:
        raise Exception("Failed to open file: " + FILE_NAME)

def handle_dns_registration(msg):
    split = msg.strip().split("\n")

    _type = split[0].split("=")[1]
    name  = split[1].split("=")[1]
    value = split[2].split("=")[1]
    ttl   = split[3].split("=")[1]

    logging.info(f"Received DNS registration request: {name} → {value}, type={_type}, ttl={ttl}")
    logging.info(f"Persisting record to {FILE_NAME}")

    with open(FILE_NAME, "a") as file:
        file.write(f"{name},{value},{_type},{ttl}\n")
    
    records_map[name] = (value, _type, ttl)  # update in-memory map

    return f"STATUS=OK\nMESSAGE=Registered {name} → {value}"

def handle_dns_query(msg):
    split = msg.strip().split("\n")

    _type = split[0].split("=")[1]
    name  = split[1].split("=")[1]

    logging.info("Received DNS query request")
    logging.info(f"Querying record for: {name} (type={_type})")

    if name in records_map:
        value, _type, ttl = records_map[name]
        response = (
            f"TYPE={_type}\n"
            f"NAME={name}\n"
            f"VALUE={value}\n"
            f"TTL={ttl}\n"
            f"STATUS=OK\n"
        )
    else:
        response = f"STATUS=NOT_FOUND\nMESSAGE=No record found for {name}\n"
    
    return response

def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((AS_HOST, AS_PORT))

    logging.info(f"Authoritative Server running on UDP port {AS_PORT}")
    load_records()
    
    try:
        while True:
            logging.info("Waiting for incoming DNS request...")

            msg, addr = sock.recvfrom(1024)
            decoded = msg.decode().strip()

            logging.info(f"Request received from {addr}:\n{decoded}")

            if "VALUE" in decoded:
                response = handle_dns_registration(decoded)
            else:
                response = handle_dns_query(decoded)

            logging.info(f"Sending response to {addr}:\n{response.strip()}")
            
            sock.sendto(response.encode(), addr)

    except KeyboardInterrupt:
        logging.info("Server interrupted by user. Shutting down...")

    finally:
        sock.close()
        logging.info("Socket closed.")

if __name__ == "__main__":
    main()
