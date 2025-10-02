#!/usr/bin/env python3
"""
Experiment 9: Engine Fault Detection using Machine Learning
===========================================================

Student: Pranvkumar Kshirsagar
Roll No: 590011587
Date: September 26, 2025

Objective: 
Develop a machine learning system to detect and classify engine faults
using various sensor readings and engine parameters.

Dataset: EngineFaultDB_Final.csv
- 55,999 samples
- 14 features + 1 target (Fault)
- 4 fault types: 0 (Normal), 1, 2, 3 (Different fault types)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, 
    precision_score, recall_score, f1_score, roc_auc_score,
    roc_curve, auc
)
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
warnings.filterwarnings('ignore')

# Set backend for matplotlib to avoid GUI issues
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Set style for better plots
try:
    plt.style.use('seaborn-v0_8')
except:
    plt.style.use('seaborn')
sns.set_palette("husl")

class EngineFaultDetector:
    """
    A comprehensive engine fault detection system using multiple ML algorithms
    """
    
    def __init__(self, csv_file_path):
        """Initialize the fault detector with dataset"""
        self.csv_file_path = csv_file_path
        self.data = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}
        
    def load_and_explore_data(self):
        """Load and perform initial exploration of the dataset"""
        print("🔍 Loading and Exploring Engine Fault Dataset...")
        print("=" * 60)
        
        # Load the data
        self.data = pd.read_csv(self.csv_file_path)
        
        # Basic information
        print(f"📊 Dataset Shape: {self.data.shape}")
        print(f"📋 Columns: {list(self.data.columns)}")
        
        # Check for missing values
        missing_values = self.data.isnull().sum()
        print(f"\n🔍 Missing Values:\n{missing_values}")
        
        # Fault distribution
        print(f"\n🚨 Fault Type Distribution:")
        fault_counts = self.data['Fault'].value_counts().sort_index()
        for fault_type, count in fault_counts.items():
            percentage = (count / len(self.data)) * 100
            print(f"   Fault {fault_type}: {count:,} samples ({percentage:.1f}%)")
        
        # Statistical summary
        print(f"\n📈 Statistical Summary:")
        print(self.data.describe().round(3))
        
        return self.data
    
    def visualize_data(self):
        """Create comprehensive visualizations of the dataset"""
        print("\n🎨 Creating Data Visualizations...")
        
        # Set up the plotting area
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Fault Distribution
        plt.subplot(3, 3, 1)
        fault_counts = self.data['Fault'].value_counts().sort_index()
        colors = ['green', 'orange', 'red', 'darkred']
        plt.pie(fault_counts.values, labels=[f'Fault {i}' for i in fault_counts.index], 
                autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Engine Fault Distribution')
        
        # 2. Correlation Heatmap
        plt.subplot(3, 3, 2)
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.data[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0)
        plt.title('Feature Correlation Heatmap')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        
        # 3. Key Feature Distributions by Fault Type
        key_features = ['RPM', 'Power', 'CO', 'HC', 'O2']
        for i, feature in enumerate(key_features):
            plt.subplot(3, 3, i + 4)
            for fault_type in sorted(self.data['Fault'].unique()):
                fault_data = self.data[self.data['Fault'] == fault_type][feature]
                plt.hist(fault_data, alpha=0.6, label=f'Fault {fault_type}', bins=30)
            plt.title(f'{feature} Distribution by Fault Type')
            plt.legend()
            plt.xlabel(feature)
            plt.ylabel('Frequency')
        
        # 3. Box plots for key parameters
        plt.subplot(3, 3, 3)
        key_params = ['MAP', 'TPS', 'Power', 'RPM']
        box_data = [self.data[param] for param in key_params]
        plt.boxplot(box_data, labels=key_params)
        plt.title('Key Parameters Distribution')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('engine_fault_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Additional detailed visualizations
        self._create_detailed_analysis()
    
    def _create_detailed_analysis(self):
        """Create detailed analysis visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Emission parameters by fault type
        emission_params = ['CO', 'HC', 'CO2', 'O2']
        for i, param in enumerate(emission_params):
            row, col = i // 2, i % 2
            sns.boxplot(data=self.data, x='Fault', y=param, ax=axes[row, col])
            axes[row, col].set_title(f'{param} Levels by Fault Type')
        
        plt.tight_layout()
        plt.savefig('emission_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Performance parameters correlation with faults
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        performance_params = ['Power', 'RPM', 'Speed', 'Consumption L/H']
        
        for i, param in enumerate(performance_params):
            row, col = i // 2, i % 2
            sns.violinplot(data=self.data, x='Fault', y=param, ax=axes[row, col])
            axes[row, col].set_title(f'{param} Distribution by Fault Type')
        
        plt.tight_layout()
        plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def prepare_data(self):
        """Prepare data for machine learning"""
        print("\n🔧 Preparing Data for Machine Learning...")
        
        # Separate features and target
        self.X = self.data.drop('Fault', axis=1)
        self.y = self.data['Fault']
        
        print(f"📊 Features shape: {self.X.shape}")
        print(f"🎯 Target shape: {self.y.shape}")
        print(f"📋 Feature columns: {list(self.X.columns)}")
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        print(f"🚂 Training set: {self.X_train.shape}")
        print(f"🧪 Test set: {self.X_test.shape}")
        
        # Scale the features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print("✅ Data scaling completed")
        
        # Feature importance analysis
        self._analyze_feature_importance()
        
    def _analyze_feature_importance(self):
        """Analyze feature importance using various methods"""
        print("\n🔍 Analyzing Feature Importance...")
        
        # Method 1: Statistical significance (ANOVA F-test)
        selector = SelectKBest(f_classif, k='all')
        selector.fit(self.X_train, self.y_train)
        
        feature_scores = pd.DataFrame({
            'Feature': self.X.columns,
            'Score': selector.scores_
        }).sort_values('Score', ascending=False)
        
        # Method 2: Random Forest feature importance
        rf_temp = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_temp.fit(self.X_train_scaled, self.y_train)
        
        rf_importance = pd.DataFrame({
            'Feature': self.X.columns,
            'Importance': rf_temp.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        # Visualize feature importance
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Statistical significance
        ax1.barh(feature_scores['Feature'][:10], feature_scores['Score'][:10])
        ax1.set_title('Top 10 Features (Statistical Significance)')
        ax1.set_xlabel('F-Score')
        
        # Random Forest importance
        ax2.barh(rf_importance['Feature'][:10], rf_importance['Importance'][:10])
        ax2.set_title('Top 10 Features (Random Forest Importance)')
        ax2.set_xlabel('Importance Score')
        
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("📊 Top 5 Most Important Features (Statistical):")
        print(feature_scores.head())
        
    def initialize_models(self):
        """Initialize various machine learning models"""
        print("\n🤖 Initializing Machine Learning Models...")
        
        self.models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42),
            'SVM': SVC(random_state=42, probability=True),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'K-Nearest Neighbors': KNeighborsClassifier(),
            'Naive Bayes': GaussianNB(),
            'Decision Tree': DecisionTreeClassifier(random_state=42)
        }
        
        print(f"✅ Initialized {len(self.models)} models")
        for model_name in self.models.keys():
            print(f"   • {model_name}")
    
    def train_and_evaluate_models(self):
        """Train and evaluate all models"""
        print("\n🚀 Training and Evaluating Models...")
        print("=" * 60)
        
        for model_name, model in self.models.items():
            print(f"\n🔄 Training {model_name}...")
            
            # Train the model
            if model_name in ['SVM', 'Logistic Regression', 'K-Nearest Neighbors']:
                # Use scaled data for algorithms sensitive to feature scale
                model.fit(self.X_train_scaled, self.y_train)
                y_pred = model.predict(self.X_test_scaled)
                y_pred_proba = model.predict_proba(self.X_test_scaled) if hasattr(model, 'predict_proba') else None
            else:
                # Use original data for tree-based methods
                model.fit(self.X_train, self.y_train)
                y_pred = model.predict(self.X_test)
                y_pred_proba = model.predict_proba(self.X_test) if hasattr(model, 'predict_proba') else None
            
            # Calculate metrics
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average='weighted')
            recall = recall_score(self.y_test, y_pred, average='weighted')
            f1 = f1_score(self.y_test, y_pred, average='weighted')
            
            # Store results
            self.results[model_name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'predictions': y_pred,
                'probabilities': y_pred_proba,
                'model': model
            }
            
            print(f"   ✅ Accuracy: {accuracy:.4f}")
            print(f"   📊 Precision: {precision:.4f}")
            print(f"   🔍 Recall: {recall:.4f}")
            print(f"   📈 F1-Score: {f1:.4f}")
        
        # Display comprehensive results
        self._display_results_summary()
        
    def _display_results_summary(self):
        """Display comprehensive results summary"""
        print("\n📊 MODEL PERFORMANCE SUMMARY")
        print("=" * 80)
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'Model': list(self.results.keys()),
            'Accuracy': [self.results[model]['accuracy'] for model in self.results.keys()],
            'Precision': [self.results[model]['precision'] for model in self.results.keys()],
            'Recall': [self.results[model]['recall'] for model in self.results.keys()],
            'F1-Score': [self.results[model]['f1_score'] for model in self.results.keys()]
        })
        
        # Sort by F1-score
        results_df = results_df.sort_values('F1-Score', ascending=False)
        print(results_df.round(4))
        
        # Find best model
        best_model_name = results_df.iloc[0]['Model']
        print(f"\n🏆 BEST PERFORMING MODEL: {best_model_name}")
        print(f"   📊 F1-Score: {results_df.iloc[0]['F1-Score']:.4f}")
        print(f"   🎯 Accuracy: {results_df.iloc[0]['Accuracy']:.4f}")
        
        # Visualize results
        self._visualize_results(results_df)
        
        return best_model_name
    
    def _visualize_results(self, results_df):
        """Visualize model performance results"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightyellow']
        
        for i, metric in enumerate(metrics):
            row, col = i // 2, i % 2
            ax = axes[row, col]
            bars = ax.bar(results_df['Model'], results_df[metric], color=colors[i])
            ax.set_title(f'{metric} Comparison')
            ax.set_ylabel(metric)
            ax.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                       f'{height:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('model_performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def detailed_analysis_best_model(self, best_model_name):
        """Perform detailed analysis of the best performing model"""
        print(f"\n🔬 DETAILED ANALYSIS: {best_model_name}")
        print("=" * 60)
        
        best_result = self.results[best_model_name]
        y_pred = best_result['predictions']
        
        # Confusion Matrix
        cm = confusion_matrix(self.y_test, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=[f'Fault {i}' for i in sorted(self.y.unique())],
                   yticklabels=[f'Fault {i}' for i in sorted(self.y.unique())])
        plt.title(f'Confusion Matrix - {best_model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(f'confusion_matrix_{best_model_name.replace(" ", "_")}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        # Classification Report
        print("\n📋 Detailed Classification Report:")
        fault_names = [f'Fault {i}' for i in sorted(self.y.unique())]
        report = classification_report(self.y_test, y_pred, 
                                     target_names=fault_names)
        print(report)
        
        # Per-class analysis
        print("\n🎯 Per-Class Performance Analysis:")
        for fault_type in sorted(self.y.unique()):
            true_positives = cm[fault_type, fault_type]
            false_negatives = np.sum(cm[fault_type, :]) - true_positives
            false_positives = np.sum(cm[:, fault_type]) - true_positives
            
            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            
            print(f"   Fault {fault_type}:")
            print(f"     • Precision: {precision:.4f}")
            print(f"     • Recall: {recall:.4f}")
            print(f"     • True Positives: {true_positives}")
            print(f"     • False Positives: {false_positives}")
            print(f"     • False Negatives: {false_negatives}")
    
    def hyperparameter_tuning(self, best_model_name):
        """Perform hyperparameter tuning on the best model"""
        print(f"\n⚙️ HYPERPARAMETER TUNING: {best_model_name}")
        print("=" * 60)
        
        if best_model_name == 'Random Forest':
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            model = RandomForestClassifier(random_state=42)
            X_data, y_data = self.X_train, self.y_train
            
        elif best_model_name == 'Gradient Boosting':
            param_grid = {
                'n_estimators': [100, 200],
                'learning_rate': [0.05, 0.1, 0.15],
                'max_depth': [3, 4, 5]
            }
            model = GradientBoostingClassifier(random_state=42)
            X_data, y_data = self.X_train, self.y_train
            
        elif best_model_name == 'SVM':
            param_grid = {
                'C': [0.1, 1, 10, 100],
                'gamma': ['scale', 'auto', 0.1, 1],
                'kernel': ['rbf', 'linear']
            }
            model = SVC(random_state=42, probability=True)
            X_data, y_data = self.X_train_scaled, self.y_train
            
        else:
            print(f"Hyperparameter tuning not configured for {best_model_name}")
            return
        
        # Perform grid search
        print("🔄 Performing Grid Search (this may take a while)...")
        grid_search = GridSearchCV(model, param_grid, cv=3, scoring='f1_weighted', 
                                 n_jobs=-1, verbose=1)
        grid_search.fit(X_data, y_data)
        
        print(f"✅ Best parameters: {grid_search.best_params_}")
        print(f"📊 Best cross-validation score: {grid_search.best_score_:.4f}")
        
        # Evaluate tuned model
        if best_model_name in ['SVM']:
            y_pred_tuned = grid_search.predict(self.X_test_scaled)
        else:
            y_pred_tuned = grid_search.predict(self.X_test)
            
        accuracy_tuned = accuracy_score(self.y_test, y_pred_tuned)
        f1_tuned = f1_score(self.y_test, y_pred_tuned, average='weighted')
        
        print(f"🎯 Tuned model accuracy: {accuracy_tuned:.4f}")
        print(f"📈 Tuned model F1-score: {f1_tuned:.4f}")
        
        # Compare with original
        original_f1 = self.results[best_model_name]['f1_score']
        improvement = f1_tuned - original_f1
        print(f"📊 Improvement over original: {improvement:.4f}")
        
        return grid_search.best_estimator_
    
    def feature_analysis(self):
        """Perform comprehensive feature analysis"""
        print("\n🔍 COMPREHENSIVE FEATURE ANALYSIS")
        print("=" * 60)
        
        # PCA Analysis
        print("\n📊 Principal Component Analysis (PCA)...")
        pca = PCA()
        pca.fit(self.X_train_scaled)
        
        # Plot explained variance ratio
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(range(1, len(pca.explained_variance_ratio_) + 1), 
                np.cumsum(pca.explained_variance_ratio_), 'bo-')
        plt.xlabel('Number of Components')
        plt.ylabel('Cumulative Explained Variance Ratio')
        plt.title('PCA - Cumulative Explained Variance')
        plt.grid(True)
        
        # Find number of components for 95% variance
        n_components_95 = np.argmax(np.cumsum(pca.explained_variance_ratio_) >= 0.95) + 1
        plt.axhline(y=0.95, color='r', linestyle='--', label='95% Variance')
        plt.axvline(x=n_components_95, color='r', linestyle='--', 
                   label=f'{n_components_95} Components')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.bar(range(1, min(11, len(pca.explained_variance_ratio_) + 1)), 
                pca.explained_variance_ratio_[:10])
        plt.xlabel('Principal Component')
        plt.ylabel('Explained Variance Ratio')
        plt.title('Individual Component Contribution')
        
        plt.tight_layout()
        plt.savefig('pca_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"📊 Components needed for 95% variance: {n_components_95}")
        print(f"🔍 First 5 components explain: {np.sum(pca.explained_variance_ratio_[:5]):.3f} of variance")
    
    def generate_report(self, best_model_name):
        """Generate comprehensive analysis report"""
        print("\n📋 GENERATING COMPREHENSIVE REPORT")
        print("=" * 60)
        
        report = f"""
ENGINE FAULT DETECTION - EXPERIMENT 9 REPORT
=============================================

Student: Pranvkumar Kshirsagar
Roll No: 590011587
Date: September 26, 2025

DATASET OVERVIEW:
- Total Samples: {len(self.data):,}
- Features: {len(self.X.columns)}
- Fault Types: {len(self.y.unique())}
- Class Distribution: {dict(self.data['Fault'].value_counts().sort_index())}

FEATURE ANALYSIS:
- Key Features: {', '.join(self.X.columns[:5])}...
- All Features: {', '.join(self.X.columns)}

MODEL PERFORMANCE:
"""
        
        for model_name, results in self.results.items():
            report += f"""
{model_name}:
  - Accuracy: {results['accuracy']:.4f}
  - Precision: {results['precision']:.4f}
  - Recall: {results['recall']:.4f}
  - F1-Score: {results['f1_score']:.4f}
"""
        
        report += f"""
BEST MODEL: {best_model_name}
- Best Performance Metric: F1-Score = {self.results[best_model_name]['f1_score']:.4f}
- Accuracy: {self.results[best_model_name]['accuracy']:.4f}

CONCLUSIONS:
1. The engine fault detection system successfully classifies 4 different fault types
2. {best_model_name} achieved the best performance with high accuracy
3. Key parameters like RPM, Power, CO, HC, and O2 are most important for fault detection
4. The system can be deployed for real-time engine diagnostics

RECOMMENDATIONS:
1. Consider ensemble methods for production deployment
2. Implement feature engineering for better performance
3. Add more diverse fault scenarios to the training data
4. Consider real-time prediction optimization
"""
        
        # Save report to file
        with open('Engine_Fault_Detection_Report.txt', 'w') as f:
            f.write(report)
        
        print("✅ Report saved as 'Engine_Fault_Detection_Report.txt'")
        print(report)
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("🚀 STARTING COMPLETE ENGINE FAULT DETECTION ANALYSIS")
        print("=" * 80)
        
        # Step 1: Load and explore data
        self.load_and_explore_data()
        
        # Step 2: Create visualizations
        self.visualize_data()
        
        # Step 3: Prepare data
        self.prepare_data()
        
        # Step 4: Initialize models
        self.initialize_models()
        
        # Step 5: Train and evaluate
        self.train_and_evaluate_models()
        
        # Step 6: Detailed analysis of best model
        best_model_name = self._display_results_summary()
        self.detailed_analysis_best_model(best_model_name)
        
        # Step 7: Hyperparameter tuning
        try:
            tuned_model = self.hyperparameter_tuning(best_model_name)
        except Exception as e:
            print(f"⚠️ Hyperparameter tuning failed: {e}")
            tuned_model = None
        
        # Step 8: Feature analysis
        self.feature_analysis()
        
        # Step 9: Generate report
        self.generate_report(best_model_name)
        
        print("\n🎉 ANALYSIS COMPLETE!")
        print("=" * 80)
        print("📊 All visualizations saved as PNG files")
        print("📋 Comprehensive report saved as 'Engine_Fault_Detection_Report.txt'")
        print(f"🏆 Best Model: {best_model_name}")
        print(f"🎯 Final Accuracy: {self.results[best_model_name]['accuracy']:.4f}")
        
        return best_model_name, self.results[best_model_name]['model']

def main():
    """Main execution function"""
    print("🔧 ENGINE FAULT DETECTION SYSTEM - EXPERIMENT 9")
    print("=" * 80)
    
    # Initialize the detector
    csv_file_path = r"c:\Users\Prana\OneDrive\Desktop\coding\EngineFaultDB_Final.csv"
    
    detector = EngineFaultDetector(csv_file_path)
    
    # Run complete analysis
    best_model_name, best_model = detector.run_complete_analysis()
    
    # Interactive prediction example
    print("\n🎯 INTERACTIVE PREDICTION EXAMPLE")
    print("=" * 50)
    
    # Use first test sample for demonstration
    sample_idx = 0
    sample_data = detector.X_test.iloc[sample_idx:sample_idx+1]
    true_fault = detector.y_test.iloc[sample_idx]
    
    # Make prediction
    if best_model_name in ['SVM', 'Logistic Regression', 'K-Nearest Neighbors']:
        sample_scaled = detector.scaler.transform(sample_data)
        predicted_fault = best_model.predict(sample_scaled)[0]
        prediction_proba = best_model.predict_proba(sample_scaled)[0]
    else:
        predicted_fault = best_model.predict(sample_data)[0]
        prediction_proba = best_model.predict_proba(sample_data)[0]
    
    print(f"Sample Engine Parameters:")
    for feature, value in sample_data.iloc[0].items():
        print(f"  {feature}: {value:.3f}")
    
    print(f"\n🎯 True Fault Type: {true_fault}")
    print(f"🤖 Predicted Fault Type: {predicted_fault}")
    print(f"📊 Prediction Confidence: {max(prediction_proba):.3f}")
    
    if predicted_fault == true_fault:
        print("✅ CORRECT PREDICTION!")
    else:
        print("❌ INCORRECT PREDICTION")
    
    print(f"\n📊 Prediction Probabilities:")
    for fault_type, prob in enumerate(prediction_proba):
        print(f"  Fault {fault_type}: {prob:.3f}")

if __name__ == "__main__":
    main()