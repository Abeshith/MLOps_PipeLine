import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from mlpipeline import logger
from mlpipeline.utils.common import save_bin
from mlpipeline.entity.config_entity import DataTransformationConfig
from mlpipeline.observability.tracing import trace_function

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    @trace_function
    def get_data_transformer_object(self, feature_columns):
        try:
            # Since we already have processed features from feature engineering,
            # we'll just apply standard scaling to all numeric features
            num_pipeline = StandardScaler()

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, feature_columns)
            ])

            return preprocessor

        except Exception as e:
            logger.exception(e)
            raise e

    @trace_function
    def initiate_data_transformation(self):
        try:
            df = pd.read_csv(self.config.data_path)
            
            target_column_name = "y"
            
            # Remove ID column if exists
            if 'id' in df.columns:
                df = df.drop(['id'], axis=1)
            
            input_feature_df = df.drop(columns=[target_column_name], axis=1)
            target_feature_df = df[target_column_name]

            # Get feature columns (all columns except target)
            feature_columns = input_feature_df.columns.tolist()
            
            preprocessing_obj = self.get_data_transformer_object(feature_columns)

            # Transform the features (apply additional scaling if needed)
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_df)
            
            # Create DataFrame with transformed features
            full_df = pd.DataFrame(input_feature_train_arr, columns=feature_columns)
            full_df[target_column_name] = target_feature_df.values

            # Sample specific sizes: 10,000 for train and 2,500 for test
            train_size = 10000
            test_size = 2500
            total_needed = train_size + test_size
            
            if len(full_df) < total_needed:
                logger.warning(f"Dataset has only {len(full_df)} samples, but {total_needed} needed. Using all available data.")
                # Use proportional split if not enough data
                train_ratio = train_size / total_needed
                train_df, test_df = train_test_split(
                    full_df, 
                    train_size=train_ratio, 
                    random_state=42, 
                    stratify=full_df[target_column_name]
                )
            else:
                # Sample the required amounts
                train_df, temp_df = train_test_split(
                    full_df, 
                    train_size=train_size,
                    random_state=42, 
                    stratify=full_df[target_column_name]
                )
                
                if len(temp_df) >= test_size:
                    test_df, _ = train_test_split(
                        temp_df, 
                        train_size=test_size,
                        random_state=42, 
                        stratify=temp_df[target_column_name]
                    )
                else:
                    test_df = temp_df

            # Create output directory
            os.makedirs(self.config.root_dir, exist_ok=True)
            
            train_df.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
            test_df.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

            save_bin(preprocessing_obj, self.config.preprocessor_obj_file_path)

            logger.info("Data transformation completed")
            logger.info(f"Training data shape: {train_df.shape}")
            logger.info(f"Test data shape: {test_df.shape}")

            # Add metrics
            from mlpipeline.observability.metrics import pipeline_metrics
            pipeline_metrics.data_size_gauge.set(len(train_df))

            return (
                train_df,
                test_df,
                self.config.preprocessor_obj_file_path,
            )

        except Exception as e:
            logger.exception(e)
            raise e
