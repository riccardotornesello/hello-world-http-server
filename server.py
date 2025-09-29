from flask import Flask, request
import os

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    identifier = os.environ.get("IDENTIFIER")

    lines = ["Hello World!"]

    requested_path = f"/{path}" if path else "/"
    lines.append(f"Path: {requested_path}")

    if identifier:
        lines.append(f"Identifier: {identifier}")

    return "\n".join(lines), 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
