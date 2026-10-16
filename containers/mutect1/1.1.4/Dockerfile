FROM mskcc/openjdk:6

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2026-06-16T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="1.0.0" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/broadinstitute/mutect/tree/1.1.4" \
      org.opencontainers.image.url="https://github.com/broadinstitute/mutect" \
      org.opencontainers.image.title="Mutect" \
      org.opencontainers.image.description="Container for Mutect 1.1.4"

ENV DEBIAN_FRONTEND=noninteractive \
    MUTECT_SOURCE=https://mskcc.jfrog.io/artifactory/omicswf-generic-prod-local/mutect_1.1.4/muTect.jar \
    MUTECT_VERSION=1.1.4 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN --mount=type=secret,id=MSK_JFROG_USERNAME \
    --mount=type=secret,id=MSK_JFROG_TOKEN \
    echo "deb http://archive.debian.org/debian/ wheezy main contrib non-free" > /etc/apt/sources.list \
    && echo "deb-src http://archive.debian.org/debian/ wheezy main contrib non-free" >> /etc/apt/sources.list \
    && echo "Acquire::Check-Valid-Until false;" > /etc/apt/apt.conf.d/10-nocheckvalid \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        procps \
        tar \
        unzip \
        bzip2 \
    && wget --progress=dot:giga --no-check-certificate --directory-prefix /usr/bin/ --user="$(cat /run/secrets/MSK_JFROG_USERNAME)" --password="$(cat /run/secrets/MSK_JFROG_TOKEN)" "${MUTECT_SOURCE}" \
    && { java -jar /usr/bin/muTect.jar > /tmp/mutect.log 2>&1 || true; } \
    && grep -qi "mutect\\|${MUTECT_VERSION}" /tmp/mutect.log \
    && apt-get clean \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
