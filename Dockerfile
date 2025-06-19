FROM python:3.11-slim

WORKDIR /mcp_server

RUN pip install uv

COPY pyproject.toml

RUN uv venv
RUN uv sync

COPY server.py
COPY client.py

EXPOSE 8000

CMD ["uv", "run", "server.py"]