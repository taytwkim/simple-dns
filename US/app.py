from flask import Flask, request, jsonify
from socket import *
import requests
import logging

US_HOST = "0.0.0.0"
US_PORT = 8080

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    app.logger.info("Received GET /fibonacci request")

    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        app.logger.warning("Missing one or more query parameters: hostname, fs_port, number, as_ip, as_port")
        return jsonify({"error": "Missing parameter"}), 400

    app.logger.info("Resolving hostname '%s' via AS at %s:%s", hostname, as_ip, as_port)

    query_msg = f"TYPE=A\nNAME={hostname}\n"
    sock = socket(AF_INET, SOCK_DGRAM)

    try:
        sock.sendto(query_msg.encode(), (as_ip, int(as_port)))
        as_response, _ = sock.recvfrom(1024)
    except Exception as e:
        app.logger.error("Error contacting AS: %s", str(e))
        return jsonify({"error": "Error reaching AS"}), 500
    finally:
        sock.close()
        app.logger.debug("Closed UDP socket after contacting AS")

    decoded = as_response.decode().strip().split("\n")
    if len(decoded) < 3 or not any(line.startswith("VALUE=") for line in decoded):
        app.logger.error("Invalid response from AS: %s", as_response.decode())
        return jsonify({"error": "Failed to resolve hostname via AS"}), 500

    ip = next((line.split('=')[1] for line in decoded if line.startswith("VALUE=")), None)
    app.logger.info("Hostname '%s' resolved to IP %s", hostname, ip)

    try:
        url = f"http://{ip}:{fs_port}/fibonacci?number={number}"
        app.logger.info("Forwarding request to FS at %s", url)
        fs_response = requests.get(url)
        return fs_response.text, fs_response.status_code
    except requests.exceptions.RequestException as e:
        app.logger.error("Error reaching FS at %s: %s", ip, str(e))
        return jsonify({"error": "Error reaching FS"}), 500

if __name__ == '__main__':
    app.logger.info("Starting User Server on http://%s:%d", US_HOST, US_PORT)
    app.run(host=US_HOST, port=US_PORT)
