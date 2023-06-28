from diffusers import StableDiffusionPipeline, StableDiffusionDepth2ImgPipeline
import torch
import random

MAX_SEED = (2**64)-1
TXT2IMG_MODEL_NAME='stabilityai/stable-diffusion-2-1'
DEPTH2IMG_MODEL_NAME='stabilityai/stable-diffusion-2-depth'

if torch.cuda.is_available() and torch.cuda.device_count() > 0:
    DEVICE = 'cuda'
    DTYPE=torch.float16

elif torch.backends.mps.is_available():
    DEVICE = 'mps'
    DTYPE=torch.float
else:
    DEVICE = 'cpu'
    DTYPE=torch.float

txt2img_pipe = None
depth2img_pipe = None

def get_txt2img_pipe():
    global txt2img_pipe
    if txt2img_pipe is None:
        txt2img_pipe = StableDiffusionPipeline.from_pretrained(TXT2IMG_MODEL_NAME, torch_dtype=DTYPE).to(DEVICE)
        txt2img_pipe.enable_attention_slicing()
    return txt2img_pipe

def get_depth2img_pipe():
    global depth2img_pipe
    if depth2img_pipe is None:
        depth2img_pipe = StableDiffusionDepth2ImgPipeline.from_pretrained(DEPTH2IMG_MODEL_NAME, torch_dtype=DTYPE).to(DEVICE)
        depth2img_pipe.enable_attention_slicing()
    return depth2img_pipe