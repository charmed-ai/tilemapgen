# Charmed
[Charmed](https://charmed.ai) is building AI tools for video game asset creation. You'll find a web version of [this tool](https://dungeon.charmed.ai), plus tools to [generate UV-mapped textures](https://texture.charmed.ai), and [generate quest dialogs](https://quest.charmed.ai).

# Tilemap Generator
The `tilemapgen` tool can be used to generate individual tiles or full tilemaps. The example project uses assets that create isometric view tiles, but the tool should work for other tile geometries with the right geometry inputs.

## Installation

### From pip

First [install pytorch3d](https://github.com/facebookresearch/pytorch3d/blob/main/INSTALL.md), then install the tilemapgen pip.
```bash
pip install tilemapgen
```

Access to the GPU will depend on the environment you are installing into.

### From code
```bash
git clone https://github.com/charmed.ai/tilemapgen
```

Clone this repository.

```bash
cd tilemapgen
conda env create -f environment.yml
```

This package was tested in an anaconda environment built from the included environment.yml file on Ubuntu 22.04.2 LTS with an NVIDIA GeForce RTX 3090 card.

```bash
pip install -e .
```

Install the pip from source


## Usage
`tilemapgen <command> [options]`

By default, outputs will be written to the `projects/example-project` directory but this can be changed by either supplying a `--config_path` with updated configuration, or by using the `--name` and `--parent_path` project arguments.

## swatch
`tilemapgen swatch [-h] [--config_path str] [--name str] [--parent_path Path] [--debug bool] [--prompt str] [--negative_prompt str] [--seed int] [--num_inference_steps int] [--guidance_scale float] [--num_images int]`

The swatch command is used to generate textures that will be used to render a tilemap. Think about this like working with an interior designer to decorate a room. You pick swatches you like to guide the design process.


`tilemapgen swatch --prompt "brick wall" --num_images 3`

Generates 3 swatch images


<img src="projects/example-project/swatches/01290f26-1fb8-463b-a725-cbfeda354d21.png"
     alt="brick wall swatch 1"
     style="margin-right: 10px; width: 128px;" />
<img src="projects/example-project/swatches/0d2315ee-3854-44f3-80d4-1d64a38ee38d.png"
     alt="brick wall swatch 1"
     style="margin-right: 10px; width: 128px;" />
<img src="projects/example-project/swatches/6e44d09a-3400-41ca-8974-d7fc081f3f76.png"
     alt="brick wall swatch 1"
     style="margin-right: 10px; width: 128px;" />



# render-tile
`tilemapgen render-tile [-h] [--config_path str] [--name str] [--parent_path Path] [--debug bool] [--obj_name str] [--mtl_name str] [--wall_texture_id str] [--floor_texture_id str] [--image_size int] [--camera_dist float] [--elevation_angle float] [--azimuth_angle float]`

The render-tile command is used to render a textured tile geometry using swatches.

`tilemapgen render-tile --wall_texture_id=01290f26-1fb8-463b-a725-cbfeda354d21 --floor_texture_id=a617b331-da86-4fcb-869e-0fdae48ea693`

<img src="projects/example-project/rendered-tiles/b2946e93-7608-49e5-b3be-e469741b25fd.png"
     alt="brick wall swatch 1"
     style="margin-right: 10px; width: 128px;" />

# generate-tile
`tilemapgen generate-tile [-h] [--config_path str] [--name str] [--parent_path Path] [--debug bool] [--negative_prompt str] [--num_images int] [--seed int] [--num_inference_steps int] [--guidance_scale float] [--rendered_tile_id str] [--prompt str] [--min_strength float] [--max_strength float] [--strength float]`

The generate-tile command uses the StableDiffusion depth2image model to explore variations from a rendered tile.

`tilemapgen generate-tile --rendered_tile_id=b2946e93-7608-49e5-b3be-e469741b25fd`

<img src="projects/example-project/generated-tiles/bff3ad0d-99fb-4883-a663-e905f4eba6a0.png"
     alt="brick wall swatch 1"
     style="margin-right: 10px; width: 128px;" />

# tilemap
`tilemapgen [-h] [--config_path str] [--name str] [--parent_path Path] [--debug bool] [--generated_tile_id str] [--width int] [--tile_obj_names List[str]]`

The tilemap command is used to generate a full set of tiles and compile them into a single image for use in a game engine.


`tilemapgen tilemap --generated_tile_id=bff3ad0d-99fb-4883-a663-e905f4eba6a0`

<img src="projects/example-project/tilemaps/8e3d5fe8-bbab-4e80-913f-96515089ed5e.png"
     alt="brick wall swatch 1"
     style="margin-right: 10px; width: 512px;" />
