import asyncio

from click import INT
from cock import Option, build_options_from_dict
from facet import ServiceMixin
from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config

from tps_exness.injector import inject, register

web_options = build_options_from_dict({
    "web": {
        "host": Option(default="0.0.0.0"),
        "port": Option(default=80, type=INT),
    },
})

ACCESS_LOG_DEFAULT_FORMAT = '%(h)s %(l)s %(l)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


class WebServer(ServiceMixin):

    def __init__(self, host=None, port=80):
        self.host = host
        self.port = port
        self.app = None
        self.hypercorn_config = Config.from_mapping(
            bind=f"{host}:{port}",
            access_log_format=ACCESS_LOG_DEFAULT_FORMAT,
            graceful_timeout=0,
        )

    async def start(self):
        self.app = FastAPI()
        self.add_task(serve(
            self.app,
            self.hypercorn_config,
            shutdown_trigger=asyncio.Future,  # no signal handling
        ))

    def add_route(self, *args, **kwargs):
        self.app.add_api_route(*args, **kwargs)

    def add_get(self, *args, **kwargs):
        self.add_route(*args, methods=["get"], **kwargs)

    def add_post(self, *args, **kwargs):
        self.add_route(*args, methods=["post"], **kwargs)


@register(name="web_server", singleton=True)
@inject
def web_server_from_config(config):
    return WebServer(
        host=config.web_host,
        port=config.web_port,
    )
