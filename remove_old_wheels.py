# Remove all but the latest N versions from wheels on Anaconda.org
from datetime import datetime, timezone, timedelta

import click
from binstar_client.utils import get_server_api

UPLOAD_TIME_FMT = r"%Y-%m-%d %H:%M:%S.%f%z"  # e.g., 2018-10-19 19:03:58.717000+00:00
MIN_DATETIME = datetime.min.replace(tzinfo=timezone(timedelta(hours=0)))


@click.command()
@click.option("--user")
@click.option("--package")
@click.option("--keep", default=-1)
@click.option("--token")
@click.option("--dry", default=False)
def remove(user, package, keep, token, dry):

    if keep < 0:
        return

    api = get_server_api(token=token)
    pkg = api.package(user, package)

    # Find versions for which wheels are available
    pypi_versions = {}
    for file_info in pkg["files"]:
        if file_info["type"] == "pypi":
            version = file_info["version"]
            upload_time = datetime.strptime(
                file_info["upload_time"],
                UPLOAD_TIME_FMT,
            )
            # Keep date of version's most recent upload
            pypi_versions[version] = max(
                pypi_versions.get(version, MIN_DATETIME),
                upload_time,
            )
    pypi_versions = [(upload_time, version) for version, upload_time in pypi_versions.items()]
    pypi_versions = sorted(pypi_versions)  # sort by upload time (then version)

    # Determine versions to remove
    versions_to_remove = [version[1] for version in pypi_versions[:-keep]]

    # Remove the files
    for file_info in pkg["files"]:
        if file_info["version"] in versions_to_remove:
            print(f"Removing {file_info['basename']}")
            if not dry:
                api.remove_dist(
                    user, package, file_info["version"], basename=file_info["basename"]
                )
        else:
            print(f"Keeping {file_info['basename']}")


if __name__ == "__main__":
    remove()
