"""Readiness and distribution checks for the Omics3D publishing workflow."""
from __future__ import annotations

import argparse
import os
from email.parser import BytesParser
from pathlib import Path
import re
import tarfile
import tomllib
import zipfile


def canonical_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def inspect_source(root: Path, *, required: bool = False) -> bool:
    path = root / "pyproject.toml"
    if not path.is_file():
        if required:
            raise ValueError(
                "Cannot publish: application source and pyproject.toml have not been added. "
                "This repository currently contains publishing configuration only."
            )
        return False
    metadata = tomllib.loads(path.read_text(encoding="utf-8"))
    project = metadata.get("project", {})
    if canonical_name(project.get("name", "")) != "omics3d":
        raise ValueError('pyproject.toml must declare [project] name = "Omics3D".')
    if not metadata.get("build-system", {}).get("build-backend"):
        raise ValueError("pyproject.toml must declare a build-system.build-backend.")
    if "version" not in project and "version" not in project.get("dynamic", []):
        raise ValueError("Declare a static or dynamic project version before building.")
    return True


def inspect_distributions(directory: Path, *, tag: str = "") -> str:
    from packaging.version import Version

    wheels = sorted(directory.glob("*.whl"))
    sdists = sorted(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError("Expected exactly one wheel and one source distribution.")
    files = {path for path in directory.iterdir() if path.is_file()}
    if files != set(wheels + sdists):
        raise ValueError("dist/ must contain only the two verified distributions.")
    with zipfile.ZipFile(wheels[0]) as archive:
        entries = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(entries) != 1:
            raise ValueError("The wheel must contain exactly one distribution metadata file.")
        wheel_metadata = BytesParser().parsebytes(archive.read(entries[0]))
    with tarfile.open(sdists[0], "r:gz") as archive:
        entries = [entry for entry in archive.getmembers()
                   if len(Path(entry.name).parts) == 2
                   and Path(entry.name).name == "PKG-INFO" and entry.isfile()]
        if len(entries) != 1:
            raise ValueError("The source distribution must contain one root PKG-INFO file.")
        with archive.extractfile(entries[0]) as stream:
            source_metadata = BytesParser().parsebytes(stream.read())
    for metadata in (wheel_metadata, source_metadata):
        if canonical_name(metadata.get("Name", "")) != "omics3d":
            raise ValueError("Distribution name must match the Omics3D trusted publisher.")
        if not metadata.get("Version"):
            raise ValueError("Distribution version is missing.")
    version = Version(wheel_metadata["Version"])
    if version != Version(source_metadata["Version"]):
        raise ValueError("Wheel and source distribution versions differ.")
    if version.local is not None:
        raise ValueError("PyPI does not accept local version identifiers.")
    if tag and (not tag.startswith("v") or tag != f"v{version}"):
        raise ValueError(f"Release tag {tag!r} must be v{version!s}.")
    print(f"Verified Omics3D {version}: wheel and source distribution.")
    return str(version)


def append_workflow_file(variable: str, content: str) -> None:
    path = os.getenv(variable)
    if path:
        with Path(path).open("a", encoding="utf-8") as stream:
            stream.write(content + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("source", "distributions"))
    parser.add_argument("path", nargs="?", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "source":
            ready = inspect_source(args.path or Path.cwd(),
                                   required=os.getenv("RELEASE_EVENT") == "1")
            append_workflow_file("GITHUB_OUTPUT", f"ready={str(ready).lower()}")
            message = ("Package metadata is ready. Build checks will run."
                       if ready else "Publishing is configured. Application source has not yet "
                       "been added; build and upload are skipped.")
            print(message)
            append_workflow_file("GITHUB_STEP_SUMMARY", message)
        else:
            inspect_distributions(args.path or Path("dist"), tag=os.getenv("RELEASE_TAG", ""))
    except (ValueError, OSError, KeyError, tarfile.TarError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Release check failed: {error}\n")


if __name__ == "__main__":
    main()

