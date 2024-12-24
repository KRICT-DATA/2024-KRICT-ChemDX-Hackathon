# Code: data_reform.py
# Reformat the dataset to machine-readable form
import numpy as np
import pandas as pd

from src.datasetHandler import (add_target_column, elements_to_bin,
                                extract_structure, get_ase_atoms,
                                get_crystal_system, get_density, get_volume,
                                parse_rawdata, rescale_lattice_vector)
from src.vars import FP_PREFIX, FP_SIZE, KEY_TARGET

# Location of raw data (formation energy dataset)
PATH_RAWDATA = "datasets/raw/MatDX_EF.csv"
PATH_PROCESSEDDATA = "datasets/processed/"

# Create Pandas dataframe
df_rawdata = pd.read_csv(PATH_RAWDATA)

# Parse 'structure' column (A list of JSON to ) into "data" and "natoms" and "element"
df_parsed = parse_rawdata(df_rawdata, "structure")

# Convert element type and number to bins, and get total mass in "mass" column
# Mass vector size (-8: 7 for crystal systems, 1 for density)
n_mass_bins = FP_SIZE - 8
df_parsed = elements_to_bin(df_parsed, "element", "natoms", n_bins=n_mass_bins)

# Compute density
# 1. Extract lattice parameters from the new column "data"
df_parsed = extract_structure(df_parsed, "data")
# 2. Rescale lattica vector elements
df_parsed = rescale_lattice_vector(df_parsed, scaler=1e10)
# 3. Compute volume and density
df_parsed = get_volume(df_parsed)
df_parsed = get_density(df_parsed, mass="mass_total", volume="volume")

# Get crystal system
df_parsed = get_crystal_system(df_parsed, "space_group")

# Drop rows without structural information
df_parsed = df_parsed.dropna(subset=["a1"])

# Add 3D structure
df_parsed = get_ase_atoms(df_parsed, "data")

# Add target column
df_parsed = add_target_column(df_parsed, "formation_energy", KEY_TARGET)

# Drop rows with Value per atom = [-3.5 eV/etom - 3.5 eV/atom]
df_parsed = df_parsed[
    (df_parsed[KEY_TARGET] >= -3.5) & (df_parsed[KEY_TARGET] <= 3.5)
].reset_index(drop=True)

# Drop other unnecessary columns
keys_to_keep = [
    key
    for key in df_parsed
    if not (
        key.startswith(FP_PREFIX) or key == "atoms" or key == KEY_TARGET or key == "id"
    )
]
df_parsed = df_parsed.drop(columns=keys_to_keep)

# Fill NaN values with 0 only in columns specified in key_list
keys_features = [key for key in df_parsed if key.startswith(FP_PREFIX)]
df_parsed[keys_features] = df_parsed[keys_features].fillna(0)

# Remove columns where all values are zero
# df_parsed = df_parsed.loc[:, (df_parsed != 0).any(axis=0)]
# keys_features = [key for key in df_parsed if key.startswith(FP_PREFIX)]

# Save unscaled dataset
df_parsed.to_csv(PATH_PROCESSEDDATA + "parsed_dataset.csv")

# Min-Max Normalization for each column
df_normalized = df_parsed.copy()
df_normalized[keys_features] = df_normalized[keys_features].apply(
    lambda x: (x - x.min()) / (x.max() - x.min())
)
df_normalized[keys_features] = df_normalized[keys_features].fillna(0)

# Scale target column [-1, 1]
df_normalized[f"{KEY_TARGET}_norm"] = (
    df_normalized[KEY_TARGET] - np.mean(df_normalized[KEY_TARGET])
) / np.std(df_normalized[KEY_TARGET])
df_normalized["mean"] = np.mean(df_normalized[KEY_TARGET])
df_normalized["std"] = np.std(df_normalized[KEY_TARGET])

# Save scaled dataset
df_normalized.to_csv(PATH_PROCESSEDDATA + "parsed_dataset_normalized.csv")
