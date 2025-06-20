FROM python:3.11-slim

WORKDIR /mcp_server

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY client.py .
COPY tools/ tools/
EXPOSE 8000

CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
