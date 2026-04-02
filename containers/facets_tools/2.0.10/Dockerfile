FROM ghcr.io/mskcc-omics-workflows/r_tidyverse:3.6.3 AS runtime_base

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

ENV DEBIAN_FRONTEND=noninteractive \
    HTSLIB_VERSION=1.5 \
    HTSTOOLS_VERSION=0.1.1 \
    FACETS_SUITE_VERSION=2.0.10 \
    FACETS_VERSION=0.5.14 \
    PCTGCDATA=0.3.0 \
    SNP_PILEUP=/usr/bin/snp-pileup \
    PYTHONNOUSERSITE=set \
    FACETS_OVERRIDE_EXITCODE=set \
    LANG=C.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        git \
        python3 \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM runtime_base AS build_base

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        build-essential \
        tar \
        bzip2 \
        gfortran \
        libbz2-dev \
        libc6-dev \
        libxt-dev \
        liblzma-dev \
        python3-dev \
    && R -e "options(repos=Sys.getenv('CRAN_MIRROR')); \
    install.packages(c('plyr','diptest','DT'), type = 'source')" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM build_base AS download_and_unpack

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

FROM runtime_base AS final

COPY --from=htslib_builder /usr/lib/libhts.so* /usr/lib/
COPY --from=htstools_builder "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}/snp-pileup" /usr/bin/
COPY --from=htstools_builder "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}/ppflag-fixer" /usr/bin/
COPY --from=facets_suite_builder "/tmp/facets-suite-${FACETS_SUITE_VERSION}/" /usr/bin/facets-suite/
COPY --from=facets_preview_builder "/tmp/facets-preview-master/" /usr/bin/facets-preview/
COPY --from=facets_preview_builder /usr/local/lib/R/site-library/ /usr/local/lib/R/site-library/

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN rm -rf /tmp/* /var/tmp/* \
    # ---------- verify R packages ----------
    && R --vanilla -e " \
    pkgs <- list( \
        plyr        = NULL, \
        diptest     = NULL, \
        DT          = NULL, \
        pctGCdata   = Sys.getenv('PCTGCDATA'), \
        facets      = Sys.getenv('FACETS_VERSION'), \
        facetsSuite = NULL, \
        facetsPreview = NULL \
    ); \
    failed <- c(); \
    for (p in names(pkgs)) { \
        if (!requireNamespace(p, quietly = TRUE)) { \
            failed <- c(failed, p); \
        } else { \
            ver <- as.character(packageVersion(p)); \
            expected <- pkgs[[p]]; \
            cat(sprintf('  %-20s %s\n', p, ver)); \
            if (!is.null(expected) && ver != expected) \
                stop(sprintf('Version mismatch for %s: expected %s, got %s', p, expected, ver)); \
        } \
    }; \
    if (length(failed) > 0) \
        stop('The following R packages failed to load: ', paste(failed, collapse = ', ')); \
    message('All R package version checks passed.')" \
    # ---------- verify binary tools ----------
    && snp-pileup --help 2>&1 | grep -q 'vcf file' \
    && ppflag-fixer --help 2>&1 | grep -q 'input file' \
    && /usr/bin/facets-suite/run-facets-wrapper.R --help | grep -q 'COUNTS_FILE'

CMD ["/bin/bash"]
