# Omics3D

Development scaffold for spatial multi-omics reconstruction and analysis.

This repository contains a minimal installable placeholder package and the PyPI publishing workflow. The placeholder provides version information and a command-line entry point. Reconstruction, analysis and the web application are not included yet.

Current development version: **0.0.1.dev0**. Adding this scaffold does not publish a package to PyPI.

## Try the scaffold

Requires Python 3.11 or newer. From a checkout of this repository:

```bash
python -m pip install .
omics3d --version
python -m omics3d
```

In Python:

```python
import omics3d

print(omics3d.__version__)
```

Running `omics3d` without arguments displays the placeholder status. No reconstruction or analysis is performed.

## Build

```bash
python -m pip install build twine
python -m build
python -m twine check --strict dist/*
```

The source package is in `src/omics3d/`. Package metadata reads the version from `src/omics3d/__init__.py`.

## PyPI publishing

The trusted publisher is configured for:

| Setting | Value |
| --- | --- |
| PyPI project | `Omics3D` |
| GitHub owner | `ultraypy` |
| GitHub repository | `Omics3D` |
| Workflow filename | `workflow.yml` |
| GitHub environment | `pypi` |

Pushes to `main`, pull requests, and manual workflow runs build a source distribution and wheel, check package metadata, verify the installed package and command-line entry points, and save the distributions as an Actions artifact.

Only publishing a GitHub Release triggers upload to PyPI. Ordinary commits and manual validation runs do not publish a package. Uploads use GitHub OIDC / PyPI Trusted Publishing; no PyPI API token is needed.

See [Publishing](docs/publishing.md) for setup details and the first-release procedure.
