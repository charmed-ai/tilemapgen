from tilemapgen import configuration, swatch
import pyrallis
import sys


def save_image(image, name: str, cfg: configuration.ProjectConfig):
    cfg.path.mkdir(parents=True, exist_ok=True)
    image.save(cfg.path / name)

def swatch_command(cfg: configuration.ProjectConfig):
    print("PROJECT CONFIG", cfg)
    print("SWATCH", cfg.wall_swatch)
    images = swatch.generate(
        cfg.wall_swatch.prompt
    )
    for idx, image in enumerate(images):
        save_image(image, f"image_{idx}.png", cfg)

COMMANDS = {
    'swatch': swatch_command
}

def execute(command, args):
    project_config = pyrallis.parse(config_class=configuration.ProjectConfig, args=sys.argv[2:])
    if command not in COMMANDS:
        print(f"{command} is not a recognized command.")
        exit(1)

    COMMANDS[command](project_config)
    print(project_config)