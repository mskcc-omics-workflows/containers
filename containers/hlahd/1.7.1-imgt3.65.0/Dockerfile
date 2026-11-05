FROM ubuntu:22.04

# HLA-HD 1.7.1 with its dictionary built from a pinned, checksummed
# IPD-IMGT/HLA release. hlahd/1.7.1 runs update.dictionary.sh, which pulls
# whatever IMGT release is "Latest" at build time and records nothing, so a
# rebuild can silently change typing calls.
ARG IMGT_VERSION=3.65.0
ARG IMGT_BRANCH=3650
ARG HLA_DAT_ZIP_SHA256=01aa70fed700cd3dc6e59a800ee2479582d0ac35e5e27df39b5db42ae54a1668

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org), Nikhil Kumar (kumarn1@mskcc.org)" \
      org.opencontainers.image.created="2026-10-16T00:00:00Z" \
      org.opencontainers.image.licenses="ACADEMIC SOFTWARE LICENSE AGREEMENT" \
      org.opencontainers.image.version="1.7.1-imgt3.65.0" \
      imageprivacy="True" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/hlahd/" \
      org.opencontainers.image.url="https://w3.genome.med.kyoto-u.ac.jp/HLA-HD/" \
      org.opencontainers.image.title="HLA-HD" \
      org.opencontainers.image.description="HLA typing software from Kyoto University, dictionary built from IPD-IMGT/HLA 3.65.0."

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# hadolint ignore=DL3003
RUN  --mount=type=secret,id=MSK_JFROG_USERNAME \
      --mount=type=secret,id=MSK_JFROG_TOKEN \
      set -eux && apt-get update -y && \
      # Install packages
      apt-get install --no-install-recommends -y \
      ca-certificates \
      build-essential \
      g++ \
      perl \
      python3 \
      python-is-python3 \
      unzip \
      wget \
      bowtie2 \
      && \
      # Download HLAHD tarball from JFrog
      mkdir -p /tmp/hlahdTmp/ && \
      wget --progress=dot:giga --directory-prefix /tmp/hlahdTmp/ --user="$(cat /run/secrets/MSK_JFROG_USERNAME)" --password="$(cat /run/secrets/MSK_JFROG_TOKEN)" "https://mskcc.jfrog.io/artifactory/omicswf-generic-prod-local/hlahd.1.7.1.tar.gz" && \
      # Extract and install HLAHD
      mkdir -p /opt/hlahd && \
      tar -zxvf /tmp/hlahdTmp/hlahd.1.7.1.tar.gz -C /opt/hlahd/ && \
      HLAHD_DIR="$(find /opt/hlahd -maxdepth 1 -type d -name 'hlahd.*' | head -1)" && \
      test -n "$HLAHD_DIR" && \
      # install.sh uses relative paths (./src, ./bin), so run it from $HLAHD_DIR.
      cd "$HLAHD_DIR" && \
      bash ./install.sh && \
      test -x "$HLAHD_DIR/bin/pm_extract" && \
      test -x "$HLAHD_DIR/bin/stfr" && \
      test -x "$HLAHD_DIR/bin/get_diff_fasta" && \
      test -x "$HLAHD_DIR/bin/split_pm_read" && \
      test -x "$HLAHD_DIR/bin/split_shell" && \
      # Same steps as update.dictionary.sh, but with a pinned, checksummed
      # hla.dat and hard failures instead of the script's silent ones.
      rm -f hla.dat.zip hla.dat dictionary/hla.dat && \
      wget -q -O hla.dat.zip "https://raw.githubusercontent.com/ANHIG/IMGTHLA/${IMGT_BRANCH}/hla.dat.zip" && \
      echo "${HLA_DAT_ZIP_SHA256}  hla.dat.zip" | sha256sum -c - && \
      unzip -o hla.dat.zip hla.dat && \
      g++ ./src/Create_fasta_from_dat.cpp -O3 -o ./bin/create_fasta_from_dat && \
      mv hla.dat dictionary/ && \
      ./bin/create_fasta_from_dat dictionary/hla.dat dictionary/ 150 && \
      cd dictionary && \
      sh create_dir.sh && \
      sh move_file.sh && \
      cat full_U_seq.fasta >> all_exon_N150.fasta && \
      cat full_U_seq.convert.list >> convert.list && \
      sh bw_build.sh && \
      # Validate the dictionary: fail the build rather than ship a stale one.
      n_alleles="$(wc -l < allele.list)" && \
      test "$n_alleles" -gt 40000 && \
      test "$(grep -c 'HLA-Y\*' allele.list)" -gt 0 && \
      grep -q 'HLA-A\*30:26' allele.list && \
      test -s Y/Y_exon2_N150.fasta && \
      u_hdr="$(head -1 full_U_seq.fasta)" && \
      test "$(grep -cxF "$u_hdr" all_exon_N150.fasta)" -eq 1 && \
      for idx in all_exon_N150 all_intron_N150 all_exon_intron_N150 all_gen_w_utr_N150; do \
          test -s "${idx}.fasta.1.bt2"; \
      done && \
      grep -q '^Y' ../HLA_gene.split.3.50.0.txt && \
      printf 'IPD-IMGT/HLA %s\nbranch %s\nhla.dat.zip sha256 %s\nalleles %s\n' \
          "$IMGT_VERSION" "$IMGT_BRANCH" "$HLA_DAT_ZIP_SHA256" "$n_alleles" > IMGT_RELEASE.txt && \
      rm -f hla.dat ../hla.dat.zip && \
      ln -s "$HLAHD_DIR" /opt/hlahd/current && \
      # Clean up
      apt-get clean && \
      rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PATH="/opt/hlahd/current/bin:${PATH}"

WORKDIR /data
