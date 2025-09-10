from mlpipeline.config.configuration import ConfigurationManager
from mlpipeline.components.feature_engineering import FeatureEngineering
from mlpipeline import logger

STAGE_NAME = "Feature Engineering stage"

class FeatureEngineeringTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        feature_engineering_config = config.get_feature_engineering_config()
        feature_config = config.get_feature_config()
        
        feature_engineering = FeatureEngineering(
            config=feature_engineering_config,
            feature_config=feature_config['feature_engineering']
        )
        
        train_featured, test_featured = feature_engineering.engineer_features()
        logger.info(f"Training data shape after feature engineering: {train_featured.shape}")
        logger.info(f"Test data shape after feature engineering: {test_featured.shape}")

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = FeatureEngineeringTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
