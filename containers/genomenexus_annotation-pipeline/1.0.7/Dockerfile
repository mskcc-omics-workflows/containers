FROM maven:3.9.9-eclipse-temurin-21 AS build

ARG GENOME_NEXUS_ANNOTATION_PIPELINE_VERSION=1.0.7
ARG MAVEN_BUILD_ARGS=-DskipTests

ENV PROJECT_VERSION=${GENOME_NEXUS_ANNOTATION_PIPELINE_VERSION}
ENV GN_HOME=/genome-nexus-annotation-pipeline
ENV GN_RESOURCES=${GN_HOME}/annotationPipeline/src/main/resources

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR ${GN_HOME}

RUN set -eux && \
    apt-get update -y && \
    apt-get install --no-install-recommends -y \
    ca-certificates \
    wget \
    && \
    wget --progress=dot:giga --output-document /tmp/genome-nexus-annotation-pipeline.tar.gz \
    "https://github.com/genome-nexus/genome-nexus-annotation-pipeline/archive/refs/tags/v${GENOME_NEXUS_ANNOTATION_PIPELINE_VERSION}.tar.gz" && \
    tar --extract --gzip --file /tmp/genome-nexus-annotation-pipeline.tar.gz --strip-components=1 --directory "${GN_HOME}" && \
    cp "${GN_RESOURCES}/log4j.properties.console.EXAMPLE" "${GN_RESOURCES}/log4j.properties" && \
    mvn "${MAVEN_BUILD_ARGS}" clean install -q && \
    jar_path="$(find "${GN_HOME}/annotationPipeline/target" -name 'annotationPipeline-*.jar' -print -quit)" && \
    test -n "${jar_path}" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

FROM eclipse-temurin:21-jre-jammy

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="John Orgera (orgeraj@mskcc.org)" \
      org.opencontainers.image.created="2026-06-09T00:00:00Z" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="1.0.7" \
      imageprivacy="False" \
      org.opencontainers.image.source="https://github.com/mskcc-omics-workflows/containers/containers/genomenexus_annotation-pipeline/" \
      org.opencontainers.image.url="https://github.com/genome-nexus/genome-nexus-annotation-pipeline/" \
      org.opencontainers.image.title="Genome Nexus Annotation Pipeline" \
      org.opencontainers.image.description="Genome Nexus variant annotation pipeline built from the upstream v1.0.7 release."

ENV DEBIAN_FRONTEND=noninteractive
ENV GN_HOME=/genome-nexus-annotation-pipeline
ENV GN_RESOURCES=${GN_HOME}/annotationPipeline/src/main/resources
ENV GN_TARGET=${GN_HOME}/annotationPipeline/target

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN set -eux && \
    apt-get update -y && \
    apt-get install --no-install-recommends -y \
    procps \
    && \
    mkdir -p "${GN_TARGET}" "${GN_RESOURCES}" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=build /genome-nexus-annotation-pipeline/annotationPipeline/target/annotationPipeline-*.jar ${GN_TARGET}/annotationPipeline.jar
COPY --from=build /genome-nexus-annotation-pipeline/scripts ${GN_HOME}/scripts
COPY --from=build /genome-nexus-annotation-pipeline/annotationPipeline/src/main/resources/application.properties.EXAMPLE ${GN_RESOURCES}/application.properties

ENV PATH="${PATH}:${GN_HOME}/scripts"

WORKDIR ${GN_TARGET}

CMD ["java", "-jar", "annotationPipeline.jar"]
