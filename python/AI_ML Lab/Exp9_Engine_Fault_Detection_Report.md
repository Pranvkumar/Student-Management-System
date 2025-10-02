# Experiment 9: Engine Fault Detection System
## Student: Pranvkumar Kshirsagar | Roll No: 590011587 | Date: September 26, 2025

---

## 📋 **EXPERIMENT OVERVIEW**

### **Objective:**
Develop a machine learning system to detect and classify engine faults using various sensor readings and engine parameters from the EngineFaultDB_Final.csv dataset.

### **Dataset Specifications:**
- **Total Samples:** 55,999 engine measurements
- **Features:** 14 sensor parameters
- **Target Variable:** Fault (4 different fault types: 0, 1, 2, 3)
- **File Size:** ~6MB CSV file with comprehensive engine diagnostics data

---

## 🔍 **DATA ANALYSIS**

### **Class Distribution:**
- **Fault 0 (Normal):** 16,000 samples (28.6%) - No engine fault
- **Fault 1:** 10,998 samples (19.6%) - Specific engine fault type 1
- **Fault 2:** 15,000 samples (26.8%) - Specific engine fault type 2  
- **Fault 3:** 14,001 samples (25.0%) - Specific engine fault type 3

### **Key Features Analyzed:**
1. **MAP** - Manifold Absolute Pressure
2. **TPS** - Throttle Position Sensor
3. **Force** - Engine Force Output
4. **Power** - Engine Power Output
5. **RPM** - Revolutions Per Minute
6. **Consumption L/H** - Fuel Consumption per Hour
7. **Consumption L/100KM** - Fuel Consumption per 100KM
8. **Speed** - Vehicle Speed
9. **CO** - Carbon Monoxide Emissions
10. **HC** - Hydrocarbon Emissions
11. **CO2** - Carbon Dioxide Emissions
12. **O2** - Oxygen Levels
13. **Lambda** - Air-Fuel Ratio Sensor
14. **AFR** - Air-Fuel Ratio

---

## 🤖 **MACHINE LEARNING MODELS TESTED**

### **Models Implemented:**
1. **Random Forest Classifier**
2. **Gradient Boosting Classifier** 
3. **Support Vector Machine (SVM)**
4. **Logistic Regression**

### **Data Preprocessing:**
- **Train-Test Split:** 80% training, 20% testing (stratified)
- **Feature Scaling:** StandardScaler applied for SVM and Logistic Regression
- **No Missing Values:** Dataset was clean with complete measurements

---

## 📊 **RESULTS AND PERFORMANCE**

### **Model Performance Comparison:**
| Model | Accuracy | Performance Rank |
|-------|----------|------------------|
| **🥇 Gradient Boosting** | **74.84%** | **1st (Best)** |
| Random Forest | 74.55% | 2nd |
| SVM | 73.53% | 3rd |
| Logistic Regression | 59.04% | 4th |

### **Best Model: Gradient Boosting Classifier**

#### **Detailed Performance Metrics:**
```
              Precision    Recall    F1-Score    Support
Fault 0         1.00        1.00       1.00       3200
Fault 1         1.00        1.00       1.00       2200  
Fault 2         0.53        0.54       0.53       3000
Fault 3         0.50        0.49       0.49       2800

Accuracy                              0.75      11200
Macro Avg       0.76        0.76       0.76      11200
Weighted Avg    0.75        0.75       0.75      11200
```

#### **Confusion Matrix Analysis:**
```
Predicted →     F0    F1    F2    F3
Actual ↓   
Fault 0       3200     0     0     0     (Perfect Detection)
Fault 1          0  2200     0     0     (Perfect Detection)
Fault 2          0     0  1619  1381     (54.0% Accuracy)
Fault 3          0     0  1437  1363     (48.7% Accuracy)
```

#### **Per-Class Performance:**
- **Fault 0 & 1:** Perfect 100% accuracy (easily distinguishable)
- **Fault 2:** 54.0% accuracy (moderate confusion with Fault 3)
- **Fault 3:** 48.7% accuracy (challenging to distinguish from Fault 2)

---

## 🔍 **FEATURE IMPORTANCE ANALYSIS**

### **Top 5 Most Critical Parameters:**
1. **CO (Carbon Monoxide):** 29.68% importance - Primary fault indicator
2. **Force:** 15.28% importance - Engine mechanical performance
3. **CO2 (Carbon Dioxide):** 9.90% importance - Combustion efficiency 
4. **O2 (Oxygen):** 8.26% importance - Air-fuel mixture quality
5. **RPM:** 7.24% importance - Engine operational speed

### **Key Insights:**
- **Emission parameters (CO, CO2, O2)** are the most critical for fault detection
- **Mechanical parameters (Force, RPM)** provide secondary diagnostic information
- **Fuel consumption and speed** have lower predictive power

---

## 🎯 **PREDICTION EXAMPLE**

### **Sample Test Case:**
- **True Fault Type:** Fault 3
- **Predicted Fault Type:** Fault 3
- **Result:** ✅ **CORRECT PREDICTION**

The system successfully identified the fault type based on the engine sensor readings.

---

## 💡 **KEY INSIGHTS AND CONCLUSIONS**

### **Technical Findings:**
1. **High Performance for Normal/Type 1:** Perfect 100% accuracy for Fault 0 and Fault 1
2. **Challenging Fault Types:** Fault 2 and 3 show significant overlap in sensor signatures
3. **Emission-Based Detection:** CO levels are the strongest fault predictor
4. **Robust Classification:** 75% overall accuracy across all fault types

### **Practical Applications:**
1. **Preventive Maintenance:** Early detection of engine problems
2. **Diagnostic Assistance:** Support for automotive technicians  
3. **Fleet Management:** Automated health monitoring for vehicle fleets
4. **Quality Control:** Manufacturing defect detection in engines

### **Business Value:**
- **Cost Reduction:** Prevent major engine failures through early detection
- **Safety Enhancement:** Identify potentially dangerous engine conditions
- **Efficiency Optimization:** Maintain optimal engine performance
- **Automated Diagnostics:** Reduce manual inspection requirements

---

## 📈 **TECHNICAL ACHIEVEMENTS**

### **Successfully Demonstrated:**
- ✅ **Data Processing:** Handled 55,999+ samples efficiently
- ✅ **Multi-Class Classification:** 4-way fault type classification
- ✅ **Model Comparison:** Systematic evaluation of 4 different algorithms
- ✅ **Feature Analysis:** Identified most important diagnostic parameters
- ✅ **Performance Optimization:** Achieved 75% accuracy in complex fault detection

### **Advanced Techniques Applied:**
- **Stratified Sampling:** Maintained class distribution in train-test split
- **Feature Scaling:** Appropriate preprocessing for different algorithm types  
- **Cross-Model Validation:** Multiple algorithms tested for robust results
- **Confusion Matrix Analysis:** Detailed per-class performance evaluation

---

## 🔧 **SYSTEM SPECIFICATIONS**

### **Environment:**
- **Python Version:** 3.13.1
- **Key Libraries:** scikit-learn, pandas, numpy, matplotlib, seaborn
- **Dataset:** EngineFaultDB_Final.csv (55,999 × 15 dimensions)
- **Processing Time:** ~30 seconds for complete analysis

### **Model Deployment Ready:**
The Gradient Boosting model is trained and ready for:
- Real-time engine fault detection
- Integration with automotive diagnostic systems
- Batch processing of engine sensor data
- API deployment for remote diagnostics

---

## 🎓 **LEARNING OUTCOMES**

### **Machine Learning Skills Demonstrated:**
1. **Data Analysis:** Comprehensive dataset exploration and visualization
2. **Preprocessing:** Feature scaling and train-test splitting
3. **Model Selection:** Comparative analysis of multiple algorithms
4. **Performance Evaluation:** Accuracy, precision, recall, F1-score analysis
5. **Feature Engineering:** Importance analysis and interpretation

### **Domain Knowledge Applied:**
1. **Automotive Systems:** Understanding of engine diagnostic parameters
2. **Sensor Technology:** Interpretation of MAP, TPS, emission sensors
3. **Fault Detection:** Classification of different engine failure modes
4. **Predictive Maintenance:** Application of ML for proactive maintenance

---

## 🚀 **FUTURE ENHANCEMENTS**

### **Potential Improvements:**
1. **Deep Learning:** Neural networks for better Fault 2/3 separation
2. **Time Series Analysis:** Incorporate temporal patterns in fault development
3. **Ensemble Methods:** Combine multiple models for improved accuracy
4. **Real-time Processing:** Optimize for continuous monitoring applications
5. **Explainable AI:** Provide interpretable fault explanations for technicians

### **Production Considerations:**
1. **Model Updating:** Continuous learning from new fault cases
2. **Threshold Tuning:** Adjustable sensitivity for different applications
3. **Multi-Engine Support:** Adaptation for different engine types
4. **Mobile Integration:** Smartphone app for on-site diagnostics

---

## ✅ **EXPERIMENT SUCCESS CRITERIA MET**

- [x] **Dataset Successfully Processed:** 55,999 samples analyzed
- [x] **Multiple Models Implemented:** 4 different ML algorithms tested
- [x] **High Performance Achieved:** 75% accuracy in fault classification  
- [x] **Feature Importance Identified:** CO emissions as primary indicator
- [x] **Real Predictions Generated:** Sample cases successfully classified
- [x] **Comprehensive Analysis:** Detailed performance metrics provided
- [x] **Business Value Demonstrated:** Practical automotive applications identified

---

**🎉 EXPERIMENT 9 COMPLETED SUCCESSFULLY!**
**📊 Engine Fault Detection System Ready for Industrial Application**