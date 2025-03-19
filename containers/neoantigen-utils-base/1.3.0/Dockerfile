FROM ubuntu:22.04

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2024-04-24T11:07:00Z" \
      org.opencontainers.image.version="1.3.0" \
      org.opencontainers.image.version.python="3.10" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/neoantigen-utils-base/" \
      org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/" \
      org.opencontainers.image.title="Neoantigen Utils Base" \
      org.opencontainers.image.description="The base image for neoantigen helper utils"

ENV DEBIAN_FRONTEND=noninteractive
ENV NEOSV_TAG=1.2
RUN set -xe && apt-get update \
    # Install packages
    && apt-get install --no-install-recommends -y \
    build-essential \
    libncurses5-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-gnutls-dev \
    zlib1g-dev \
    libssl-dev \
    wget \
    perl \
    bzip2 \
    pkg-config \
    libpng-dev \
    libjpeg8-dev \
    libfreetype6-dev \
    unzip \
    git \
    python3.10 \
    python3-pip\
    # Install vcflib
    && git clone https://github.com/Sentieon/vcflib.git /usr/bin/vcflib/ \
    # Upgrade pip
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir "numpy<2" \
    && pip3 install --no-cache-dir pandas \
    # Install neosv
    && git clone https://github.com/pintoa1-mskcc/NeoSV.git /usr/bin/NeoSV/ \
    && python3 /usr/bin/NeoSV/setup.py install \ 
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
