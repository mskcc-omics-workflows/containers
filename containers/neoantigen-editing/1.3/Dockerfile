FROM ubuntu:24.04

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org), John Orgera (orgeraj@mskcc.org)" \
      org.opencontainers.image.created="2025-08-21T11:07:00Z" \
      imageprivacy="False" \
      org.opencontainers.image.licenses="ACRRI_TERMS_OF_USE" \
      org.opencontainers.image.version="1.3" \
      org.opencontainers.image.source="https://github.com/mskcc/NeoantigenEditing" \
      org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/containers/NeoantigenEditing/" \
      org.opencontainers.image.title="neoantigen-editing" \
      org.opencontainers.image.description="Tools for computing neoantigen qualities and for performing clone composition predictions."

ENV DEBIAN_FRONTEND=noninteractive
ENV NEOANTIGEN_EDITING_TAG 1.3
ARG TARGETPLATFORM

RUN apt-get update -y \
      # Install packages
      && apt-get install -y --no-install-recommends  python3 python3-pip git make build-essential ncbi-blast+ python3-pandas python3-matplotlib python3-scipy python3-numpy python3-biopython \
      # Install neoantigenEditing
      && git clone --branch ${NEOANTIGEN_EDITING_TAG} https://github.com/mskcc/NeoantigenEditing /tmp/NeoantigenEditing \
      && cp -r /tmp/NeoantigenEditing/ /usr/bin \
      # Clean up
      && rm -r /tmp/NeoantigenEditing \
      && apt-get clean \
      && apt-get purge \
      && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
