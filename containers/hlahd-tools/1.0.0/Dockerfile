# hlahd-tools — Python/bioinformatics runtime for the msk annotate_hlahd module
# (and future HLA-HD post-processing modules), with the mskcc/hla-annotate
# package (https://github.com/mskcc/hla-annotate) installed on top.
FROM condaforge/miniforge3:25.3.1-0

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org)" \
      org.opencontainers.image.created="2026-08-26T00:00:00Z" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="1.0.0" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/hlahd-tools/" \
      org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/modules" \
      org.opencontainers.image.title="hlahd-tools" \
      org.opencontainers.image.description="Python + bowtie2/samtools runtime for HLA-HD post-processing modules (e.g. annotate_hlahd), with mskcc/hla-annotate installed."

ENV HLA_ANNOTATE_TAG=v1.0.0

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# bowtie2/samtools are on PATH for modules that shell out to them (e.g. a future
# pileup-evidence module); weasyprint comes from conda-forge (not pip) so its
# pango/cairo/harfbuzz system libraries install alongside it.
RUN mamba install -y -c conda-forge -c bioconda \
        python=3.11 \
        bowtie2=2.5.5 \
        samtools=1.21 \
        pysam \
        matplotlib \
        requests \
        weasyprint \
        git \
        pip \
    && mamba clean -afy

# hla-annotate is private, so cloning it needs a token (fine-grained PAT, read-only,
# scoped to just this repo) passed as a BuildKit secret — never baked into the image.
# Tests run at build time so a broken release fails the image build, not a pipeline run.
RUN --mount=type=secret,id=MSK_GH_TOKEN \
    git clone --depth 1 --branch ${HLA_ANNOTATE_TAG} \
        "https://x-access-token:$(cat /run/secrets/MSK_GH_TOKEN)@github.com/mskcc/hla-annotate.git" \
        /tmp/hla-annotate \
    && pip install --no-cache-dir -e '/tmp/hla-annotate[dev]' \
    && pytest /tmp/hla-annotate \
    && pip install --no-cache-dir --no-deps --force-reinstall /tmp/hla-annotate \
    && rm -rf /tmp/hla-annotate

# matplotlib/fontconfig write caches on first use; $HOME is not writable under
# Nextflow's container user mapping.
ENV MPLCONFIGDIR=/tmp/mplconfig \
    XDG_CACHE_HOME=/tmp/cache

WORKDIR /data
