FROM python:3.11-slim

WORKDIR /mcp_server

RUN pip install uv

COPY pyproject.toml .

RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e .  

COPY server.py .
COPY client.py .
COPY tools/ tools/

EXPOSE 8000

CMD ["uv", "run", "server.py"]
