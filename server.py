import os
import socket
import time
import threading
from datetime import datetime, timezone
from flask import Flask, request

app = Flask(__name__)

# Thread-safe request counter
request_counter_lock = threading.Lock()
request_counter = 0


@app.route("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return "OK\n", 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
def catch_all(path):
    global request_counter
    
    # Thread-safe increment of request counter
    with request_counter_lock:
        request_counter += 1
        current_count = request_counter
    
    identifier = os.environ.get("IDENTIFIER")
    
    # Parse delay with error handling
    try:
        delay = int(os.environ.get("DELAY", 0))
    except ValueError:
        delay = 0
    
    # Simulate delay if configured
    if delay > 0:
        time.sleep(delay)

    output = "Hello World!\n"

    # Request method
    output += f"Method: {request.method}\n"
    
    # Requested path
    requested_path = f"/{path}" if path else "/"
    output += f"Path: {requested_path}\n"
    
    # Query parameters
    if request.query_string:
        output += f"Query: {request.query_string.decode('utf-8')}\n"
    
    # Timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    output += f"Timestamp: {timestamp}\n"
    
    # Client IP
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    output += f"Client IP: {client_ip}\n"
    
    # User-Agent
    user_agent = request.headers.get('User-Agent', 'Unknown')
    output += f"User-Agent: {user_agent}\n"

    # Hostname
    hostname = socket.gethostname()
    output += f"Hostname: {hostname}\n"

    # Identifier (optional)
    if identifier:
        output += f"Identifier: {identifier}\n"
    
    # Request counter
    output += f"Request Count: {current_count}\n"

    return output, 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
