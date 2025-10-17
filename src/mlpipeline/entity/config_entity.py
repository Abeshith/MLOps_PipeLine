from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    raw_data_dir: Path
    train_data_dir: Path
    test_data_dir: Path
    competition_name: str
    local_train_file: Path
    local_test_file: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    validation_status_file: Path
    drift_report_file: Path
    data_quality_report_file: Path
    schema: dict
    validation_split: float
    train_file_path: Path
    test_file_path: Path

@dataclass(frozen=True)
class FeatureEngineeringConfig:
    root_dir: Path
    engineered_features_dir: Path
    feature_importance_dir: Path
    correlation_analysis_dir: Path
    feature_selection_dir: Path
    train_data_path: Path
    test_data_path: Path
    processed_train_path: Path
    processed_test_path: Path
    feature_importance_path: Path
    feature_importance_plot_path: Path
    correlation_matrix_path: Path
    correlation_plot_path: Path
    feature_selection_report: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    preprocessor_obj_file_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str
    target_column: str
    expected_accuracy: float
    model_params: dict

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    metric_file_name: Path
    target_column: str
    mlflow_uri: str