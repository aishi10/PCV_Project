# DepthWizard

## Interactive 3D reconstruction from aerial imagery

DepthWizard is a browser-based terrain viewer for exploring a sample aerial image and generating an estimated 3D surface from an uploaded image. It combines a fine-tuned Depth Anything V2 model with a Three.js terrain renderer. The web page presents image texture, predicted surface relief, sample reference layers, measurements, and simple flood visualization in one interactive scene.

DepthWizard is a **single-image reconstruction tool**. It estimates a relative surface from visual cues in one image; it does not recover a surveyed digital elevation model, true building dimensions, or hidden sides of objects.

## What the website provides

### Visualization layers

- **RGB** displays the source image as a texture over the 3D surface.
- **HEIGHT** colors the active height grid with an elevation-style color ramp.
- **REFERENCE** shows the sample tile’s available GAMUS AGL height reference.
- **LAND COVER** shows the sample tile’s reference class labels, such as ground, vegetation, building, water, road, and tree.
- **WIRE** displays the height surface as a wireframe.

The REFERENCE and LAND COVER layers belong to the included `DC_28_04` example tile. They are not predictions or reference data for an uploaded image.

### Terrain and geometry

The viewer renders a 128 × 128 height grid on an interpolated Three.js plane. The terrain surface follows the active height field, while an optional building-geometry overlay fits cuboids to elevated, locally flat patches. For uploaded images, the depth grid is filtered to suppress isolated noise while preserving stronger height edges.

The cuboids are a geometric heuristic. They can help make flat-topped elevated features easier to inspect, but they are not guaranteed building detections and can include trees or other raised surfaces.

### Interactive tools

- Orbit the camera by dragging, zoom with the scroll wheel, and pan with the right mouse button.
- Use **Side profile** to inspect the surface from a near-horizontal angle.
- Use **Measure path** to pick two terrain points and see their distance, elevation difference, and slope.
- Use **Flood simulation** to move a horizontal level through the active height grid and visualize the portion below it.
- Use **Restore sample tile** to return to the original RGB image and height data after an upload.

Measurement labels marked with `*` are approximate. Uploaded-image elevation differences are relative units; they are not meters.

## Reconstruction pipeline

The upload workflow has a browser frontend and a local Python inference service:

1. The browser reads the selected image and submits it to `POST /api/reconstruct` on the local viewer server.
2. The server decodes the image with OpenCV and runs the GAMUS fine-tuned Depth Anything V2 ViT-B model using an input size of 518 pixels.
3. The server converts the model prediction to a robust relative range by clipping at the 2nd and 98th percentiles, then normalizes it to 0–1.
4. OpenCV resizes the prediction to a 128 × 128 grid and returns the grid as JSON.
5. The browser applies two edge-aware smoothing passes, rebuilds the mesh and estimated cuboids, and applies the uploaded image as the RGB texture.

The model checkpoint is loaded once when `viewer_server.py` starts. Inference uses CUDA when available, otherwise Apple MPS when available, and otherwise CPU.

### Upload constraints

- Maximum file size: **20 MB**
- Maximum decoded image size: **12 megapixels**
- Model input size: **518 pixels**
- Rendered reconstruction grid: **128 × 128 cells**

The depth model’s prediction is normalized independently for each image. This means heights are relative within that image and cannot be compared directly across different uploads. Accurate metric elevation requires suitable calibration or external elevation data.

## Sample data and evaluation figures

The viewer includes a `DC_28_04` GAMUS sample with an RGB texture, model-derived height grid, AGL reference heights, and reference land-cover classes. The website also displays the following epoch 13 held-out test-set figures:

| Evaluation measure | Reported result |
| --- | ---: |
| Test tiles | 100 |
| Overall MAE | 2.23 m |
| Overall RMSE | 4.81 m |
| Building MAE | 2.94 m |
| Tree MAE | 6.61 m |

These figures describe a benchmark evaluation using train-fitted calibration and ground-truth class masks. They are sample-set results, **not** an accuracy score or validation result for a user-uploaded image.

## Technology

- **Frontend:** HTML, CSS, JavaScript, and Three.js r128.
- **Backend:** Python `http.server` with a `POST /api/reconstruct` inference endpoint.
- **Model:** GAMUS fine-tuned Depth Anything V2 ViT-B, epoch 13.
- **Image and array processing:** OpenCV and NumPy.
- **Inference runtime:** PyTorch.
- **Transport:** local HTTP at `127.0.0.1:8765`.

The HTML page loads the Three.js library from cdnjs, so a network connection is needed to load that library. The selected image is sent to the local Python process for inference; it is not sent to a hosted model API.

## Project layout

```text
PCV_Project/
├── README.md
├── terrain_viewer.html
├── viewer_server.py
├── requirements.txt
├── .gitattributes
├── depth_anything_v2/
│   ├── dpt.py
│   ├── dinov2.py
│   ├── dinov2_layers/
│   └── util/
└── checkpoints/
    └── depth_anything_v2_vitb_gamus_epoch13.pth
```

`terrain_viewer.html` is the browser application. `viewer_server.py` serves the HTML and performs model inference. The `depth_anything_v2/` package implements the model architecture, and the checkpoint contains its fine-tuned weights. `requirements.txt` lists the Python dependencies.

## Run locally

From the repository root, create an environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the server from that same repository root:

```bash
python3 viewer_server.py
```

When the server reports that the model is ready, open:

```text
http://127.0.0.1:8765/terrain_viewer.html
```

Keep the terminal process running while using the viewer. Opening the HTML directly with a `file://` URL does not provide access to the inference endpoint.

## Git LFS and model weights

The epoch 13 checkpoint is approximately 390 MB. Track `.pth` files with Git LFS before adding the checkpoint to a Git repository:

```bash
git lfs install
git lfs track "*.pth"
git add .gitattributes checkpoints/depth_anything_v2_vitb_gamus_epoch13.pth
```

Git LFS must be installed on machines that clone the repository and need the actual checkpoint. LFS storage and bandwidth usage are subject to the repository owner’s GitHub plan.

## Scope and limitations

- A single image cannot reveal occluded surfaces or the full shape of objects.
- Perspective, image angle, shadows, trees, and scene content can influence the predicted relief.
- Uploaded output is relative and normalized; it is not a georeferenced or metric digital surface model.
- The 128 × 128 grid limits the fine detail visible in the mesh.
- Cuboid overlays are generated from local height patterns and may not align with real building footprints.
- The sample reference and benchmark layers apply only to the included GAMUS tile and benchmark dataset.
- GitHub Pages can host the static HTML, but cannot run the Python inference server. Uploaded-image reconstruction requires the local server or a separately deployed backend.

## Data and model attribution

This project uses the Depth Anything V2 codebase and a GAMUS fine-tuned ViT-B checkpoint. Retain the upstream model license and follow the applicable model and dataset terms when redistributing the source, checkpoint, or derived outputs. The reference and evaluation data originate from the GAMUS project assets included with the viewer.
