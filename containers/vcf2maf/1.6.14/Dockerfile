FROM alpine:3.20 AS base

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2026-03-26T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="1.6.14" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/vcf2maf/" \
      org.opencontainers.image.url="https://github.com/mskcc/vcf2maf" \
      org.opencontainers.image.title="VCF2MAF" \
      org.opencontainers.image.description="VCF to MAF conversion tool for somatic variant annotation and analysis"

ENV VCF2MAF_VERSION=1.6.14 \
    VEP_VERSION=86 \
    VEP_PATH=/usr/local/bin/vep \
    HTSLIB_VERSION=1.9 \
    SAMTOOLS_VERSION=1.9 \
    BCFTOOLS_VERSION=1.9 \
    PATH="/usr/local/bin:${PATH}" \
    LANG=C.UTF-8

# Install bash first so we can switch the shell for pipefail support
RUN apk add --no-cache bash

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install runtime libs, build toolchain, Perl modules, then clean up build-deps
RUN apk add --no-cache \
      ca-certificates \
      procps \
      curl \
      git \
      perl \
      perl-dev \
      rsync \
      wget \
      zlib \
      bzip2 \
      xz \
      ncurses-libs \
      libgcc \
      libstdc++ \
      libxml2 \
      mariadb-connector-c \
      perl-dbi \
      perl-dbd-mysql \
      perl-json \
      perl-cgi \
      perl-archive-zip \
      perl-time-hires \
      perl-file-copy-recursive \
      perl-module-metadata \
      perl-net-ssleay \
      perl-io-socket-ssl \
    && apk add --no-cache --virtual .build-deps \
      build-base \
      curl-dev \
      db-dev \
      zlib-dev \
      bzip2-dev \
      xz-dev \
      ncurses-dev \
      openssl-dev \
      libxml2-dev \
      mariadb-connector-c-dev \
      expat-dev \
      unzip \
      autoconf \
      automake \
      libtool \
      make \
      gcc \
      g++ \
    && curl -fsSL https://cpanmin.us | perl - App::cpanminus \
    && cpanm --notest \
        LWP \
        LWP::Simple \
        LWP::Protocol::https \
        Archive::Extract \
        Archive::Tar \
        Archive::Zip \
        CGI \
        DBI \
        Encode \
        version \
        Time::HiRes \
        File::Copy::Recursive \
        Perl::OSType \
        Module::Metadata \
        Sereal \
        JSON \
        Bio::Root::Version \
        Set::IntervalTree \
        PerlIO::gzip \
    && rm -rf /root/.cpanm \
    && rm -rf /var/cache/apk/*

FROM base AS download_and_unpack

WORKDIR /tmp

RUN wget -q "https://github.com/samtools/htslib/releases/download/${HTSLIB_VERSION}/htslib-${HTSLIB_VERSION}.tar.bz2" \
    && wget -q "https://github.com/samtools/bcftools/releases/download/${BCFTOOLS_VERSION}/bcftools-${BCFTOOLS_VERSION}.tar.bz2" \
    && wget -q "https://github.com/samtools/samtools/releases/download/${SAMTOOLS_VERSION}/samtools-${SAMTOOLS_VERSION}.tar.bz2" \
    && wget -q "https://github.com/Ensembl/ensembl-tools/archive/release/${VEP_VERSION}.zip" -O "ensembl-tools-release-${VEP_VERSION}.zip" \
    && wget -q "https://github.com/mskcc/vcf2maf/archive/v${VCF2MAF_VERSION}.zip" -O "vcf2maf-v${VCF2MAF_VERSION}.zip" \
    && tar -xjf "htslib-${HTSLIB_VERSION}.tar.bz2" \
    && tar -xjf "bcftools-${BCFTOOLS_VERSION}.tar.bz2" \
    && tar -xjf "samtools-${SAMTOOLS_VERSION}.tar.bz2" \
    && unzip -q "ensembl-tools-release-${VEP_VERSION}.zip" \
    && unzip -q "vcf2maf-v${VCF2MAF_VERSION}.zip"

FROM download_and_unpack AS htslib_builder

WORKDIR "/tmp/htslib-${HTSLIB_VERSION}"

RUN ./configure && make -j"$(nproc)" && make install

FROM htslib_builder AS bcftools_builder

WORKDIR "/tmp/bcftools-${BCFTOOLS_VERSION}"

RUN make HTSDIR="/tmp/htslib-${HTSLIB_VERSION}" -j"$(nproc)" && make install

FROM bcftools_builder AS samtools_builder

WORKDIR "/tmp/samtools-${SAMTOOLS_VERSION}"

RUN ./configure --with-htslib="/tmp/htslib-${HTSLIB_VERSION}" && make -j"$(nproc)" && make install

FROM samtools_builder AS vep_builder

WORKDIR "/tmp/ensembl-tools-release-${VEP_VERSION}/scripts/variant_effect_predictor"

RUN perl INSTALL.pl --AUTO a --NO_HTSLIB \
    && mv "/tmp/ensembl-tools-release-${VEP_VERSION}/scripts/variant_effect_predictor" /usr/local/vep

FROM vep_builder AS vcf2maf_builder

WORKDIR "/tmp/vcf2maf-${VCF2MAF_VERSION}"

RUN mkdir -p /usr/local/vcf2maf \
    && cp -a . /usr/local/vcf2maf/ \
    && ln -sf /usr/local/vcf2maf/vcf2maf.pl /usr/local/bin/vcf2maf.pl \
    && ln -sf /usr/local/vep/vep /usr/local/bin/vep

FROM base AS final

COPY --from=vcf2maf_builder /usr/local/bin/bcftools /usr/local/bin/bcftools
COPY --from=vcf2maf_builder /usr/local/bin/samtools /usr/local/bin/samtools
COPY --from=vcf2maf_builder /usr/local/bin/tabix    /usr/local/bin/tabix
COPY --from=vcf2maf_builder /usr/local/bin/bgzip    /usr/local/bin/bgzip
COPY --from=vcf2maf_builder /usr/local/lib/libhts.so* /usr/local/lib/
COPY --from=vcf2maf_builder /usr/local/lib/perl5    /usr/local/lib/perl5
COPY --from=vcf2maf_builder /usr/local/share/perl5  /usr/local/share/perl5
COPY --from=vcf2maf_builder /usr/local/vep                /usr/local/vep
COPY --from=vcf2maf_builder /usr/local/vcf2maf            /usr/local/vcf2maf

ENV PATH="/usr/local/bin:${PATH}"

RUN set -eux \
    && ln -sf /usr/local/vep/variant_effect_predictor.pl /usr/local/bin/variant_effect_predictor.pl \
    && ln -sf /usr/local/vcf2maf/vcf2maf.pl /usr/local/bin/vcf2maf.pl \
    && chmod +x /usr/local/bin/vcf2maf.pl \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/* /tmp/* \
    && ldconfig /usr/local/lib 2>/dev/null || true \
    && vcf2maf.pl --help >/dev/null \
    && variant_effect_predictor.pl --help >/dev/null \
    && bcftools --version >/dev/null \
    && samtools --version >/dev/null \
    && perl -e 'for my $m (qw( \
        LWP LWP::Simple LWP::Protocol::https \
        Archive::Extract Archive::Tar Archive::Zip \
        CGI DBI DBD::mysql Encode version Time::HiRes \
        File::Copy::Recursive Perl::OSType Module::Metadata \
        Sereal JSON Bio::Root::Version Set::IntervalTree \
        PerlIO::gzip Net::SSLeay IO::Socket::SSL \
    )) { eval "use ${m} (); 1" or die "Missing Perl module: ${m} - $@\n"; }' \
    && echo "All tools and dependencies are installed and working correctly."

CMD ["vcf2maf.pl", "--help"]
