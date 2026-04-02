import logging
from pathlib import Path

# -------------------------------------------------------------------
# Logging configuration
# -------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Project configuration
# -------------------------------------------------------------------
PROJECT_NAME = "WasteVision-YOLOv5"

FILES_TO_CREATE = [
    ".github/workflows/main.yml",

    f"{PROJECT_NAME}/__init__.py",
    f"{PROJECT_NAME}/components/__init__.py",
    f"{PROJECT_NAME}/components/data_ingestion.py",
    f"{PROJECT_NAME}/components/data_validation.py",
    f"{PROJECT_NAME}/components/model_trainer.py",
    f"{PROJECT_NAME}/constant/__init__.py",
    f"{PROJECT_NAME}/constant/training_pipeline/__init__.py",
    f"{PROJECT_NAME}/constant/application.py",
    f"{PROJECT_NAME}/entity/config_entity.py",
    f"{PROJECT_NAME}/entity/artifacts_entity.py",
    f"{PROJECT_NAME}/exception/__init__.py",
    f"{PROJECT_NAME}/logger/__init__.py",
    f"{PROJECT_NAME}/pipeline/__init__.py",
    f"{PROJECT_NAME}/pipeline/training_pipeline.py",
    f"{PROJECT_NAME}/utils/__init__.py",
    f"{PROJECT_NAME}/utils/main_utils.py",
    
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html",
]


# -------------------------------------------------------------------
# File system utilities
# -------------------------------------------------------------------
def create_file(path: Path) -> None:
    """Create an empty file if it does not exist or is empty."""
    if path.exists() and path.stat().st_size > 0:
        logger.info("File already exists: %s", path)
        return

    path.touch()
    logger.info("Created file: %s", path)


def create_project_structure(files: list[str]) -> None:
    """Create required directories and files for the project."""
    for file in files:
        path = Path(file)
        path.parent.mkdir(parents=True, exist_ok=True)
        create_file(path)


# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------
if __name__ == "__main__":
    create_project_structure(FILES_TO_CREATE)
    logger.info("Project structure initialized successfully.")
