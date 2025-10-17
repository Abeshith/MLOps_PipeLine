import pandas as pd
import os
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from mlpipeline import logger
from mlpipeline.utils.common import save_bin
from mlpipeline.entity.config_entity import ModelTrainerConfig
from mlpipeline.observability.tracing import trace_function
from mlpipeline.observability.metrics import pipeline_metrics
import dagshub
import time

# Retry DagHub initialization with exponential backoff
for attempt in range(3):
    try:
        dagshub.init(repo_owner='abheshith7', repo_name='MLOPS_PipeLine', mlflow=True)
        break
    except RuntimeError as e:
        if "429" in str(e) and attempt < 2:
            time.sleep(2 ** attempt)
            continue
        raise

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    @trace_function
    def train(self):
        try:
            # Set MLflow tracking URI
            mlflow.set_tracking_uri("https://dagshub.com/abheshith7/MLOPS_PipeLine.mlflow/")
            
            train_data = pd.read_csv(self.config.train_data_path)
            test_data = pd.read_csv(self.config.test_data_path)

            train_x = train_data.drop([self.config.target_column], axis=1)
            test_x = test_data.drop([self.config.target_column], axis=1)
            train_y = train_data[self.config.target_column]
            test_y = test_data[self.config.target_column]

            # Get model parameters from config
            rf_params = self.config.model_params.get("RandomForestClassifier", {})
            lr_params = self.config.model_params.get("LogisticRegression", {})
            xgb_params = self.config.model_params.get("XGBClassifier", {})

            # Dictionary to store models and their scores
            models = {}
            model_scores = {}

            # Train Random Forest
            logger.info("Training Random Forest Classifier...")
            with mlflow.start_run(run_name="RandomForest_bank_marketing", nested=True):
                rf = RandomForestClassifier(**rf_params)
                rf.fit(train_x, train_y)
                
                train_pred_rf = rf.predict(train_x)
                test_pred_rf = rf.predict(test_x)
                
                train_acc_rf = accuracy_score(train_y, train_pred_rf)
                test_acc_rf = accuracy_score(test_y, test_pred_rf)
                test_f1_rf = f1_score(test_y, test_pred_rf, average='weighted')
                
                # Log parameters and metrics
                for param, value in rf_params.items():
                    mlflow.log_param(param, value)
                mlflow.log_metric("train_accuracy", train_acc_rf)
                mlflow.log_metric("test_accuracy", test_acc_rf)
                mlflow.log_metric("test_f1_score", test_f1_rf)
                
                models["RandomForest"] = rf
                model_scores["RandomForest"] = test_acc_rf
                
                logger.info(f"Random Forest - Test Accuracy: {test_acc_rf:.4f}")

            # Train Logistic Regression
            logger.info("Training Logistic Regression...")
            with mlflow.start_run(run_name="LogisticRegression_bank_marketing", nested=True):
                lr = LogisticRegression(**lr_params)
                lr.fit(train_x, train_y)
                
                train_pred_lr = lr.predict(train_x)
                test_pred_lr = lr.predict(test_x)
                
                train_acc_lr = accuracy_score(train_y, train_pred_lr)
                test_acc_lr = accuracy_score(test_y, test_pred_lr)
                test_f1_lr = f1_score(test_y, test_pred_lr, average='weighted')
                
                # Log parameters and metrics
                for param, value in lr_params.items():
                    mlflow.log_param(param, value)
                mlflow.log_metric("train_accuracy", train_acc_lr)
                mlflow.log_metric("test_accuracy", test_acc_lr)
                mlflow.log_metric("test_f1_score", test_f1_lr)
                
                models["LogisticRegression"] = lr
                model_scores["LogisticRegression"] = test_acc_lr
                
                logger.info(f"Logistic Regression - Test Accuracy: {test_acc_lr:.4f}")

            # Train XGBoost
            logger.info("Training XGBoost Classifier...")
            with mlflow.start_run(run_name="XGBoost_bank_marketing", nested=True):
                xgb = XGBClassifier(**xgb_params)
                xgb.fit(train_x, train_y)
                
                train_pred_xgb = xgb.predict(train_x)
                test_pred_xgb = xgb.predict(test_x)
                
                train_acc_xgb = accuracy_score(train_y, train_pred_xgb)
                test_acc_xgb = accuracy_score(test_y, test_pred_xgb)
                test_f1_xgb = f1_score(test_y, test_pred_xgb, average='weighted')
                
                # Log parameters and metrics
                for param, value in xgb_params.items():
                    mlflow.log_param(param, value)
                mlflow.log_metric("train_accuracy", train_acc_xgb)
                mlflow.log_metric("test_accuracy", test_acc_xgb)
                mlflow.log_metric("test_f1_score", test_f1_xgb)
                
                models["XGBoost"] = xgb
                model_scores["XGBoost"] = test_acc_xgb
                
                logger.info(f"XGBoost - Test Accuracy: {test_acc_xgb:.4f}")

            # Select best model
            best_model_name = max(model_scores, key=model_scores.get)
            best_model = models[best_model_name]
            best_score = model_scores[best_model_name]

            logger.info(f"Best model: {best_model_name} with accuracy: {best_score:.4f}")

            # Save best model if it meets the threshold
            if best_score >= self.config.expected_accuracy:
                os.makedirs(self.config.root_dir, exist_ok=True)
                save_bin(best_model, os.path.join(self.config.root_dir, self.config.model_name))
                
                # Update metrics
                pipeline_metrics.model_accuracy_gauge.set(best_score)
                pipeline_metrics.model_training_counter.inc()
                
                logger.info(f"Best model ({best_model_name}) saved successfully with accuracy: {best_score:.4f}")
                
                # Final MLflow run with best model (without model logging due to DagHub endpoint issue)
                with mlflow.start_run(run_name=f"Best_Model_{best_model_name}"):
                    mlflow.log_param("best_model", best_model_name)
                    mlflow.log_metric("best_accuracy", best_score)
                    # Note: Model logging disabled due to DagHub endpoint limitations
                
            else:
                raise Exception(f"Best model accuracy {best_score:.4f} is below threshold {self.config.expected_accuracy}")

        except Exception as e:
            logger.exception(e)
            raise e
