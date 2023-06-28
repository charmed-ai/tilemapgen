from dataclasses import dataclass, field
from pathlib import Path
import random
from typing import Optional, Tuple, List

@dataclass
class ProjectConfig:
    name: str = 'example-project'
    parent_path: Path = Path('./projects')
    debug: bool = False
    @property
    def root_path(self) -> Path:
        return self.parent_path / self.name

    @property
    def swatch_path(self) -> Path:
        return self.root_path / "swatches"

    @property
    def rendered_tile_path(self) -> Path:
        return self.root_path / "rendered-tiles"

    @property
    def generated_tile_path(self) -> Path:
        return self.root_path / "generated-tiles"

    @property
    def tilemap_path(self) -> Path:
        return self.root_path / "tilemaps"

    @property
    def geometry_path(self) -> Path:
        return self.root_path / "geometry"


@dataclass
class SwatchConfig(ProjectConfig):
    prompt: str = None
    negative_prompt: str = None
    seed: int = None
    num_inference_steps: int = 10
    guidance_scale: float = 7.5
    num_images: int = 1

@dataclass
class RenderTileConfig(ProjectConfig):
    obj_name: str = 'wall_edge_ne.obj'
    mtl_name: str = 'wall_edge_ne.mtl'

    wall_texture_id: str = None
    floor_texture_id: str = None

    image_size: int = 512
    camera_dist: float = 10
    elevation_angle: float = 30
    azimuth_angle: float = 45

    @property
    def obj_path(self) -> Path:
        return self.geometry_path / self.obj_name

    @property
    def mtl_path(self) -> Path:
        return self.geometry_path / self.mtl_name

    @property
    def wall_texture_image_path(self) -> Path:
        if self.wall_texture_id is None:
            return None
        return self.swatch_path / f"{self.wall_texture_id}.png"

    @property
    def wall_texture_config_path(self) -> Path:
        if self.wall_texture_id is None:
            return None
        return self.swatch_path / f"{self.wall_texture_id}.yaml"

    @property
    def floor_texture_image_path(self) -> Path:
        if self.floor_texture_id is None:
            return None
        return self.swatch_path / f"{self.floor_texture_id}.png"

    @property
    def floor_texture_config_path(self) -> Path:
        if self.floor_texture_id is None:
            return None
        return self.swatch_path / f"{self.floor_texture_id}.yaml"

@dataclass
class GenerateTileConfig(ProjectConfig):

    negative_prompt: str = "logo, words, letters, writing, chaotic. blurry. low quality. terrible art. bad art. glitchy. holes, gaps, people. characters, ugly, broken. muddled. busy. deep fried, complicated. boring. confusing. mutated. artifacts. watermark."
    num_images: int = 1
    seed: int = None
    num_inference_steps: int = 30
    guidance_scale: float = 7.5

    rendered_tile_id: str = None

    prompt: str = None
    min_strength: float = 0.3
    max_strength: float = 0.8
    strength: float = None

    def __post_init__(self):
        if self.strength is None:
            self.strength = self.min_strength + (self.max_strength - self.min_strength) * random.random()

    @property
    def rendered_tile_image_path(self) -> Path:
        if self.rendered_tile_id is None:
            return None
        return self.rendered_tile_path / f"{self.rendered_tile_id}.png"

    @property
    def rendered_tile_config_path(self) -> Path:
        if self.rendered_tile_id is None:
            return None
        return self.rendered_tile_path / f"{self.rendered_tile_id}.yaml"

@dataclass
class TilemapConfig(ProjectConfig):
    generated_tile_id: str = None
    width: int = 256
    tile_obj_names: List[str] = field(default_factory=[
        "wall_edge_ne.obj",
        "wall_edge_nw.obj",
        "wall_edge_se.obj",
        "wall_edge_sw.obj",
        "floor_empty.obj",
        "floor_raised.obj",
        "floor_ramp_ne.obj",
        "floor_ramp_nw.obj",
        "floor_ramp_se.obj",
        "floor_ramp_sw.obj",
    ].copy)

    @property
    def generated_tile_image_path(self) -> Path:
        if self.generated_tile_id is None:
            return None
        return self.generated_tile_path / f"{self.generated_tile_id}.png"

    @property
    def generated_tile_config_path(self) -> Path:
        if self.generated_tile_id is None:
            return None
        return self.generated_tile_path / f"{self.generated_tile_id}.yaml"