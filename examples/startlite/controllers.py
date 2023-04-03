from loguru import logger
from models import HelloWorld
from starlite import Controller, get

from stela import env
from stela.asyncio import aread_env


class HelloWorldController(Controller):
    path = "/"

    @get()
    async def get_info(self) -> HelloWorld:
        another_env = await aread_env()
        logger.debug(another_env.list())
        return HelloWorld(
            environment=env.current_environment,
            secret=env.MY_SECRET,
        )
