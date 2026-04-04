import sys, os
from WasteVision.logger import logging
from WasteVision.exception import AppException
from WasteVision.components.data_ingestion import DataIngestionimport
from typing import Optional

from WasteVision.logger import logging
from WasteVision.exception import AppException

from WasteVision.components.data_ingestion import DataIngestion
from WasteVision.components.data_validation import DataValidation
from WasteVision.components.model_trainer import ModelTrainer

from WasteVision.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    ModelTrainerConfig,
)

from WasteVision.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact,
)


class TrainPipeline:

    def __init__(self) -> None:
        """Initialize pipeline configurations."""
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.model_trainer_config = ModelTrainerConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Executes data ingestion stage.

        Returns:
            DataIngestionArtifact: Artifact containing ingestion outputs
        """
        try:
            logging.info("Starting data ingestion stage")

            ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            artifact = ingestion.initiate_data_ingestion()

            logging.info("Data ingestion completed successfully")
            return artifact

        except Exception as e:
            logging.error("Error during data ingestion")
            raise AppException(e, sys) from e

    def start_data_validation(
        self, ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        """
        Executes data validation stage.

        Args:
            ingestion_artifact (DataIngestionArtifact): Output from ingestion stage

        Returns:
            DataValidationArtifact: Validation results
        """
        try:
            logging.info("Starting data validation stage")

            validation = DataValidation(
                data_ingestion_artifact=ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            artifact = validation.initiate_data_validation()

            logging.info("Data validation completed successfully")
            return artifact

        except Exception as e:
            logging.error("Error during data validation")
            raise AppException(e, sys) from e

    def start_model_trainer(self) -> ModelTrainerArtifact:
        """
        Executes model training stage.

        Returns:
            ModelTrainerArtifact: Trained model details
        """
        try:
            logging.info("Starting model training stage")

            trainer = ModelTrainer(model_trainer_config=self.model_trainer_config)

            artifact = trainer.initiate_model_trainer()

            logging.info("Model training completed successfully")
            return artifact

        except Exception as e:
            logging.error("Error during model training")
            raise AppException(e, sys) from e

    def run_pipeline(self) -> Optional[ModelTrainerArtifact]:
        """
        Runs the complete ML pipeline.

        Returns:
            Optional[ModelTrainerArtifact]: Final model artifact if successful
        """
        try:
            logging.info("Pipeline execution started")

            ingestion_artifact = self.start_data_ingestion()

            validation_artifact = self.start_data_validation(
                ingestion_artifact=ingestion_artifact
            )

            if not validation_artifact.validation_status:
                raise ValueError("Data validation failed. Pipeline aborted.")

            model_artifact = self.start_model_trainer()

            logging.info("Pipeline execution completed successfully")
            return model_artifact

        except Exception as e:
            logging.critical("Pipeline execution failed")
            raise AppException(e, sys) from e
