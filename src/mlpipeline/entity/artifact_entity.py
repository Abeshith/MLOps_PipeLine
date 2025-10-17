from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionArtifact:
    root_dir: Path
    raw_data_dir: Path
    train_data_dir: Path
    test_data_dir: Path
    train_file_path: Path
    test_file_path: Path
    message: str

@dataclass(frozen=True)
class DataValidationArtifact:
    validation_status: bool
    validation_status_file_path: Path
    drift_report_file_path: Path
    data_quality_report_file_path: Path
    train_file_path: Path
    test_file_path: Path

@dataclass(frozen=True)
class FeatureEngineeringArtifact:
    processed_train_path: Path
    processed_test_path: Path
    feature_importance_plot: Path
    correlation_matrix: Path
    feature_selection_report: Path
    selected_features: list[str]
    feature_importance_scores: dict

@dataclass(frozen=True)
class DataTransformationArtifact:
    transformed_train_file_path: Path
    transformed_test_file_path: Path
    preprocessor_object_file_path: Path


@dataclass(frozen=True)
class ModelTrainerArtifact:
    trained_model_file_path: Path
    train_metric_artifact: dict
    test_metric_artifact: dict

@dataclass(frozen=True)
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: Path
    trained_model_path: Path
    train_model_metric_artifact: dict
    best_model_metric_artifact: dict