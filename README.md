# containers
Mono-repository for custom docker containers used in nextflow modules

For further information on how to contribute or use images in this repository, visit our [Gitbook documentation](https://mskcc-omics-workflows.gitbook.io/omics-wf/GMaCKqX0TmAhUOoZmuc6/image-management)

## Naming conventions

Each Dockerfile should be saved within a specific folder structure:

```
containers/<softwarename>/<version>/Dockerfile
```

Any custom scripts or resource files that are included in the image or required for building the image should be contained in the same folder as the Dockerfile. When you open a pull request for the container, an image will be automatically created and be labeled `$REGISTRY/<softwarename>:version`

The version of the image should correspond to the version of the software it contains. If the image has multiple independent software packages, the image version should start at 0.1.0 and increment in accordance with [Semantic Versioning](https://semver.org/#semantic-versioning-200).

## Image repository

Development images are stored at `mskcc.jfrog.io/omicswf-docker-dev-local/mskcc-omics-workflows`. When a pull request is created against the `develop` branch, and the image passes basic checks, the image is automatically built and pushed to this location.

Productions images are stored at `mskcc.jfrog.io/omicswf-docker-prod-local/mskcc-omics-workflows`. When a pull request is created against the `master` branch, and the image passes basic checks, the image is automatically built and pushed to this location.

When contributing an image you should first open a pull request to `develop`. The `develop` branch will be merged regularly into `master`.

## Image Requirements

Requirements are based on [OCI image-spec annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md). The image must have the following labels:
```
org.opencontainers.image.url
org.opencontainers.image.created
org.opencontainers.image.authors
org.opencontainers.image.source
org.opencontainers.image.version
org.opencontainers.image.title
org.opencontainers.image.description
```
You can optionally use any of the above properties with an extension related to a specific software in the image, and you can use multiple of them as well. For example, if you want to label versions for both the Java version and the abra version:
```
LABEL \
    org.opencontainers.image.version.java=${JAVA_VERSION} \
    org.opencontainers.image.version.abra2=${ABRA2_VERSION}
```
It is also acceptable to use no extension.