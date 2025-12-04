FROM ubuntu:25.10
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
ENV PYTHON_VERSION=3.10.15

WORKDIR /tmp

RUN set -xe && apt-get update \
    # Install packages
    && apt-get install --no-install-recommends -y \
    build-essential \
    cmake \
    libncurses5-dev \
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
    libjpeg8-dev \
    libfreetype6-dev \
    unzip \
    # Install vcflib
    libvcflib-tools \
    libvcflib-dev \
    # Additional dependencies for building Python from source
    libffi-dev \
    libgdbm-dev \
    libsqlite3-dev \
    libreadline-dev \
    tk-dev \
    uuid-dev \
    ca-certificates \
    # Download and extract Python source
    && wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz \
    && tar -xf Python-${PYTHON_VERSION}.tar.xz \
    # Build Python 3.10 from source with optimizations
    && (cd Python-${PYTHON_VERSION} \
        && ./configure \
            --enable-optimizations \
            --with-lto \
            --enable-shared \
            --with-computed-gotos \
            --with-system-ffi \
            --enable-loadable-sqlite-extensions \
            --with-ensurepip=install \
            LDFLAGS="-Wl,-rpath /usr/local/lib" \
        && make -j$(nproc) PROFILE_TASK='-m test.regrtest --pgo -j$(nproc)' \
        && make altinstall) \
    && ldconfig \
    && rm -rf Python-${PYTHON_VERSION} Python-${PYTHON_VERSION}.tar.xz \
    # Create symlinks for python3 and pip3
    && ln -sf /usr/local/bin/python3.10 /usr/local/bin/python3 \
    && ln -sf /usr/local/bin/pip3.10 /usr/local/bin/pip3 \
    # Upgrade pip
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir "numpy<2" \
    && pip3 install --no-cache-dir pandas \
    && pip3 install --use-pep517 --no-cache-dir git+https://github.com/mskcc/mutalyzer.git@${MUTALYZER_TAG} \
    # Install neosv
    &&  pip3 install --use-pep517 --no-cache-dir git+https://github.com/pintoa1-mskcc/NeoSV.git@${NEOSV_TAG} \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /
