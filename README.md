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

#### Created Date

The `org.opencontainers.image.created` label should be used to timestamp the image as accurately as possible. The value should match the following regular expression:
```
"^(\\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(?:T([01][0-9]|2[0-3])(:[0-5][0-9])(:[0-5][0-9])(?:\\.[0-9]+)?Z?)?$"
```
For example: `"2020-12-16T15:55:35Z"`. 

## Testing image build locally

The Github Actions dev workflow has been configured to run locally with [act](https://github.com/nektos/act) (although it is not required to contribute to the repository, as the workflow will also be executed by a Github Action Runner). Here is a sample command:
```
act \
    -s MSK_JFROG_USERNAME=<jfrogusername> \
    -s MSK_JFROG_TOKEN=<jfrogtoken> \
    -s GITHUB_TOKEN=<personalgithubtoken> \
    --workflows .github/workflows/dev-build.yml
```
The `-s` parameters indicate "secrets" that are needed in the environment of the workflow. Certain steps may fail without them. Currently only `.github/workflows/dev-build.yml` has been properly enabled with `act`, but `.github/workflows/prod-build.yml` is not.
