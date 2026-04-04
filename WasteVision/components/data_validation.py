import os
import sys
import shutil
from typing import List

from WasteVision.logger import logging
from WasteVision.exception import AppException

from WasteVision.entity.config_entity import DataValidationConfig
from WasteVision.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
)


class DataValidation:
    """
    Handles validation of ingested data before model training.
    Ensures required files are present and dataset structure is correct.
    """

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ) -> None:
        """
        Initialize DataValidation with required artifacts and configs.
        """
        try:
            self.ingestion_artifact = data_ingestion_artifact
            self.config = data_validation_config
        except Exception as e:
            raise AppException(e, sys) from e

    def _write_validation_status(self, status: bool) -> None:
        """
        Writes validation status to a file.

        Args:
            status (bool): Validation result
        """
        os.makedirs(self.config.data_validation_dir, exist_ok=True)

        with open(self.config.valid_status_file_dir, "w") as f:
            f.write(f"validation_status: {status}")

    def validate_all_files_exist(self) -> bool:
        """
        Validates whether all required files exist in the feature store.

        Returns:
            bool: True if validation passes, else False
        """
        try:
            logging.info("Validating presence of required files")

            feature_store_path = self.ingestion_artifact.feature_store_path
            required_files: List[str] = self.config.required_file_list

            available_files = os.listdir(feature_store_path)

            missing_files = [
                file for file in required_files if file not in available_files
            ]

            if missing_files:
                logging.error(f"Missing required files: {missing_files}")
                self._write_validation_status(False)
                return False

            logging.info("All required files are present")
            self._write_validation_status(True)
            return True

        except Exception as e:
            logging.error("Error during file validation")
            raise AppException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Executes the data validation pipeline step.

        Returns:
            DataValidationArtifact: Validation results
        """
        logging.info("Data validation started")

        try:
            validation_status = self.validate_all_files_exist()

            artifact = DataValidationArtifact(validation_status=validation_status)

            if validation_status:
                logging.info("Copying validated data for downstream tasks")
                shutil.copy(
                    self.ingestion_artifact.data_zip_file_path,
                    os.getcwd(),
                )

            logging.info("Data validation completed successfully")
            return artifact

        except Exception as e:
            logging.critical("Data validation failed")
            raise AppException(e, sys) from e
