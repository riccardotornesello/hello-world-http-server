# hello-world-http-server

A simple Python HTTP server running in a Docker container. It responds to GET requests with:

- **First line:** `Hello World!`
- **Second line:** `Path: ...` (the path requested)
- **Third line:** `Identifier: ...` (the value of the `IDENTIFIER` environment variable, if set)

The app listens on **port 8080**.

## 🐳 Docker Image

This project is available as a Docker image:

```bash
docker pull riccardotornesello/hello-world-http-server
```

## 🚀 Running the Server

Run the container exposing port `8080`:

```bash
docker run -p 8080:8080 riccardotornesello/hello-world-http-server
```

If you want to set a custom identifier:

```bash
docker run -p 8080:8080 -e IDENTIFIER="MyServer123" riccardotornesello/hello-world-http-server
```

## 🌐 Example Response

Request:

```bash
curl http://localhost:8080/test
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
| IDENTIFIER | Optional identifier to include in output. | (none)  |

## 📜 License

This project is licensed under the MIT License.
