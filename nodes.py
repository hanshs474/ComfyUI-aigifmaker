import io
import os
import time

from . import aigifmaker_client as gm

KEY_TOOLTIP = (
    "Key from aigifmaker.ai/settings/apikeys. Leave empty to read AIGIFMAKER_API_KEY from the environment. "
    "Each GIF costs 1 credit on your AI GIF Maker account, the same as on the website."
)


def _output_dir() -> str:
    try:
        import folder_paths  # ComfyUI's own module, present when running inside ComfyUI

        return folder_paths.get_output_directory()
    except ImportError:
        return os.getcwd()


def _frames(data: bytes):
    """Decode every GIF frame into one IMAGE batch (N, H, W, 3)."""
    import numpy as np
    import torch
    from PIL import Image, ImageSequence

    gif = Image.open(io.BytesIO(data))
    arrs = [np.asarray(f.convert("RGB")).astype(np.float32) / 255.0 for f in ImageSequence.Iterator(gif)]
    return torch.from_numpy(np.stack(arrs))


class AigifmakerTextToGif:
    """Text to animated GIF with AI GIF Maker. Saves the .gif to ComfyUI's output folder and also
    returns its frames as an IMAGE batch, the file path and the hosted URL."""

    CATEGORY = "AI GIF Maker"
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("frames", "gif_path", "url")
    FUNCTION = "generate"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "a corgi in sunglasses dancing on a beach, looping"}),
            },
            "optional": {
                "api_key": ("STRING", {"default": "", "tooltip": KEY_TOOLTIP}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFF, "tooltip": "Change to force a new run"}),
            },
        }

    def generate(self, prompt, api_key="", seed=0):
        url = gm.generate(prompt, api_key=api_key or None)
        data = gm.download(url)
        path = os.path.join(_output_dir(), f"aigifmaker-{int(time.time())}.gif")
        with open(path, "wb") as f:
            f.write(data)
        return {"ui": {"text": [url]}, "result": (_frames(data), path, url)}


NODE_CLASS_MAPPINGS = {"AigifmakerTextToGif": AigifmakerTextToGif}
NODE_DISPLAY_NAME_MAPPINGS = {"AigifmakerTextToGif": "AI GIF Maker: Text to GIF"}
