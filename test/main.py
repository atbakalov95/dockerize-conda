import logging as log
import pathlib
from time import sleep

from api.api import SpawnWrapper

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)

    project_path: str = \
        str(pathlib.Path(__file__).parent.resolve())
    spawn_wrapper = SpawnWrapper(
        mount_path=project_path,
        env_folder_path=project_path,
        env_file_name="test_env.yml"
    )

    spawn_wrapper.spawn()

    sleep(2)

    spawn_wrapper.eval(script_name="main_2.py")
