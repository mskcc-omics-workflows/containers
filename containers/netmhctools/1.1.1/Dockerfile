FROM ubuntu:22.04

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2025-08-20T11:07:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="1.1.1" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/netmhctools/" \
      org.opencontainers.image.url="https://services.healthtech.dtu.dk/" \
      org.opencontainers.image.title="Netmhctools" \
      org.opencontainers.image.description="Suite of Netmhctools for binding prediction"

ENV DEBIAN_FRONTEND=noninteractive
ENV NETMHC_PACKAGE=https://mskcc.jfrog.io/artifactory/omicswf-generic-prod-local/netMHC.Linux.tar.gz
ENV NETMHCTOOLS_TAG=1.1.1
ARG TARGETPLATFORM

RUN  --mount=type=secret,id=MSK_JFROG_USERNAME \
      --mount=type=secret,id=MSK_JFROG_TOKEN \
      set -xe && apt-get update -y && \
      # Install packages
      apt-get install --no-install-recommends -y \
      build-essential \
      python3.10 \
      python3-pip \
      python2 \
      libc6-dev \
      tcsh \
      libnss-sss \
      git \
      curl \
      wget \
      gawk \
      vim  \
      && python3 -m pip install --no-cache-dir --upgrade pip \
      # Install python packages
      && pip3 install --no-cache-dir \
            numpy \ 
            pandas \
            python-dateutil \
            psutil \
      # Download NetMHC binary
      && mkdir -p /tmp/netMHCTmp/ \
      && wget --progress=dot:giga --directory-prefix /tmp/netMHCTmp/ --user="$(cat /run/secrets/MSK_JFROG_USERNAME)" --password="$(cat /run/secrets/MSK_JFROG_TOKEN)" "https://mskcc.jfrog.io/artifactory/omicswf-generic-prod-local/netMHC.Linux.tar.gz" \
      && tar -xvzf /tmp/netMHCTmp/netMHC.Linux.tar.gz -C /tmp/netMHCTmp/ \
      # Store Academic License
      && cp /tmp/netMHCTmp/netMHC/netMHCpan-4.2_license.txt /usr/local/ \
      # Install netmhc 3.4
      && tar -xvzf /tmp/netMHCTmp/netMHC/netMHC-3.4.Linux.tar.gz -C /usr/local/bin/ \
      && chmod -R 777 /usr/local/bin/netMHC-3.4/ \
      # Install netmhcpan 4.1
      && mkdir -p /tmp/netMHCTmp/netMHCpan-4.1 \
      && tar -xvzf /tmp/netMHCTmp/netMHC/netMHCpan-4.1b.Linux.tar.gz -C /usr/local/bin/ \
      && wget --progress=dot:giga --directory-prefix /tmp/netMHCTmp/netMHCpan-4.1 "https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/data.tar.gz" \
      && tar -zxvf /tmp/netMHCTmp/netMHCpan-4.1/data.tar.gz -C /usr/local/bin/netMHCpan-4.1/  \
      && sed -i 's|'/net/sund-nas.win.dtu.dk/storage/services/www/packages/netMHCpan/4.1/netMHCpan-4.1'|'/usr/local/bin/netMHCpan-4.1'|' /usr/local/bin/netMHCpan-4.1/netMHCpan \
      && sed -i '32c\setenv NETMHCpan /usr/local/bin/netMHCpan-4.1/Linux_x86_64' /usr/local/bin/netMHCpan-4.1/netMHCpan \
      && chmod -R 777 /usr/local/bin/netMHCpan-4.1 \
      # Install netmhcpan 4.2
      && tar -xvzf /tmp/netMHCTmp/netMHC/netMHCpan-4.2bstatic.Linux.tar.gz -C /usr/local/bin/ \
      && sed -i 's|'/tools/src/netMHCpan-4.2'|'/usr/local/bin/netMHCpan-4.2'|' /usr/local/bin/netMHCpan-4.2/netMHCpan \
      && sed -i '32c\setenv NETMHCpan /usr/local/bin/netMHCpan-4.2/Linux_x86_64' /usr/local/bin/netMHCpan-4.2/netMHCpan \
      && chmod -R 777 /usr/local/bin/netMHCpan-4.2 \      
      # Install netmhcstabpan 1.0
      && mkdir -p /tmp/netMHCTmp/netMHCstabpan-1.0 \
      && tar -xvzf /tmp/netMHCTmp/netMHC/netMHCstabpan-1.0b.Linux.tar.gz -C /usr/local/bin/ \
      && wget --progress=dot:giga --directory-prefix /tmp/netMHCTmp/netMHCstabpan-1.0 "https://services.healthtech.dtu.dk/services/NetMHCstabpan-1.0/data.tar.gz" \
      && tar -zxvf /tmp/netMHCTmp/netMHCstabpan-1.0/data.tar.gz -C /usr/local/bin/netMHCstabpan-1.0/ \
      && sed -i 's|'/net/sund-nas.win.dtu.dk/storage/services/www/packages/netMHCstabpan/1.0/netMHCstabpan-1.0'|'/usr/local/bin/netMHCstabpan-1.0'|' /usr/local/bin/netMHCstabpan-1.0/netMHCstabpan \
      && sed -i 's|'/tools/src/netMHCpan-2.8/netMHCpan'|'/usr/local/bin/netMHCpan-4.1/netMHCpan'|' /usr/local/bin/netMHCstabpan-1.0/netMHCstabpan \
      && sed -i '35c\setenv NETMHCstabpan /usr/local/bin/netMHCstabpan-1.0/Linux_x86_64' /usr/local/bin/netMHCstabpan-1.0/netMHCstabpan \
      && chmod -R 777 /usr/local/bin/netMHCstabpan-1.0 \
      # Clean up
      && apt-get clean \
      && apt-get purge \
      && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*