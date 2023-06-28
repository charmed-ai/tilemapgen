from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProjectConfig:
    name: str = 'example-project'
    parent_path: Path = Path('./projects')

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
class SwatchConfig:
    prompt: str = None
    negative_prompt: str = None
    seed: int = None
    num_inference_steps: int = 10
    guidance_scale: float = 7.5
    num_images: int = 1
    project: ProjectConfig = field(default_factory=ProjectConfig)

@dataclass
class RenderTileConfig:
    obj_name: str = 'wall_edge_ne.obj'
    mtl_name: str = 'wall_edge_ne.mtl'
    wall_texture_path: str = None
    floor_texture_path: str = None
    image_size: int = 512
    camera_dist: float = 10
    elevation_angle: float = 30
    azimuth_angle: float = 45
    project: ProjectConfig = field(default_factory=ProjectConfig)

    @property
    def obj_path(self) -> Path:
        return self.project.geometry_path / self.obj_name

    @property
    def mtl_path(self) -> Path:
        return self.project.geometry_path / self.mtl_name


