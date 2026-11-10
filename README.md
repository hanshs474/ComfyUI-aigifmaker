# ComfyUI-aigifmaker

Turn text into animated GIFs with AI GIF Maker. Native GIF generation — no video conversion. Type what you want and download your GIF in about a minute.

This is a ComfyUI node for [AI GIF Maker](https://aigifmaker.ai/?utm_source=comfyui&utm_medium=node): type a prompt in a graph, get back a real animated `.gif`. No local GPU and no model downloads, just one API key.

| Node | Inputs | Outputs |
|---|---|---|
| **AI GIF Maker: Text to GIF** | prompt, optional api_key, seed | `frames` (every GIF frame as an IMAGE batch), `gif_path` (the .gif saved in ComfyUI's output folder), `url` (hosted GIF) |

`frames` plugs into any IMAGE node, so you can upscale, recolor or re-encode the animation further down the graph.

## Install

ComfyUI Manager: search **ComfyUI-aigifmaker**. Or clone into `custom_nodes`:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/hanshs474/ComfyUI-aigifmaker
```

No extra Python dependencies: the client uses the standard library, and the node uses the torch, numpy and Pillow that ComfyUI already ships.

## API key

Create a key at https://aigifmaker.ai/settings/apikeys, then paste it into the node's `api_key` field or set `AIGIFMAKER_API_KEY` before starting ComfyUI.

Each GIF costs 1 credit on your AI GIF Maker account, the same as on the website. New accounts get one free GIF (it carries a small aigifmaker.ai badge). Credit packs are on the [pricing](https://aigifmaker.ai/pricing?utm_source=comfyui&utm_medium=node) page.

## Notes

- Describe the motion in the prompt ("waving", "spinning", "looping"); the model draws the frames itself as a GIF, not a converted video clip.
- The node blocks until the GIF is ready (15-minute limit). GIFs from accounts that have not bought credits may wait in a short queue first.
- Change `seed` to force a new run with the same prompt.
- A failed generation refunds its credit. Errors name the cause: a missing or wrong key, an empty balance, or a prompt the content filter refused.

Questions: support@aigifmaker.ai. MIT licensed.
