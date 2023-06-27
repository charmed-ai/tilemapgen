from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class SwatchConfig:
    prompt: str = None
    negative_prompt: str = None
    seed: int = None
    num_inference_steps: int = 10
    guidance_scale: float = 7.5
    num_images: int = 1

@dataclass
class ProjectConfig:
    name: str = 'example-project'
    parent_path: Path = Path('./projects')

    @property
    def path(self) -> Path:
        return self.parent_path / self.name
