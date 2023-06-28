from tilemapgen.logging import logger
from pathlib import Path
from PIL import Image
import numpy as np
import pyrallis

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