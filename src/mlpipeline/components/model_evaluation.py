import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from mlpipeline.utils.common import load_bin, save_json
from mlpipeline.entity.config_entity import ModelEvaluationConfig
from mlpipeline import logger
from mlpipeline.observability.tracing import trace_function
import dagshub
try:
    dagshub.init(repo_owner='abheshith7', repo_name='MLOPS_PipeLine', mlflow=True)
except RuntimeError as e:
    if "429" in str(e):
        print("DagHub rate limit reached, continuing without DagHub integration")
    else:
        raise

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    @trace_function
    def eval_metrics(self, actual, pred, pred_proba=None):
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred, average='weighted')
        recall = recall_score(actual, pred, average='weighted')
        f1 = f1_score(actual, pred, average='weighted')
        
        auc = 0.5
        if pred_proba is not None:
            try:
                auc = roc_auc_score(actual, pred_proba)
            except:
                pass
                
        return accuracy, precision, recall, f1, auc

    @trace_function
    def log_into_mlflow(self):
        try:
            # Set MLflow tracking URI
            mlflow.set_tracking_uri("https://dagshub.com/abheshith7/MLOPS_PipeLine.mlflow/")
            
            test_data = pd.read_csv(self.config.test_data_path)
            model = load_bin(self.config.model_path)

            test_x = test_data.drop([self.config.target_column], axis=1)
            test_y = test_data[self.config.target_column]

            predicted_qualities = model.predict(test_x)
            
            try:
                predicted_proba = model.predict_proba(test_x)[:, 1]
            except:
                predicted_proba = None

            (accuracy, precision, recall, f1, auc) = self.eval_metrics(test_y, predicted_qualities, predicted_proba)

            # Log metrics to MLflow
            with mlflow.start_run(run_name="model_evaluation"):
                mlflow.log_metric("eval_accuracy", accuracy)
                mlflow.log_metric("eval_precision", precision)
                mlflow.log_metric("eval_recall", recall)
                mlflow.log_metric("eval_f1_score", f1)
                mlflow.log_metric("eval_auc_score", auc)

            scores = {
                "accuracy": accuracy, 
                "precision": precision, 
                "recall": recall, 
                "f1": f1,
                "auc": auc
            }
            save_json(path=self.config.metric_file_name, data=scores)

            logger.info(f"Model evaluation completed. Scores: {scores}")

        except Exception as e:
            logger.exception(e)
            raise e
