FROM ubuntu:24.04

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org), John Orgera (orgeraj@mskcc.org)" \
      org.opencontainers.image.created="2025-08-21T11:07:00Z" \
      imageprivacy="False" \
      org.opencontainers.image.licenses="ACRRI_TERMS_OF_USE" \
      org.opencontainers.image.version="1.1" \
      org.opencontainers.image.source="https://github.com/LukszaLab/NeoantigenEditing" \
      org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/tree/main/containers/neoantigen-editing/" \
      org.opencontainers.image.title="neoantigen-editing" \
      org.opencontainers.image.description="Tools for computing neoantigen qualities and for performing clone composition predictions."

ENV DEBIAN_FRONTEND=noninteractive
ENV NEOANTIGEN_EDITING_TAG 6877bf296ce96f357c101f91a6d8e123742eb8a6
# `cp -r /tmp/NeoantigenEditing/ /usr/bin` (below) copies the whole checkout
# in as /usr/bin/NeoantigenEditing/, not flattened onto /usr/bin, so the
# scripts are never actually on PATH; the checkout is also not executable.
# Modules invoke these scripts as bare commands (e.g. compute_fitness.py,
# align_neoantigens_to_IEDB.py), so put the checkout's directory on PATH
# and make its scripts executable instead of relying on /usr/bin placement.
ENV PATH="/usr/bin/NeoantigenEditing:${PATH}"

RUN apt-get update -y \
      # Install packages
      && apt-get install -y --no-install-recommends  python3 python3-pip git make build-essential ncbi-blast+ python3-pandas python3-matplotlib python3-scipy python3-numpy python3-biopython \
      # Install neoantigenEditing
      && git clone https://github.com/LukszaLab/NeoantigenEditing /tmp/NeoantigenEditing \
      && git -C /tmp/NeoantigenEditing checkout ${NEOANTIGEN_EDITING_TAG} \
      && cp -r /tmp/NeoantigenEditing/ /usr/bin \
      && chmod +x /usr/bin/NeoantigenEditing/*.py \
      # Clean up
      && rm -r /tmp/NeoantigenEditing \
      && apt-get clean \
      && apt-get purge \
      && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
