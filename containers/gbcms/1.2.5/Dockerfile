################## BUILD STAGE ######################
# Kept on ubuntu:16.04 to match the toolchain this codebase (GetBaseCountsMultiSample
# + its vendored bamtools-master, built with -std=c++03) has always been built with.
FROM ubuntu:16.04 AS builder

ARG GBCMS_VERSION=1.2.5

WORKDIR /usr/src

RUN apt-get update && \
	apt-get install --no-install-recommends -y \
	wget ca-certificates openssl gcc g++ make zlib1g-dev cmake libjsoncpp-dev && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN wget -q --no-check-certificate "https://github.com/msk-access/GetBaseCountsMultiSample/archive/refs/tags/${GBCMS_VERSION}.tar.gz" && \
	tar -xzf "${GBCMS_VERSION}.tar.gz" && \
	rm "${GBCMS_VERSION}.tar.gz"

# Build stage layers don't affect the final image (see final stage below), so
# these stay as separate WORKDIR/RUN steps per source directory rather than
# chaining `cd` -- keeps each step's working directory explicit and BuildKit
# cache reuse per-directory instead of invalidating the whole chain at once.
WORKDIR /usr/src/GetBaseCountsMultiSample-${GBCMS_VERSION}/bamtools-master
RUN rm -rf build && mkdir build

WORKDIR /usr/src/GetBaseCountsMultiSample-${GBCMS_VERSION}/bamtools-master/build
RUN cmake -DCMAKE_CXX_FLAGS=-std=c++03 .. && \
	make -j"$(nproc)" && \
	make install && \
	cp ../lib/libbamtools.so.2.3.0 /usr/lib/

WORKDIR /usr/src/GetBaseCountsMultiSample-${GBCMS_VERSION}
RUN make -j"$(nproc)" && \
	cp GetBaseCountsMultiSample /usr/local/bin/

################## FINAL IMAGE ######################
# Ubuntu 24.04 is smaller and actively maintained; the binary built above only
# needs its shared library ABI (glibc/libstdc++/libgomp/zlib), all of which
# newer Ubuntu provides -- no compilers, cmake, or -dev headers required here.
FROM ubuntu:24.04

ARG GBCMS_VERSION=1.2.5

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
	org.opencontainers.image.authors="Ronak Shah (shahr2@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
	org.opencontainers.image.created="2026-08-18T20:54:45Z" \
	imageprivacy="False" \
	org.opencontainers.image.version="1.2.5" \
	org.opencontainers.image.licenses="Apache-2.0" \
	org.opencontainers.image.source="https://github.com/msk-access/GetBaseCountsMultiSample/releases/" \
	org.opencontainers.image.url="https://github.com/mskcc/GetBaseCountsMultiSample" \
	org.opencontainers.image.title="GBCMS" \
	org.opencontainers.image.description="GetBaseCountsMultiSample ${GBCMS_VERSION}, built on Ubuntu 16.04 and packaged into a slim Ubuntu 24.04 runtime image."

# bash/procps (ps) are required by the pipeline's own smoke test and by
# Nextflow's task runner; libgomp1/zlib1g/libstdc++6 are the binary's runtime
# shared-library dependencies (see `ldd`).
RUN apt-get update && \
	apt-get install --no-install-recommends -y \
	bash \
	procps \
	libgomp1 \
	libstdc++6 \
	zlib1g && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=builder /usr/local/bin/GetBaseCountsMultiSample /usr/local/bin/GetBaseCountsMultiSample
COPY --from=builder /usr/lib/libbamtools.so.2.3.0 /usr/lib/libbamtools.so.2.3.0
RUN ldconfig
