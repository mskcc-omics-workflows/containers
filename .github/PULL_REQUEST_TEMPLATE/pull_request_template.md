<!--
# mskcc-omics-workflows/containers pull request

Many thanks for contributing to mskcc-omics-workflows/containers!

Please fill in the appropriate checklist below (delete whatever is not relevant).
These are the most common things requested on pull requests (PRs).

Remember that PRs should be made against the master branch.

Learn more about contributing: [gitbook](https://app.gitbook.com/o/Txb2lda7D1fX9CVuQbQ0/s/x32s1acwH78k3hruISMe/contributing)
-->

## PR checklist

Closes #XXX <!-- If this PR fixes an issue, please link it here! -->

- [ ] Dockerfile is contained in a folder structure that follows naming conventions. 
- [ ] The image version matches the version of the installed package. If the image is a composite of different independent packages, the image's first version should ideally be 0.1.0.
- [ ] You have tested the Docker image in a Nextflow module that is or will be available in [mskcc-omics-workflows/modules](https://github.com/mskcc-omics-workflows/modules)
- [ ] You have updated the `maintainer`/`contributer` attributes within the Dockerfile, and listed yourself as one of them.
