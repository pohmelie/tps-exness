import httpx
import pytest
from cock import Config

from tps_exness.server import web_server_from_config
from tps_exness.logging import configure_logging_from_config
from tps_exness.service import TPSExnessService


@pytest.fixture
async def web_port(unused_tcp_port):
    return unused_tcp_port


@pytest.fixture
async def config(web_port):
    config = Config({
        "web_host": "127.0.0.1",
        "web_port": web_port,
        "log_level": "debug",
    })
    configure_logging_from_config(config)
    return config


@pytest.fixture
async def web_server(config):
    return web_server_from_config(config)


@pytest.fixture
async def service(web_server):
    async with TPSExnessService(web_server) as s:
        yield s


@pytest.fixture
async def client(service, web_port):
    async with httpx.AsyncClient(base_url=f"http://127.0.0.1:{web_port}") as c:
        yield c
