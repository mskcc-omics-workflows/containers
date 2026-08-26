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
ENV NEOANTIGEN_EDITING_TAG 15bfb99bab8a4ca0e9303867f4508520e220fd3e
ENV PATH="/usr/bin/NeoantigenEditing:${PATH}"

RUN apt-get update -y \
      # Install packages
      && apt-get install -y --no-install-recommends  python3 python3-pip git make build-essential ncbi-blast+ python3-pandas python3-matplotlib python3-scipy python3-numpy python3-biopython \
      # Install neoantigenEditing
      && git clone https://github.com/LukszaLab/NeoantigenEditing -b neoQual /tmp/NeoantigenEditing \
      && git -C /tmp/NeoantigenEditing checkout ${NEOANTIGEN_EDITING_TAG} \
      && cp -r /tmp/NeoantigenEditing/ /usr/bin \
      && chmod +x /usr/bin/NeoantigenEditing/*.py \
      # Clean up
      && rm -r /tmp/NeoantigenEditing \
      && apt-get clean \
      && apt-get purge \
      && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
