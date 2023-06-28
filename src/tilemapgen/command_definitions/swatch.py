import torch
import random
from tilemapgen.configuration import SwatchConfig
from tilemapgen.stable_diffusion import get_txt2img_pipe, DEVICE, MAX_SEED

def generate(cfg: SwatchConfig):
    pipe = get_txt2img_pipe()

    if cfg.seed is None:
        cfg.seed = int(random.randint(0,MAX_SEED))
    generator = torch.Generator(DEVICE).manual_seed(cfg.seed)

    for i in range(cfg.num_images):
        if i > 0:
            cfg.seed = int(random.randint(0,MAX_SEED))
            generator = torch.Generator(DEVICE).manual_seed(cfg.seed)

        image = pipe(
            f'texture of a {cfg.prompt}',
            negative_prompt=cfg.negative_prompt,
            num_inference_steps=cfg.num_inference_steps,
            guidance_scale=cfg.guidance_scale,
            generator=generator,
        ).images[0]

        yield image


def config_class():
    return SwatchConfig

def output_path(cfg: SwatchConfig):
    return cfg.swatch_path



