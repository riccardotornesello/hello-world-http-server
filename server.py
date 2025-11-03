import os
import socket
import time
import threading
import uuid
from datetime import datetime, timezone
from flask import Flask, request

app = Flask(__name__)

# Thread-safe request counter
request_counter_lock = threading.Lock()
request_counter = 0


def get_server_ip():
    """Get the server's local IP address"""
    try:
        # Create a socket to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        # Fallback to hostname resolution
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "unknown"


def get_mac_address():
    """Get the server's MAC address"""
    try:
        mac = uuid.getnode()
        mac_str = ":".join(["{:02x}".format((mac >> elements) & 0xFF) for elements in range(0, 2 * 6, 2)][::-1])
        return mac_str
    except Exception:
        return "unknown"


def log_request_info(request_obj, url):
    """Log detailed request information to console"""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    source_ip = request_obj.headers.get("X-Forwarded-For", request_obj.remote_addr)
    destination_ip = get_server_ip()
    source_ethernet = "N/A"  # Not available at HTTP layer
    destination_ethernet = get_mac_address()

    print(
        f"[REQUEST LOG] Timestamp: {timestamp} | "
        f"Source IP: {source_ip} | "
        f"Destination IP: {destination_ip} | "
        f"Source Ethernet: {source_ethernet} | "
        f"Destination Ethernet: {destination_ethernet} | "
        f"URL: {url}"
    )


@app.route("/health")
def health_check():
    """Health check endpoint for monitoring"""
    # Log request information to console
    log_request_info(request, "/health")
    return "OK\n", 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
def catch_all(path):
    global request_counter

    # Thread-safe increment of request counter
    with request_counter_lock:
        request_counter += 1
        current_count = request_counter

    # Construct full URL
    requested_path = f"/{path}" if path else "/"
    if request.query_string:
        full_url = f"{requested_path}?{request.query_string.decode('utf-8')}"
    else:
        full_url = requested_path

    # Log request information to console
    log_request_info(request, full_url)

    identifier = os.environ.get("IDENTIFIER")

    # Parse delay with error handling
    # Query parameter takes precedence over environment variable
    delay_param = request.args.get("delay")
    if delay_param is not None:
        try:
            delay = int(delay_param)
        except ValueError:
            delay = 0
    else:
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
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    output += f"Client IP: {client_ip}\n"

    # User-Agent
    user_agent = request.headers.get("User-Agent", "Unknown")
    output += f"User-Agent: {user_agent}\n"

    # Hostname
    hostname = socket.gethostname()
    output += f"Hostname: {hostname}\n"

    # Identifier (optional)
    if identifier:
        output += f"Identifier: {identifier}\n"

    # Request counter
    output += f"Request Count: {current_count}\n"

    # Note: We return Content-Type as text/plain, which prevents XSS attacks
    # as browsers will not interpret the content as HTML. User-provided values
    # (path, query params) are safely displayed as plain text.
    return output, 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
