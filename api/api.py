import logging as log
import os
import pathlib
import shutil
from functools import reduce
from typing import Dict, List


class SpawnWrapper:
    def __init__(self,
                 mount_path: str,
                 env_folder_path: str,
                 env_file_name: str,
                 image_name: str = "basic_image_name",
                 port: int = 8081,
                 is_win: bool = False,
                 ):
        self.image_name = image_name
        self.port = port
        self.mount_path = mount_path.replace("\\", "/")
        self.env_folder_path = env_folder_path.replace("\\", "/")
        self.env_file_name = env_file_name
        self.env_name = self.env_file_name.split('.')[0]
        self.env_file_absolute_path = self.env_folder_path + "/" + self.env_file_name
        self.root_path: pathlib.Path = \
            pathlib.Path(__file__).parent.parent.resolve()
        self.local_env_file_path: str = os.path.join(self.root_path, self.env_file_name)
        self.is_win = is_win

    # need this copy because docker can work only with files within docker scope
    def __copy_env_file_to_docker_context(self):
        shutil.copyfile(self.env_file_absolute_path, self.local_env_file_path)

    def __delete_env_file_copy(self):
        os.remove(self.local_env_file_path)

    def __get_create_docker_image_command(self) -> str:
        return f"docker build {self.root_path} " \
               f"-t {self.image_name} " \
               f"--build-arg MOUNT_DRIVE={self.mount_path} " \
               f"--build-arg ENV_PATH={self.env_file_name} "

    def __get_run_docker_container_command(self):
        return f"docker run " \
               f"-d " \
               f"-p {self.port}:8080 " \
               f"--mount type=bind,source={self.mount_path},target=/mount_drive " \
               f"{self.image_name}"

    def __serialize_request(self, request: Dict) -> str:
        start_curl = "'{"
        end_curl = "}'"

        values: List[str] = list()
        for key, value in request.items():
            string_key = str(key)
            string_value = str(value)
            values.append(f"\"{string_key}\":\"{string_value}\"")

        values_string: str = reduce(lambda x, y: x + ',' + y, values)

        base_result = f"{start_curl}{values_string}{end_curl}"
        if self.is_win:
            base_result = base_result\
                .replace('"', '\\"')\
                .replace("'", '"')
        return base_result

    def spawn(self):
        self.__copy_env_file_to_docker_context()
        os.system(self.__get_create_docker_image_command())
        self.__delete_env_file_copy()
        os.system(self.__get_run_docker_container_command())

    def eval(self, script_name: str):
        request_json = {
            "script": script_name,
            "env": self.env_name
        }
        curl_request_string = self.__serialize_request(request_json)
        log.info(f"Curl request: {curl_request_string}")
        curl_command: str = f"curl " \
                            f"-d {curl_request_string} " \
                            f"-H \"Content-Type: application/json\" " \
                            f"-X POST \"http://localhost:{self.port}/execute\""
        log.info(f"Curl command: {curl_command}")

        os.system(curl_command)
