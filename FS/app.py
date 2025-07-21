from flask import Flask, request, jsonify
from socket import *
import requests

FS_HOST = "0.0.0.0"
FS_PORT = 9090

app = Flask(__name__)

def fib(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)

@app.route('/register', methods=['PUT'])
def register():
    app.logger.info("Received PUT /register request")

    data = request.json
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        app.logger.warning("Missing parameter in request body: %s", data)
        return jsonify({"error": "Missing parameter"}), 400

    app.logger.info("Preparing DNS registration message")
    app.logger.debug("hostname=%s, ip=%s, as_ip=%s, as_port=%s", hostname, ip, as_ip, as_port)

    msg = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    sock = socket(AF_INET, SOCK_DGRAM)

    try:
        sock.sendto(msg.encode(), (as_ip, int(as_port)))
        app.logger.info("Sent registration message to AS at %s:%s", as_ip, as_port)
        return "Registration Success", 201

    except Exception as e:
        app.logger.error("Failed to reach AS at %s:%s — %s", as_ip, as_port, str(e))
        return jsonify({"error": "Error reaching AS"}), 500

    finally:
        sock.close()
        app.logger.debug("Closed UDP socket")

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    app.logger.info("Received GET /fibonacci request")

    number = request.args.get('number')
    if not number:
        app.logger.warning("Missing 'number' query parameter")
        return jsonify({"error": "Missing 'number' parameter"}), 400

    try:
        n = int(number)
    except ValueError:
        app.logger.warning("Non-integer input for 'number': %s", number)
        return jsonify({"error": "'number' must be an integer"}), 400

    if n <= 0:
        app.logger.warning("Invalid 'number' provided (non-positive): %d", n)
        return jsonify({"error": "'number' must be positive"}), 400

    app.logger.info("Calculating Fibonacci number for n=%d", n)
    res = fib(n)
    app.logger.info("Fibonacci(%d) = %d", n, res)

    return jsonify({"fibonacci": res}), 200

if __name__ == '__main__':
    app.logger.info("Starting Fibonacci Server on http://%s:%d", FS_HOST, FS_PORT)
    app.run(host=FS_HOST, port=FS_PORT)
