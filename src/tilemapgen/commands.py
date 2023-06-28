from tilemapgen import configuration, utils
from tilemapgen.command_definitions import swatch, render_tile, tile2tile
from tilemapgen.logging import configure_logger, logger
import pyrallis
import sys
from uuid import uuid4


def generate_and_save(command_module, cfg, name):
    images = command_module.generate(cfg)
    for image in images:
        id = str(uuid4())
        logger.info(f"Generated id = {id}")
        utils.save_image(image, f"{id}.png", command_module.output_path(cfg))
        utils.save_config(cfg, f"{id}.yaml", command_module.output_path(cfg))

COMMANDS = {
    'swatch': swatch,
    'render-tile': render_tile,
    'tile2tile': tile2tile
}

def execute(command_name, args):
    if command_name not in COMMANDS:
        print(f"{command_name} is not a recognized command {list(COMMANDS.keys())}.")
        exit(1)

    command_module = COMMANDS[command_name]
    config = pyrallis.parse(config_class=command_module.config_class(), args=sys.argv[2:])
    configure_logger(config)

    logger.info(f"Executing {command_name}")
    generate_and_save(command_module, config, command_name)