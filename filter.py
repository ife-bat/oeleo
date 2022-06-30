from pathlib import Path
import os

import dotenv

dotenv.load_dotenv()
base_directory_from = os.environ["BASE_DIR_FROM"]
base_directory_to = os.environ["BASE_DIR_TO"]


if __name__ == '__main__':
    print(f"from: {base_directory_from}\nto: {base_directory_to}")
