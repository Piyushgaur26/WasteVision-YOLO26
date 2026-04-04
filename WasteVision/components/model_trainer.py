import os
import sys
import shutil
from ultralytics import YOLO

from WasteVision.logger import logging
from WasteVision.exception import AppException
from WasteVision.entity.config_entity import ModelTrainerConfig
from WasteVision.entity.artifacts_entity import ModelTrainerArtifact


class ModelTrainer:
    """
    Handles model training using Ultralytics YOLO (YOLO26).
    """

    def __init__(self, model_trainer_config: ModelTrainerConfig) -> None:
        self.config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Trains YOLO model using Ultralytics API.

        Returns:
            ModelTrainerArtifact: Path to trained model
        """
        try:
            logging.info("Starting YOLO training")

            # ✅ Load model
            model = YOLO(self.config.weight_name)

            # ✅ Train model
            results = model.train(
                data=self.config.data_yaml_path,
                epochs=self.config.no_epochs,
                batch=self.config.batch_size,
                project=self.config.project_dir,
                name=self.config.run_name,
                imgsz=416,
            )

            # ✅ Get best model path
            best_model_path = os.path.join(
                self.config.project_dir,
                self.config.run_name,
                "weights",
                "best.pt",
            )

            # ✅ Save to artifacts
            os.makedirs(self.config.model_trainer_dir, exist_ok=True)

            final_model_path = os.path.join(self.config.model_trainer_dir, "best.pt")

            shutil.copy(best_model_path, final_model_path)

            logging.info(
                f"Model training completed. Model saved at: {final_model_path}"
            )

            return ModelTrainerArtifact(trained_model_file_path=final_model_path)

        except Exception as e:
            logging.error("Error during model training")
            raise AppException(e, sys) from e
