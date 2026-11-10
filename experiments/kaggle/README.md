# DFU-XAI: Kaggle GPU Training Guide

This guide walks you through training deep learning segmentation and representation models for **DFU-XAI** using Kaggle's free GPU resources (NVIDIA Tesla T4 x2 or P100, up to 30 hours per week).

---

## 1. Why Train on Kaggle?
- **Hardware Acceleration**: Local development machines without discrete NVIDIA GPUs (e.g. CPU-only laptops) cannot practically train Vision Transformers (SegFormer, ViT, DINOv2) within reasonable timeframes.
- **Pre-configured Medical ML Stack**: Kaggle environments provide pre-installed PyTorch, CUDA, torchvision, OpenCV, and high-speed network connections.
- **Dataset Access**: Public medical datasets (including DFU benchmarks) can be added to the notebook environment with one click.

---

## 2. Recommended Public DFU Datasets on Kaggle
You can attach any of the following existing public datasets directly to your Kaggle notebook:
1. **Diabetic Foot Ulcers Dataset**: Search "Diabetic Foot Ulcer" or "DFU" in the Kaggle Dataset tab.
2. **DFUC2020 (Diabetic Foot Ulcers Challenge 2020)**: Detection and localization benchmark.
3. **DFUC2021**: Multi-class classification (Infection, Ischemia).
4. **Foot Ulcer Segmentation Challenge / Medetec**: Pair of chronic wound photographs with ground-truth binary/tissue segmentation masks.

*(Note: The notebook also has a built-in procedural synthesizer, so you can test the entire GPU training loop and weight export immediately even before attaching external data!)*

---

## 3. Step-by-Step Training Instructions

### Step 1: Upload Notebook to Kaggle
1. Open your browser and go to [kaggle.com](https://www.kaggle.com) and log into your account.
2. Click **+ Create** in the top left and select **New Notebook**.
3. In the notebook menu bar, select:
   - **File** $\rightarrow$ **Import Notebook** $\rightarrow$ **Upload**.
   - Choose the file from your local machine:
     `experiments/kaggle/dfu_xai_kaggle_training.ipynb`

### Step 2: Enable GPU Acceleration
1. On the right-hand settings panel in Kaggle, expand the **Notebook options**.
2. Find **Accelerator** (defaults to None) and change it to **GPU T4 x2** (or **GPU P100**).
3. Ensure **Internet** is toggled **ON** (needed for `pip install transformers`).

### Step 3: Attach Dataset (Optional)
- In the right-hand panel under **Data**, click **+ Add Input**.
- Search for `Diabetic Foot Ulcer` or upload your institutionally approved dataset zip.
- The notebook will automatically search `/kaggle/input/` for `.jpg` and `.png` images and masks.

### Step 4: Run the Notebook
- Click **Run All** (or execute cells sequentially with `Shift + Enter`).
- The notebook will:
  1. Verify GPU availability (`torch.cuda.is_available()`).
  2. Load images and prepare zero-leakage patient-level splits.
  3. Initialize **SegFormer-B0** (`nvidia/mit-b0`).
  4. Train with combined **Dice + Cross-Entropy Loss** across epochs.
  5. Compute validation **Dice Score** and **IoU**.
  6. Plot an epistemic uncertainty heatmap sample.
  7. Save the best model weights to `/kaggle/working/segformer_b0_dfu_best.pt`.

---

## 4. Transferring the Weights Back to This Project

1. When training completes, go to the right-hand panel under **Output (/kaggle/working/)**.
2. Click the three dots `...` next to `segformer_b0_dfu_best.pt` and select **Download**.
3. Place the downloaded checkpoint file into your project's weights directory:
   ```bash
   mv ~/Downloads/segformer_b0_dfu_best.pt /home/devil/Documents/Projects/ME_Project/ml/weights/
   ```
4. Verify that the local model wrapper recognizes the weights:
   ```bash
   python3 -c "import os; print('Checkpoint exists:', os.path.exists('ml/weights/segformer_b0_dfu_best.pt'))"
   ```
5. Once in place, the FastAPI backend and Next.js frontend will automatically transition from demonstration heuristic mode to deep-learning neural network inference!
