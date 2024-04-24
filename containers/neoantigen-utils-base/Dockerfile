FROM ubuntu:20.04

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2024-04-24T11:07:00Z" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.version.python="3.8" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/neoantigen-utils-base/" \
      org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/" \
      org.opencontainers.image.title="Neoantigen Utils Base" \
      org.opencontainers.image.description="The base image for neoantigen helper utils"

ENV DEBIAN_FRONTEND=noninteractive

RUN set -xe && apt-get update \
    # Install packages
    && apt-get install --no-install-recommends -y \
    libncurses5-dev=6.2-0ubuntu2.1 \
    libbz2-dev=1.0.8-2 \
    liblzma-dev=5.2.4-1ubuntu1.1 \
    libcurl4-gnutls-dev=7.68.0-1ubuntu2.22 \
    zlib1g-dev=1:1.2.11.dfsg-2ubuntu1.5 \
    libssl-dev=1.1.1f-1ubuntu2.22 \
    gcc=4:9.3.0-1ubuntu2 \
    wget=1.20.3-1ubuntu2 \
    make=4.2.1-1.2 \
    perl=5.30.0-9ubuntu0.5 \
    bzip2=1.0.8-2 \
    pkg-config=0.29.1-0ubuntu4 \
    libpng-dev=1.6.37-2 \
    libjpeg8-dev=8c-2ubuntu8 \
    libfreetype6-dev=2.10.1-2ubuntu0.3 \
    unzip=6.0-25ubuntu1.2 \
    git=1:2.25.1-1ubuntu3.11 \
    python3.8=3.8.10-0ubuntu1~20.04.9 \
    python3-pip=20.0.2-5ubuntu1.10 \
    g++=4:9.3.0-1ubuntu2 \
    # Install vcflib
    && git clone https://github.com/Sentieon/vcflib.git /usr/bin/vcflib/ \
    # Upgrade pip
    && python3 -m pip install --upgrade pip \
    && pip3 install --no-cache-dir numpy==1.24.4 \
    && pip3 install --no-cache-dir pandas==2.0.3 \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
