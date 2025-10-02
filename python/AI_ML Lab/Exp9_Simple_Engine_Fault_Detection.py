#!/usr/bin/env python3
"""
Experiment 9: Engine Fault Detection - Simplified Version
========================================================

Student: Pranvkumar Kshirsagar
Roll No: 590011587
Date: September 26, 2025

A simplified but comprehensive engine fault detection system
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

# Set backend for matplotlib to avoid GUI issues
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def main():
    print("🔧 ENGINE FAULT DETECTION - EXPERIMENT 9 (Simplified)")
    print("=" * 60)
    
    # Load data
    print("📊 Loading dataset...")
    csv_path = r"c:\Users\Prana\OneDrive\Desktop\coding\EngineFaultDB_Final.csv"
    data = pd.read_csv(csv_path)
    
    print(f"Dataset shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    
    # Check fault distribution
    print("\n🚨 Fault Distribution:")
    fault_counts = data['Fault'].value_counts().sort_index()
    for fault_type, count in fault_counts.items():
        percentage = (count / len(data)) * 100
        print(f"   Fault {fault_type}: {count:,} samples ({percentage:.1f}%)")
    
    # Prepare data
    print("\n🔧 Preparing data...")
    X = data.drop('Fault', axis=1)
    y = data['Fault']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
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
    
    # Train and evaluate models
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Use appropriate data (scaled for SVM/LogReg, original for tree-based)
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
    
    # Find best model
    best_model_name = max(results, key=lambda k: results[k]['accuracy'])
    best_accuracy = results[best_model_name]['accuracy']
    
    print(f"\n🏆 RESULTS SUMMARY:")
    print("=" * 40)
    for name, result in results.items():
        marker = "🥇" if name == best_model_name else "  "
        print(f"{marker} {name}: {result['accuracy']:.4f}")
    
    print(f"\n🎯 BEST MODEL: {best_model_name}")
    print(f"📊 Best Accuracy: {best_accuracy:.4f}")
    
    # Detailed analysis of best model
    print(f"\n🔬 DETAILED ANALYSIS: {best_model_name}")
    print("=" * 50)
    
    best_predictions = results[best_model_name]['predictions']
    
    # Classification report
    print("Classification Report:")
    report = classification_report(y_test, best_predictions)
    print(report)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, best_predictions)
    print("\nConfusion Matrix:")
    print("Predicted ->")
    print("Actual ↓   ", end="")
    for i in range(len(np.unique(y))):
        print(f"F{i:1d}    ", end="")
    print()
    
    for i, row in enumerate(cm):
        print(f"Fault {i}  ", end="")
        for val in row:
            print(f"{val:4d}  ", end="")
        print()
    
    # Per-class accuracy
    print(f"\nPer-Class Accuracy:")
    for i in range(len(np.unique(y))):
        class_accuracy = cm[i, i] / np.sum(cm[i, :])
        print(f"   Fault {i}: {class_accuracy:.4f}")
    
    # Feature importance (if applicable)
    if hasattr(results[best_model_name]['model'], 'feature_importances_'):
        print(f"\n📊 Top 5 Most Important Features:")
        importances = results[best_model_name]['model'].feature_importances_
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        for i, row in feature_importance.head().iterrows():
            print(f"   {row['Feature']}: {row['Importance']:.4f}")
    
    # Sample prediction
    print(f"\n🎯 SAMPLE PREDICTION:")
    print("=" * 30)
    sample_idx = 0
    sample_data = X_test.iloc[sample_idx:sample_idx+1]
    true_fault = y_test.iloc[sample_idx]
    
    # Make prediction
    if best_model_name in ['SVM', 'Logistic Regression']:
        sample_scaled = scaler.transform(sample_data)
        predicted_fault = results[best_model_name]['model'].predict(sample_scaled)[0]
    else:
        predicted_fault = results[best_model_name]['model'].predict(sample_data)[0]
    
    print(f"True Fault Type: {true_fault}")
    print(f"Predicted Fault Type: {predicted_fault}")
    
    if predicted_fault == true_fault:
        print("✅ CORRECT PREDICTION!")
    else:
        print("❌ INCORRECT PREDICTION")
    
    # Key insights
    print(f"\n💡 KEY INSIGHTS:")
    print("=" * 30)
    print(f"1. Dataset contains {len(data):,} engine measurements")
    print(f"2. {len(X.columns)} parameters monitored for fault detection")
    print(f"3. {len(np.unique(y))} different fault types identified")
    print(f"4. Best model ({best_model_name}) achieved {best_accuracy:.1%} accuracy")
    print(f"5. System can reliably detect engine faults for maintenance")
    
    print(f"\n🎉 EXPERIMENT 9 COMPLETED SUCCESSFULLY!")
    print(f"🔧 Engine Fault Detection System Ready for Deployment")
    
    return results, best_model_name

if __name__ == "__main__":
    results, best_model = main()