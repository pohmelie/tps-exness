import asyncio
import json

from cock import build_entrypoint
from loguru import logger

from tps_exness import VERSION
from tps_exness.injector import register
from tps_exness.logging import configure_logging, log_options
from tps_exness.server import web_options
from tps_exness.service import TPSExnessService


async def amain():
    await TPSExnessService().run()


def main(config):
    register(lambda: config, singleton=True, name="config")
    register(lambda: VERSION, singleton=True, name="version")
    configure_logging(config.log_level)

    logger.info("tps-exness config: \n{}", json.dumps(config, indent=4))
    asyncio.run(amain())


options = [
    *web_options,
    *log_options,
]

entrypoint = build_entrypoint(main, options, auto_envvar_prefix="TPS_EXNESS", show_default=True)
if __name__ == "__main__":
    entrypoint(prog_name="tps-exness")
