FROM ghcr.io/mskcc-omics-workflows/r_tidyverse:3.6.3 AS runtime_base

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2026-03-31T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="1.0.0" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/somatic_germline/" \
      org.opencontainers.image.url="https://github.com/taylor-lab/somatic-germline-workflow" \
      org.opencontainers.image.title="Somatic Germline" \
      org.opencontainers.image.description="Container for the Somatic-Germline workflow"

ENV DEBIAN_FRONTEND=noninteractive \
    HTSLIB_VERSION=1.5 \
    HTSTOOLS_VERSION=0.1.1 \
    FACETS_SUITE_VERSION=2.0.10 \
    FACETS_VERSION=0.5.14 \
    PCTGCDATA=0.3.0 \
    BWA_VERSION=0.7.5a \
    SAMTOOLS_VERSION=0.1.19 \
    FASTQC_VERSION=0.11.9 \
    PYTHONNOUSERSITE=set \
    FACETS_OVERRIDE_EXITCODE=set \
    SOMATIC_GERMLINE_TOOLS=https://mskcc.jfrog.io/artifactory/omicswf-generic-prod-local/somatic_germline_tools.tar.gz \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        git \
        python3 \
        python3-dev \
        python3-pip \
        gcc \
        default-jdk \
        perl \
        perl-modules \
        bedtools \
        procps \
        tar \
        unzip \
        bzip2 \
        libcurl4-openssl-dev \
    && pip3 install --no-cache-dir \
        numpy pandas python-dateutil pytz six cutadapt==4.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM runtime_base AS build_base

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        libbz2-dev \
        libc6-dev \
        libncurses-dev \
        libxt-dev \
        liblzma-dev \
        python3-dev \
    && R -e "options(repos=c(CRAN='https://packagemanager.posit.co/cran/__linux__/jammy/2025-06-01')); \
    install.packages(c('plyr','diptest','DT','bit','bit64','Ckmeans.1d.dp','gplots','memoise', \
    'rappdirs','rbibutils','Rdpack','tinytex','crosstalk'), Ncpus=parallel::detectCores()); \
    if (!requireNamespace('BiocManager', quietly=TRUE)) install.packages('BiocManager'); \
    BiocManager::install('DNAcopy', ask=FALSE, update=FALSE)" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM build_base AS download_and_unpack

WORKDIR /tmp

RUN --mount=type=secret,id=MSK_JFROG_USERNAME \
    --mount=type=secret,id=MSK_JFROG_TOKEN \
    wget --progress=dot:giga --directory-prefix /tmp --user="$(cat /run/secrets/MSK_JFROG_USERNAME)" --password="$(cat /run/secrets/MSK_JFROG_TOKEN)" "${SOMATIC_GERMLINE_TOOLS}" \
    && wget -q "https://github.com/samtools/htslib/releases/download/${HTSLIB_VERSION}/htslib-${HTSLIB_VERSION}.tar.bz2" \
    && wget -q "https://github.com/mskcc/htstools/archive/snp_pileup_${HTSTOOLS_VERSION}.tar.gz" \
    && wget -q "https://github.com/mskcc/facets/archive/v${FACETS_VERSION}.tar.gz" -O "facets-v${FACETS_VERSION}.tar.gz" \
    && wget -q "https://github.com/mskcc/pctGCdata/archive/v${PCTGCDATA}.tar.gz" -O "pctGCdata-v${PCTGCDATA}.tar.gz" \
    && wget -q "https://github.com/mskcc/facets-suite/archive/${FACETS_SUITE_VERSION}.tar.gz" -O "facets-suite-${FACETS_SUITE_VERSION}.tar.gz" \
    && wget -q "https://sourceforge.net/projects/bio-bwa/files/bwa-${BWA_VERSION}.tar.bz2" \
    && wget -q "https://sourceforge.net/projects/samtools/files/samtools/${SAMTOOLS_VERSION}/samtools-${SAMTOOLS_VERSION}.tar.bz2" \
    && wget -q "https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v${FASTQC_VERSION}.zip" \
    && git clone --single-branch --branch master https://github.com/mskcc/facets-preview.git facets-preview-master \
    && tar -xzf /tmp/somatic_germline_tools.tar.gz -C /tmp \
    && rm /tmp/tools.tar.gz \
    && tar xjf "htslib-${HTSLIB_VERSION}.tar.bz2" \
    && tar xzf "snp_pileup_${HTSTOOLS_VERSION}.tar.gz" \
    && tar xzf "facets-v${FACETS_VERSION}.tar.gz" \
    && tar xzf "pctGCdata-v${PCTGCDATA}.tar.gz" \
    && tar xzf "facets-suite-${FACETS_SUITE_VERSION}.tar.gz" \
    && tar xjf "bwa-${BWA_VERSION}.tar.bz2" \
    && tar xjf "samtools-${SAMTOOLS_VERSION}.tar.bz2" \
    && unzip -q "fastqc_v${FASTQC_VERSION}.zip" \
    && rm -f "fastqc_v${FASTQC_VERSION}.zip"

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

FROM download_and_unpack AS sg_tools_builder

ARG TARGETPLATFORM

RUN mkdir -p /usr/bin/tools/bwa \
    /usr/bin/tools/samtools \
    /usr/bin/tools/trim_galore \
    /usr/bin/tools/igvtools \
    /usr/bin/tools/mutect \
    /usr/bin/tools/picard

WORKDIR /tmp/bwa-${BWA_VERSION}
# Arm64 build: use sse2neon compatibility header to map SSE intrinsics to NEON
RUN case "${TARGETPLATFORM}" in \
    *arm64*) wget -q -O /usr/local/include/sse2neon.h https://raw.githubusercontent.com/DLTcollab/sse2neon/master/sse2neon.h \
        && printf '#ifndef __EMMINTRIN_H\n#define __EMMINTRIN_H\n#include "sse2neon.h"\n#endif\n' > /usr/local/include/emmintrin.h ;; \
    esac \
    && make -j"$(nproc)" \
    && cp bwa /usr/bin/tools/bwa/

WORKDIR /tmp/samtools-${SAMTOOLS_VERSION}
RUN make -j"$(nproc)" \
    && cp samtools /usr/bin/tools/samtools/ \
    && cp misc/*.pl /usr/bin/tools/samtools/

RUN cp -r /tmp/tools/IGVTools_v2.3.12/. /usr/bin/tools/igvtools/ \
    && cp -r /tmp/tools/muTect-1.1.4/. /usr/bin/tools/mutect/ \
    && cp -r /tmp/tools/picard-tools-1.96/. /usr/bin/tools/picard/ \
    && cp -r /tmp/tools/trimgalore-0.2.5.mod/. /usr/bin/tools/trim_galore/ \
    && cp -r /tmp/FastQC /usr/bin/tools/FastQC \
    && chmod -R +x /usr/bin/tools/*

FROM runtime_base AS final

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PATH=/usr/bin/tools:/usr/bin:$PATH

COPY --from=htslib_builder /usr/lib/libhts.so* /usr/lib/
COPY --from=htstools_builder "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}/snp-pileup" /usr/bin/
COPY --from=htstools_builder "/tmp/htstools-snp_pileup_${HTSTOOLS_VERSION}/ppflag-fixer" /usr/bin/
COPY --from=facets_suite_builder "/tmp/facets-suite-${FACETS_SUITE_VERSION}/" /usr/bin/facets-suite/
COPY --from=facets_preview_builder "/tmp/facets-preview-master/" /usr/bin/facets-preview/
COPY --from=facets_preview_builder /usr/local/lib/R/site-library/ /usr/local/lib/R/site-library/
COPY --from=sg_tools_builder /usr/bin/tools/ /usr/bin/tools/

RUN ln -sf /usr/bin/tools/bwa/bwa /usr/bin/bwa \
    && ln -sf /usr/bin/tools/samtools/samtools /usr/bin/samtools \
    && ln -sf /usr/bin/tools/trim_galore/trim_galore /usr/bin/trim_galore \
    && ln -sf /usr/bin/tools/igvtools/igvtools /usr/bin/igvtools \
    && ln -sf /usr/bin/tools/FastQC/fastqc /usr/bin/fastqc \
    && chmod +x /usr/bin/tools/*/* 2>/dev/null || true \
    && rm -rf /tmp/* /var/tmp/* \
    && R --vanilla -e ' \
    pkgs <- list( \
        plyr=NULL, \
        diptest=NULL, \
        DT=NULL, \
        bit=NULL, \
        bit64=NULL, \
        Ckmeans.1d.dp=NULL, \
        gplots=NULL, \
        memoise=NULL, \
        rappdirs=NULL, \
        rbibutils=NULL, \
        Rdpack=NULL, \
        tinytex=NULL, \
        crosstalk=NULL, \
        DNAcopy=NULL, \
        pctGCdata=Sys.getenv("PCTGCDATA"), \
        facets=Sys.getenv("FACETS_VERSION"), \
        facetsSuite=NULL, \
        facetsPreview=NULL); \
    failed <- c(); \
    for (p in names(pkgs)) { \
        if (!requireNamespace(p, quietly=TRUE)) { \
            failed <- c(failed, p); \
        } else { \
            ver <- as.character(packageVersion(p)); \
            expected <- pkgs[[p]]; \
            cat(sprintf("  %-20s %s\n", p, ver)); \
            if (!is.null(expected) && ver != expected) \
                stop(sprintf("Version mismatch for %s: expected %s, got %s", \
                    p, expected, ver)); \
        } \
    }; \
    if (length(failed) > 0) \
        stop("The following R packages failed to load: ", \
            paste(failed, collapse=", ")); \
    message("All R package version checks passed.") \
    ' \
    && bwa > /tmp/bwa.log 2>&1 || true \
    && grep -q "${BWA_VERSION}" /tmp/bwa.log \
    && samtools > /tmp/samtools.log 2>&1 || true \
    && grep -q "${SAMTOOLS_VERSION}" /tmp/samtools.log \
    && bedtools --version | grep -q 'bedtools' \
    && fastqc --version | grep -q "${FASTQC_VERSION}" \
    && cutadapt --version \
    && python3 --version \
    && snp-pileup --help 2>&1 | grep -q 'vcf file' \
    && ppflag-fixer --help 2>&1 | grep -q 'input file' \
    && /usr/bin/facets-suite/run-facets-wrapper.R --help | grep -q 'COUNTS_FILE' \
    && java -version \
    && rm -rf /tmp/* \
    && echo "All binary tool version checks passed (htstools ${HTSTOOLS_VERSION}, bwa ${BWA_VERSION}, samtools ${SAMTOOLS_VERSION}, fastqc ${FASTQC_VERSION})."

CMD ["/bin/bash"]