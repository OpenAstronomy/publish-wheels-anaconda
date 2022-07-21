# Remove all but the latest N versions from wheels on Anaconda.org

import sys

import click
from binstar_client.utils import get_server_api


@click.command()
@click.option('--user')
@click.option('--package')
@click.option('--keep', default=-1)
@click.option('--token')
@click.option('--dry', default=False)
def remove(org, package, keep, token, dry):

    if keep < 0:
        return

    api = get_server_api(token=token)
    package = api.package(org, package)

    # Find versions for which wheels are available
    pypi_versions = set()
    for file_info in package["files"]:
        if file_info["type"] == "pypi":
            pypi_versions.add(file_info["version"])
    pypi_versions = sorted(pypi_versions)

    # Determine versions to remove
    versions_to_remove = pypi_versions[:-keep]

    # Remove the files
    for file_info in package["files"]:
        if file_info["version"] in versions_to_remove:
            print(f"Removing {file_info['basename']}")
            if not dry:
                api.remove_dist(
                    "astropy",
                    "astropy",
                    file_info["version"],
                    basename=file_info["basename"]
                )

if __name__ == '__main__':
    remove()
