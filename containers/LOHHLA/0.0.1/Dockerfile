FROM cmopipeline/lohhla:1.1.3

ENV LOHHLA_VERSION 1.1.7

LABEL   org.opencontainers.image.url="https://github.com/mskcc/lohhla/releases/tag/1.1.7" \
	org.opencontainers.image.created="6/26/24" \
	org.opencontainers.image.authors="Yixiao Gong (gongy@mskcc.com), John orgera (orgeraj@mskcc.com), " \
	org.opencontainers.image.source="10.1016/j.cell.2017.10.001" \
	org.opencontainers.image.version=${LOHHLA_VERSION} \
	org.opencontainers.image.title="lohhla" \
	org.opencontainers.image.description="This container provides an environment to run version ${LOHHLA_VERSION} of LOHHLA.  LOHHLA is a tool that analyzes Loss of Heterozygosity of the HLA Alleles.  LOHHLA works on HLA-A, B, and C." 


RUN R -e "install.packages(c('plyr'), repos = 'http://cran.r-project.org')"

WORKDIR /

RUN rm -rf /lohhla

RUN wget -q https://github.com/mskcc/lohhla/archive/${LOHHLA_VERSION}.zip && unzip ${LOHHLA_VERSION}.zip && mv /lohhla-${LOHHLA_VERSION} /lohhla

WORKDIR /lohhla
RUN wget -q https://raw.githubusercontent.com/jason-weirather/hla-polysolver/master/data/abc_complete.fasta && mv abc_complete.fasta /lohhla/data/

