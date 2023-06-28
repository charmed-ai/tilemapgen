from tilemapgen import configuration, utils
from tilemapgen.command_definitions import swatch, render_tile, generate_tile, tilemap
from tilemapgen.logging import configure_logger, logger
import pyrallis
import sys
from uuid import uuid4


COMMANDS = {
    'swatch': swatch,
    'render-tile': render_tile,
    'generate-tile': generate_tile,
    'tilemap': tilemap,
}

def execute(command_name, args):
    if command_name not in COMMANDS:
        print(f"{command_name} is not a recognized command {list(COMMANDS.keys())}.")
        exit(1)

    command_module = COMMANDS[command_name]
    config = pyrallis.parse(config_class=command_module.config_class(), args=sys.argv[2:])
    configure_logger(config)

    logger.info(f"Executing {command_name}")
    utils.generate_and_save(command_module, config)