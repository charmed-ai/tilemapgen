from diffusers import StableDiffusionPipeline
import torch
import random


MODEL_NAME='stabilityai/stable-diffusion-2-1'
MAX_SEED = (2**64)-1


DEVICE = 'mps'
DTYPE=torch.float
if torch.cuda.is_available() and torch.cuda.device_count() > 0:
    DEVICE = 'cuda'
    DTYPE=torch.float16

pipe = StableDiffusionPipeline.from_pretrained(MODEL_NAME, torch_dtype=DTYPE).to(DEVICE)
pipe.enable_attention_slicing()


def generate(
    prompt: str,
    generator: torch.Generator = None,
    negative_prompt: str = None,
    num_inference_steps: int = 10,
    guidance_scale: float = 7.5,
    num_images: int = 1,
):
    if generator is None:
        generator = torch.Generator(DEVICE).manual_seed(int(random.randint(0,MAX_SEED)))
    images = pipe(
        [f'texture of a {prompt}'] * num_images,
        negative_prompt=negative_prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator,
    ).images
    return images



