from tilemapgen.configuration import ProjectConfig
from pathlib import Path
from PIL import Image
import numpy as np

def save_image(image, name: str, path: Path):
    path.mkdir(parents=True, exist_ok=True)
    image.save(path / name)

def read_image(file_name):
    image = Image.open(file_name).convert("RGB")
    return np.asarray(image).astype(np.float32)