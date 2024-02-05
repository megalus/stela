from loguru import logger

from stela.config import StelaOptions


def custom_loader(options: StelaOptions, env_data: dict[str, any]) -> dict[str, any]:
    logger.info("Running custom loader")
    logger.debug(env_data)
    env_data.update({"NEW_ATTRIBUTE": "NEW_ATTRIBUTE", "SECRET": "ANOTHER_SECRET"})

    return env_data
