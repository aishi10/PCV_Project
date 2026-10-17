"""Serve the terrain viewer and reconstruct uploaded images with the local GAMUS model."""
from __future__ import annotations

import base64
import binascii
import json
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import urlparse

import cv2
import numpy as np
import torch

from depth_anything_v2.dpt import DepthAnythingV2


ROOT = Path(__file__).resolve().parent
CHECKPOINT = ROOT / "checkpoints" / "depth_anything_v2_vitb_gamus_epoch13.pth"
GRID_SIZE = 128
MAX_IMAGE_BYTES = 20 * 1024 * 1024
MAX_IMAGE_PIXELS = 12_000_000
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
MODEL_NAME = "GAMUS fine-tuned Depth Anything V2 ViT-B (epoch 13)"


def load_model():
    if not CHECKPOINT.is_file():
        raise FileNotFoundError(f"Fine-tuned checkpoint is missing: {CHECKPOINT}")
    model = DepthAnythingV2(
        encoder="vitb", features=128, out_channels=[96, 192, 384, 768]
    )
    state = torch.load(CHECKPOINT, map_location="cpu", weights_only=True)
    model.load_state_dict(state, strict=True)
    return model.to(DEVICE).eval()


MODEL = load_model()
INFERENCE_LOCK = Lock()


class ViewerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if urlparse(self.path).path != "/api/reconstruct":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_IMAGE_BYTES * 2:
                return self.send_json(413, {"error": "Upload is too large (20 MB maximum)"})
            payload = json.loads(self.rfile.read(length))
            data_url = payload.get("image", "")
            match = re.fullmatch(r"data:image/[a-zA-Z0-9.+-]+;base64,([A-Za-z0-9+/=]+)", data_url)
            if not match:
                return self.send_json(400, {"error": "Upload must be a supported image"})
            encoded = match.group(1)
            if len(encoded) > ((MAX_IMAGE_BYTES + 2) // 3) * 4:
                return self.send_json(413, {"error": "Upload is too large (20 MB maximum)"})
            raw = base64.b64decode(encoded, validate=True)
            image = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                return self.send_json(400, {"error": "Could not decode this image"})
            if image.shape[0] * image.shape[1] > MAX_IMAGE_PIXELS:
                return self.send_json(413, {"error": "Image dimensions exceed 12 megapixels"})
            with INFERENCE_LOCK, torch.inference_mode():
                prediction = MODEL.infer_image(image, input_size=518)
            prediction = np.asarray(prediction, dtype=np.float32)
            valid = np.isfinite(prediction)
            if not valid.any():
                return self.send_json(422, {"error": "The model could not infer depth for this image"})
            low, high = np.percentile(prediction[valid], [2, 98])
            if not np.isfinite(low + high) or high - low < 1e-6:
                return self.send_json(422, {"error": "The model returned a nearly flat depth map"})
            normalized = np.clip((prediction - low) / (high - low), 0, 1)
            normalized[~valid] = 0
            grid = cv2.resize(normalized, (GRID_SIZE, GRID_SIZE), interpolation=cv2.INTER_AREA)
            filename = str(payload.get("name", "uploaded image"))[:160]
            self.send_json(200, {
                "filename": filename,
                "grid_size": GRID_SIZE,
                "heights": grid.astype(np.float32).ravel().tolist(),
                "unit": "relative",
                "model": MODEL_NAME,
            })
        except (ValueError, json.JSONDecodeError, binascii.Error) as error:
            self.send_json(400, {"error": f"Invalid upload: {error}"})
        except Exception as error:
            self.log_error("Reconstruction failed: %s", error)
            self.send_json(500, {"error": "Depth reconstruction failed on the local server"})

    def send_json(self, status, value):
        body = json.dumps(value, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), ViewerHandler)
    print(f"Depth model ready on {DEVICE}; open http://127.0.0.1:8765/terrain_viewer.html", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping terrain viewer server")
    finally:
        server.server_close()
