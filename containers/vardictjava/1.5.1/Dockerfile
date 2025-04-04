################## BASE IMAGE ######################

FROM ubuntu:22.04

################## ARGUMENTS########################

ARG BUILD_DATE="2025-04-04T14:23:15Z"
ARG BUILD_VERSION="0.0.1"
ARG LICENSE="MIT License"
ARG VARDICTJAVA_VERSION=1.5.1
ARG VCS_REF
ENV DEBIAN_FRONTEND=noninteractive
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
WORKDIR /
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
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

# Detect Java 8 directory using ls and set JAVA_HOME + PATH
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# # Install VarDictJava v1.5.1
WORKDIR /opt
RUN git clone --recursive https://github.com/AstraZeneca-NGS/VarDictJava.git \
    && cd VarDictJava \
    && git checkout v1.5.1 \ 
    && ./gradlew clean installApp

# # Make VarDict and helpers accessible system-wide
# Create a script for vardict-java to point to the actual executable
WORKDIR /
RUN printf '#!/bin/bash\n/opt/VarDictJava/build/install/VarDict/bin/VarDict "$@"' > /usr/local/bin/vardict-java && \
    chmod +x /usr/local/bin/vardict-java

# Symlink Perl script (var2vcf_valid.pl) and make it executable
WORKDIR /
RUN printf '#!/bin/bash\n perl /opt/VarDictJava/VarDict/var2vcf_valid.pl "$@"' > /usr/local/bin/var2vcf_valid.pl && \
    chmod +x /usr/local/bin/var2vcf_valid.pl

# Symlink R script (testsomatic.R) and make it executable
WORKDIR /
RUN printf '#!/bin/bash\n Rscript /opt/VarDictJava/VarDict/testsomatic.R "$@"' > /usr/local/bin/testsomatic.R && \
    chmod +x /usr/local/bin/testsomatic.R

ENV PATH="/usr/local/bin:$PATH"