import torch
import random
from tilemapgen.configuration import Tile2TileConfig, TileConfig, SwatchConfig
from tilemapgen.stable_diffusion import get_depth2img_pipe, DEVICE, MAX_SEED
from tilemapgen.logging import logger
import pyrallis
from pyrallis.cfgparsing import load_config
from pyrallis.parsers.decoding import decode
from PIL import Image


def get_tile_config(path):
    with open(path, 'r') as f:
        dict = load_config(f)
        return decode(TileConfig, {
            'tile_id': dict.get('tile_id', None),
            'wall_texture_id': dict.get('wall_texture_id', None),
            'floor_texture_id': dict.get('floor_texture_id', None),
            'prompt': dict.get('prompt', None),
        })

def get_prompt(cfg: Tile2TileConfig):
    if cfg.prompt is not None:
        return cfg.prompt

    tile_config = get_tile_config(cfg.tile_config_path)
    if tile_config.prompt is not None:
        return tile_config.prompt

    wall_prompt = None
    if tile_config.wall_texture_config_path is not None:
        config = pyrallis.load(SwatchConfig, open(cfg.wall_texture_config_path,'r'))
        wall_prompt = config.prompt

    floor_prompt = None
    if tile_config.floor_texture_config_path is not None:
        config = pyrallis.load(SwatchConfig, open(cfg.floor_texture_config_path, 'r'))
        floor_prompt = config.prompt

    if wall_prompt is not None and floor_prompt is not None:
        return f"a vector illustration of an isometric game tile with a solid wall made of {wall_prompt} on a floor made of {floor_prompt}. in the style of an isometric rpg. starcraft. sim city. the sims. rollercoaster tycoon. simple"

    if floor_prompt is not None:
        return f"a vector illustration of an isometric game tile with a floor made of {floor_prompt}. in the style of an isometric rpg. starcraft. sim city. the sims. rollercoaster tycoon. simple"

    if wall_prompt is not None:
        return f"a vector illustration of an isometric game tile with a solid wall made of {wall_prompt}. in the style of an isometric rpg. starcraft. sim city. the sims. rollercoaster tycoon. simple"

    logger.error("No valid tile prompt. Falling back to generic.")
    return "a vevtor illustration of an isometric game tile. in the style of an isometric rpg. starcraft. sim city. the sims. rollercoaster tycoon. simple"

def generate(cfg: Tile2TileConfig):
    pipe = get_depth2img_pipe()
    seed = cfg.seed

    if seed is None:
        seed = int(random.randint(0,MAX_SEED))
    generator = torch.Generator(DEVICE).manual_seed(seed)


    images = pipe(
        [get_prompt(cfg)] * cfg.num_images,
        image=Image.open(cfg.tile_image_path),
        negative_prompt=[cfg.negative_prompt] * cfg.num_images,
        num_inference_steps=cfg.num_inference_steps,
        guidance_scale=cfg.guidance_scale,
        strength=cfg.resolved_strength,
        generator=generator,
    ).images
    return images

def config_class():
    return Tile2TileConfig

def output_path(cfg: Tile2TileConfig):
    return cfg.tile_path



