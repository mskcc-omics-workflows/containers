FROM openjdk:8-jdk

################## ARGUMENTS ########################
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
      org.opencontainers.image.url="https://github.com/AstraZeneca-NGS/VarDictJava/tree/v${VARDICTJAVA_VERSION}" \
      org.opencontainers.image.created=${BUILD_DATE} \
      org.opencontainers.image.version=${BUILD_VERSION} \
      org.opencontainers.image.revision=${VCS_REF} \
      org.opencontainers.image.licenses=${LICENSE} \
      org.opencontainers.image.source="https://github.com/AstraZeneca-NGS/VarDictJava/tree/v${VARDICTJAVA_VERSION}" \
      org.opencontainers.image.description="This container uses OpenJDK 8 as the base image to build VarDictJava version ${VARDICTJAVA_VERSION} in a way that will be compatible with the nf-core module"

################## INSTALL DEPENDENCIES ########################
WORKDIR /opt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    r-base \
    perl \
    curl \
    wget \
    unzip \
    git \
    gradle \
    tabix \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

################## INSTALL VARDICTJAVA ########################
WORKDIR /opt
RUN git clone --branch v${VARDICTJAVA_VERSION} --recurse-submodules https://github.com/AstraZeneca-NGS/VarDictJava.git && \
    cd VarDictJava && \
    ./gradlew clean installApp 

################## CREATE ALIASES ########################
WORKDIR  /opt/VarDictJava/VarDict/
RUN chmod +x /opt/VarDictJava/VarDict/var2vcf_paired.pl \
    && chmod +x /opt/VarDictJava/VarDict/testsomatic.R
ENV PATH="/opt/VarDictJava/VarDict/:$PATH"

WORKDIR /opt/VarDictJava/VarDict
RUN ln -s /opt/VarDictJava/build/install/VarDict/bin/VarDict /usr/local/bin/vardict-java 
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /opt/VarDictJava/VarDict/