import nox
import os
import pathlib
import shutil

import dotenv

dotenv.load_dotenv()


@nox.session
def pack(session):
    # TODO: put all deps inside one folder ("dependencies")
    # TODO: fix so that also py3.8, py3.10 and py3.11 is packed
    # TODO: fix so that packages for win32 py3.8 and win_amd64 py3.10 and py3.11 are packed

    out = session.run("poetry", "version", silent=True, external=True)
    version = out.strip().replace("oeleo ", "")
    print(f"version: {version}")
    folder_name_base = out.strip().replace(" ", "_").replace(".", "_")
    print(f"folder_name_base: {folder_name_base}")
    wheel_name = f"oeleo-{version}-py3-none-any.whl"

    print(" creating frozen requirements file for py3.8 win32".center(80, "-"))
    session.run(
        "poetry",
        "export",
        "-f",
        "requirements.txt",
        # "--extras",
        # "'python==3.8'",
        "--without-hashes",
        "--output",
        r"oeleo-bins\oeleo-requirements-py38.txt",
        external=True,
    )
    print("---------------------")
    print(" downloading packages for py3.8 win32 ".center(80, "-"))

    session.run(
        r"pip",
        "download",
        "--python-version",
        "3.8",
        "--platform",
        "win32",
        "--no-deps",
        f"oeleo=={version}",
        "-d",
        r"oeleo-bins",
        external=True,
    )
    win_32_file = pathlib.Path(wheel_name).name.replace("-any.whl", "-any-win32.whl")

    with session.chdir(r"oeleo-bins"):
        shutil.move(wheel_name, win_32_file)
        print(f"win_32_file: {win_32_file}")

    with session.chdir(r"oeleo-bins"):
        session.run(
            "pip",
            "download",
            "--platform",
            "win32",
            "--no-deps",
            "-r",
            "oeleo-requirements-py38.txt",
            "-d",
            f"dependencies",
            external=True,
        )

    print("-------ok-win-32---------")

    print(" downloading packages for win64 ".center(80, "-"))
    session.run(
        r"pip",
        "download",
        "--platform",
        "win_amd64",
        "--no-deps",
        f"oeleo=={version}",
        "-d",
        r"oeleo-bins",
        external=True,
    )

    with session.chdir(r"oeleo-bins"):
        session.run(
            "pip",
            "download",
            "--platform",
            "win_amd64",
            "--no-deps",
            "-r",
            "oeleo-requirements.txt",
            "-d",
            f"dependencies",
            external=True,
        )
    with session.chdir(r"oeleo-bins"):
        session.run(
            "pip",
            "download",
            "--platform",
            "win_amd64",
            "--no-deps",
            "-r",
            "oeleo-requirements-py38.txt",
            "-d",
            f"dependencies",
            external=True,
        )
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
                f"dependencies",
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
                wheel_name,
                f"{server_name}:{server_folder}",
                external=True,
            )
            print("-------OK----------")
            print()
        else:
            print("To upload to server, use:")
            print(f"# if in oeleo-bins folder and uploading win32 to server <server>")
            print(f"> scp -r dependencies <server>:/srv/share/oeleo-bin")
            print()
    print("To install on win32, use:")
    print(f"pip install {win_32_file} --no-index --find-links dependencies")
    print("To install on win, use:")
    print(f"pip install {wheel_name} --no-index --find-links dependencies")
