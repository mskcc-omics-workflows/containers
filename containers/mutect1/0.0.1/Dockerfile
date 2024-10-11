################## BASE IMAGE ######################
FROM openjdk:7

################## ARGUMENTS/Environments ##########

ARG BUILD_DATE
ARG BUILD_VERSION=0.1.0
ARG MUTECT_VERSION=1.1.5

################## METADATA ########################

LABEL   org.opencontainers.image.url="https://github.com/broadinstitute/mutect" \
	org.opencontainers.image.created=${BUILD_DATE} \
	org.opencontainers.image.authors="Yu Hu"  \
	org.opencontainers.image.source="https://github.com/broadinstitute/mutect/releases/download/${MUTECT_VERSION}/muTect-${MUTECT_VERSION}-bin.zip" \
	org.opencontainers.image.version=${BUILD_VERSION} \
	org.opencontainers.image.title="mutect1" \
	org.opencontainers.image.description="This container uses java7 as the base image to build mutect version ${MUTECT_VERSION}" 
LABEL org.opencontainers.image.vendor="MSKCC"
LABEL org.opencontainers.image.authors="Yu Hu" 


################## INSTALL ##########################

ENV MUTECT_VERSION=${MUTECT_VERSION}

#Get Mutect
RUN wget https://github.com/broadinstitute/mutect/releases/download/${MUTECT_VERSION}/muTect-${MUTECT_VERSION}-bin.zip
RUN unzip muTect-${MUTECT_VERSION}-bin.zip
RUN rm muTect-${MUTECT_VERSION}-bin.zip
RUN chmod a+x muTect-${MUTECT_VERSION}.jar
RUN mv muTect-${MUTECT_VERSION}.jar /usr/local/bin/muTect.jar
