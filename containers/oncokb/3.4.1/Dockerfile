FROM ubuntu:20.04

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org)" \
      org.opencontainers.image.created="2024-12-27T11:07:00Z" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.version.python="3.8" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/oncokb/" \
      org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/" \
      org.opencontainers.image.title="OncoKB Base" \
      org.opencontainers.image.description="The image for Oncokb Maf annotation"

ENV DEBIAN_FRONTEND=noninteractive
ARG ONCOKB_ANNOTATOR_VERSION=3.4.1
ENV ONCOKB_ANNOTATOR_VERSION=${ONCOKB_ANNOTATOR_VERSION}

RUN set -xe && apt-get update \
    # Install packages
    && apt-get install --no-install-recommends -y \
    libncurses5-dev \
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
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /usr/bin/oncokb/ 
ENV PATH="/usr/bin/oncokb/:$PATH"

WORKDIR /tmp/
RUN wget -q https://github.com/oncokb/oncokb-annotator/archive/refs/tags/v${ONCOKB_ANNOTATOR_VERSION}.zip \
    && unzip v${ONCOKB_ANNOTATOR_VERSION}.zip  \
    && mv oncokb-annotator-${ONCOKB_ANNOTATOR_VERSION}/* /usr/bin/oncokb/
    
RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r /usr/bin/oncokb/requirements/common.txt -r /usr/bin/oncokb/requirements/pip3.txt
    