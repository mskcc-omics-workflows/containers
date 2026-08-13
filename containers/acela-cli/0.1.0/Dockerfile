FROM python:3.11-slim

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Eric Buehler (buehlere@mskcc.org)" \
      org.opencontainers.image.created="2026-08-13T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="1.0.0" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc/acela-cli/releases/tag/v0.1.0" \
      org.opencontainers.image.url="https://github.com/mskcc/acela-cli" \
      org.opencontainers.image.title="acela-cli" \
      org.opencontainers.image.description="Container for acela-cli 0.1.0"

WORKDIR /app
COPY pyproject.toml README.md ./
COPY acela_cli/ ./acela_cli/

RUN pip install --no-cache-dir . \
    && useradd --create-home --uid 1000 acela

USER acela
WORKDIR /home/acela

CMD ["acela"]
