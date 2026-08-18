FROM ubuntu:24.04 AS base

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
	org.opencontainers.image.authors="Ronak Shah (shahr2@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
	org.opencontainers.image.created="2026-08-18T20:54:45Z" \
	imageprivacy="False" \
	org.opencontainers.image.version="1.2.5" \
	org.opencontainers.image.licenses="Apache-2.0" \
	org.opencontainers.image.source="https://github.com/msk-access/GetBaseCountsMultiSample/releases/" \
	org.opencontainers.image.url="https://github.com/mskcc/GetBaseCountsMultiSample" \
	org.opencontainers.image.title="GBCMS" \
	org.opencontainers.image.description="GetBaseCountsMultiSample 1.2.5, built on Ubuntu 16.04 and packaged into a slim Ubuntu 24.04 runtime image."

# BUILD STAGE
# A separate, unrelated base (ubuntu:16.04) from `base` above -- kept on
# 16.04 to match the toolchain this code (c++03, vendored bamtools-master)
# has always built against. Labels don't carry across unrelated FROMs, which
# is why the final stage below re-enters `FROM base` instead of building on
# top of this stage.
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

# FINAL IMAGE
FROM base

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
