from loguru import logger

from stela import env

logger.debug(env.to_dict)

NUMBER = env.CATS_NUMBER
NAMES = env.CATS_NAMES
