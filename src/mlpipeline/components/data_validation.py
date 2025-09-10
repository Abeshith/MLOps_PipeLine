import os
import json
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from mlpipeline import logger
from mlpipeline.entity.config_entity import DataValidationConfig
from mlpipeline.observability.tracing import trace_function
from typing import Dict, Tuple

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def _convert_to_serializable(self, obj):
        """Convert numpy types to native Python types for JSON serialization"""
        if isinstance(obj, (np.integer, np.int8, np.int16, np.int32, np.int64,
                          np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, tuple):
            return tuple(self._convert_to_serializable(x) for x in obj)
        elif isinstance(obj, list):
            return [self._convert_to_serializable(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        return obj

    def generate_data_quality_report(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> Dict:
        """Generate data quality metrics for both datasets"""
        report = {
            "train_data": {
                "shape": train_df.shape,
                "missing_values": train_df.isnull().sum().to_dict(),
                "duplicates": int(train_df.duplicated().sum()),
                "numeric_columns": {
                    col: {
                        "mean": float(train_df[col].mean()),
                        "std": float(train_df[col].std()),
                        "min": float(train_df[col].min()),
                        "max": float(train_df[col].max())
                    }
                    for col in train_df.select_dtypes(include=[np.number]).columns
                }
            },
            "test_data": {
                "shape": train_df.shape,
                "missing_values": test_df.isnull().sum().to_dict(),
                "duplicates": int(test_df.duplicated().sum()),
                "numeric_columns": {
                    col: {
                        "mean": float(test_df[col].mean()),
                        "std": float(test_df[col].std()),
                        "min": float(test_df[col].min()),
                        "max": float(test_df[col].max())
                    }
                    for col in test_df.select_dtypes(include=[np.number]).columns
                }
            }
        }
        return self._convert_to_serializable(report)

    def generate_drift_report(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> Tuple[Dict, bool]:
        """Calculate drift between train and test datasets"""
        drift_report = {}
        drift_detected = False

        # Only compare numerical columns that are in both datasets
        numeric_cols = train_df.select_dtypes(include=[np.number]).columns
        test_numeric_cols = test_df.select_dtypes(include=[np.number]).columns
        common_numeric_cols = set(numeric_cols).intersection(test_numeric_cols)

        for column in common_numeric_cols:
            # Skip target column in test data if present
            if column == self.config.schema.get("target_column") and column in test_df.columns:
                continue

            # Perform Kolmogorov-Smirnov test
            ks_statistic, p_value = ks_2samp(train_df[column], test_df[column])
            
            # Consider drift if p-value < 0.05
            is_drift = p_value < 0.05
            if is_drift:
                drift_detected = True

            drift_report[column] = {
                "ks_statistic": float(ks_statistic),
                "p_value": float(p_value),
                "drift_detected": bool(is_drift)
            }

        return self._convert_to_serializable(drift_report), drift_detected

    @trace_function
    def validate_all_columns(self) -> bool:
        try:
            train_df = pd.read_csv(self.config.train_file_path)
            test_df = pd.read_csv(self.config.test_file_path)

            # Get expected columns from schema
            schema_cols = self.config.schema["columns"]
            target_col = self.config.schema["target_column"]

            # Validate train data columns
            train_cols = list(train_df.columns)
            missing_cols_train = [col for col in schema_cols if col not in train_cols]
            train_validation_status = len(missing_cols_train) == 0

            # Validate test data columns (excluding target)
            test_cols = list(test_df.columns)
            test_schema_cols = {k: v for k, v in schema_cols.items() if k != target_col}
            missing_cols_test = [col for col in test_schema_cols if col not in test_cols]
            test_validation_status = len(missing_cols_test) == 0

            # Validate data types
            dtype_validation_errors = []
            if train_validation_status:
                for col, dtype in schema_cols.items():
                    if col in train_df.columns and str(train_df[col].dtype) != str(dtype):
                        train_validation_status = False
                        dtype_validation_errors.append(f"{col} (expected type: {dtype}, got: {train_df[col].dtype})")

            # Generate validation status report
            validation_status = train_validation_status and test_validation_status
            validation_report = {
                "validation_status": validation_status,
                "train_validation": {
                    "status": train_validation_status,
                    "missing_columns": missing_cols_train,
                    "dtype_errors": dtype_validation_errors
                },
                "test_validation": {
                    "status": test_validation_status,
                    "missing_columns": missing_cols_test
                }
            }

            # Write validation status
            with open(self.config.validation_status_file, 'w') as f:
                json.dump(validation_report, f, indent=4)

            # Generate and save data quality report
            quality_report = self.generate_data_quality_report(train_df, test_df)
            with open(self.config.data_quality_report_file, 'w') as f:
                json.dump(quality_report, f, indent=4)

            # Generate and save drift report
            drift_report, drift_detected = self.generate_drift_report(train_df, test_df)
            
            # Create HTML drift report
            drift_html = self._create_drift_report_html(drift_report, validation_report)
            with open(self.config.drift_report_file, 'w') as f:
                f.write(drift_html)

            if validation_status:
                logger.info("Data validation successful")
            else:
                logger.warning("Data validation failed - Check reports for details")

            return validation_status

        except Exception as e:
            logger.exception("Error in data validation")
            raise e

    def _create_drift_report_html(self, drift_report: Dict, validation_report: Dict) -> str:
        """Create an HTML report for data drift analysis"""
        html = [
            "<html>",
            "<head>",
            "<title>Data Drift Report</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 20px; }",
            ".header { background-color: #f4f4f4; padding: 20px; }",
            ".section { margin: 20px 0; }",
            "table { border-collapse: collapse; width: 100%; }",
            "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "th { background-color: #f4f4f4; }",
            ".drift-detected { color: red; }",
            ".no-drift { color: green; }",
            "</style>",
            "</head>",
            "<body>",
            "<div class='header'>",
            "<h1>Data Drift Analysis Report</h1>",
            f"<p>Validation Status: <strong>{'Passed' if validation_report['validation_status'] else 'Failed'}</strong></p>",
            "</div>",
            "<div class='section'>",
            "<h2>Validation Details</h2>",
            "<h3>Training Data Validation</h3>",
            f"<p>Status: {validation_report['train_validation']['status']}</p>",
            f"<p>Missing Columns: {', '.join(validation_report['train_validation']['missing_columns']) or 'None'}</p>",
            f"<p>Data Type Errors: {', '.join(validation_report['train_validation'].get('dtype_errors', [])) or 'None'}</p>",
            "<h3>Test Data Validation</h3>",
            f"<p>Status: {validation_report['test_validation']['status']}</p>",
            f"<p>Missing Columns: {', '.join(validation_report['test_validation']['missing_columns']) or 'None'}</p>",
            "</div>",
            "<div class='section'>",
            "<h2>Data Drift Analysis</h2>",
            "<table>",
            "<tr>",
            "<th>Feature</th>",
            "<th>KS Statistic</th>",
            "<th>P-Value</th>",
            "<th>Drift Status</th>",
            "</tr>"
        ]

        for feature, details in drift_report.items():
            drift_status = "Drift Detected" if details["drift_detected"] else "No Drift"
            status_class = "drift-detected" if details["drift_detected"] else "no-drift"
            html.extend([
                "<tr>",
                f"<td>{feature}</td>",
                f"<td>{details['ks_statistic']:.4f}</td>",
                f"<td>{details['p_value']:.4f}</td>",
                f"<td class='{status_class}'>{drift_status}</td>",
                "</tr>"
            ])
        
        html.extend([
            "</table>",
            "</div>",
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html)

        return html_content
