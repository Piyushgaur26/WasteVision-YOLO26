from setuptools import setup, find_packages
from pathlib import Path

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="WasteVision-YOLO26",
    version="0.0.1",
    author="Piyush Gaur",
    author_email="piyushgaur934@gmail.com",
    description="Waste Object Detection Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Piyushgaur26/WasteVision-YOLO26",
    project_urls={
        "Bug Tracker": "https://github.com/Piyushgaur26/WasteVision-YOLO26/issues",
    },
    packages=find_packages(),
)
