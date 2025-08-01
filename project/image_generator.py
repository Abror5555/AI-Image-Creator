# image_generator.py
import uuid
import os
from diffusers import StableDiffusionPipeline  # yoki o'zingiz ishlatayotgan model
import torch

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

MEDIA_DIR = "media"

def generate_image_from_text(prompt):
    image = pipe(prompt).images[0]

    file_name = f"gen_{uuid.uuid4().hex[:8]}.jpg"
    output_path = os.path.join(MEDIA_DIR, file_name)
    image.save(output_path)

    return output_path
