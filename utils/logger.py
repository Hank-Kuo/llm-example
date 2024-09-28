import logging
import sys
import typing as t
from types import FrameType

from loguru import logger

_LOGGERS_MOVE_TO_LOGURU = [
    "uvicorn.asgi",
    "uvicorn.access",
    "uvicorn",
    "langfuse",
    "langchain",
]


class EndpointFilter(logging.Filter):
    """
    Simple filter to exclude logs from a specific endpoint
    """

    def __init__(
        self,
        path: str,
        *args: t.Any,
        **kwargs: t.Any,
    ):
        super().__init__(*args, **kwargs)
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self._path) == -1


class InterceptHandler(logging.Handler):
    """
    Intercept standard logging messages and redirect them to Loguru
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find the right caller from where the logging message was generated
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = t.cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class Logger:
    def __init__(self):
        self.logger = logger
        # remove default setting
        self.logger.remove()

        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<level>{message}</level>",
        )

    def init_config(self):
        # Remove health check logs
        logging.getLogger("uvicorn.access").addFilter(EndpointFilter(path="/health"))

        # change handlers for loguru
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in _LOGGERS_MOVE_TO_LOGURU:
            logging.getLogger(logger_name).handlers = [InterceptHandler()]

    def get_logger(self):
        return self.logger


Loggers = Logger()
log = Loggers.get_logger()