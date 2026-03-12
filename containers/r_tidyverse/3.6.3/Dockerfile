FROM ubuntu:22.04 AS base

LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2026-03-03T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="3.6.3" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/R_tidyverse/" \
      org.opencontainers.image.url="https://tidyverse.org/" \
      org.opencontainers.image.title="Modernized R Tidyverse 3.6.3" \
      org.opencontainers.image.description="Modernized R Tidyverse 3.6.3 with an updated base image"

ENV DEBIAN_FRONTEND=noninteractive \
    R_VERSION=3.6.3 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        locales \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen en_US.utf8 \
    && /usr/sbin/update-locale LANG=en_US.UTF-8 \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-jdk \
        gfortran \
        libblas-dev \
        libbz2-dev \
        libcairo2-dev \
        libcurl4-openssl-dev \
        libicu-dev \
        libjpeg-dev \
        libopenblas-dev \
        libpango1.0-dev \
        libpcre2-dev \
        libpng-dev \
        libreadline-dev \
        libssl-dev \
        libtiff5-dev \
        libx11-dev \
        libxext-dev \
        libxt-dev \
        libxml2-dev \
        perl \
        tcl8.6-dev \
        tk8.6-dev \
        texinfo \
        x11proto-dev \
        xauth \
        xvfb \
        zlib1g-dev \
    && curl -fsSL "https://cran.r-project.org/src/base/R-3/R-${R_VERSION}.tar.gz" \
        -o "/tmp/R-${R_VERSION}.tar.gz" \
    && tar -xf "/tmp/R-${R_VERSION}.tar.gz" -C /usr/local/src/ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/*

FROM base AS build_r

WORKDIR /usr/local/src/R-3.6.3

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
    && echo "R_LIBS_USER=\${R_LIBS_USER-'/usr/local/lib/R/site-library'}" \
        >> /usr/local/lib/R/etc/Renviron \
    && echo "R_LIBS=\${R_LIBS-'/usr/local/lib/R/site-library:/usr/local/lib/R/library:/usr/lib/R/library'}" \
        >> /usr/local/lib/R/etc/Renviron \
    && echo 'if(is.na(Sys.getenv("HTTR_LOCALHOST", unset=NA))) { options(httr_oob_default = TRUE) }' \
        >> /usr/local/lib/R/etc/Rprofile.site \
    && rm -rf /tmp/* /var/lib/apt/lists/*

FROM build_r AS final

WORKDIR /

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV CRAN_MIRROR="https://packagemanager.posit.co/cran/__linux__/jammy/2025-06-01" \
    BIOC_MIRROR="https://packagemanager.posit.co/bioconductor"

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        fonts-texgyre \
        gsfonts \
        libblas3 \
        libbz2-1.0 \
        libcurl4 \
        libicu70 \
        libgomp1 \
        libjpeg-turbo8 \
        libopenblas0 \
        libpangocairo-1.0-0 \
        libpcre2-8-0 \
        libpng16-16 \
        libreadline8 \
        libtiff5 \
        liblzma5 \
        libssl3 \
        libxt6 \
        make \
        unzip \
        zip \
        zlib1g \
        nano \
        git \
        tar \
        xauth \
        xdg-utils \
        inotify-tools \
        fontconfig \
        ttf-mscorefonts-installer \
        libcairo2-dev \
        libcurl4-openssl-dev \
        libgit2-dev \
        libgtk2.0-dev \
        liblzma-dev \
        libmariadb-dev \
        libpq-dev \
        libsasl2-dev \
        libssh2-1-dev \
        libssl-dev \
        libxml2-dev \
        libxt-dev \
        unixodbc-dev \
    && echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" \
        | debconf-set-selections \
    && fc-cache -vr \
    && R -e " \
        options(repos = c(CRAN = Sys.getenv('CRAN_MIRROR')), \
                Ncpus = parallel::detectCores()); \
        install.packages('tidyverse', version = '1.3.1', type = 'source')" \
    && R -e " \
        options(repos = c(CRAN = Sys.getenv('CRAN_MIRROR')), \
                Ncpus = parallel::detectCores()); \
        install.packages(c( \
            'devtools', 'remotes', 'formatR', 'caTools', \
            'Cairo', 'argparse', 'gridExtra', 'binom', 'egg', \
            'shiny', 'shinyWidgets', 'shinyjs', 'rhandsontable', \
            'doParallel', 'R.utils', 'shinyFiles', 'here', 'configr' \
        ), type = 'source')" \
    && R -e " \
        options(repos = c(CRAN = Sys.getenv('CRAN_MIRROR'))); \
        install.packages('BiocManager', type = 'source'); \
        BiocManager::install(version = '3.10', ask = FALSE); \
        BiocManager::install('rtracklayer', ask = FALSE, update = FALSE)" \
    && R -e " \
        options(repos = c(CRAN = Sys.getenv('CRAN_MIRROR')), \
                Ncpus = parallel::detectCores());" \
    && apt-get purge -y --auto-remove \
        libcairo2-dev \
        libcurl4-openssl-dev \
        libgit2-dev \
        libgtk2.0-dev \
        liblzma-dev \
        libmariadb-dev \
        libpq-dev \
        libsasl2-dev \
        libssh2-1-dev \
        libssl-dev \
        libxml2-dev \
        libxt-dev \
        unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && find /usr/local/lib/R -type f -name "*.o" -delete \
    && find /usr/local/lib/R -type f -name "*.a" -delete \
    && find /usr/local/lib/R/library -mindepth 2 -maxdepth 2 \
        -type d \( -name help -o -name doc -o -name tests -o -name demo \) \
        -exec rm -rf {} + \
    && rm -rf /usr/local/src/R-3.6.3 \
    && R --vanilla -e " \
    packages <- c( \
        'tidyverse', 'dplyr', 'devtools', 'remotes', 'formatR', \
        'selectr', 'caTools', 'BiocManager', 'Cairo', 'argparse', \
        'gridExtra', 'binom', 'egg', 'shiny', 'shinyWidgets', \
        'shinyjs', 'rhandsontable', 'doParallel', 'configr', \
        'R.utils', 'shinyFiles', 'here', 'httr', 'jsonlite', \
        'rtracklayer', 'ggplot2' \
    ); \
    failed <- Filter(function(p) !requireNamespace(p, quietly = TRUE), packages); \
    if (length(failed) > 0) { \
        stop('The following packages failed to load: ', paste(failed, collapse = ', ')); \
    } else { \
        message('All ', length(packages), ' R packages loaded successfully.'); \
    }; \
    pinned <- c('ggplot2', 'dplyr', 'shiny', 'tidyverse', 'devtools', 'rlang', 'vctrs'); \
    for (p in pinned) cat(sprintf('  %-12s %s\n', p, as.character(packageVersion(p))))"