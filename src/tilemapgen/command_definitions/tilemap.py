from tilemapgen.configuration import TilemapConfig, GenerateTileConfig, RenderTileConfig
from tilemapgen.stable_diffusion import DEVICE, MAX_SEED
from tilemapgen.command_definitions import render_tile, generate_tile
from tilemapgen.utils import generate_and_save
import pyrallis
from math import ceil, sqrt, floor
from PIL import Image

def generate(cfg: TilemapConfig):

    generated_tile_config = pyrallis.load(GenerateTileConfig, open(cfg.generated_tile_config_path, 'r'))
    rendered_tile_config = pyrallis.load(RenderTileConfig, open(generated_tile_config.rendered_tile_config_path, 'r'))


    generated_tiles = {}
    for obj_name in cfg.tile_obj_names:
        rendered_tile_config.obj_name = obj_name
        rendered_tile_id, rendered_tile_image_path = generate_and_save(render_tile, rendered_tile_config)[0]
        generated_tile_config.rendered_tile_id = rendered_tile_id
        generated_tile_config.num_images = 1
        generated_tile_id, generated_tile_image_path = generate_and_save(generate_tile, generated_tile_config)[0]
        generated_tiles[obj_name] = generated_tile_image_path

    tilemap = draw_tilemap(generated_tiles, cfg.width)
    return [tilemap]

def draw_tilemap(style_dict, width):
    width_count = ceil(sqrt(len(style_dict)))
    height_count = ceil(len(style_dict)/width_count)
    size = (width_count * width, height_count * width)
    tilemap = Image.new(mode="RGBA", size=size)

    for idx, (obj_path, tile_image_path) in enumerate(style_dict.items()):
        x = idx % width_count
        y = floor(idx / width_count)
        print(f"({x},{y})")
        cursor = (x * width, y * width)
        tile = Image.open(tile_image_path).resize((width, width))
        tilemap.paste(tile, cursor)

    return tilemap

def config_class():
    return TilemapConfig

def output_path(cfg: TilemapConfig):
    return cfg.tilemap_path



