FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
EXPOSE 8050
ENV HOST=0.0.0.0
ENV PORT=8050
ENV DEBUG=False

CMD ["uv", "run", "--no-dev", "main.py"]