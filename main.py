from mlpipeline import logger
from mlpipeline.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from mlpipeline.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from mlpipeline.pipeline.stage_03_feature_engineering import FeatureEngineeringTrainingPipeline
from mlpipeline.pipeline.stage_04_data_transformation import DataTransformationTrainingPipeline
from mlpipeline.pipeline.stage_05_model_trainer import ModelTrainerTrainingPipeline
from mlpipeline.pipeline.stage_06_model_evaluation import ModelEvaluationTrainingPipeline
from mlpipeline.observability.metrics import pipeline_metrics
from mlpipeline.observability.logging_config import setup_logging
import os
import dagshub
dagshub.init(repo_owner='abheshith7', repo_name='MLOPS_PipeLine', mlflow=True)

# Setup observability
setup_logging()
pipeline_metrics.start_metrics_server(8000)



STAGE_NAME = "Data Ingestion stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Validation stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Feature Engineering stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    feature_engineering = FeatureEngineeringTrainingPipeline()
    feature_engineering.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Transformation stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Trainer stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    model_trainer = ModelTrainerTrainingPipeline()
    model_trainer.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Evaluation stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    model_evaluation = ModelEvaluationTrainingPipeline()
    model_evaluation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
