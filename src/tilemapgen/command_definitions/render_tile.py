
from tilemapgen.stable_diffusion import DEVICE
from tilemapgen.configuration import RenderTileConfig
from tilemapgen.utils import read_image
import torch
from urllib.parse import urlparse
import numpy as np
import torchvision.transforms as transforms
from pytorch3d.common.datatypes import Device
from pytorch3d.io.mtl_io import make_mesh_texture_atlas
from pytorch3d.io import load_obj
from pytorch3d.structures import Meshes
from pytorch3d.renderer import (
    look_at_view_transform,
    FoVOrthographicCameras,
    RasterizationSettings,
    MeshRenderer,
    MeshRasterizer,
    SoftPhongShader,
    TexturesAtlas,
    DirectionalLights,
    BlendParams
)

def generate(cfg: RenderTileConfig):
    images = render(
        cfg.obj_path,
        cfg.mtl_path,
        cfg.wall_texture_image_path,
        cfg.floor_texture_image_path,
        cfg.image_size,
        cfg.camera_dist,
        cfg.elevation_angle,
        cfg.azimuth_angle,
        DEVICE,
    )
    return images

def config_class():
    return RenderTileConfig

def output_path(cfg: RenderTileConfig):
    return cfg.tile_path

def load_mtl(
    mtl_filename,
    texture_dict
):
    '''
    Returns:
        material_properties: dict of properties for each material. If a material
                does not have any properties it will have an empty dict.
                {
                    material_name_1:  {
                        "ambient_color": tensor of shape (1, 3),
                        "diffuse_color": tensor of shape (1, 3),
                        "specular_color": tensor of shape (1, 3),
                        "shininess": tensor of shape (1)
                    },
                    material_name_2: {},
                    ...
                }
        texture_images: dict of material names and texture images
                {
                    material_name_1: (H, W, 3) image,
                    ...
                }
    '''
    material_properties = {}
    texture_images = {}
    for name, texture_path in texture_dict.items():
        material_properties[name] = {}
        image = read_image(texture_path)
        texture_images[name] = torch.from_numpy(image/ 255.0).to(DEVICE)


    return material_properties, texture_images

def get_mesh(
    obj_filename,
    mtl_filename,
    wall_texture_path,
    floor_texture_path,
    device: Device = DEVICE,
):


    # Get vertices, faces, and auxiliary information
    # Get vertices, faces, and auxiliary information
    verts, faces, aux = load_obj(
        obj_filename,
        device=device,
        load_textures=False,
        create_texture_atlas=False,
    )

    #Load a new atlas
    material_names = ["Material", "Material.001"]
    material_properties, texture_images = load_mtl(
        mtl_filename,
        {
            "Material": wall_texture_path,
            "Material.001": floor_texture_path,
        }
    )

    idx = faces.materials_idx.cpu().numpy()
    face_material_names = np.array(material_names)[idx]  # (F,)
    face_material_names[idx == -1] = ""

    # Construct the atlas.
    texture_atlas = make_mesh_texture_atlas(
        material_properties,
        texture_images,
        face_material_names,
        faces.textures_idx,
        aux.verts_uvs,
        512,
        "repeat",
    )

    # Create a textures object
    atlas = TexturesAtlas(atlas=[texture_atlas])
    # Create Meshes object
    mesh = Meshes(
        verts=[verts],
        faces=[faces.verts_idx],
        textures=atlas,
    )
    return mesh


def get_renderer(image_size, dist, device, elev, azim):
    """
    Generates a mesh renderer by combining a rasterizer and a shader.

    Args:
        image_size: int, the size of the rendered .png image
        dist: int, distance between the camera and 3D object
        device: str, the torch device containing a device type ('cpu' or
        'cuda')
        elev: list, contains elevation values
        azim: list, contains azimuth angle values

    Returns:
        renderer: MeshRenderer class
    """
    # Initialize the camera with camera distance, elevation, azimuth angle,
    # and image size
    R, T = look_at_view_transform(dist=dist, elev=elev, azim=azim, degrees=True)

    cameras = FoVOrthographicCameras(device=device,  R=R, T=T, znear=0., max_y=2.83, min_y=-2.83,
                max_x=2.83, min_x=-2.83,)
    #cameras = FoVPerspectiveCameras(device=device, R=R, T=T,)
    raster_settings = RasterizationSettings(
        image_size=image_size,
        blur_radius=0.0,
        faces_per_pixel=5,
    )
    # Initialize rasterizer by using a MeshRasterizer class
    rasterizer = MeshRasterizer(
        cameras=cameras,
        raster_settings=raster_settings
    )
    # The textured phong shader interpolates the texture uv coordinates for
    # each vertex, and samples from a texture image.
    #lights = PointLights(device=device, location=[[7.0, -7.0, 3.0]])
    lights = DirectionalLights(ambient_color=((0.3, 0.3, 0.3), ), diffuse_color=((0.5, 0.5, 0.5), ), specular_color=((0.2, 0.2, 0.2), ), direction=((0,  -0.5, 1), ), device=DEVICE)
    blend_params = BlendParams(sigma=1e-4, gamma=1e-4, background_color=(0.0, 0.0, 0.0))
    shader = SoftPhongShader(device=device, cameras=cameras, lights=lights, blend_params=blend_params)
    # Create a mesh renderer by composing a rasterizer and a shader
    renderer = MeshRenderer(rasterizer, shader)
    return renderer


def render(
    obj_filename,
    mtl_filename,
    wall_texture_path,
    floor_texture_path,
    image_size,
    dist,
    elev,
    azim,
    device,
):
    """
    Combines the above steps.

    Args:
        image_size: int, the size of the rendered .png image
        dist: int, distance between the camera and 3D object
        device: str, the torch device containing a device type ('cpu' or
        'cuda')
        elev: list, contains elevation values
        azim: list, contains azimuth angle values
        obj_filename: str, path to the 3D obj filename

    Returns:
        None
    """
    renderer = get_renderer(image_size, dist, device, elev, azim)
    mesh = get_mesh(
        obj_filename,
        mtl_filename,
        wall_texture_path,
        floor_texture_path,
        device,
    )
    images = renderer(mesh)
    return [transforms.ToPILImage()(image.transpose(2,0 ).transpose(1,2)[:3,...]) for image in images]