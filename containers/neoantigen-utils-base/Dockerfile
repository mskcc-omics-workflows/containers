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
    && apt-get install -y libncurses5-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-gnutls-dev \
    zlib1g-dev \
    libssl-dev \
    gcc \
    wget \
    make \
    perl \
    bzip2 \
    pkg-config \
    libpng-dev \
    libjpeg8-dev \
    libfreetype6-dev \
    unzip \
    git \
    python3.8 \
    python3-pip \
    g++ \
    # Install vcflib
    && git clone https://github.com/Sentieon/vcflib.git /usr/bin/vcflib/ \
    # Upgrade pip
    && python3 -m pip install --upgrade pip \
    && pip3 install numpy \
    && pip3 install pandas
