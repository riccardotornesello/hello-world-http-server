# hello-world-http-server

A simple Python HTTP server running in a Docker container. It responds to GET requests with:

- **First line:** `Hello World!`
- **Second line:** `Path: ...` (the path requested)
- **Third line**: `Hostname: ...`
- **Fourth line:** `Identifier: ...` (the value of the `IDENTIFIER` environment variable, if set)

The app listens on **port 80** by default (configurable via `PORT` environment variable).

## 🐳 Docker Image

This project is available as a Docker image:

```bash
docker pull riccardotornesello/hello-world-http-server
```

## 🚀 Running the Server

Run the container exposing port `80`:

```bash
docker run -p 80:80 riccardotornesello/hello-world-http-server
```

Run on a custom port (e.g., port 3000):

```bash
docker run -p 3000:3000 -e PORT=3000 riccardotornesello/hello-world-http-server
```

If you want to set a custom identifier:

```bash
docker run -p 80:80 -e IDENTIFIER="MyServer123" riccardotornesello/hello-world-http-server
```

## 🌐 Example Response

Request:

```bash
curl http://localhost/test
```

Response:

```
Hello World!
Path: /test
Identifier: MyServer123
```

_(If `IDENTIFIER` is not set, the third line is omitted.)_

## ⚙️ Environment Variables

| Variable   | Description                               | Default |
| ---------- | ----------------------------------------- | ------- |
| PORT       | Port number for the HTTP server           | 80      |
| IDENTIFIER | Optional identifier to include in output. | (none)  |

## 📜 License

This project is licensed under the MIT License.
