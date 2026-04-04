# ♻️ WasteVision-YOLO26 

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![YOLO26](https://img.shields.io/badge/Model-YOLO26-orange)
![Flask](https://img.shields.io/badge/Framework-Flask-green)

## 📌 Project Overview
This project implements a robust, end-to-end object detection pipeline designed to identify and classify 13 distinct categories of waste (e.g., plastic bags, food packaging, drink cans) to facilitate automated waste management. 

Built with scalability and reproducibility in mind, the project strictly adheres to Object-Oriented Programming (OOP) principles and MLOps best practices. It features a fully modular architecture with dedicated pipeline components for data ingestion, data validation, and model training. The final deep learning model is served via a Flask web application and fully containerized using Docker.

## 🚀 Key Features
*   **Deep Learning Architecture:** Utilizes the **YOLO26** algorithm for high-speed, accurate object detection and bounding box prediction.
*   **Custom Data Curation:** Dataset meticulously annotated in YOLO format using the `labelImg` tool.
*   **Modular MLOps Pipeline:** Codebase is structured into independent, reusable Python components (`Data Ingestion`, `Data Validation`, and `Model Trainer`).
*   **Automated Data Pipeline:** Securely fetches, extracts, and routes dataset splits from Google Drive utilizing `gdown`.
*   **Custom Logging & Exception Handling:** Features an advanced tracking system using Python's `logging` and custom `sys` exceptions to isolate pipeline errors and capture timestamped execution logs.
*   **Interactive Web App:** Includes a user-friendly Flask interface supporting both static image uploads (`/predict`) and live web-camera inferencing (`/live`).

## 🛠️ Technologies Used
*   **Machine Learning/Computer Vision:** YOLO26, OpenCV, PyTorch
*   **Programming & Backend:** Python 3.7, Flask, OOP principles
*   **Data Tools:** `labelImg`, `gdown`, PyYAML

## 🏗️ Pipeline Architecture 
The training pipeline is executed systematically through the `training_pipeline.py` script, which orchestrates the following stages:

1.  **Data Ingestion:** Downloads the zipped image dataset from a remote storage link (Google Drive), unzips the payload, and structures it into a `feature_store` containing `train`, `valid`, and `data.yaml` files.
2.  **Data Validation:** Automatically verifies the integrity of the ingested data. It checks that the required directories and structural files exist before permitting the model to train, returning a `True/False` validation status.
3.  **Model Trainer:** Fine-tunes the YOLO26 model on the validated dataset based on custom parameters (e.g., batch size, epochs). It generates the finalized `best.pt` weights and saves them to an artifacts directory for inferencing.

## 📂 Project Structure
```text
├── artifacts/              # Contains generated models and pipeline outputs
├── components/             # Core MLOps pipeline scripts
│   ├── data_ingestion.py   # Automated data downloading & extraction
│   ├── data_validation.py  # Dataset integrity checks
│   └── model_trainer.py    # YOLO26 fine-tuning script
├── constant/               # Hardcoded path variables and configuration constraints
├── entity/                 # Config and Artifact dataclasses
├── exception/              # Custom Python exception handling
├── logger/                 # Timestamped execution logging
├── templates/              # HTML/Bootstrap templates for the Flask app
├── app.py                  # Flask application entry point
├── requirements.txt        # Python package dependencies
└── setup.py                # Local package installation setup
```

## 💻 Installation & Local Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Piyushgaur26/end-to-end-waste-detection.git
cd end-to-end-waste-detection
```

### 2. Set Up a Virtual Environment
```bash
conda create -n waste_env python=3.13 -y
conda activate waste_env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application Locally
Launch the Flask web server:
```bash
python app.py
```
*   Access the web interface at `http://localhost:8080`.
*   To trigger the model training pipeline, navigate to `http://localhost:8080/train`.
*   To perform live web-camera prediction, navigate to `http://localhost:8080/live`.

