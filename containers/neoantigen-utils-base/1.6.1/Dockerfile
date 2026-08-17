FROM python:3.12-slim-trixie AS base

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2026-08-13T21:00:00Z" \
      imageprivacy="False" \
      org.opencontainers.image.version="1.6.1" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/neoantigen-utils-base/" \
      org.opencontainers.image.url="https://github.com/mskcc/neoantigen-utils" \
      org.opencontainers.image.title="Neoantigen Utils Base" \
      org.opencontainers.image.description="The base image for neoantigen helper utils"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV NEOSV_TAG=0.0.4-mskv1
ENV MUTALYZER_TAG=3.1.1-mskv1
ENV NEOANTIGEN_UTILS_TAG=1.6.1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

FROM base AS builder


SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    # Install build dependencies
    && apt-get install --no-install-recommends -y \
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
    && python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    # setuptools<81 still ships pkg_resources, required by some mutalyzer dependencies
    && /opt/venv/bin/pip install --no-cache-dir "setuptools<81" \
    && /opt/venv/bin/pip install --no-cache-dir "numpy<2" \
    && /opt/venv/bin/pip install --no-cache-dir pandas \
    && /opt/venv/bin/pip install --no-cache-dir pytest \
    # Install & test mutalyzer
    && git clone --depth 1 --branch ${MUTALYZER_TAG} https://github.com/mskcc/mutalyzer.git /tmp/mutalyzer \
    && /opt/venv/bin/pip install --use-pep517 --no-cache-dir -e '/tmp/mutalyzer[dev]' \
    && /opt/venv/bin/pytest /tmp/mutalyzer \
    && /opt/venv/bin/pip install --use-pep517 --no-cache-dir --no-deps --force-reinstall /tmp/mutalyzer \
    && rm -rf /tmp/mutalyzer \
    # Install & test NeoSV
    && git clone --depth 1 --branch ${NEOSV_TAG} https://github.com/pintoa1-mskcc/NeoSV.git /tmp/NeoSV \
    && /opt/venv/bin/pip install --use-pep517 --no-cache-dir -e /tmp/NeoSV \
    && mkdir -p /tmp/neosv-functest \
    && wget -q -O /tmp/neosv-functest/test.sv.bedpe https://raw.githubusercontent.com/mskcc-omics-workflows/test-datasets/neoantigen/neoantigen/test.sv.bedpe \
    && wget -q -O /tmp/neosv-functest/gtf.gz https://raw.githubusercontent.com/mskcc-omics-workflows/test-datasets/neoantigen/neoantigen/Homo_sapiens.GRCh37.75.gtf.gz \
    && wget -q -O /tmp/neosv-functest/cdna.fa.gz https://raw.githubusercontent.com/mskcc-omics-workflows/test-datasets/neoantigen/neoantigen/Homo_sapiens.GRCh37.75.cdna.all.fa.gz \
    && echo 'HLA-A24:02,HLA-A24:02,HLA-B39:01,HLA-B39:01,HLA-C07:01,HLA-C06:02' | tr ',' '\n' | sed 's/^[ \t]*//;s/[ \t]*$//' > /tmp/neosv-functest/hla.txt \
    && awk 'NF {print substr($0,1,5)"*"substr($0,6)}' /tmp/neosv-functest/hla.txt > /tmp/neosv-functest/hla2.txt \
    && mv /tmp/neosv-functest/hla2.txt /tmp/neosv-functest/hla.txt \
    && /opt/venv/bin/neosv --sv-file /tmp/neosv-functest/test.sv.bedpe --out /tmp/neosv-functest/out --hla-file /tmp/neosv-functest/hla.txt --gtf-file /tmp/neosv-functest/gtf.gz --cdna-file /tmp/neosv-functest/cdna.fa.gz --pyensembl-cache-dir /tmp/neosv-functest/pyensembl_cache --prefix test \
    && test -s /tmp/neosv-functest/out/test.net.in.txt \
    && test -s /tmp/neosv-functest/out/test.WT.net.in.txt \
    && rm -rf /tmp/neosv-functest \
    && /opt/venv/bin/pip install --use-pep517 --no-cache-dir --no-deps --force-reinstall /tmp/NeoSV \
    && rm -rf /tmp/NeoSV \
    # install and test neoantigen-utils
    && mkdir /tmp/neoantigen-utils \
    && git -C /tmp/neoantigen-utils init -q \
    && git -C /tmp/neoantigen-utils remote add origin https://github.com/mskcc/neoantigen-utils.git \
    && git -C /tmp/neoantigen-utils fetch --depth 1 origin ${NEOANTIGEN_UTILS_TAG} \
    && git -C /tmp/neoantigen-utils checkout FETCH_HEAD \
    && /opt/venv/bin/pip install --use-pep517 --no-cache-dir -e '/tmp/neoantigen-utils[dev]' \
    && /opt/venv/bin/pytest /tmp/neoantigen-utils \
    && /opt/venv/bin/pip install --use-pep517 --no-cache-dir --no-deps --force-reinstall /tmp/neoantigen-utils \
    && rm -rf /tmp/neoantigen-utils


# Final image
FROM base

RUN apt-get update \
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
    tabix \
    procps \
    perl \
    bzip2 \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
