from typing import Tuple, Union

import falcon

from classic.http_api import App

from ...application import services

from . import controllers


def create_app(
    is_dev_mode: bool,
    allow_origins: Union[str, Tuple[str, ...]],
    task: services.TaskService,
) -> App:
    if is_dev_mode:
        cors_middleware = falcon.CORSMiddleware(allow_origins='*')
    else:
        cors_middleware = falcon.CORSMiddleware(allow_origins=allow_origins)

    middleware = [cors_middleware]

    app = App(middleware=middleware, prefix='/api')

    app.register(
        controllers.TaskController(task=task)
    )

    return app
