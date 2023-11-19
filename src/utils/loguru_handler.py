# Created by https://t.me/vlasovdev loguru_handler file | Создано https://t.me/vlasovdev loguru_handler file

import logging
import sys

from loguru import logger


class LoguruHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = (sys._getframe(6), 6)  # noqa
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
