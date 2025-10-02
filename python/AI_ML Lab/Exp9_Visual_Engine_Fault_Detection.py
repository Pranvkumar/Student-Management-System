#!/usr/bin/env python3
"""
Experiment 9: Engine Fault Detection with Visual Confusion Matrix
================================================================

Student: Pranvkumar Kshirsagar
Roll No: 590011587
Date: September 26, 2025

Enhanced version with beautiful confusion matrix visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Set backend for matplotlib
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def create_beautiful_confusion_matrix(y_true, y_pred, class_names, model_name, save_path=None):
    """
    Create a beautiful confusion matrix visualization like the one shown
    """
    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Create figure and axis
    plt.figure(figsize=(10, 8))
    
    # Create heatmap with custom styling
    sns.heatmap(cm, 
                annot=True,           # Show numbers
                fmt='d',              # Integer format
                cmap='Blues',         # Blue color scheme like your example
                square=True,          # Square cells
                linewidths=0.5,       # Lines between cells
                cbar_kws={"shrink": .8}, # Colorbar size
                annot_kws={'size': 14, 'weight': 'bold'}) # Number styling
    
    # Set labels and title
    plt.title(f'Confusion Matrix - {model_name}', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Predicted Label', fontsize=14, fontweight='bold')
    plt.ylabel('True Label', fontsize=14, fontweight='bold')
    
    # Set tick labels
    plt.xticks(np.arange(len(class_names)) + 0.5, class_names, fontsize=12)
    plt.yticks(np.arange(len(class_names)) + 0.5, class_names, fontsize=12, rotation=0)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"📊 Confusion matrix saved as: {save_path}")
    
    # Display the plot (will save to file due to Agg backend)
    plt.savefig(f'confusion_matrix_{model_name.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return cm

def create_performance_comparison_chart(results, save_path=None):
    """
    Create a performance comparison chart for all models
    """
    # Prepare data
    models = list(results.keys())
    accuracies = [results[model]['accuracy'] for model in models]
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Create bar chart
    bars = plt.bar(models, accuracies, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    # Customize chart
    plt.title('Model Performance Comparison', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Machine Learning Models', fontsize=14, fontweight='bold')
    plt.ylabel('Accuracy Score', fontsize=14, fontweight='bold')
    plt.ylim(0, 1.0)
    
    # Add value labels on bars
    for bar, accuracy in zip(bars, accuracies):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{accuracy:.3f}', ha='center', va='bottom', 
                fontsize=12, fontweight='bold')
    
    # Add grid
    plt.grid(axis='y', alpha=0.3)
    
    # Rotate x-axis labels if needed
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Save chart
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.savefig('model_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_feature_importance_chart(model, feature_names, model_name, save_path=None):
    """
    Create feature importance visualization
    """
    if not hasattr(model, 'feature_importances_'):
        return
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Create DataFrame for sorting
    feature_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=True)  # Ascending for horizontal bar
    
    # Create figure
    plt.figure(figsize=(10, 8))
    
    # Create horizontal bar chart
    bars = plt.barh(feature_df['Feature'], feature_df['Importance'], color='skyblue')
    
    # Customize chart
    plt.title(f'Feature Importance - {model_name}', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Importance Score', fontsize=14, fontweight='bold')
    plt.ylabel('Engine Parameters', fontsize=14, fontweight='bold')
    
    # Add value labels
    for bar, importance in zip(bars, feature_df['Importance']):
        width = bar.get_width()
        plt.text(width + 0.005, bar.get_y() + bar.get_height()/2.,
                f'{importance:.3f}', ha='left', va='center', fontsize=10)
    
    # Add grid
    plt.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Save chart
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    plt.savefig(f'feature_importance_{model_name.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("🎨 ENGINE FAULT DETECTION WITH VISUAL ANALYSIS")
    print("=" * 60)
    
    # Load data
    print("📊 Loading dataset...")
    csv_path = r"c:\Users\Prana\OneDrive\Desktop\coding\EngineFaultDB_Final.csv"
    data = pd.read_csv(csv_path)
    
    print(f"Dataset shape: {data.shape}")
    print(f"Fault types: {sorted(data['Fault'].unique())}")
    
    # Prepare data
    print("\n🔧 Preparing data...")
    X = data.drop('Fault', axis=1)
    y = data['Fault']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'SVM': SVC(random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
    }
    
    print(f"\n🤖 Training {len(models)} models...")
    results = {}
    
    # Class names for visualization
    class_names = [f'{i}' for i in sorted(y.unique())]
    
    # Train and evaluate models
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Use appropriate data
        if name in ['SVM', 'Logistic Regression']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = {
            'accuracy': accuracy,
            'predictions': y_pred,
            'model': model
        }
        
        print(f"   Accuracy: {accuracy:.4f}")
        
        # Create confusion matrix for each model
        print(f"   📊 Creating confusion matrix...")
        create_beautiful_confusion_matrix(
            y_test, y_pred, class_names, name,
            f'confusion_matrix_{name.replace(" ", "_")}.png'
        )
    
    # Find best model
    best_model_name = max(results, key=lambda k: results[k]['accuracy'])
    best_model = results[best_model_name]['model']
    
    print(f"\n🏆 RESULTS SUMMARY:")
    print("=" * 40)
    for name, result in results.items():
        marker = "🥇" if name == best_model_name else "  "
        print(f"{marker} {name}: {result['accuracy']:.4f}")
    
    # Create performance comparison chart
    print(f"\n📈 Creating performance comparison chart...")
    create_performance_comparison_chart(results)
    
    # Create feature importance chart for best model
    if hasattr(best_model, 'feature_importances_'):
        print(f"\n📊 Creating feature importance chart for {best_model_name}...")
        create_feature_importance_chart(best_model, X.columns, best_model_name)
    
    # Detailed analysis of best model
    print(f"\n🔬 DETAILED ANALYSIS: {best_model_name}")
    print("=" * 50)
    
    best_predictions = results[best_model_name]['predictions']
    cm = confusion_matrix(y_test, best_predictions)
    
    # Print confusion matrix in text format
    print("\nConfusion Matrix (Text Format):")
    print("Predicted →", end="")
    for i in class_names:
        print(f"    {i}", end="")
    print()
    
    for i, (class_name, row) in enumerate(zip(class_names, cm)):
        print(f"Actual {class_name}  ", end="")
        for val in row:
            print(f"{val:5d}", end="")
        print()
    
    # Calculate per-class accuracy
    print(f"\nPer-Class Accuracy:")
    for i, class_name in enumerate(class_names):
        if np.sum(cm[i, :]) > 0:  # Avoid division by zero
            class_accuracy = cm[i, i] / np.sum(cm[i, :])
            print(f"   Fault {class_name}: {class_accuracy:.4f}")
    
    # Classification report
    print(f"\nClassification Report:")
    report = classification_report(y_test, best_predictions)
    print(report)
    
    # Feature importance for best model
    if hasattr(best_model, 'feature_importances_'):
        print(f"\n📊 Top 5 Most Important Features ({best_model_name}):")
        importances = best_model.feature_importances_
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        for i, (_, row) in enumerate(feature_importance.head().iterrows()):
            print(f"   {i+1}. {row['Feature']}: {row['Importance']:.4f}")
    
    print(f"\n🎉 ANALYSIS COMPLETED!")
    print("📊 Generated Visualizations:")
    print("   • Confusion matrices for all models")
    print("   • Model performance comparison chart")
    if hasattr(best_model, 'feature_importances_'):
        print("   • Feature importance chart")
    
    print(f"\n🏆 Best Model: {best_model_name} ({results[best_model_name]['accuracy']:.4f} accuracy)")
    
    return results, best_model_name

if __name__ == "__main__":
    results, best_model = main()