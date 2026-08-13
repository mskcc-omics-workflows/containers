FROM python:3.11-slim

ARG ACELA_CLI_VERSION=0.1.0

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Eric Buehler (buehlere@mskcc.org)" \
      org.opencontainers.image.created="2026-08-13T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version=${ACELA_CLI_VERSION} \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc/acela-cli/releases/tag/v${ACELA_CLI_VERSION}" \
      org.opencontainers.image.url="https://github.com/mskcc/acela-cli" \
      org.opencontainers.image.title="acela_cli" \
      org.opencontainers.image.description="Container for acela-cli ${ACELA_CLI_VERSION}"

RUN apt-get update \
    && apt-get install --no-install-recommends -y git ca-certificates \
    && git clone --branch v${ACELA_CLI_VERSION} --depth 1 https://github.com/mskcc/acela-cli.git /tmp/acela-cli \
    && pip install --no-cache-dir /tmp/acela-cli \
    && rm -rf /tmp/acela-cli \
    && apt-get purge -y --auto-remove git \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 acela

USER acela
WORKDIR /home/acela

CMD ["acela"]
