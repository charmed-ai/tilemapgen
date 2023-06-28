# Tilemap Generator

## Commands

### swatch

The swatch command is used to generate textures that will be used to render a tilemap. Think about this like working with an interior designer to decorate a room. You pick swatches you like to guide the design process.


```
options:
  --config_path str     Path for a config file
  --name str            Project directory where all images and metadata are stored
  --parent_path Path    Parent project directory where all projects are stored
  --debug bool
  --prompt str
  --negative_prompt str
  --seed int
  --num_inference_steps int
  --guidance_scale float
  --num_images int
```

`tilemapgen swatch --prompt "brick wall" --num_images 3`
Generates 3 swatch images


<img src="projects/example-project/swatches/01290f26-1fb8-463b-a725-cbfeda354d21.png"
     alt="brick wall swatch 1"
     style="margin-right: 10px; width: 128px;" />



# Render a tile
`tilegen render-tile --tile_geometry=/path/to/model.obj --wall_swatch=/path/to/swatch.png --floor_swatch=/path/to/swatch.png --prompt="my tile prompt"`

# Reimagine a tile
`tilegen tile2tile --tile_image=/path/to/rendering.png --prompt="my tile prompt" --seed=123`

# Render a tilemap
`tilegen render-tilemap --tilemap_config=/path/to/config.yaml --wall_swatch=/path/to/swatch.png --floor_swatch=/path/to/swatch.png --prompt="my tile prompt" --seed=123`