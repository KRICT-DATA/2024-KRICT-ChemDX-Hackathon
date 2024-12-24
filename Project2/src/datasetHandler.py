# Code: datasetHandler.py
# Some aux functions for dataset reformatting

import json

import numpy as np
import pandas as pd
from ase import Atoms

from .vars import ATOMIC_MASS, CRYASTAL_SYSTEMS_SPACE_GROUPS, FP_PREFIX


def add_target_column(df, key, key_target):
    value_per_atom = []
    for data in df[key]:
        data_dict = json.loads(data.replace("'", '"'))
        value_per_atom.append(data_dict.get(key_target, None))
    df[key_target] = value_per_atom
    return df


def get_ase_atoms(df, key):
    atoms_ = []
    for _i, row in df.iterrows():
        data = row[key]
        cell = [
            [x * 1e10 for x in data["a"]],
            [y * 1e10 for y in data["b"]],
            [z * 1e10 for z in data["c"]],
        ]
        pos = [
            [val["x"] * 10e10, val["y"] * 10e10, val["z"] * 10e10]
            for val in data["atoms"]
        ]
        symbols = [val["element"] for val in data["atoms"]]
        atoms_.append(Atoms(cell=cell, positions=pos, symbols=symbols).todict())

    df["atoms"] = atoms_
    return df


def parse_rawdata(df, json_column, drop_original=False):
    """Parse Jsonian column.
    Newly added columns' name will be the key in the JSON.
    Parameters: df - Pandas Dataframe
                json_column - Name of the header of column to parse
    """
    # Extract the JSON string from the stringified list
    df[json_column] = df[json_column].apply(
        lambda x: json.loads(x.replace("'", '"'))[0] if isinstance(x, str) else {}
    )
    # Parse the JSON string into individual columns
    json_cols = df[json_column].apply(pd.Series)
    # Concatenate the new columns to the original DataFrame
    df = pd.concat([df, json_cols], axis=1)
    # Rename natoms to num_natoms
    # if "natoms" in df:
    #     df = df.rename(columns={"natoms": "num_natoms"})
    # Drop original columns if requested
    if drop_original:
        df = df.drop(columns=[json_column])

    return df


def extract_structure(df, key):
    """Get lattice parameters and atom dict"""
    # Expand the 'data' list into separate columns (a1, a2, a3, b1, b2, b3, c1, c2, c3, atoms:dict)
    data_columns = df[key].apply(pd.Series)

    # Concatenate the expanded 'atoms' columns with the rest of the DataFrame
    df_expanded = pd.concat([df, data_columns], axis=1)

    # Split vector to individual columns
    for l in ["a", "b", "c"]:
        new_keys = [f"{l}1", f"{l}2", f"{l}3"]
        # Expand the 'a' column into separate columns
        df_l = df_expanded[l].apply(pd.Series)

        # Rename the columns (optional, based on your desired naming convention)
        df_l.columns = new_keys

        df_expanded = pd.concat([df_expanded.drop(columns=[l]), df_l], axis=1)

    return df_expanded


def rescale_lattice_vector(
    df, scaler=1e10, keys=["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
):
    for key in keys:
        df[key] = df[key] * scaler

    return df


def get_crystal_system(df, key="space_group"):
    """Add a column for crystal system"""
    for crysta_system in CRYASTAL_SYSTEMS_SPACE_GROUPS:
        df[f"{FP_PREFIX}{crysta_system}"] = 0
    for index, row in df.iterrows():
        for crysta_system in CRYASTAL_SYSTEMS_SPACE_GROUPS:
            if row[key] in CRYASTAL_SYSTEMS_SPACE_GROUPS[crysta_system]:
                df.at[index, f"{FP_PREFIX}{crysta_system}"] = 1
    return df


def elements_to_bin(df, key, key_natoms, n_bins=56):
    """Convert elements information into generalized binned vector
    And add a mass (total mass)"""
    # Initialize mass bins
    max_mass = 300

    for i in range(n_bins):
        df[f"{FP_PREFIX}mass_{i}"] = 0

    for index, row in df.iterrows():
        elements = row[key]
        mass_total = 0
        for element in elements:
            mass_bin = (
                f"{FP_PREFIX}mass_{int(ATOMIC_MASS[element] / (max_mass / n_bins))}"
            )
            df.at[index, str(mass_bin)] = row[mass_bin] + elements[element]
            mass_total = mass_total + ATOMIC_MASS[element]
        df.at[index, "mass_total"] = mass_total

    # Normalize using the total number of atoms
    # VERY IMPORTANT !!!
    for i in range(n_bins):
        df[f"{FP_PREFIX}mass_{i}"] = df[f"{FP_PREFIX}mass_{i}"] / df[key_natoms]

    return df


def get_volume(df):
    for index, row in df.iterrows():
        a = np.array([row["a1"], row["a2"], row["a3"]])
        b = np.array([row["b1"], row["b2"], row["b3"]])
        c = np.array([row["c1"], row["c2"], row["c3"]])

        # Compute the cross product of b and c
        cross_product = np.cross(b, c)

        # Compute the dot product of a with the cross product of b and c
        volume = np.abs(np.dot(a, cross_product))

        # Add volume to the df
        df.at[index, "volume"] = volume

    return df


def get_density(df, mass="mass_total", volume="volume"):
    for index, row in df.iterrows():
        df.at[index, f"{FP_PREFIX}density"] = row[mass] / row[volume]

    return df
