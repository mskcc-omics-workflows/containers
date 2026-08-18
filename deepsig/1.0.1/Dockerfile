FROM ubuntu:22.04

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (john.orgera@gmail.com)" \
      org.opencontainers.image.created="2026-08-18T00:00:00Z" \
      org.opencontainers.image.licenses="GPL-2.0-or-later" \
      org.opencontainers.image.version="1.0.1" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/deepsig/" \
      org.opencontainers.image.url="https://github.com/mskcc/DeepSig" \
      org.opencontainers.image.title="DeepSig" \
      org.opencontainers.image.description="Deep learning-based mutational signature caller for MSK-IMPACT/WES data, with pretrained v1.0 models bundled."

ENV DEBIAN_FRONTEND=noninteractive
ENV CPATH=/usr/include
ENV RETICULATE_PYTHON=/opt/DeepSig/.venv/bin/python3
ENV DEEPSIG_MODEL_DIR=/opt/DeepSig/inst/extdata/dlsig/v1.0
ENV PATH="/opt/DeepSig/exec:${PATH}"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN set -eux && apt-get update -y && \
    apt-get install --no-install-recommends -y \
        ca-certificates \
        build-essential \
        curl libcurl4-openssl-dev \
        gfortran \
        git \
        lbzip2 libbz2-dev \
        libblas-dev liblapack-dev \
        liblzma-dev \
        xz-utils \
        openssl \
        libssl-dev \
        libxml2-dev \
        pkgconf \
        python3-dev python3-pip python3-venv python3-virtualenv \
        libgsl-dev \
        libpng-dev \
        libhdf5-dev \
        r-base && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo 'options(repos = c(CRAN = "https://cloud.r-project.org/"), download.file.method = "libcurl")' >> "$(Rscript -e 'cat(R.home())')"/etc/Rprofile.site && \
    echo 'options(Ncpus = parallel::detectCores())' >> "$(Rscript -e 'cat(R.home())')"/etc/Rprofile.site && \
    Rscript -e 'options(warn=2); install.packages("remotes")'

RUN Rscript -e 'remotes::install_version("RColorBrewer", "1.1-3")' && \
    Rscript -e 'remotes::install_version("RCurl", "1.98-1.14")' && \
    Rscript -e 'remotes::install_version("Rcpp", "1.0.12")' && \
    Rscript -e 'remotes::install_version("RcppEigen", "0.3.4.0.0")' && \
    Rscript -e 'remotes::install_version("XML", "3.99-0.16.1")' && \
    Rscript -e 'remotes::install_version("argparse", "2.2.3")' && \
    Rscript -e 'remotes::install_version("clue", "0.3-65")' && \
    Rscript -e 'remotes::install_version("coneproj")' && \
    Rscript -e 'remotes::install_version("cowplot", "1.1.3")' && \
    Rscript -e 'remotes::install_version("data.table", "1.15.4")' && \
    Rscript -e 'remotes::install_version("ggplot2", "3.5.1")' && \
    Rscript -e 'remotes::install_version("ggrepel", "0.9.5")' && \
    Rscript -e 'remotes::install_version("gridGraphics", "0.5-1")' && \
    Rscript -e 'remotes::install_version("gtools", "3.9.5")' && \
    Rscript -e 'remotes::install_version("reticulate", "1.38.0")' && \
    Rscript -e 'remotes::install_version("scales", "1.3.0")' && \
    Rscript -e 'remotes::install_version("tidyr", "1.3.1")' && \
    Rscript -e 'remotes::install_version("httr2")'

RUN Rscript -e 'options(warn=2); install.packages("BiocManager")' && \
    Rscript -e 'options(warn=2); BiocManager::install(c( \
        "BSgenome", \
        "BSgenome.Hsapiens.UCSC.hg19", \
        "Biostrings", \
        "S4Vectors", \
        "GenomeInfoDb", \
        "GenomicAlignments", \
        "GenomicRanges", \
        "Rhtslib", \
        "Rsamtools", \
        "SummarizedExperiment", \
        "rtracklayer" \
    ))' && \
    Rscript -e 'remotes::install_version("restfulr", "0.0.15")'

# Clone the pinned tag, then prune every model directory except the current
# v1.0 (impact-platform) set in the same layer, so the large historical/wes
# trees are never actually persisted in an image layer.
RUN git clone --branch v1.0.1 --depth 1 https://github.com/mskcc/DeepSig.git /opt/DeepSig && \
    find /opt/DeepSig/inst/extdata/dlsig -mindepth 1 -maxdepth 1 -type d \
        ! -name v1.0 -exec rm -rf {} + && \
    chmod +x /opt/DeepSig/exec/*.R

RUN python3 -m venv /opt/DeepSig/.venv && \
    /opt/DeepSig/.venv/bin/python -m pip install --no-cache-dir pandas h5py tensorflow==2.15.0 keras==2.15.0

RUN Rscript -e 'options(warn=2); remotes::install_local("/opt/DeepSig", dependencies = FALSE)'
