# Omics3D

Spatial multi-omics reconstruction and analysis.

This repository currently contains release configuration only. Application source code and datasets have not been uploaded, and no package has been published by this setup.

## PyPI publishing

The trusted publisher is configured for:

| Setting | Value |
| --- | --- |
| PyPI project | `Omics3D` |
| GitHub owner | `ultraypy` |
| GitHub repository | `Omics3D` |
| Workflow filename | `workflow.yml` |
| GitHub environment | `pypi` |

Pushes to `main`, pull requests, and manual workflow runs validate the packaging configuration. Once application source and `pyproject.toml` are added, the workflow also builds a source distribution and wheel, checks package metadata, and saves the distributions as an Actions artifact.

Only publishing a GitHub Release triggers upload to PyPI. Ordinary commits and manual validation runs do not publish a package. Uploads use GitHub OIDC / PyPI Trusted Publishing; no PyPI API token is needed.

See [Publishing](docs/publishing.md) for setup details and the first-release procedure.
