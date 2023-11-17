import nox
import os
import pathlib
import shutil

import dotenv

dotenv.load_dotenv()

@nox.session
def pack(session):

    session.install("oeleo")

    out = session.run("poetry", "version", silent=True, external=True)
    version = out.strip().replace("oeleo ", "")
    print(f"version: {version}")
    folder_name_base = out.strip().replace(" ", "_").replace(".", "_")

    print(" creating frozen requirements file ".center(80, "-"))
    requirements_file = open(r"oeleo-bins\oeleo-requirements.txt", "w")
    session.run("pip", "freeze", silent=False, stdout=requirements_file)
    requirements_file.close()
    print("---------------------")

    print(" downloading packages for win32 ".center(80, "-"))
    with session.chdir(r"oeleo-bins"):
        session.run(
            "pip",
            "download",
            "--platform",
            "win32",
            "--no-deps",
            "-r",
            "oeleo-requirements.txt",
            "-d",
            f"{folder_name_base}-win32",
        )
        oeleo_file = (
            pathlib.Path(f"{folder_name_base}-win32")
            .resolve()
            .glob(f"oeleo-*-py3-none-any.whl")
        )
        f = next(oeleo_file)
        win_32_file = f.name.replace("-any.whl", "any-win32.whl")
        shutil.copy(f, win_32_file)

    print("-------ok-win-32---------")

    print(" downloading packages for win64 ".center(80, "-"))
    with session.chdir(r"oeleo-bins"):
        session.run(
            "pip",
            "download",
            "--no-deps",
            "-r",
            "oeleo-requirements.txt",
            "-d",
            f"{folder_name_base}",
        )
        oeleo_file = (
            pathlib.Path(f"{folder_name_base}")
            .resolve()
            .glob(f"oeleo-*-py3-none-any.whl")
        )
        f = next(oeleo_file)
        shutil.copy(f, f.name)

    print("--------OK-----------")
    print()

    server_name = os.getenv("BIN_SERVER_NAME")
    server_folder = os.getenv("BIN_SERVER_FOLDER")
    with session.chdir(r"oeleo-bins"):
        if server_name and server_folder:
            print("Uploading to server".center(80, "-"))
            session.run(
                "scp",
                "-r",
                f"{folder_name_base}-win32",
                f"{server_name}:{server_folder}",
                external=True,
            )
            session.run(
                "scp",
                win_32_file,
                f"{server_name}:{server_folder}",
                external=True,
            )
            session.run(
                "scp",
                "-r",
                f"{folder_name_base}",
                f"{server_name}:{server_folder}",
                external=True,
            )
            session.run(
                "scp",
                f.name,
                f"{server_name}:{server_folder}",
                external=True,
            )
            print("-------OK----------")
            print()
        else:
            print("To upload to server, use:")
            print(f"# if in oeleo-bins folder and uploading win32 to server <server>")
            print(f"> scp -r {folder_name_base}-win32 <server>:/srv/share/oeleo-bin")
            print()
    print("To install on win32, use:")
    print(f"pip install {win_32_file} --no-index --find-links {folder_name_base}-win32")
    print("To install on win, use:")
    print(f"pip install {f.name} --no-index --find-links {folder_name_base}")
