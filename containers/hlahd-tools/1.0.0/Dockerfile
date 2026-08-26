# hlahd-tools — generic Python/bioinformatics runtime for the msk annotate_hlahd
# module (and future HLA-HD post-processing modules). The module scripts
# themselves live in modules/msk/annotate_hlahd/resources/usr/bin/ and are
# staged onto PATH by Nextflow — this image supplies only the interpreter,
# system libraries, and third-party packages they depend on.
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
      org.opencontainers.image.description="Python + bowtie2/samtools runtime for HLA-HD post-processing modules (e.g. annotate_hlahd)."

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# bowtie2/samtools are on PATH for modules that shell out to them (e.g. a future
# pileup-evidence module); weasyprint comes from conda-forge (not pip) so its
# pango/cairo/harfbuzz system libraries install alongside it.
RUN mamba install -y -c conda-forge -c bioconda \
        python=3.11 \
        bowtie2=2.5.5 \
        samtools=1.21 \
        pandas \
        jinja2 \
        pysam \
        matplotlib \
        requests \
        weasyprint \
    && mamba clean -afy

# matplotlib/fontconfig write caches on first use; $HOME is not writable under
# Nextflow's container user mapping.
ENV MPLCONFIGDIR=/tmp/mplconfig \
    XDG_CACHE_HOME=/tmp/cache

WORKDIR /data
