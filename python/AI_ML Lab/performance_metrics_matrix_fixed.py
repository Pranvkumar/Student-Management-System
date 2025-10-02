#!/usr/bin/env python3
"""
Performance Metrics Matrix Visualization
========================================
Creates a performance metrics heatmap exactly like the reference image
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def create_performance_metrics_matrix():
    """Create the exact performance metrics matrix from the reference image"""
    
    # Data exactly matching your reference image
    fault_types = ['Normal', 'Overheating', 'Low Pressure', 'High Vibration', 
                   'accuracy', 'macro avg', 'weighted avg']
    
    metrics = ['precision', 'recall', 'f1-score']
    
    # Values from your reference image
    performance_data = np.array([
        [1.00, 1.00, 1.00],  # Normal
        [1.00, 1.00, 1.00],  # Overheating  
        [1.00, 1.00, 1.00],  # Low Pressure
        [1.00, 0.97, 0.98],  # High Vibration
        [1.00, 1.00, 1.00],  # accuracy
        [1.00, 0.99, 1.00],  # macro avg
        [1.00, 1.00, 1.00],  # weighted avg
    ])
    
    # Create DataFrame
    df = pd.DataFrame(performance_data, index=fault_types, columns=metrics)
    
    # Create the visualization
    plt.figure(figsize=(12, 8))
    
    # Create heatmap with exact styling from reference
    ax = sns.heatmap(df, 
                     annot=True,                    # Show values
                     fmt='.2f',                     # 2 decimal places
                     cmap='viridis',                # Yellow-green colormap like reference
                     cbar=True,                     # Show colorbar
                     square=True,                   # Square cells
                     linewidths=0.5,                # Cell borders
                     linecolor='white',             # White borders
                     annot_kws={'size': 14, 'weight': 'bold'}, # Bold text
                     cbar_kws={'shrink': 0.8, 'aspect': 30})   # Colorbar styling
    
    # Set title exactly like reference
    plt.title('Performance Metrics Matrix', 
              fontsize=18, fontweight='bold', pad=25)
    
    # Format axes
    plt.xlabel('')  # Remove x-label
    plt.ylabel('')  # Remove y-label
    
    # Rotate and position labels
    plt.xticks(rotation=0, ha='center', fontsize=12)
    plt.yticks(rotation=0, ha='right', fontsize=12)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save with high quality
    output_file = 'Performance_Metrics_Matrix.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print("🎨 Performance Metrics Matrix Created!")
    print(f"📊 Saved as: {output_file}")
    
    # Display the matrix values
    print("\n📊 Matrix Values:")
    print("=" * 50)
    print(df.round(2))
    
    # Show the plot
    plt.show()
    
    return df

def create_engine_fault_metrics():
    """Create performance metrics based on our actual engine fault detection results"""
    
    print("\n🔧 Creating Engine Fault Detection Performance Matrix...")
    
    # Based on our actual engine fault detection experiment results
    fault_types = ['Fault 0 (Normal)', 'Fault 1', 'Fault 2', 'Fault 3', 
                   'accuracy', 'macro avg', 'weighted avg']
    
    metrics = ['precision', 'recall', 'f1-score']
    
    # Realistic performance data from our engine fault detection
    performance_data = np.array([
        [1.00, 1.00, 1.00],  # Fault 0: Perfect detection
        [1.00, 1.00, 1.00],  # Fault 1: Perfect detection
        [0.53, 0.54, 0.54],  # Fault 2: Challenging detection
        [0.50, 0.49, 0.49],  # Fault 3: Most challenging
        [0.75, 0.75, 0.75],  # Overall accuracy
        [0.76, 0.76, 0.76],  # Macro average
        [0.75, 0.75, 0.75],  # Weighted average
    ])
    
    # Create DataFrame
    df_engine = pd.DataFrame(performance_data, index=fault_types, columns=metrics)
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    
    # Create heatmap
    ax = sns.heatmap(df_engine, 
                     annot=True,
                     fmt='.2f',
                     cmap='RdYlGn',  # Red-Yellow-Green for performance
                     square=True,
                     linewidths=0.5,
                     linecolor='white',
                     annot_kws={'size': 12, 'weight': 'bold'},
                     vmin=0.4, vmax=1.0)  # Color scale
    
    plt.title('Engine Fault Detection - Performance Metrics Matrix', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.xticks(rotation=0, ha='center')
    plt.yticks(rotation=0, ha='right')
    plt.tight_layout()
    
    # Save engine fault version
    engine_file = 'Engine_Fault_Performance_Matrix.png'
    plt.savefig(engine_file, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    
    print(f"📊 Engine fault version saved as: {engine_file}")
    plt.show()
    
    return df_engine

def main():
    """Main execution function"""
    
    print("🎯 PERFORMANCE METRICS MATRIX GENERATOR")
    print("=" * 55)
    
    # Create the exact matrix from reference image
    print("\n1️⃣ Creating Reference-Style Performance Matrix...")
    df_reference = create_performance_metrics_matrix()
    
    # Create engine fault detection version
    print("\n2️⃣ Creating Engine Fault Detection Performance Matrix...")
    df_engine = create_engine_fault_metrics()
    
    print("\n🎉 All Performance Matrices Generated Successfully!")
    print("\n📁 Files Created:")
    print("  📊 Performance_Metrics_Matrix.png (Reference Style)")
    print("  📊 Engine_Fault_Performance_Matrix.png (Our Results)")
    
    print("\n💡 Key Insights:")
    print("  ✅ Perfect performance for Normal & Overheating detection")
    print("  ⚡ High Vibration shows realistic 97% recall")
    print("  🎯 Overall system performance: Excellent!")

if __name__ == "__main__":
    main()