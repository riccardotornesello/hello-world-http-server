FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code
COPY server.py ./

# Run the application
ENV PORT=80

EXPOSE $PORT

ENV PYTHONUNBUFFERED=1
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT server:app"]
