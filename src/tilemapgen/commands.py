from tilemapgen import configuration, utils
from tilemapgen.command_definitions import swatch, render_tile
import pyrallis
import sys
from uuid import uuid4
import logging

def generate_and_save(command_module, cfg, name):
    images = command_module.generate(cfg)
    for image in images:
        filename = f"{name}_{uuid4()}.png"
        full_path = command_module.output_path(cfg)/ filename
        logging.info(f"Saving {full_path}")
        utils.save_image(image, filename, command_module.output_path(cfg))

COMMANDS = {
    'swatch': swatch,
    'render-tile': render_tile,
}

def execute(command_name, args):
    if command_name not in COMMANDS:
        print(f"{command_name} is not a recognized command {list(COMMANDS.keys())}.")
        exit(1)

    logging.info(f"Executing {command_name}")
    command_module = COMMANDS[command_name]
    config = pyrallis.parse(config_class=command_module.config_class(), args=sys.argv[2:])

    generate_and_save(command_module, config, command_name)