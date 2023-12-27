import logging

import pytest
from _pytest.logging import caplog as _caplog  # noqa
from loguru import logger


@pytest.fixture
def caplog(_caplog):  # noqa
    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    logger.add(PropogateHandler(), format="{message}")
    yield _caplog
