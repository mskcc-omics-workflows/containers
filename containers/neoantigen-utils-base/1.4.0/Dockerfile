# Build Python from source
FROM --platform=$BUILDPLATFORM ubuntu:25.10 AS python-builder

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.10.15

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    wget \
    ca-certificates \
    libffi-dev \
    libgdbm-dev \
    libsqlite3-dev \
    libreadline-dev \
    libbz2-dev \
    liblzma-dev \
    libssl-dev \
    zlib1g-dev \
    tk-dev \
    uuid-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/python-build

RUN wget -q https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz \
    && tar -xf Python-${PYTHON_VERSION}.tar.xz \
    && rm Python-${PYTHON_VERSION}.tar.xz

WORKDIR /tmp/python-build/Python-${PYTHON_VERSION}

RUN ./configure \
        --prefix=/opt/python \
        --enable-optimizations \
        --with-lto \
        --enable-shared \
        --with-computed-gotos \
        --with-system-ffi \
        --enable-loadable-sqlite-extensions \
        --with-ensurepip=install \
        LDFLAGS="-Wl,-rpath /opt/python/lib" \
    && make -j"$(nproc)" PROFILE_TASK="-m test.regrtest --pgo -j$(nproc)" \
    && make install

# Final image
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
ENV PATH=/opt/python/bin:$PATH
ENV LD_LIBRARY_PATH=/opt/python/lib:$LD_LIBRARY_PATH
ARG TARGETPLATFORM

# Copy Python installation from builder stage
COPY --from=python-builder /opt/python /opt/python

RUN apt-get update \
    # Install runtime dependencies for Python
    && apt-get install --no-install-recommends -y \
    libffi8 \
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
    libjpeg8-dev \
    libfreetype6-dev \
    unzip \
    git \
    # Install vcflib
    libvcflib-tools \
    libvcflib-dev \
    && ldconfig \
    # Create symlinks for python3 and pip3
    && ln -sf /opt/python/bin/python3.10 /usr/local/bin/python3 \
    && ln -sf /opt/python/bin/pip3.10 /usr/local/bin/pip3 \
    && ln -sf /opt/python/bin/python3.10 /usr/local/bin/python \
    && ln -sf /opt/python/bin/pip3.10 /usr/local/bin/pip \
    # Upgrade pip
    && /usr/local/bin/pip install --no-cache-dir --upgrade pip \
    && /usr/local/bin/pip install --no-cache-dir "numpy<2" \
    && /usr/local/bin/pip install --no-cache-dir pandas \
    && /usr/local/bin/pip install --use-pep517 --no-cache-dir git+https://github.com/mskcc/mutalyzer.git@${MUTALYZER_TAG} \
    # Install neosv
    && /usr/local/bin/pip install --use-pep517 --no-cache-dir git+https://github.com/pintoa1-mskcc/NeoSV.git@${NEOSV_TAG} \ 
    && rm -rf /var/lib/apt/lists/*
