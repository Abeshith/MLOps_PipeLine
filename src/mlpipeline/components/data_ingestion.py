import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from mlpipeline import logger
from mlpipeline.utils.common import get_size
from mlpipeline.entity.config_entity import DataIngestionConfig
from mlpipeline.entity.artifact_entity import DataIngestionArtifact
from mlpipeline.observability.metrics import pipeline_metrics
from mlpipeline.observability.tracing import trace_function

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    @trace_function
    def download_file(self):
        """Download train and test data files from Kaggle"""
        try:
            # Initialize the Kaggle API
            api = KaggleApi()
            api.authenticate()
            
            # Download competition data
            logger.info(f"Downloading data from Kaggle competition: {self.config.competition_name}")
            
            # First download to raw data directory
            api.competition_download_file(
                competition=self.config.competition_name,
                file_name='train.csv',
                path=self.config.raw_data_dir
            )
            api.competition_download_file(
                competition=self.config.competition_name,
                file_name='test.csv',
                path=self.config.raw_data_dir
            )
            
            # Move files to their respective directories
            train_downloaded = os.path.join(self.config.raw_data_dir, 'train.csv')
            test_downloaded = os.path.join(self.config.raw_data_dir, 'test.csv')
            
            os.makedirs(os.path.dirname(self.config.local_train_file), exist_ok=True)
            os.makedirs(os.path.dirname(self.config.local_test_file), exist_ok=True)
            
            os.replace(train_downloaded, self.config.local_train_file)
            os.replace(test_downloaded, self.config.local_test_file)
                
            logger.info("Successfully downloaded competition data")
            pipeline_metrics.data_ingestion_counter.inc()
            
        except Exception as e:
            logger.error("Error downloading data files")
            raise e

    @trace_function
    def extract_data(self):
        """Verify, sample, and log information about the downloaded data"""
        try:
            # Load and verify training data
            train_df_full = pd.read_csv(self.config.local_train_file)
            logger.info(f"Full train data loaded - Shape: {train_df_full.shape}")
            
            # Sample 10,000 training samples
            train_sample_size = 10000
            if len(train_df_full) >= train_sample_size:
                # Sample with stratification if target column exists
                if 'y' in train_df_full.columns:
                    from sklearn.model_selection import train_test_split
                    train_df, _ = train_test_split(
                        train_df_full, 
                        train_size=train_sample_size,
                        random_state=42,
                        stratify=train_df_full['y']
                    )
                else:
                    train_df = train_df_full.sample(n=train_sample_size, random_state=42)
            else:
                logger.warning(f"Dataset has only {len(train_df_full)} samples, using all available")
                train_df = train_df_full
            
            # Save sampled train data
            train_df.to_csv(self.config.local_train_file, index=False)
            logger.info(f"Train data sampled and saved - Shape: {train_df.shape}")
            logger.info(f"Train data size: {get_size(self.config.local_train_file)}")
            pipeline_metrics.data_size_gauge.set(train_df.shape[0])
                
            # Load and verify test data
            test_df_full = pd.read_csv(self.config.local_test_file)
            logger.info(f"Full test data loaded - Shape: {test_df_full.shape}")
            
            # Sample 2,500 test samples
            test_sample_size = 2500
            if len(test_df_full) >= test_sample_size:
                test_df = test_df_full.sample(n=test_sample_size, random_state=42)
            else:
                logger.warning(f"Test dataset has only {len(test_df_full)} samples, using all available")
                test_df = test_df_full
            
            # Save sampled test data
            test_df.to_csv(self.config.local_test_file, index=False)
            logger.info(f"Test data sampled and saved - Shape: {test_df.shape}")
            logger.info(f"Test data size: {get_size(self.config.local_test_file)}")
                
            return train_df, test_df
            
        except FileNotFoundError as e:
            logger.error(f"Data file not found: {str(e)}")
            raise
        except pd.errors.EmptyDataError:
            logger.error("One or more data files are empty")
            raise
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            raise
            
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiate the data ingestion process
        :return: DataIngestionArtifact
        """
        try:
            self.download_file()
            train_df, test_df = self.extract_data()
            
            # Create success message
            message = "Data ingestion completed successfully."
            if train_df is None or test_df is None:
                message = "Warning: Some data files were not found or could not be loaded."
            
            data_ingestion_artifact = DataIngestionArtifact(
                root_dir=self.config.root_dir,
                raw_data_dir=self.config.raw_data_dir,
                train_data_dir=self.config.train_data_dir,
                test_data_dir=self.config.test_data_dir,
                train_file_path=self.config.local_train_file,
                test_file_path=self.config.local_test_file,
                message=message
            )
            
            logger.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
            
        except Exception as e:
            logger.error("Error in data ingestion")
            raise e
        except Exception as e:
            logger.exception(e)
            raise e
