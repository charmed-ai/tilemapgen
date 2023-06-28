from tilemapgen.logging import logger
from pathlib import Path
from PIL import Image
import numpy as np
import pyrallis
from uuid import uuid4

def save_image(image, name: str, path: Path):
    logger.info(f"Saving {path/name}")
    path.mkdir(parents=True, exist_ok=True)
    image.save(path / name)

def save_config(cfg, name: str, path: Path):
    logger.info(f"Saving {path/name}")
    path.mkdir(parents=True, exist_ok=True)
    pyrallis.dump(cfg, open(path / name,'w'))

def read_image(file_name):
    image = Image.open(file_name).convert("RGB")
    return np.asarray(image).astype(np.float32)

def generate_and_save(command_module, cfg):
    result = []
    for image in command_module.generate(cfg):
        id = str(uuid4())
        logger.info(f"Generated id = {id}")
        image_name = f"{id}.png"
        save_image(image, image_name, command_module.output_path(cfg))
        save_config(cfg, f"{id}.yaml", command_module.output_path(cfg))
        result.append((id, command_module.output_path(cfg) / image_name))
    return result