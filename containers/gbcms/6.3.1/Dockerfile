# syntax=docker/dockerfile:1

################## ARGUMENTS ########################

ARG GBCMS_VERSION=6.3.1

################## BUILDER STAGE ####################

FROM python:3.11-bookworm AS builder

ARG GBCMS_VERSION

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies for Rust compilation
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    pkg-config \
    git \
    cmake \
    clang \
    libclang-dev \
    llvm-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

ENV LIBCLANG_PATH="/usr/lib/llvm-14/lib"
ENV BINDGEN_EXTRA_CLANG_ARGS="-I/usr/lib/llvm-14/lib/clang/14.0.6/include"

# Install Rust
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

ENV CARGO_NET_RETRY=10 \
    CARGO_HTTP_MULTIPLEXING=false \
    CARGO_NET_GIT_FETCH_WITH_CLI=true

RUN pip install --no-cache-dir "maturin[patchelf]" \
    && git clone --branch ${GBCMS_VERSION} --depth 1 https://github.com/msk-access/gbcms.git /app

# Build unified wheel with maturin (includes both Python and Rust)
RUN maturin build --release --no-default-features --out /app/dist

################## RUNTIME STAGE ####################

FROM python:3.11-slim-bookworm

ARG GBCMS_VERSION

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Ronak Shah (shahr2@mskcc.org)" \
      org.opencontainers.image.created="2026-08-26T00:00:00Z" \
      org.opencontainers.image.licenses="AGPL-3.0" \
      org.opencontainers.image.version=${GBCMS_VERSION} \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/msk-access/gbcms/releases/tag/${GBCMS_VERSION}" \
      org.opencontainers.image.url="https://github.com/msk-access/gbcms" \
      org.opencontainers.image.title="gbcms" \
      org.opencontainers.image.description="Container for gbcms ${GBCMS_VERSION}: high-performance variant counting (Get Base Count Multi Sample)"

WORKDIR /app

# procps and bash are required for Nextflow task metrics and shell execution
RUN apt-get update && apt-get install --no-install-recommends -y \
    libcurl4 \
    libssl3 \
    zlib1g \
    libbz2-1.0 \
    liblzma5 \
    procps \
    bash \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/dist/*.whl /app/dist/
RUN pip install --no-cache-dir /app/dist/*.whl \
    && rm -rf /app/dist

# Verify installation
RUN python -c "from gbcms import _rs; import gbcms; print(f'gbcms {gbcms.__version__} ready')"

ENTRYPOINT ["gbcms"]
CMD ["--help"]
