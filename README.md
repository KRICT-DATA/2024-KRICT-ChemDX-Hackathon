# Hackathon KRICT: Universal Formation Energy Prediction

## Project Overview

This project aims to develop a machine learning model for predicting formation energy, a crucial property in materials science, by leveraging large datasets from the MatDX API. It was created as part of the **KRICT Hackathon** held from **November 6-8, 2024**.

### Authors
- **Kisung Kang**
- **Michail Minotakis**

## Objectives

1. **Data Collection**: Extract ~20k data points (binary and ternary compositions) from the MatDX API.
2. **Data Curation**: Address imbalances and outliers, particularly in the low-negative and high-positive formation energy regions.
3. **Model Training**: Develop and optimize various ML models to predict formation energy accurately.

## Dataset

The dataset comprises approximately 20,000 data points, mainly binary and ternary data with a focus on formation energy. A large proportion of data is concentrated around the 0 eV region, with notable outliers in extreme positive and negative ranges.

### Key Features in Dataset
- **Space Group Distribution**: A range of crystallographic space groups.
- **Element Distribution**: Diverse elements to enrich the dataset.
- **Descriptors**:
  - **Elemental Properties**: Mean electronegativity, atomic mass, and radius.
  - **Structural Properties**: Atomic volumes and space groups.
  - **Statistical Properties**: Standard deviation of electronegativity, atomic number differences.

## Methodology

The project explores multiple machine learning techniques to achieve optimal performance in predicting formation energy. 

### Model Training
Models tested include:
- **Linear Regression**
- **Ridge & Lasso Regression**
- **Decision Tree & Random Forest**
- **Gradient Boosting**
- **Support Vector Regressor**
- **k-Nearest Neighbors**

### Model Optimization
Further optimizations are conducted using pretrained multi-layer perceptron models (e.g., MACE MP0, SevenNet, Orb v2) to improve model accuracy.

### Results
- **Mean Absolute Error (MAE)**: Achieved a best score of **0.549 eV**.
- **R² Score**: Reached **0.910**, indicating a strong predictive model.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Minotakm/hackathon_KRICT.git
    ```
2. Navigate to the project directory:
    ```bash
    cd hackathon_KRICT
    ```

## Usage

1. **Download Data**:
   Use the MatDX API to retrieve and preprocess the data as described in `data_extraction.py`.

2. Follow the instruction of jupyter notebooks from 1 to 5.
   Notebook 0 is optional.
