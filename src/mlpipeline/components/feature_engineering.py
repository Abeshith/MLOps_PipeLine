import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import mutual_info_classif
from sklearn.compose import ColumnTransformer
import json
from mlpipeline import logger
from mlpipeline.entity.config_entity import FeatureEngineeringConfig
from mlpipeline.observability.tracing import trace_function
from typing import Tuple, Dict, List

class FeatureEngineering:
    def __init__(self, config: FeatureEngineeringConfig, feature_config: Dict):
        self.config = config
        self.feature_config = feature_config
        self.numeric_features = feature_config['numeric_features']
        self.categorical_features = feature_config['categorical_features']
        self.target_column = feature_config['target_column']
        self.preprocessor = None

    def _create_preprocessor(self) -> ColumnTransformer:
        """Create a preprocessor for both numeric and categorical features"""
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(
            handle_unknown=self.feature_config['encoding']['handle_unknown'],
            sparse_output=False
        )

        return ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)
            ]
        )

    def _transform_data(self, df: pd.DataFrame) -> np.ndarray:
        """Transform the data using the preprocessor"""
        if self.preprocessor is None:
            self.preprocessor = self._create_preprocessor()
            self.preprocessor.fit(df[self.numeric_features + self.categorical_features])
        
        return self.preprocessor.transform(df[self.numeric_features + self.categorical_features])

    def _apply_transformations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply specified transformations to numeric features"""
        df = df.copy()
        transformations = self.feature_config.get('transformations', {})
        
        for feature, transforms in transformations.items():
            if feature in df.columns:
                for transform in transforms:
                    if transform == 'log':
                        # Add small constant to handle zeros/negative values
                        df[f'{feature}_log'] = np.log1p(df[feature] - df[feature].min() + 1)
        
        return df

    def _select_features(self, X: np.ndarray, y: pd.Series) -> Tuple[List[int], np.ndarray]:
        """Select features using mutual information"""
        k = self.feature_config['feature_selection']['k_best']
        mi_scores = mutual_info_classif(X, y)
        selected_indices = np.argsort(mi_scores)[-k:]
        return selected_indices.tolist(), mi_scores

    def _analyze_correlations(self, df: pd.DataFrame) -> None:
        """Calculate and save correlation analysis for numeric features"""
        numeric_data = df[self.numeric_features]
        correlation_matrix = numeric_data.corr()
        
        # Save correlation matrix
        os.makedirs(os.path.dirname(self.config.correlation_matrix_path), exist_ok=True)
        correlation_matrix.to_csv(self.config.correlation_matrix_path)
        
        # Create correlation heatmap using seaborn
        import seaborn as sns
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Feature Correlation Heatmap')
        
        # Save correlation heatmap
        os.makedirs(os.path.dirname(self.config.correlation_plot_path), exist_ok=True)
        plt.savefig(self.config.correlation_plot_path)
        plt.close()

    def _save_feature_importance(self, feature_names: List[str], mi_scores: np.ndarray) -> None:
        """Save feature importance analysis"""
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': mi_scores
        })
        importance_df = importance_df.sort_values('importance', ascending=False)
        
        # Save feature importance data
        os.makedirs(os.path.dirname(self.config.feature_importance_path), exist_ok=True)
        importance_df.to_csv(self.config.feature_importance_path, index=False)
        
        # Create feature importance plot
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(mi_scores)), importance_df['importance'])
        plt.xticks(range(len(mi_scores)), importance_df['feature'], rotation=45, ha='right')
        plt.title('Feature Importance (Mutual Information)')
        plt.tight_layout()
        
        # Save feature importance plot
        os.makedirs(os.path.dirname(self.config.feature_importance_plot_path), exist_ok=True)
        plt.savefig(self.config.feature_importance_plot_path)
        plt.close()

    @trace_function
    def engineer_features(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Main method to engineer features"""
        try:
            # Read the data
            train_df = pd.read_csv(self.config.train_data_path)
            test_df = pd.read_csv(self.config.test_data_path)

            logger.info("Applying transformations...")
            train_df = self._apply_transformations(train_df)
            test_df = self._apply_transformations(test_df)

            # Transform features
            logger.info("Transforming features...")
            X_train = self._transform_data(train_df)
            X_test = self._transform_data(test_df)

            # Get feature names after preprocessing
            feature_names = (
                self.numeric_features + 
                [f"{col}_{val}" for col, vals in 
                 zip(self.categorical_features, 
                     self.preprocessor.named_transformers_['cat'].categories_) 
                 for val in vals]
            )

            # Perform correlation analysis
            logger.info("Performing correlation analysis...")
            self._analyze_correlations(train_df)

            # Select features
            if 'feature_selection' in self.feature_config:
                logger.info("Selecting features...")
                selected_indices, mi_scores = self._select_features(X_train, train_df[self.target_column])
                X_train = X_train[:, selected_indices]
                X_test = X_test[:, selected_indices]
                selected_features = [feature_names[i] for i in selected_indices]
                
                # Save feature importance analysis
                logger.info("Saving feature importance analysis...")
                self._save_feature_importance(feature_names, mi_scores)
                
                # Save feature selection report
                selection_report = {
                    "selected_features": selected_features,
                    "n_features": len(selected_features)
                }
                os.makedirs(os.path.dirname(self.config.feature_selection_report), exist_ok=True)
                with open(self.config.feature_selection_report, 'w') as f:
                    json.dump(selection_report, f, indent=4)

            # Convert to DataFrame
            train_featured = pd.DataFrame(X_train, columns=selected_features)
            test_featured = pd.DataFrame(X_test, columns=selected_features)

            # Add target column to train data
            train_featured[self.target_column] = train_df[self.target_column]

            # Save processed data
            os.makedirs(os.path.dirname(self.config.processed_train_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.config.processed_test_path), exist_ok=True)
            train_featured.to_csv(self.config.processed_train_path, index=False)
            test_featured.to_csv(self.config.processed_test_path, index=False)

            logger.info("Feature engineering completed successfully")
            # Increment the feature engineering counter metric
            from mlpipeline.observability.metrics import pipeline_metrics
            pipeline_metrics.feature_engineering_counter.inc()
            return train_featured, test_featured

        except Exception as e:
            logger.error(f"Error in feature engineering: {str(e)}")
            raise e
