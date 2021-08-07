import os

import cowsay

BASE_PATH: str = "mount_drive"

if __name__ == '__main__':
    cowsay.cow("Hello world from cow")

    os.system(f"mkdir {BASE_PATH}/test_dir_from_docker")
