FROM python:3.10-slim-trixie

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2025-11-25T11:07:00Z" \
      imageprivacy="False" \
      org.opencontainers.image.version="1.4.0" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/neoantigen-utils-base/" \
      org.opencontainers.image.url="https://github.com/mskcc/neoAntigen-Pipeline" \
      org.opencontainers.image.title="Neoantigen Utils Base" \
      org.opencontainers.image.description="The base image for neoantigen helper utils"

ENV DEBIAN_FRONTEND=noninteractive
ENV NEOSV_TAG=0.0.4-mskv1
ENV TZ=Etc/UTC
ENV MUTALYZER_TAG=3.1.1-mskv1
ARG TARGETPLATFORM

RUN apt-get update \
    # Install runtime dependencies for Python
    && apt-get install --no-install-recommends -y \
    libffi8 \
    gzip \
    coreutils \
    libgdbm6 \
    libsqlite3-0 \
    libreadline8 \
    libbz2-1.0 \
    liblzma5 \
    libssl3 \
    zlib1g \
    libtk8.6 \
    uuid-runtime \
    ca-certificates \
    # Install other required packages
    build-essential \
    cmake \
    libncurses5-dev \
    libncurses-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-gnutls-dev \
    zlib1g-dev \
    libssl-dev \
    wget \
    perl \
    bzip2 \
    tabix \
    pkg-config \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    unzip \
    git \
    # Install vcflib
    libvcflib-tools \
    libvcflib-dev \
    && ldconfig \
    # Upgrade pip
    && /usr/local/bin/pip install --no-cache-dir --upgrade pip \
    && /usr/local/bin/pip install --no-cache-dir "numpy<2" \
    && /usr/local/bin/pip install --no-cache-dir pandas \
    && /usr/local/bin/pip install --use-pep517 --no-cache-dir git+https://github.com/mskcc/mutalyzer.git@${MUTALYZER_TAG} \
    # Install neosv
    && /usr/local/bin/pip install --use-pep517 --no-cache-dir git+https://github.com/pintoa1-mskcc/NeoSV.git@${NEOSV_TAG} \ 
    && rm -rf /var/lib/apt/lists/*
