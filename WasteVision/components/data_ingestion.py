from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from typing import Optional

import gdown

from WasteVision.logger import logging
from WasteVision.exception import AppException
from WasteVision.entity.config_entity import DataIngestionConfig
from WasteVision.entity.artifacts_entity import DataIngestionArtifact


class DataIngestion:
    """Handles data download and extraction pipeline."""

    def __init__(self, config: DataIngestionConfig) -> None:
        if config is None:
            raise ValueError("DataIngestionConfig must not be None")
        self.config = config

    def _build_download_url(self, url: str) -> str:
        """Convert Google Drive URL to direct download link."""
        try:
            file_id = url.split("/")[-2]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        except Exception as e:
            raise AppException(f"Invalid Google Drive URL: {url}", sys) from e

    def download_data(self) -> Path:
        """Download dataset from configured URL."""
        try:
            download_dir = Path(self.config.data_ingestion_dir)
            download_dir.mkdir(parents=True, exist_ok=True)

            zip_path = download_dir / "dataset.zip"
            download_url = self._build_download_url(self.config.data_download_url)

            logging.info(
                "Starting dataset download",
                extra={"url": download_url, "output_path": str(zip_path)},
            )

            gdown.download(download_url, str(zip_path), quiet=False)

            if not zip_path.exists():
                raise FileNotFoundError(f"Download failed: {zip_path}")

            logging.info("Download completed", extra={"file": str(zip_path)})

            return zip_path

        except Exception as e:
            raise AppException(e, sys) from e

    def extract_zip_file(self, zip_path: Path) -> Path:
        """Extract zip file into feature store directory."""
        try:
            if not zip_path.exists():
                raise FileNotFoundError(f"Zip file not found: {zip_path}")

            extract_dir = Path(self.config.feature_store_file_path)
            extract_dir.mkdir(parents=True, exist_ok=True)

            logging.info(
                "Extracting dataset",
                extra={"zip_path": str(zip_path), "extract_to": str(extract_dir)},
            )

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

            logging.info("Extraction completed", extra={"output_dir": str(extract_dir)})

            return extract_dir

        except Exception as e:
            raise AppException(e, sys) from e

    def run(self) -> DataIngestionArtifact:
        """Execute full data ingestion pipeline."""
        logging.info("Data ingestion started")

        try:
            zip_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_path)

            artifact = DataIngestionArtifact(
                data_zip_file_path=str(zip_path),
                feature_store_path=str(feature_store_path),
            )

            logging.info(
                "Data ingestion completed successfully",
                extra={"artifact": str(artifact)},
            )

            return artifact

        except Exception as e:
            logging.error("Data ingestion failed", exc_info=True)
            raise AppException(e, sys) from e
