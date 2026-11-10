"""Command-line entry point for the Omics3D development scaffold."""

import argparse

from . import __version__


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="omics3d",
        description="Omics3D development scaffold for spatial multi-omics tools.",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"Omics3D {__version__}"
    )
    parser.parse_args()
    print(f"Omics3D {__version__}: placeholder package.")
    print("Reconstruction and analysis functionality is not included yet.")
    return 0
