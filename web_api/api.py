import os

import logging as log

from aiohttp import web

routes = web.RouteTableDef()


@routes.post('/execute')
async def execute(request):
    try:
        data = await request.json()

        exec_full_path = f"{os.curdir}/{data['script']}"
        env_name = data["env"]

        log.info(f"exec full path: {str(exec_full_path)}")
        log.info(f"env name: {str(env_name)}")
        conda_command = f"conda run " \
                        f"--no-capture-output " \
                        f"-n {env_name} " \
                        f"python mount_drive/{exec_full_path}"

        log.info(f"conda command: {str(conda_command)}")
        os.system(conda_command)
        response_json = {
            "info": "executed"
        }
        return web.json_response(response_json)
    except Exception as exc:
        log.error(exc)

        response_json = {
            "info": "error"
        }
        return web.json_response(response_json)


def get_app():
    log.basicConfig(level=log.INFO)
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    web.run_app(get_app(), port=8080)
