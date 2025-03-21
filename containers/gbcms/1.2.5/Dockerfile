################## BASE IMAGE ######################

FROM ubuntu:16.04

################## ARGUMENTS########################

ARG BUILD_DATE="2024-12-12T15:08:40Z"
ARG BUILD_VERSION
ARG LICENSE="Apache-2.0"
ARG GBCMS_VERSION=1.2.5
ARG VCS_REF
################## METADATA ########################

LABEL org.opencontainers.image.vendor="MSKCC"
LABEL org.opencontainers.image.authors="Ronak Shah (shahr2@mskcc.org)"

LABEL org.opencontainers.image.title="GBCMS"\
	org.opencontainers.image.version.gbcms=${GBCMS_VERSION} \
	org.opencontainers.image.url="https://github.com/mskcc/GetBaseCountsMultiSample" \
	org.opencontainers.image.created=${BUILD_DATE} \
	org.opencontainers.image.version=${BUILD_VERSION} \
	org.opencontainers.image.revision=${VCS_REF} \
	org.opencontainers.image.licenses=${LICENSE} \
	org.opencontainers.image.source="https://github.com/msk-access/GetBaseCountsMultiSample/releases/" \ 
	org.opencontainers.image.description="This container uses Ubuntu 16.04 as the base image to build GetBaseCountsMultiSample version ${GBCMS_VERSION}"

################## INSTALL ##########################

WORKDIR /usr/src

RUN apt-get update && \
	apt-get --no-install-recommends install -y \
	wget ca-certificates openssl gcc g++ make zlib1g-dev cmake libjsoncpp-dev && \
	apt-get clean autoclean && \
	apt-get autoremove -y && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


WORKDIR /usr/src
# Download and extract the tarball
RUN wget -q --no-check-certificate "https://github.com/msk-access/GetBaseCountsMultiSample/archive/refs/tags/${GBCMS_VERSION}.tar.gz" && \
	tar -xzvf ${GBCMS_VERSION}.tar.gz && \
	rm ${GBCMS_VERSION}.tar.gz

WORKDIR /usr/src/GetBaseCountsMultiSample-${GBCMS_VERSION}/bamtools-master

# Clean, build, and install bamtools
RUN rm -r build/ && \
	mkdir build

WORKDIR /usr/src/GetBaseCountsMultiSample-${GBCMS_VERSION}/bamtools-master/build

RUN cmake -DCMAKE_CXX_FLAGS=-std=c++03 .. && \
	make && \
	make install && \
	cp ../lib/libbamtools.so.2.3.0 /usr/lib/
	
# Switch to the main GetBaseCountsMultiSample directory
WORKDIR /usr/src/GetBaseCountsMultiSample-${GBCMS_VERSION}
# Build GetBaseCountsMultiSample
RUN make && \
	cp GetBaseCountsMultiSample /usr/local/bin/
	