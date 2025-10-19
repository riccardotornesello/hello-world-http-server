# hello-world-http-server

A simple Python HTTP server running in a Docker container. It responds to HTTP requests with detailed information about the request.

## 📋 Response Information

The server responds with the following information:

- **First line:** `Hello World!`
- **Method:** The HTTP method used (GET, POST, PUT, DELETE, etc.)
- **Path:** The path requested
- **Query:** Query parameters (if any)
- **Timestamp:** Request timestamp in UTC
- **Client IP:** Client's IP address (supports X-Forwarded-For header)
- **User-Agent:** Client's User-Agent header
- **Hostname:** Server's hostname
- **Identifier:** Optional identifier (from `IDENTIFIER` environment variable)
- **Request Count:** Total number of requests served

## 🏥 Health Check Endpoint

A dedicated `/health` endpoint is available for monitoring and health checks:

```bash
curl http://localhost/health
```

Response: `OK`

This endpoint is ideal for container orchestration systems like Kubernetes or Docker Swarm.

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
curl http://localhost/test?query=example
```

Response:

```
Hello World!
Method: GET
Path: /test
Query: query=example
Timestamp: 2025-10-19 23:00:00 UTC
Client IP: 172.17.0.1
User-Agent: curl/8.5.0
Hostname: abc123def456
Identifier: MyServer123
Request Count: 42
```

_(If `IDENTIFIER` is not set, that line is omitted.)_

## ⚙️ Environment Variables

| Variable   | Description                                              | Default |
| ---------- | -------------------------------------------------------- | ------- |
| PORT       | Port number for the HTTP server                          | 80      |
| IDENTIFIER | Optional identifier to include in output                 | (none)  |
| DELAY      | Optional delay in seconds before responding (for testing)| 0       |

### Using DELAY for Testing

The `DELAY` environment variable is useful for simulating slow responses and testing timeout handling:

```bash
docker run -p 80:80 -e DELAY=2 riccardotornesello/hello-world-http-server
```

This will make the server wait 2 seconds before responding to each request.

## 🔧 Supported HTTP Methods

The server accepts all standard HTTP methods:
- GET
- POST
- PUT
- DELETE
- PATCH
- HEAD
- OPTIONS

Example:
```bash
curl -X POST http://localhost/api/data
curl -X PUT http://localhost/api/update
curl -X DELETE http://localhost/api/resource
```

## 🧪 Testing

Run the test suite:

```bash
pip install -r requirements-dev.txt
pytest test_server.py -v
```

## 📜 License

This project is licensed under the MIT License.
