FROM python:2.7

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org), John Orgera (orgeraj@mskcc.org)" \
      org.opencontainers.image.created="2025-08-21T11:07:00Z" \
      org.opencontainers.image.licenses="GPL-3.0" \
      org.opencontainers.image.version="1.5-msk" \
      org.opencontainers.image.source="https://github.com/mskcc/phylowgs" \
      org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/containers/phylowgs/" \
      org.opencontainers.image.title="Phylowgs" \
      org.opencontainers.image.description="Application for inferring subclonal composition and evolution from whole-genome sequencing data."

ENV DEBIAN_FRONTEND=noninteractive
ENV PHYLOWGS_TAG="v1.5-msk"

RUN apt-get update -y \
      # Install packages
      && apt-get install -y --no-install-recommends python2 git make build-essential libgsl-dev \
      # Install phylowgs
      && cd /tmp \
      && git clone --branch 1.5 https://github.com/mskcc/phylowgs \
      && cd phylowgs \
      && pip2 install --no-cache-dir -r requirements.txt  \
      && g++ -o mh.o -O3 mh.cpp  util.cpp 'gsl-config --cflags --libs' \
      && cp -r . /usr/bin \
      # Clean up
      && rm -r /tmp/phylowgs \
      && apt-get clean \
      && apt-get purge \
      && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*