FROM ghcr.io/mskcc-omics-workflows/r_tidyverse:3.6.3 AS runtime_base

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Adam Price (price2@mskcc.org), Anne Marie Noronha (noronhaa@mskcc.org), Yixiao Gong (gongy@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org), Philip Jonsson (jonssonp@mskcc.org), Ryan Ptashkin (ptashkir@mskcc.org)" \
      org.opencontainers.image.created="2026-08-06T00:00:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="3.0.0" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/facets_tools_2n/" \
      org.opencontainers.image.url="https://github.com/mskcc/facets-suite-2n" \
      org.opencontainers.image.title="Facets Tools 2N" \
      org.opencontainers.image.description="FACETS copy number suite for the unmatched-normal (2N) workflow: facets-suite-2n 3.0.0, facets2n, facets, snp-pileup and facets-preview."

ENV DEBIAN_FRONTEND=noninteractive \
    HTSLIB_VERSION=1.5 \
    HTSTOOLS_VERSION=0.1.1 \
    FACETS_SUITE_VERSION=3.0.0 \
    FACETS_VERSION=0.5.14 \
    PCTGCDATA=0.3.0 \
    DATA_TABLE_VERSION=1.17.4 \
    SNP_PILEUP=/usr/bin/snp-pileup \
    PYTHONNOUSERSITE=set \
    FACETS_OVERRIDE_EXITCODE=set \
    LANG=C.UTF-8

# facets2n, facets-suite-2n and facets-preview have no release tags at these
# versions, so each is pinned to an explicit commit rather than a branch tip to
# keep rebuilds reproducible. FACETS2N_SHA carries the flat-genome dipLogR guard
# in findDiploidLogR.
ENV FACETS2N_SHA=34016dcbbfdc8dc5583388a782bd442a545a683c \
    FACETS_SUITE_2N_SHA=d66ad19499181b1f8c557619e5b7e0652c94ea5c \
    FACETS_PREVIEW_SHA=a78fe1708665c17223893c63084805bb2639217d

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        python3 \
        python3-pip \
        wget \
        xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM runtime_base AS build_base

# The r_tidyverse base already carries Cairo, argparse, gridExtra, binom, egg,
# shiny, shinyWidgets, shinyjs, rhandsontable, doParallel, configr, R.utils,
# shinyFiles, here, dplyr, httr, jsonlite, data.table, lifecycle, bit64,
# lubridate, digest, glue, stringr, bslib and rtracklayer, so only these four
# need installing here.
#
# bslib is not pinned. It is only ever a transitive dependency of shiny and
# shinyWidgets -- no facets code references it. The base's shiny 1.7.3 needs
# bslib (>= 0.3.0), which the base's 0.4.1 satisfies.
#
# reshape2 is not required by any of the three packages' DESCRIPTIONs, but
# facets-preview ships a top-level arranging_facets.R that calls
# library(reshape2), and that script is copied into the image below. It is kept
# so that script stays runnable.
#
# data.table is upgraded past the base's snapshot version. facets-suite-2n only
# declares data.table (>= 1.11.8), but it leans on it heavily, so this pins the
# version the 2N pipeline was actually validated against rather than inheriting
# whatever the base's CRAN snapshot happens to carry. The final stage asserts
# the exact version, so a base bump cannot silently move it.
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        build-essential \
        bzip2 \
        gfortran \
        libbz2-dev \
        libc6-dev \
        libcurl4-openssl-dev \
        liblzma-dev \
        libxt-dev \
        python3-dev \
        tar \
        zlib1g-dev \
    && R -e "options(repos = Sys.getenv('CRAN_MIRROR')); \
    install.packages(c('plyr','diptest','DT','reshape2'), type = 'source')" \
    && R -e "remotes::install_version('data.table', version = Sys.getenv('DATA_TABLE_VERSION'), \
    repos = 'https://cloud.r-project.org', upgrade = 'never')" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM build_base AS download_and_unpack

WORKDIR /tmp

RUN wget -q "https://github.com/samtools/htslib/releases/download/${HTSLIB_VERSION}/htslib-${HTSLIB_VERSION}.tar.bz2" \
    && wget -q "https://github.com/mskcc/htstools/archive/snp_pileup_${HTSTOOLS_VERSION}.tar.gz" \
    && wget -q "https://github.com/mskcc/facets/archive/v${FACETS_VERSION}.tar.gz" -O "facets-v${FACETS_VERSION}.tar.gz" \
    && wget -q "https://github.com/mskcc/pctGCdata/archive/v${PCTGCDATA}.tar.gz" -O "pctGCdata-v${PCTGCDATA}.tar.gz" \
    && tar xjf "htslib-${HTSLIB_VERSION}.tar.bz2" \
    && tar xzf "snp_pileup_${HTSTOOLS_VERSION}.tar.gz" \
    && tar xzf "facets-v${FACETS_VERSION}.tar.gz" \
    && tar xzf "pctGCdata-v${PCTGCDATA}.tar.gz" \
    && git clone --quiet https://github.com/mskcc/facets2n.git facets2n \
    && git -C facets2n checkout --quiet "${FACETS2N_SHA}" \
    && git clone --quiet https://github.com/mskcc/facets-suite-2n.git "facets-suite-${FACETS_SUITE_VERSION}" \
    && git -C "facets-suite-${FACETS_SUITE_VERSION}" checkout --quiet "${FACETS_SUITE_2N_SHA}" \
    && git clone --quiet https://github.com/mskcc/facets-preview.git facets-preview \
    && git -C facets-preview checkout --quiet "${FACETS_PREVIEW_SHA}"

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

FROM facets_builder AS facets2n_builder
WORKDIR /tmp/facets2n
RUN R CMD INSTALL .

FROM facets2n_builder AS facets_suite_builder
WORKDIR "/tmp/facets-suite-${FACETS_SUITE_VERSION}"
RUN R CMD INSTALL .

FROM facets_suite_builder AS facets_preview_builder
WORKDIR /tmp/facets-preview
RUN mkdir -p inst/facets_qc \
    && cp -r facets_qc/. inst/facets_qc/ \
    && R CMD INSTALL .

FROM runtime_base AS final

COPY --from=htslib_builder /usr/lib/libhts.so* /usr/lib/
COPY --from=htstools_builder "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}/snp-pileup" /usr/bin/
COPY --from=htstools_builder "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}/ppflag-fixer" /usr/bin/
COPY --from=facets_suite_builder "/tmp/facets-suite-${FACETS_SUITE_VERSION}/" /usr/bin/facets-suite/
COPY --from=facets_preview_builder /tmp/facets-preview/ /usr/bin/facets-preview/
COPY --from=facets_preview_builder /usr/local/lib/R/site-library/ /usr/local/lib/R/site-library/

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /

RUN rm -rf /tmp/* /var/tmp/* \
    && ldconfig \
    # ---------- verify R packages ----------
    && R --vanilla -e " \
    pkgs <- list( \
        plyr          = NULL, \
        diptest       = NULL, \
        DT            = NULL, \
        reshape2      = NULL, \
        rtracklayer   = NULL, \
        data.table    = Sys.getenv('DATA_TABLE_VERSION'), \
        pctGCdata     = Sys.getenv('PCTGCDATA'), \
        facets        = Sys.getenv('FACETS_VERSION'), \
        facets2n      = NULL, \
        facetsSuite   = Sys.getenv('FACETS_SUITE_VERSION'), \
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
    # ---------- verify the pinned facets2n flat-genome dipLogR guard ----------
    && R --vanilla -e " \
    src <- paste(deparse(facets2n:::findDiploidLogR), collapse = ' '); \
    if (!grepl('length(cn2logR) == 0', src, fixed = TRUE)) \
        stop('facets2n is missing the flat-genome dipLogR guard; wrong revision installed.'); \
    message('facets2n flat-genome dipLogR guard present.')" \
    # ---------- verify binary tools ----------
    && snp-pileup --help 2>&1 | grep -q 'vcf file' \
    && ppflag-fixer --help 2>&1 | grep -q 'input file' \
    && /usr/bin/facets-suite/run-facets-wrapper.R --help | grep -q 'COUNTS_FILE' \
    # 2N-specific flags: assert this is facets-suite-2n and not stock facets-suite
    && /usr/bin/facets-suite/run-facets-wrapper.R --help | grep -q 'facets2n-lib-path' \
    && /usr/bin/facets-suite/run-facets-wrapper.R --help | grep -q 'MandUnormal' \
    && /usr/bin/facets-suite/snp-pileup-wrapper.R --help | grep -q 'unmatched-normal-BAMS'

CMD ["/bin/bash"]
