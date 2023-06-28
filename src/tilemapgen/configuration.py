from dataclasses import dataclass, field
from pathlib import Path
import random

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
    def tile_path(self) -> Path:
        return self.root_path / "tiles"

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
    num_inference_steps: int = 30
    guidance_scale: float = 7.5
    num_images: int = 1

@dataclass
class TileConfig(ProjectConfig):
    tile_id: str = None
    wall_texture_id: str = None
    floor_texture_id: str = None
    prompt: str = None
    min_strength: float = 0.3
    max_strength: float = 0.8
    strength: float = None

    @property
    def resolved_strength(self) -> float:
        if self.strength is not None:
            return self.strength
        return self.min_strength + (self.max_strength - self.min_strength) * random.random()

    @property
    def tile_image_path(self) -> Path:
        if self.tile_id is None:
            return None
        return self.tile_path / f"{self.tile_id}.png"

    @property
    def tile_config_path(self) -> Path:
        if self.tile_id is None:
            return None
        return self.tile_path / f"{self.tile_id}.yaml"

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
class Tile2TileConfig(TileConfig):

    negative_prompt: str = "chaotic. blurry. low quality. terrible art. bad art. glitchy. holes, gaps, people. characters, ugly, broken. muddled. busy. deep fried, complicated. boring. confusing. mutated. artifacts. watermark."
    num_images: int = 1
    seed: int = None
    num_inference_steps: int = 10
    guidance_scale: float = 7.5

@dataclass
class RenderTileConfig(TileConfig):
    obj_name: str = 'wall_edge_ne.obj'
    mtl_name: str = 'wall_edge_ne.mtl'

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


