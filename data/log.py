"""Custom logger."""
from sys import stdout, stderr
from loguru import logger


def create_logger():
    """Create custom logger."""

    logger.remove()
    logger.add(
        stderr,
        colorize=True,
        level="INFO",
        catch=True,
        format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
        + "<light-green>{level}</light-green>: "
        + "<light-white>{message}</light-white>"
    )
    logger.add("log/file_{time}.log", rotation="500 MB")
    return logger


LOGGER = create_logger()
