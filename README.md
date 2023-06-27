# Tilemap Generator

# Generate 4 swatch images
`tilegen swatch --prompt="my swatch prompt" -n 4`

# Render a tile
`tilegen render-tile --tile_geometry=/path/to/model.obj --wall_swatch=/path/to/swatch.png --floor_swatch=/path/to/swatch.png --prompt="my tile prompt"`

# Reimagine a tile
`tilegen tile2tile --tile_image=/path/to/rendering.png --prompt="my tile prompt" --seed=123`

# Render a tilemap
`tilegen render-tilemap --tilemap_config=/path/to/config.yaml --wall_swatch=/path/to/swatch.png --floor_swatch=/path/to/swatch.png --prompt="my tile prompt" --seed=123`