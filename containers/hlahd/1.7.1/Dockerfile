FROM ubuntu:22.04

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2025-08-20T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="1.7.1" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/hlahd/" \
      org.opencontainers.image.url="https://w3.genome.med.kyoto-u.ac.jp/HLA-HD/" \
      org.opencontainers.image.title="HLA-HD" \
      org.opencontainers.image.description="HLA typing software from Kyoto University, built with Bowtie2 and dependencies pre-installed."

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN  --mount=type=secret,id=MSK_JFROG_USERNAME \
      --mount=type=secret,id=MSK_JFROG_TOKEN \
      set -eux && apt-get update -y && \
      # Install packages
      apt-get install --no-install-recommends -y \
      ca-certificates \
      build-essential \
      g++ \
      perl \
      python3 \
      wget \
      bowtie2 \
      && \
      # Download HLAHD tarball from JFrog
      mkdir -p /tmp/hlahdTmp/ && \
      wget --progress=dot:giga --directory-prefix /tmp/hlahdTmp/ --user="$(cat /run/secrets/MSK_JFROG_USERNAME)" --password="$(cat /run/secrets/MSK_JFROG_TOKEN)" "https://mskcc.jfrog.io/artifactory/omicswf-generic-prod-local/hlahd.1.7.1.tar.gz" && \
      # Extract and install HLAHD
      mkdir -p /opt/hlahd && \
      tar -zxvf /tmp/hlahdTmp/hlahd.1.7.1.tar.gz -C /opt/hlahd/ && \
      HLAHD_DIR="$(find /opt/hlahd -maxdepth 1 -type d -name 'hlahd.*' | head -1)" && \
      test -n "$HLAHD_DIR" && \
      bash "$HLAHD_DIR/install.sh" && \
      sh "$HLAHD_DIR/update.dictionary.sh" && \
      ln -s "$HLAHD_DIR" /opt/hlahd/current && \
      # Clean up
      apt-get clean && \
      rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PATH="/opt/hlahd/current/bin:${PATH}"

WORKDIR /data
