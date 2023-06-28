import logging
from tilemapgen.configuration import ProjectConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()

def configure_logger(cfg: ProjectConfig):
    level = logging.DEBUG if cfg.debug else logging.INFO
    logger.setLevel(level)


