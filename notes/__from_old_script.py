"""Upload / update files from local folder to TEAMS / SharePoint"""
# This script is not very fast. But it works.

# TODO (priority):
#   - get cell names from db and copy also from I-drive
#   - copy relevant items from db
# TODO (low priority):
#   - store hashes of files either on teams-channel (start sync session by download hash-file)
#     or in a local sqlite file.

from dataclasses import dataclass
import hashlib
import pathlib
import os
import sys
from typing import Union

from turtle import up
from dotenv import load_dotenv

from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from shareplum.errors import ShareplumRequestError


@dataclass
class SharpointTransferConfiguration:
    password: str = ""
    username: str = ""
    url: str = ""
    site_name: str = ""
    doc_library: str = ""
    local_folder: str = ""
    glob_txt: str = ""
    testing: int = 0

    def update_from_environment_variables(self):
        load_dotenv()

        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.url = os.getenv("URL")
        self.site_name = os.getenv("SITE_NAME")
        self.doc_library = os.getenv("DOC_LIBRARY")
        self.local_folder = os.getenv("LOCAL_FOLDER")
        self.glob_txt = os.getenv("GLOB_TXT")
        self.testing = int(os.getenv("TESTING"))

        if not self.site_name:
            print("Seems you are missing the .env file!")
            sys.exit(-1)


def connect_to_site_folder(url, site_name, username, password, doc_library):
    site_url = "/".join([url, "sites", site_name])
    authcookie = Office365(url, username=username, password=password).GetCookies()
    site = Site(site_url, version=Version.v365, authcookie=authcookie)
    folder = site.Folder(doc_library)
    return folder


def upload_file(file_path: pathlib.Path, folder: Site) -> Union[None, pathlib.Path]:
    """Uploads the file to TEAMS (sharepoint).

    Returns:
        the file path if successfull, else None

    Raises:
        Exception for unhandlede / unknown error.
    """
    print(f"uploading {file_path}", end=" ")
    try:
        file_content = file_path.read_bytes()
        folder.upload_file(file_content, file_path.name)
    except FileNotFoundError:
        print(" - ERROR - file not found")
    except ShareplumRequestError as e:
        print(" - ERROR - request error during uploading")
        print(80 * "-")
        print(e)
        print(80 * "-")
    except Exception as e:
        print(f" - Unhandled ERROR")
        print(80 * "*")
        print(e)
        print("....aborting!")
        print(80 * "*")
        raise Exception(f"Could not upload {file_path}")
    else:
        print(" - OK")
        return file_path


def file_exist(file_path, folder):
    """Check if the file has already been updated and has not been modified.

    Note! The function only checkes if the local file and the file on TEAMS are the same. It does not try to interpret which file is the most recent one.
    """
    try:
        uploaded_file = folder.get_file(file_path.name)
    except ShareplumRequestError:
        return False

    c_uploaded_file = get_checksum_uploaded_file(uploaded_file)
    c_local_file = get_checksum_local_file(file_path)
    return c_uploaded_file == c_local_file


def get_file_paths(local_folder, glob_txt):
    local_folder = pathlib.Path(local_folder)
    all_local_files = local_folder.glob(
        glob_txt,
    )
    return all_local_files


def get_checksum_local_file(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def get_checksum_uploaded_file(b):
    file_hash = hashlib.md5(b)
    return file_hash.hexdigest()


def main():
    conf = SharpointTransferConfiguration()
    conf.update_from_environment_variables()

    print(f" Upload from {conf.local_folder} ".center(80, "="))
    sharepoint_folder = connect_to_site_folder(
        conf.url, conf.site_name, conf.username, conf.password, conf.doc_library
    )

    all_files = get_file_paths(conf.local_folder, conf.glob_txt)
    bad_files = []
    for i, file_path in enumerate(all_files):
        print(f"[{i:04d}]", end=" ")
        if file_exist(file_path, sharepoint_folder):
            print(f"{file_path.name} - already updated")
        else:
            uploaded = upload_file(file_path, sharepoint_folder)
            if not uploaded:
                bad_files.append(file_path)

    print(" Finished! ".center(80, "-"))
    if bad_files:
        print(" Bad files: ")
        print(bad_files)
    print(80 * "=")


if __name__ == "__main__":
    main()
