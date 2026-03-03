FROM ubuntu:20.04 AS builder

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Adam Price (price2@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org), Anne Marie Noronha (noronhaa@mskcc.org), John Orgera (orgeraj@mskcc.org), Yixiao Gong (gongy@mskcc.org), Philip Jonsson (jonssonp@mskcc.org)" \
      org.opencontainers.image.created="2026-03-02T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="2.0.10" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/facets_tools/" \
      org.opencontainers.image.url="https://github.com/mskcc/facets-suite" \
      org.opencontainers.image.title="Facets Tools" \
      org.opencontainers.image.description="Suite of Facets tools for copy number analysis"

ENV DEBIAN_FRONTEND=noninteractive
ENV HTSLIB_VERSION=1.5
ENV HTSTOOLS_VERSION=0.1.1
ENV FACETS_SUITE_VERSION=2.0.10
ENV FACETS_VERSION=0.5.14
ENV PCTGCDATA=0.3.0
ENV SNP_PILEUP=/usr/bin/snp-pileup
ENV PYTHONNOUSERSITE=set
ENV FACETS_OVERRIDE_EXITCODE=set
ENV LANG=C.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# ---------- R 3.6.3 + system deps ----------
# Add CRAN repo for R 3.6 on Focal (Posit signs packages for focal)
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        software-properties-common \
        dirmngr \
        gnupg \
        apt-transport-https \
        ca-certificates \
        wget \
    && wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc \
        | gpg --dearmor -o /usr/share/keyrings/r-project.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/r-project.gpg] https://cloud.r-project.org/bin/linux/ubuntu focal-cran35/" \
        > /etc/apt/sources.list.d/r-cran.list \
    && apt-get update -qq \
    # Pin R to exactly 3.6.3
    && apt-get install -y --no-install-recommends \
        r-base=3.6.3-1.2004.0 \
        r-base-dev=3.6.3-1.2004.0 \
        r-recommended=3.6.3-1.2004.0 \
    # tidyverse-equivalent system libraries
    && apt-get install -y --no-install-recommends \
        libxml2-dev \
        libcurl4-openssl-dev \
        libssl-dev \
        libpq-dev \
        libssh2-1-dev \
        unixodbc-dev \
        libsasl2-dev \
        libmariadb-dev \
    && apt-get install -y --no-install-recommends \
        apt-utils nano git \
        g++ tar bzip2 \
        libbz2-dev libc6-dev libxt-dev liblzma-dev \
        libgtk2.0-dev libcairo2-dev \
        xvfb xauth xfonts-base xdg-utils inotify-tools \
        python3 python3-pip python3-dev \
        fontconfig \
    # MS Core Fonts
    && echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections \
    && apt-get install -y --no-install-recommends ttf-mscorefonts-installer \
    && fc-cache -vr \
    # ---------- tidyverse + R packages ----------
    && R -e "options(repos=c(CRAN='https://packagemanager.posit.co/cran/__linux__/focal/2025-06-01')); \
        install.packages(c('tidyverse','dplyr','devtools','remotes','formatR','selectr','caTools','BiocManager', \
        'Cairo','argparse','gridExtra','binom','diptest','egg','shiny','shinyWidgets','shinyjs', \
        'rhandsontable','doParallel','configr','R.utils','shinyFiles','here','httr','jsonlite'), \
        Ncpus=parallel::detectCores())" \
    && R -e "options(repos=c(CRAN='https://packagemanager.posit.co/cran/__linux__/focal/2025-06-01')); \
        BiocManager::install('rtracklayer', ask=FALSE, update=FALSE)" \
    && R -q -e "remotes::install_version('bslib', version='0.7.0', repos='https://cloud.r-project.org')" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---------- htslib + htstools ----------
FROM builder AS download_and_unpack

WORKDIR /tmp

RUN wget -q "https://github.com/samtools/htslib/releases/download/${HTSLIB_VERSION}/htslib-${HTSLIB_VERSION}.tar.bz2" \
    && wget -q "https://github.com/mskcc/htstools/archive/snp_pileup_${HTSTOOLS_VERSION}.tar.gz" \
    && wget -q "https://github.com/mskcc/facets/archive/v${FACETS_VERSION}.tar.gz" -O "facets-v${FACETS_VERSION}.tar.gz" \
    && wget -q "https://github.com/mskcc/pctGCdata/archive/v${PCTGCDATA}.tar.gz" -O "pctGCdata-v${PCTGCDATA}.tar.gz" \
    && wget -q "https://github.com/mskcc/facets-suite/archive/${FACETS_SUITE_VERSION}.tar.gz" -O "facets-suite-${FACETS_SUITE_VERSION}.tar.gz" \
    && git clone --single-branch --branch master https://github.com/mskcc/facets-preview.git facets-preview-master \
    && tar xjf "htslib-${HTSLIB_VERSION}.tar.bz2" \
    && tar xzf "snp_pileup_${HTSTOOLS_VERSION}.tar.gz" \
    && tar xzf "facets-v${FACETS_VERSION}.tar.gz" \
    && tar xzf "pctGCdata-v${PCTGCDATA}.tar.gz" \
    && tar xzf "facets-suite-${FACETS_SUITE_VERSION}.tar.gz"

FROM download_and_unpack AS htslib_builder
WORKDIR "/tmp/htslib-${HTSLIB_VERSION}"
RUN ./configure && make && make install && cp libhts.so* /usr/lib

FROM htslib_builder AS htstools_builder
WORKDIR "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}"
RUN g++ -std=c++11 snp-pileup.cpp -lhts -o snp-pileup \
    && g++ -std=c++11 ppflag-fixer.cpp -lhts -o ppflag-fixer

FROM htstools_builder AS pctgcdata_builder
WORKDIR "/tmp/pctGCdata-${PCTGCDATA}"
RUN R CMD INSTALL .

# ---------- facets tools ----------
FROM pctgcdata_builder AS facets_builder
WORKDIR "/tmp/facets-${FACETS_VERSION}"
RUN R CMD INSTALL .

FROM facets_builder AS facets_suite_builder
WORKDIR "/tmp/facets-suite-${FACETS_SUITE_VERSION}"
RUN R CMD INSTALL .

FROM facets_suite_builder AS facets_preview_builder
WORKDIR /tmp/facets-preview-master
RUN mkdir -p inst/facets_qc \
    && cp -r facets_qc/* inst/facets_qc/ \
    && R CMD INSTALL .

# ---------- final image ----------
FROM facets_preview_builder AS final

COPY --from=htstools_builder "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}/snp-pileup" /usr/bin/
COPY --from=htstools_builder "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}/ppflag-fixer" /usr/bin/
COPY --from=facets_suite_builder "/tmp/facets-suite-${FACETS_SUITE_VERSION}/" /usr/bin/facets-suite/
COPY --from=facets_preview_builder "/tmp/facets-preview-master/" /usr/bin/facets-preview/

RUN apt-get clean && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*