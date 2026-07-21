FROM debian:12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gnucobol3 \
        python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY report.cob server.py ./