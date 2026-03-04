# Build R 3.6.3 from source + install all R packages
FROM ubuntu:22.04 AS BASE

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2026-03-03T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="3.6.3" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/R_tidyverse/" \
      org.opencontainers.image.url="" \
      org.opencontainers.image.title="Modernized R Tidyverse 3.6.3" \
      org.opencontainers.image.description="Modernized R Tidyverse 3.6.3 with an updated base image"

ENV DEBIAN_FRONTEND=noninteractive
ENV R_VERSION=3.6.3
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        bash-completion \
        ca-certificates \
        file \
        fonts-texgyre \
        g++ \
        gfortran \
        gsfonts \
        libblas-dev \
        libbz2-1.0 \
        libcurl4 \
        libicu70 \
        libjpeg-turbo8 \
        libopenblas-dev \
        libpangocairo-1.0-0 \
        libpcre2-8-0 \
        libpcre3 \
        libpng16-16 \
        libreadline8 \
        libtiff5 \
        liblzma5 \
        libssl3 \
        libxt6 \
        locales \
        make \
        unzip \
        zip \
        zlib1g \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen en_US.utf8 \
    && /usr/sbin/update-locale LANG=en_US.UTF-8 \
    && BUILDDEPS=" \
        curl \
        default-jdk \
        libbz2-dev \
        libcairo2-dev \
        libcurl4-openssl-dev \
        libpango1.0-dev \
        libjpeg-dev \
        libicu-dev \
        libpcre2-dev \
        libpcre3-dev \
        libpng-dev \
        libreadline-dev \
        libtiff5-dev \
        liblzma-dev \
        libssl-dev \
        libx11-dev \
        libxt-dev \
        libxml2-dev \
        perl \
        tcl8.6-dev \
        tk8.6-dev \
        texinfo \
        texlive-extra-utils \
        texlive-fonts-recommended \
        texlive-fonts-extra \
        texlive-latex-recommended \
        x11proto-dev \
        xauth \
        xfonts-base \
        xvfb \
        zlib1g-dev \
    " \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends $BUILDDEPS \
    && cd /tmp \
    && curl -fsSL "https://cran.r-project.org/src/base/R-3/R-${R_VERSION}.tar.gz" -o "/tmp/R-${R_VERSION}.tar.gz" \
    && tar -xf "/tmp/R-${R_VERSION}.tar.gz"

    FROM BASE as BUILD_R
    WORKDIR "/tmp/R-${R_VERSION}"
    RUN R_PAPERSIZE=letter \
       R_BATCHSAVE="--no-save --no-restore" \
       R_BROWSER=xdg-open \
       PAGER=/usr/bin/pager \
       PERL=/usr/bin/perl \
       R_UNZIPCMD=/usr/bin/unzip \
       R_ZIPCMD=/usr/bin/zip \
       R_PRINTCMD=/usr/bin/lpr \
       LIBnn=lib \
       AWK=/usr/bin/awk \
       CFLAGS="-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2" \
       CXXFLAGS="-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2" \
       ./configure \
           --enable-R-shlib \
           --enable-memory-profiling \
           --with-readline \
           --with-blas \
           --with-lapack \
           --with-tcltk \
           --disable-nls \
           --with-recommended-packages \
           --with-pcre2 \
    && make -j"$(nproc)" \
    && make install \
    && mkdir -p /usr/local/lib/R/site-library \
    && chown root:staff /usr/local/lib/R/site-library \
    && chmod g+ws /usr/local/lib/R/site-library \
    && sed -i '/^R_LIBS_USER=.*$/d' /usr/local/lib/R/etc/Renviron \
    && echo "R_LIBS_USER=\${R_LIBS_USER-'/usr/local/lib/R/site-library'}" >> /usr/local/lib/R/etc/Renviron \
    && echo "R_LIBS=\${R_LIBS-'/usr/local/lib/R/site-library:/usr/local/lib/R/library:/usr/lib/R/library'}" >> /usr/local/lib/R/etc/Renviron \
    && echo 'if(is.na(Sys.getenv("HTTR_LOCALHOST", unset=NA))) { options(httr_oob_default = TRUE) }' \
        >> /usr/local/lib/R/etc/Rprofile.site \
    && cd / && rm -rf /tmp/* \
    && apt-get remove --purge -y $BUILDDEPS \
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && rm -rf /var/lib/apt/lists/*

FROM BUILD_R as FINAL
WORKDIR "/"
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        nano \
        wget \
        git \
        tar \
        bzip2 \
        libbz2-dev \
        libc6-dev \
        libxt-dev \
        liblzma-dev \
        libcurl4-openssl-dev \
        libssl-dev \
        libxml2-dev \
        libgtk2.0-dev \
        libcairo2-dev \
        libmariadb-dev \
        libpq-dev \
        libssh2-1-dev \
        libsasl2-dev \
        unixodbc-dev \
        xvfb \
        xauth \
        xfonts-base \
        xdg-utils \
        inotify-tools \
        fontconfig \
    ## MS Core Fonts
    && echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections \
    && R -e " \
    options(repos=c(CRAN='https://packagemanager.posit.co/cran/__linux__/focal/2025-06-01')); \
    install.packages(c( \
        'tidyverse','dplyr','devtools','remotes','formatR','selectr','caTools', \
        'BiocManager','Cairo','argparse','gridExtra','binom','diptest','egg', \
        'shiny','shinyWidgets','shinyjs','rhandsontable','doParallel', \
        'configr','R.utils','shinyFiles','here','httr','jsonlite' \
    ), Ncpus=parallel::detectCores())" \
    && R -e " \
    options(repos=c(CRAN='https://packagemanager.posit.co/cran/__linux__/focal/2025-06-01')); \
    BiocManager::install('rtracklayer', ask=FALSE, update=FALSE)" \
    && R -q -e "remotes::install_version('bslib', version='0.7.0', repos='https://cloud.r-project.org')" \
    && apt-get install -y --no-install-recommends ttf-mscorefonts-installer \
    && fc-cache -vr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*