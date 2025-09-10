from mlpipeline.constants import *
from mlpipeline.utils.common import read_yaml, create_directories
from mlpipeline.entity.config_entity import *
from typing import Dict

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config["artifacts_root"]])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config["data_ingestion"]
        
        # Create all required directories
        create_directories([
            config["root_dir"],
            config["raw_data_dir"],
            config["train_data_dir"],
            config["test_data_dir"]
        ])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config["root_dir"],
            raw_data_dir=config["raw_data_dir"],
            train_data_dir=config["train_data_dir"],
            test_data_dir=config["test_data_dir"],
            competition_name=config["competition_name"],
            local_train_file=config["local_train_file"],
            local_test_file=config["local_test_file"]
        )
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config["data_validation"]
        data_ingestion_config = self.config["data_ingestion"]
        
        create_directories([config["root_dir"]])

        data_validation_config = DataValidationConfig(
            root_dir=config["root_dir"],
            validation_status_file=config["validation_status_file"],
            drift_report_file=config["drift_report_file"],
            data_quality_report_file=config["data_quality_report_file"],
            schema=self.schema,
            validation_split=config["validation_split"],
            train_file_path=data_ingestion_config["local_train_file"],
            test_file_path=data_ingestion_config["local_test_file"]
        )
        return data_validation_config
    
    def get_feature_engineering_config(self) -> FeatureEngineeringConfig:
        config = self.config["feature_engineering"]
        
        create_directories([
            config["root_dir"],
            config["engineered_features_dir"],
            config["feature_importance_dir"],
            config["correlation_analysis_dir"],
            config["feature_selection_dir"]
        ])

        feature_engineering_config = FeatureEngineeringConfig(
            root_dir=config["root_dir"],
            engineered_features_dir=config["engineered_features_dir"],
            feature_importance_dir=config["feature_importance_dir"],
            correlation_analysis_dir=config["correlation_analysis_dir"],
            feature_selection_dir=config["feature_selection_dir"],
            train_data_path=config["train_data_path"],
            test_data_path=config["test_data_path"],
            processed_train_path=config["processed_train_path"],
            processed_test_path=config["processed_test_path"],
            feature_importance_path=config["feature_importance_path"],
            feature_importance_plot_path=config["feature_importance_plot_path"],
            correlation_matrix_path=config["correlation_matrix_path"],
            correlation_plot_path=config["correlation_plot_path"],
            feature_selection_report=config["feature_selection_report"]
        )
        return feature_engineering_config
        
    def get_feature_config(self) -> Dict:
        """Get feature engineering configuration from feature_config.yaml"""
        feature_config = read_yaml("config/feature_config.yaml")
        return feature_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config["data_transformation"]
        create_directories([config["root_dir"]])

        data_transformation_config = DataTransformationConfig(
            root_dir=config["root_dir"],
            data_path=config["data_path"],
            preprocessor_obj_file_path=config["preprocessor_obj_file_path"],
        )
        return data_transformation_config
    

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config["model_trainer"]
        params = self.params
        create_directories([config["root_dir"]])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config["root_dir"],
            train_data_path=config["train_data_path"],
            test_data_path=config["test_data_path"],
            model_name=config["model_name"],
            target_column=config["target_column"],
            expected_accuracy=config["expected_accuracy"],
            model_params=params
        )
        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config["model_evaluation"]
        create_directories([config["root_dir"]])

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config["root_dir"],
            test_data_path=config["test_data_path"],
            model_path=config["model_path"],
            metric_file_name=config["metric_file_name"],
            target_column=config["target_column"],
            mlflow_uri=config["mlflow_uri"]
        )
        return model_evaluation_config