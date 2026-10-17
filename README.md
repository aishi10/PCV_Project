# 🛰️ DepthWizard
 
## Single-View Height Estimation and 3D Flythrough
 
**Smart India Hackathon 2026 — Problem Statement SIH26175**  
**Theme:** Disaster Management  
**Category:** Software  
**Team:** HEXORA
 
---
 
## 📌 Overview
 
**DepthWizard** is an AI-powered geospatial analysis platform designed to estimate terrain elevation and building heights from a **single RGB satellite or aerial image**.
 
The system uses **monocular depth estimation** to extract relative depth information from a single image and combines it with available geospatial information such as **SRTM 30 m DEMs, Ground Control Points (GCPs), and geospatial metadata** to transform relative depth into real-world metric heights.
 
The reconstructed elevation information is used to generate a **Digital Surface Model (DSM)** that can be explored through an interactive **3D terrain and city flythrough platform**.
 
DepthWizard also incorporates **per-pixel uncertainty/confidence estimation** and spatial accuracy visualization to identify regions where elevation predictions may be unreliable.
 
A key disaster-management application is **flood/inundation simulation**, where users can set water levels and identify potentially vulnerable areas using the reconstructed DSM.
 
---
 
# 🎯 Problem Statement
 
### SIH Problem Statement ID
 
**SIH26175**
 
### Problem Statement Title
 
**DepthWizard - Single-View Height Estimation and 3D Flythrough**
 
Traditional elevation mapping can require expensive systems such as LiDAR, stereo imaging, or specialized surveying equipment.
 
DepthWizard proposes a more accessible approach by combining **AI-based monocular depth estimation with geospatial scale calibration** to derive useful elevation and building-height information from a single RGB satellite/aerial image.
 
The system is designed to support applications in:
 
- Disaster Management
- Urban Planning
- Infrastructure Monitoring
- Terrain Analysis
- Defense Applications
---
 
# 💡 Proposed Solution
 
DepthWizard combines computer vision, remote sensing, geospatial calibration, and interactive 3D visualization into a unified workflow.
 
### Core Pipeline
 
```text
RGB Satellite / Aerial Image
            │
            ▼
     Image Preprocessing
            │
            ▼
   Monocular Depth Estimation
       (Depth Anything V2)
            │
            ▼
      Relative Depth Map
            │
            ▼
   DEM / GCP / Metadata
      Scale Calibration
            │
            ▼
     Metric Elevation
            │
            ▼
 Digital Surface Model (DSM)
            │
      ┌─────┴─────┐
      ▼           ▼
  3D Terrain    Accuracy &
  Visualization  Confidence
      │           Analysis
      ▼
 Flood / Inundation Simulation
```
 
---
 
# 🚀 Key Features
 
## 🛰️ 1. Single-View Height Estimation
 
Estimate elevation and building-height information from a **single RGB satellite or aerial image** using monocular depth estimation.
 
---
 
## 🧠 2. AI-Powered Depth Estimation
 
DepthWizard uses **Depth Anything V2** to generate relative depth maps from single-view RGB imagery.
 
The depth model provides the initial depth representation that is subsequently processed and calibrated using geospatial information.
 
---
 
## 📏 3. Intelligent Scale Calibration
 
Monocular depth estimation produces **relative depth rather than absolute elevation**.
 
DepthWizard addresses this scale ambiguity using:
 
* SRTM 30 m DEM
* Ground Control Points (GCPs)
* Geospatial metadata
This allows relative depth to be transformed into real-world metric heights.
 
---
 
## 🗺️ 4. Digital Surface Model Generation
 
The calibrated elevation information is used to generate a **Digital Surface Model (DSM)**.
 
The DSM can represent:
 
* Terrain
* Buildings
* Structures
* Other visible surface features
Building-height information can also be extracted from the reconstructed elevation data.
 
---
 
## 🎯 5. Confidence & Uncertainty Maps
 
DepthWizard proposes generating **per-pixel uncertainty/confidence scores** along with the estimated DSM.
 
This allows potentially unreliable regions to be identified instead of presenting every prediction as equally accurate.
 
Examples of challenging regions include:
 
* Dense vegetation
* Deep shadows
* Water
* Complex terrain
Spatial accuracy heatmaps can also be generated to visualize elevation errors against reference data.
 
---
 
## 🌍 6. Interactive 3D Terrain Visualization
 
The generated DSM can be converted into a 3D terrain representation.
 
The proposed platform provides:
 
* Interactive 3D terrain
* City flythrough
* Distance measurement
* Slope measurement
* Elevation-profile analysis
The visualization layer can be implemented using technologies such as:
 
* Three.js
* Unity
---
 
## 🌊 7. Flood / Inundation Simulation
 
DepthWizard enables disaster-management analysis by allowing users to define water levels.
 
The reconstructed DSM can then be used to identify areas potentially vulnerable to flooding.
 
```text
          Water Level
               │
               ▼
        ┌─────────────┐
        │     DSM     │
        └──────┬──────┘
               │
               ▼
     Compare Elevation
       Against Water
          Level
               │
               ▼
     Potentially Vulnerable
            Regions
```
 
---
 
# 🔬 Technical Approach
 
## 1. Data Acquisition & Preprocessing
 
RGB aerial/satellite imagery is collected from datasets such as:
 
* **ISPRS Potsdam**
* **HighBuild**
Images are then:
 
* Resized
* Normalized
* Prepared for model inference
---
 
## 2. Monocular Depth Estimation
 
**Depth Anything V2** is used to generate dense relative depth information from single-view RGB imagery.
 
### Input
 
```text
RGB Satellite / Aerial Image
```
 
### Output
 
```text
Relative Depth Map
```
 
The resulting depth map provides the foundation for subsequent elevation reconstruction.
 
---
 
## 3. Height Calibration & DSM Generation
 
Relative depth does not directly correspond to absolute elevation.
 
Therefore, DepthWizard proposes using:
 
* DEM data
* Ground Control Points
* Geospatial metadata
for scale calibration.
 
```text
Relative Depth
      +
DEM / GCP / Metadata
      ↓
Metric Elevation
      ↓
DSM Generation
```
 
---
 
## 4. 3D Visualization & Flythrough
 
The estimated DSM is converted into a 3D terrain mesh.
 
Users can interact with the reconstructed environment through a 3D viewer.
 
Proposed technologies:
 
* Three.js
* Unity
The platform supports terrain exploration and measurement tools.
 
---
 
## 5. Accuracy & Reliability
 
DepthWizard evaluates reconstructed elevation against reference data.
 
### Evaluation Metrics
 
#### RMSE
 
**Root Mean Square Error**
 
Measures the magnitude of elevation prediction errors while emphasizing larger errors.
 
#### MAE
 
**Mean Absolute Error**
 
Measures the average absolute difference between predicted and reference elevation values.
 
### Spatial Evaluation
 
The system also proposes:
 
* Per-pixel confidence maps
* Uncertainty maps
* Spatial accuracy heatmaps
* Error visualization
This allows users to understand not only **how accurate the model is overall**, but also **where the model may be unreliable**.
 
---
 
# 🧩 System Architecture
 
```text
┌─────────────────────────────────┐
│   RGB Satellite / Aerial Image  │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│       Image Preprocessing       │
│                                 │
│  • Resize                       │
│  • Normalize                    │
│  • Prepare for inference        │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│       Depth Anything V2         │
│    Monocular Depth Estimation   │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│        Relative Depth Map       │
└───────────────┬─────────────────┘
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
┌───────────────┐  ┌────────────────┐
│ SRTM / DEM    │  │ GCP / Metadata │
└───────┬───────┘  └───────┬────────┘
        │                  │
        └────────┬─────────┘
                 ▼
┌─────────────────────────────────┐
│     Geospatial Scale            │
│          Calibration            │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│       Metric Elevation / DSM    │
└───────────────┬─────────────────┘
                │
        ┌───────┼───────────┐
        │       │           │
        ▼       ▼           ▼
   ┌────────┐ ┌─────────┐ ┌──────────────┐
   │   3D   │ │Accuracy │ │  Confidence  │
   │ Viewer │ │Analysis │ │ / Uncertainty│
   └────┬───┘ └─────────┘ └──────────────┘
        │
        ▼
┌─────────────────────────────────┐
│     Flood / Inundation          │
│           Simulation             │
└─────────────────────────────────┘
```
 
---
 
# 🛠️ Technology Stack
 
| Component           | Technology                      |
| ------------------- | -------------------------------- |
| Programming         | Python                          |
| Depth Estimation    | Depth Anything V2               |
| Input Data          | RGB Satellite / Aerial Imagery  |
| Reference Elevation | SRTM 30 m DEM                   |
| Calibration         | DEM / GCP / Geospatial Metadata |
| DSM Generation      | Calibrated Depth Estimation     |
| 3D Visualization    | Three.js / Unity                |
| Evaluation          | RMSE, MAE                       |
| Datasets            | ISPRS Potsdam, HighBuild        |
 
---
 
# 📊 Datasets
 
## ISPRS Potsdam Dataset
 
The **ISPRS Potsdam dataset** provides high-resolution aerial imagery and DSM ground-truth information for urban scene analysis.
 
It can be used for:
 
* Training/evaluation
* DSM validation
* Building-height analysis
* Elevation reconstruction
---
 
## HighBuild Dataset
 
The **HighBuild dataset** is considered for remote-sensing-based building-height estimation and elevation modeling.
 
It can support:
 
* Training
* Fine-tuning
* Calibration
* Benchmarking
* Building-height estimation
---
 
# ⚠️ Challenges & Proposed Solutions
 
| Challenge                                        | Proposed Solution                                      |
| ------------------------------------------------ | -------------------------------------------------------- |
| Domain gap between natural and satellite imagery | Fine-tune depth models using remote-sensing datasets   |
| Monocular scale ambiguity                        | DEM/GCP-based scale calibration                        |
| Different terrain types                          | Validate across diverse terrain and reference datasets |
| Vegetation                                       | Confidence/uncertainty estimation                      |
| Shadows                                          | Confidence maps and spatial error analysis             |
| Water                                            | Identify low-confidence regions                        |
| Elevation prediction errors                      | RMSE/MAE validation and accuracy heatmaps              |
 
---
 
# 📈 Evaluation Strategy
 
DepthWizard evaluates reconstructed DSMs against reference elevation data.
 
## Quantitative Evaluation
 
The primary metrics are:
 
```text
RMSE
MAE
```
 
### RMSE
 
```text
                 ┌─────────────────────────┐
                 │   Predicted Elevation   │
                 └────────────┬────────────┘
                              │
                              ▼
                     Compare with
                     Reference DSM
                              │
                              ▼
                             RMSE
```
 
### MAE
 
```text
Predicted Elevation
        +
Reference Elevation
        ↓
Absolute Error
        ↓
       MAE
```
 
## Spatial Evaluation
 
Numerical metrics are complemented by:
 
* Confidence maps
* Uncertainty maps
* Accuracy heatmaps
* Error visualization
This helps identify regions where the model performs well or poorly.
 
---
 
# 🌍 Applications
 
## 🌊 Disaster Management
 
* Flood/inundation simulation
* Identification of potentially vulnerable regions
* Rapid terrain assessment
* Elevation-based disaster analysis
## 🏙️ Urban Planning
 
* Building-height estimation
* 3D city visualization
* Terrain analysis
* Urban structure analysis
## 🏗️ Infrastructure Monitoring
 
* Height estimation
* Terrain-based assessment
* Geospatial monitoring
## 🗺️ Terrain Analysis
 
* Elevation visualization
* Slope analysis
* Elevation profiling
* 3D terrain exploration
## 🛡️ Defense Applications
 
The reconstructed terrain and 3D visualization can potentially support terrain-based analysis and situational understanding.
 
---
 
# 💥 Impact & Benefits
 
### Enhanced Terrain Intelligence
 
Generates elevation and height information from single-view imagery for improved geospatial analysis.
 
### 💰 Cost-Effective
 
Reduces dependence on expensive LiDAR, stereo imaging, and specialized sensors.
 
### 📊 Improved Decision Making
 
Supports applications in:
 
* Disaster management
* Urban planning
* Infrastructure monitoring
* Terrain analysis
* Defense
### ⚡ Rapid Processing
 
The proposed approach aims to produce elevation maps and 3D visualizations faster than traditional surveying workflows.
 
### 🌎 Scalable & Accessible
 
Uses widely available satellite and aerial imagery, along with publicly available elevation information.
 
### 🎮 Interactive Visualization
 
3D flythroughs and measurement tools provide an intuitive way to explore complex terrain and structural information.
 
---
 
# 📂 Project Structure
 
The project structure may evolve during implementation.
 
```text
DepthWizard/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
│
├── models/
│   └── depth_anything/
│
├── preprocessing/
│   ├── image_preprocessing.py
│   └── data_loader.py
│
├── depth_estimation/
│   └── depth_inference.py
│
├── calibration/
│   ├── dem_calibration.py
│   └── gcp_calibration.py
│
├── dsm/
│   └── dsm_generation.py
│
├── evaluation/
│   ├── metrics.py
│   └── error_analysis.py
│
├── confidence/
│   └── uncertainty.py
│
├── visualization/
│   ├── terrain_viewer/
│   └── flythrough/
│
├── simulation/
│   └── flood_simulation.py
│
├── notebooks/
│
├── requirements.txt
├── README.md
└── LICENSE
```
 
> **Note:** Update this structure to match the actual repository once development is finalized.
 
---
 
# ⚙️ Installation
 
## 1. Clone the Repository
 
```bash
git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPOSITORY>.git
cd <YOUR-REPOSITORY>
```
 
## 2. Create a Virtual Environment
 
```bash
python -m venv venv
```
 
### Windows
 
```bash
venv\Scripts\activate
```
 
### Linux / macOS
 
```bash
source venv/bin/activate
```
 
## 3. Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
---
 
# ▶️ Usage
 
The general workflow is:
 
### Step 1 — Input Image
 
Provide an RGB satellite or aerial image.
 
```text
RGB Satellite / Aerial Image
```
 
### Step 2 — Depth Estimation
 
Run Depth Anything V2.
 
```text
RGB Image
    ↓
Depth Anything V2
    ↓
Relative Depth Map
```
 
### Step 3 — Geospatial Calibration
 
Provide available:
 
* DEM
* GCP
* Geospatial metadata
```text
Relative Depth
      +
Geospatial Reference
      ↓
Metric Elevation
```
 
### Step 4 — DSM Generation
 
Generate the calibrated Digital Surface Model.
 
### Step 5 — 3D Visualization
 
Load the DSM into the 3D visualization platform.
 
Available analysis tools include:
 
* Distance
* Slope
* Elevation profile
* 3D flythrough
### Step 6 — Flood Simulation
 
Specify a water level and identify potentially vulnerable regions based on reconstructed elevation.
 
> **Note:** Exact execution commands will be added once the implementation is finalized.
 
---
 
# 🖥️ Demo & Screenshots
 
Screenshots and demo videos will be added as the implementation progresses.
 
## Input RGB Image
 
```text
[ Add Screenshot Here ]
```
 
## Relative Depth Map
 
```text
[ Add Screenshot Here ]
```
 
## Calibrated DSM
 
```text
[ Add Screenshot Here ]
```
 
## Confidence / Uncertainty Map
 
```text
[ Add Screenshot Here ]
```
 
## Interactive 3D Terrain
 
```text
[ Add Screenshot Here ]
```
 
## Flood Simulation
 
```text
[ Add Screenshot Here ]
```
 
---
 
# 🔬 Research Foundation
 
DepthWizard builds upon research in monocular depth estimation and remote sensing.
 
### Depth Anything V2
 
**Depth Anything V2: A More Capable Foundation Model for Monocular Depth Estimation (2024)**
 
Depth Anything V2 serves as the proposed monocular depth-estimation backbone.
 
### MiDaS
 
**Vision Transformers for Dense Prediction (2021)**
 
MiDaS demonstrates the feasibility of monocular depth estimation across diverse datasets.
 
### ISPRS Potsdam
 
High-resolution aerial imagery and DSM benchmark data for urban scene analysis.
 
### HighBuild
 
Remote-sensing dataset considered for building-height estimation and elevation modeling.
 
---
 
# 🔮 Future Scope
 
Potential extensions include:
 
* Fine-tuning depth models specifically for remote-sensing imagery
* Improved DEM/GCP-based calibration
* Advanced uncertainty estimation
* Semantic-aware elevation calibration
* Support for additional satellite datasets
* Improved building-height estimation
* Large-scale DSM generation
* Advanced flood-risk analysis
* More detailed 3D terrain interaction
* Integration of additional geospatial data sources
* Real-time disaster scenario analysis
---
 
# 🏆 Smart India Hackathon 2026
 
This project is developed as part of **Smart India Hackathon 2026**.
 
| Detail               | Information                                                       |
| -------------------- | ------------------------------------------------------------------- |
| Problem Statement ID | **SIH26175**                                                      |
| Problem Statement    | **DepthWizard - Single-View Height Estimation and 3D Flythrough** |
| Theme                | **Disaster Management**                                           |
| Category             | **Software**                                                      |
| Team                 | **HEXORA**                                                        |
 
 
 
# 📚 References
 
1. Yang et al. — **Depth Anything V2: A More Capable Foundation Model for Monocular Depth Estimation**, 2024.
2. Ranftl et al. — **Vision Transformers for Dense Prediction**, 2021.
3. **ISPRS Potsdam Dataset** — High-resolution aerial imagery and DSM benchmark for urban scene analysis.
4. **HighBuild Dataset** — Remote-sensing dataset for building-height estimation and elevation modeling.
---
 
# ⭐ Why DepthWizard?
 
DepthWizard brings together four major capabilities:
 
```text
        🧠 AI DEPTH ESTIMATION
                 +
        🗺️ GEOSPATIAL CALIBRATION
                 +
        🌍 3D VISUALIZATION
                 +
        🌊 DISASTER SIMULATION
                 │
                 ▼
          ┌─────────────┐
          │ DEPTHWIZARD │
          └─────────────┘
```
 
Instead of treating monocular depth as the final output, DepthWizard proposes a complete pipeline connecting:
 
**Single RGB Image → Relative Depth → Metric Elevation → DSM → Confidence Analysis → 3D Visualization → Disaster Simulation**
 
This provides a unified framework for exploring how AI-based depth estimation can contribute to accessible terrain intelligence and disaster-management applications.
 
 
</div>
 
