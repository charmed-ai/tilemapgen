import torch
import random
from tilemapgen.configuration import GenerateTileConfig, SwatchConfig, RenderTileConfig
from tilemapgen.stable_diffusion import get_depth2img_pipe, DEVICE, MAX_SEED
from tilemapgen.logging import logger
import pyrallis
from pyrallis.parsers.decoding import decode
from PIL import Image


def get_prompt(cfg: GenerateTileConfig):
    if cfg.prompt is not None:
        return cfg.prompt

    tile_config = pyrallis.load(RenderTileConfig, open(cfg.rendered_tile_config_path, 'r'))

    wall_prompt = None
    if tile_config.wall_texture_config_path is not None:
        config = pyrallis.load(SwatchConfig, open(tile_config.wall_texture_config_path,'r'))
        wall_prompt = config.prompt

    floor_prompt = None
    if tile_config.floor_texture_config_path is not None:
        config = pyrallis.load(SwatchConfig, open(tile_config.floor_texture_config_path, 'r'))
        floor_prompt = config.prompt

    if wall_prompt is not None and floor_prompt is not None:
        return f"a vector illustration of an isometric game tile with a solid wall made of {wall_prompt} on a floor made of {floor_prompt}. in the style of an isometric rpg. starcraft. sim city. the sims. rollercoaster tycoon. simple"

    if floor_prompt is not None:
        return f"a vector illustration of an isometric game tile with a floor made of {floor_prompt}. in the style of an isometric rpg. starcraft. sim city. the sims. rollercoaster tycoon. simple"

    if wall_prompt is not None:
        return f"a vector illustration of an isometric game tile with a solid wall made of {wall_prompt}. in the style of an isometric rpg. starcraft. sim city. the sims. rollercoaster tycoon. simple"

    logger.error("No valid tile prompt. Falling back to generic.")
    return "a vevtor illustration of an isometric game tile. in the style of an isometric rpg. starcraft. sim city. the sims. rollercoaster tycoon. simple"

def generate(cfg: GenerateTileConfig):
    pipe = get_depth2img_pipe()

    if cfg.seed is None:
        cfg.seed = int(random.randint(0,MAX_SEED))
    generator = torch.Generator(DEVICE).manual_seed(cfg.seed)

    cfg.prompt = get_prompt(cfg)

    for i in range(cfg.num_images):
        if i > 0:
            cfg.seed = int(random.randint(0,MAX_SEED))
            generator = torch.Generator(DEVICE).manual_seed(cfg.seed)
        image = pipe(
            cfg.prompt,
            image=Image.open(cfg.rendered_tile_image_path),
            negative_prompt=cfg.negative_prompt,
            num_inference_steps=cfg.num_inference_steps,
            guidance_scale=cfg.guidance_scale,
            strength=cfg.strength,
            generator=generator,
        ).images[0]
        yield image

def config_class():
    return GenerateTileConfig

def output_path(cfg: GenerateTileConfig):
    return cfg.generated_tile_path



