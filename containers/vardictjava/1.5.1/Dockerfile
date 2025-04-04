################## BASE IMAGE ######################

FROM ubuntu:22.04

################## ARGUMENTS########################

ARG BUILD_DATE="2025-04-04T14:23:15Z"
ARG BUILD_VERSION="0.0.1"
ARG LICENSE="MIT License"
ARG VARDICTJAVA_VERSION=1.5.1
ARG VCS_REF
################## METADATA ########################

LABEL org.opencontainers.image.vendor="MSKCC"
LABEL org.opencontainers.image.authors="Eric Buehler (buehlere@mskcc.org)"

LABEL org.opencontainers.image.title="VARDICTJAVA"\
	org.opencontainers.image.version.VARDICTJAVA=${VARDICTJAVA_VERSION} \
	org.opencontainers.image.url="https://github.com/AstraZeneca-NGS/VarDictJava/tree/v1.5.1" \
	org.opencontainers.image.created=${BUILD_DATE} \
	org.opencontainers.image.version=${BUILD_VERSION} \
	org.opencontainers.image.revision=${VCS_REF} \
	org.opencontainers.image.licenses=${LICENSE} \
	org.opencontainers.image.source="https://github.com/AstraZeneca-NGS/VarDictJava/tree/v1.5.1" \ 
	org.opencontainers.image.description="This container uses Ubuntu 22.04 as the base image to build VarDictJava version ${VARDICTJAVA_VERSION} in a way that will be compatible with the nf-core module"

################## INSTALL ##########################

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    r-base \
    perl \
    curl \
    wget \
    unzip \
    git \
    gradle \
    tabix \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install VarDictJava v1.5.1
WORKDIR /opt
RUN git clone --branch v1.5.1 https://github.com/AstraZeneca-NGS/VarDictJava.git \
    && cd VarDictJava \
    && gradle build

# Make VarDict and helpers accessible system-wide
RUN ln -s /opt/VarDictJava/build/libs/VarDict.jar /usr/local/bin/VarDict.jar && \
    echo -e '#!/bin/bash\njava -jar /usr/local/bin/VarDict.jar "$@"' > /usr/local/bin/vardict-java && \
    chmod +x /usr/local/bin/vardict-java && \
    ln -s /opt/VarDictJava/VarDict /usr/local/bin/VarDict

# Link helper scripts with aliases
RUN ln -s /opt/VarDictJava/var2vcf_valid.pl /usr/local/bin/var2vcf_valid.pl && \
    ln -s /opt/VarDictJava/testsomatic.R /usr/local/bin/testsomatic.R && \
    echo -e '#!/bin/bash\nperl /usr/local/bin/var2vcf_valid.pl "$@"' > /usr/local/bin/var2vcf_valid && \
    chmod +x /usr/local/bin/var2vcf_valid && \
    echo -e '#!/bin/bash\nRscript /usr/local/bin/testsomatic.R "$@"' > /usr/local/bin/testsomatic && \
    chmod +x /usr/local/bin/testsomatic
