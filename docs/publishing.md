# Publishing Omics3D to PyPI

## Current scope

This repository contains publishing infrastructure and a minimal installable
placeholder package, version `0.0.1.dev0`. It provides version information and a
command-line entry point. Reconstruction, analysis and web application code are
not included. Scientific data, uploads, server settings and credentials have not
been copied into this repository. Adding the scaffold does not create a release
or upload a package to PyPI.

The workflow lives at `.github/workflows/workflow.yml`. Its filename and the
`pypi` environment match the intended PyPI pending trusted publisher.

## Trusted publisher settings

In [PyPI account publishing](https://pypi.org/manage/account/publishing/), use:

| Field | Value |
| --- | --- |
| PyPI project name | `Omics3D` |
| Owner | `ultraypy` |
| Repository name | `Omics3D` |
| Workflow name | `workflow.yml` |
| Environment name | `pypi` |

Use the workflow **filename**, not its display title. The owner is `ultraypy`.
No PyPI password, API token, or GitHub repository secret is needed. The publish
job alone receives `id-token: write` to authenticate through GitHub OIDC.

The initial `main` workflow run initializes the GitHub environment named `pypi`
without uploading anything. Existing environment settings are not changed.
Administrators can manage protection rules under **Settings → Environments → pypi**.

## What each event does

| Event | Result |
| --- | --- |
| Push to `main` | Build distributions, validate metadata and verify installation |
| Pull request targeting `main` | Build distributions, validate metadata and verify installation |
| Actions → Run workflow | Validation only; never uploads to PyPI |
| Publish a GitHub Release | Build, validate, and upload the verified artifacts |

The scaffold includes `pyproject.toml`, so the build job now runs. If that file
is removed, ordinary validation reports missing source and skips building; a
release without it fails explicitly. Packaging checks verify installation, not
scientific functionality.

## Before the first release

1. Replace the development scaffold with the intended public functionality and
   update the README. The package name is already `Omics3D`; the version is read
   from `src/omics3d/__init__.py`. Update dependencies and supported Python versions
   as needed. The build workflow currently uses Python 3.11.
2. Add the package's README and license information, the intended public assets,
   and application tests. Explicitly exclude credentials, runtime state, user
   uploads and scientific data from distributions.
3. Push the source and confirm **Build and verify distributions** passes. It
   builds the wheel from the source distribution using `python -m build`, runs
   `twine check --strict`, verifies the package name and matching versions,
   checks the installed wheel and command-line entry points, and stores both
   distributions in the `python-package-distributions` artifact.
   These packaging checks do not replace application tests.
4. Create and publish a GitHub Release with a tag matching the package version:
   version `0.1.0` uses tag `v0.1.0`; version `0.1.0rc1` uses tag `v0.1.0rc1`.
   Use the commit containing the tested source and workflow.
5. Check the **Publish to PyPI** job. The package is uploaded only after the build
   checks succeed. The workflow downloads the verified artifact into a separate
   publish job; it does not build application code with publishing permission.

After the first successful upload, PyPI creates the project and converts the
pending publisher into an ordinary trusted publisher. Adding a pending publisher
does not reserve the package name. A GitHub Release alone also does not guarantee
PyPI publication: the upload job must succeed.

## Troubleshooting

- **No source yet / build skipped:** check that the selected commit includes
  `pyproject.toml` and the package source.
- **Publisher mismatch / invalid publisher:** check owner `ultraypy`, repository
  `Omics3D`, filename `workflow.yml`, environment `pypi`, and whether the pending
  publisher is configured on PyPI rather than TestPyPI.
- **Release tag mismatch:** the tag must be `v` followed by the normalized package
  version. Correct the package version before creating a new release.
- **Waiting for environment approval:** review the `pypi` environment's configured
  rules. This is a GitHub environment gate, not PyPI account review.
- **Version already exists:** use a new package version and matching tag. PyPI
  does not allow overwriting an uploaded distribution.

## References

- [PyPI: create a project through Trusted Publishing](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)
- [PyPI: publish with a Trusted Publisher](https://docs.pypi.org/trusted-publishers/using-a-publisher/)
- [Python Packaging Guide: GitHub Actions publishing](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [GitHub: manage deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
