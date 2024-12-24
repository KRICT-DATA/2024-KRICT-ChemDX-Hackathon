# Code: vars.py
# Global variables.  We can do this smarter...


# Target column
KEY_TARGET = "value_per_atom"

# Fingerprint prefix
FP_PREFIX = "num_"

# Fingerprint vector size
FP_SIZE = 64

# Atomic mass dictionary: Element name as key, atomic mass as value
ATOMIC_MASS = {
    "H": 1.008,  # Hydrogen
    "He": 4.0026,  # Helium
    "Li": 6.94,  # Lithium
    "Be": 9.0122,  # Beryllium
    "B": 10.81,  # Boron
    "C": 12.011,  # Carbon
    "N": 14.007,  # Nitrogen
    "O": 15.999,  # Oxygen
    "F": 18.998,  # Fluorine
    "Ne": 20.180,  # Neon
    "Na": 22.990,  # Sodium
    "Mg": 24.305,  # Magnesium
    "Al": 26.982,  # Aluminum
    "Si": 28.085,  # Silicon
    "P": 30.974,  # Phosphorus
    "S": 32.06,  # Sulfur
    "Cl": 35.45,  # Chlorine
    "Ar": 39.948,  # Argon
    "K": 39.098,  # Potassium
    "Ca": 40.078,  # Calcium
    "Sc": 44.956,  # Scandium
    "Ti": 47.867,  # Titanium
    "V": 50.941,  # Vanadium
    "Cr": 52.00,  # Chromium
    "Mn": 54.938,  # Manganese
    "Fe": 55.845,  # Iron
    "Co": 58.933,  # Cobalt
    "Ni": 58.693,  # Nickel
    "Cu": 63.546,  # Copper
    "Zn": 65.38,  # Zinc
    "Ga": 69.723,  # Gallium
    "Ge": 72.63,  # Germanium
    "As": 74.922,  # Arsenic
    "Se": 78.971,  # Selenium
    "Br": 79.904,  # Bromine
    "Kr": 83.798,  # Krypton
    "Rb": 85.468,  # Rubidium
    "Sr": 87.62,  # Strontium
    "Y": 88.906,  # Yttrium
    "Zr": 91.224,  # Zirconium
    "Nb": 92.906,  # Niobium
    "Mo": 95.95,  # Molybdenum
    "Tc": 98.0,  # Technetium
    "Ru": 101.07,  # Ruthenium
    "Rh": 102.91,  # Rhodium
    "Pd": 106.42,  # Palladium
    "Ag": 107.87,  # Silver
    "Cd": 112.41,  # Cadmium
    "In": 114.82,  # Indium
    "Sn": 118.71,  # Tin
    "Sb": 121.76,  # Antimony
    "I": 126.90,  # Iodine
    "Te": 127.60,  # Tellurium
    "Xe": 131.29,  # Xenon
    "Cs": 132.91,  # Cesium
    "Ba": 137.33,  # Barium
    "La": 138.91,  # Lanthanum
    "Ce": 140.12,  # Cerium
    "Pr": 140.91,  # Praseodymium
    "Nd": 144.24,  # Neodymium
    "Pm": 145.0,  # Promethium
    "Sm": 150.36,  # Samarium
    "Eu": 152.00,  # Europium
    "Gd": 157.25,  # Gadolinium
    "Tb": 158.93,  # Terbium
    "Dy": 162.50,  # Dysprosium
    "Ho": 164.93,  # Holmium
    "Er": 167.26,  # Erbium
    "Tm": 168.93,  # Thulium
    "Yb": 173.04,  # Ytterbium
    "Lu": 175.00,  # Lutetium
    "Hf": 178.49,  # Hafnium
    "Ta": 180.95,  # Tantalum
    "W": 183.84,  # Tungsten
    "Re": 186.21,  # Rhenium
    "Os": 190.23,  # Osmium
    "Ir": 192.22,  # Iridium
    "Pt": 195.08,  # Platinum
    "Au": 196.97,  # Gold
    "Hg": 200.59,  # Mercury
    "Tl": 204.38,  # Thallium
    "Pb": 207.2,  # Lead
    "Bi": 208.98,  # Bismuth
    "Po": 209.98,  # Polonium
    "At": 210.0,  # Astatine
    "Rn": 222.0,  # Radon
    "Fr": 223.0,  # Francium
    "Ra": 226.03,  # Radium
    "Ac": 227.03,  # Actinium
    "Th": 232.04,  # Thorium
    "Pa": 231.04,  # Protactinium
    "U": 238.03,  # Uranium
    "Np": 237.0,  # Neptunium
    "Pu": 244.0,  # Plutonium
    "Am": 243.0,  # Americium
    "Cm": 247.0,  # Curium
    "Bk": 247.0,  # Berkelium
    "Cf": 251.0,  # Californium
    "Es": 252.0,  # Einsteinium
    "Fm": 257.0,  # Fermium
    "Md": 258.0,  # Mendelevium
    "No": 259.0,  # Nobelium
    "Lr": 262.0,  # Lawrencium
    "Rf": 267.0,  # Rutherfordium
    "Db": 270.0,  # Dubnium
    "Sg": 271.0,  # Seaborgium
    "Bh": 270.0,  # Bohrium
    "Hs": 277.0,  # Hassium
    "Mt": 276.0,  # Meitnerium
    "Ds": 281.0,  # Darmstadtium
    "Rg": 280.0,  # Roentgenium
    "Cn": 285.0,  # Copernicium
    "Nh": 284.0,  # Nihonium
    "Fl": 289.0,  # Flerovium
    "Mc": 288.0,  # Moscovium
    "Lv": 293.0,  # Livermorium
    "Ts": 294.0,  # Tennessine
    "Og": 294.0,  # Oganesson
}

CRYASTAL_SYSTEMS_SPACE_GROUPS = {
    "Triclinic": ["P1", "P-1"],
    "Monoclinic": [
        "P2",
        "P2_1",
        "C2",
        "Pm",
        "Pc",
        "Cm",
        "Cc",
        "P2/m",
        "P2_1/m",
        "C2/m",
        "P2/c",
        "P2_1/c",
        "C2/c",
    ],
    "Orthorhombic": [
        "P222",
        "P222_1",
        "P2_12_12",
        "P2_12_12_1",
        "C222_1",
        "C222",
        "F222",
        "I222",
        "I2_12_12_1",
        "Pmm2",
        "Pmc2_1",
        "Pcc2",
        "Pma2",
        "Pca2_1",
        "Pnc2",
        "Pmn2_1",
        "Pba2",
        "Pna2_1",
        "Pnn2",
        "Cmm2",
        "Cmc2_1",
        "Ccc2",
        "Amm2",
        "Aem2",
        "Ama2",
        "Aea2",
        "Fmm2",
        "Fdd2",
        "Imm2",
        "Iba2",
        "Ima2",
        "Pmmm",
        "Pnnn",
        "Pccm",
        "Pban",
        "Pmma",
        "Pnna",
        "Pmna",
        "Pcca",
        "Pbam",
        "Pccn",
        "Pbcm",
        "Pnnm",
        "Pmmn",
        "Pbcn",
        "Pbca",
        "Pnma",
        "Cmcm",
        "Cmce",
        "Cmmm",
        "Cccm",
        "Cmme",
        "Ccce",
        "Fmmm",
        "Fddd",
        "Immm",
        "Ibam",
        "Ibca",
        "Imma",
    ],
    "Tetragonal": [
        "P4",
        "P41",
        "P4_2",
        "P4_3",
        "I4",
        "I4_1",
        "P-4",
        "I-4",
        "P4/m",
        "P4_2/m",
        "P4/n",
        "P4_2/n",
        "I4/m",
        "I4_1/a",
        "P422",
        "P4212",
        "P4_122",
        "P4_12_12",
        "P4_222",
        "P4_22_12",
        "P4_322",
        "P4_3212",
        "I422",
        "I4_122",
        "P4mm",
        "P4bm",
        "P4_2cm",
        "P4_2nm",
        "P4cc",
        "P4nc",
        "P4_2mc",
        "P4_2bc",
        "I4mm",
        "I4cm",
        "I4_1md",
        "I4_1cd",
        "P-42m",
        "P-42c",
        "P-42_1m",
        "P-421c",
        "P-4m2",
        "P-4c2",
        "P-4b2",
        "P-4n2",
        "I-4m2",
        "I-4c2",
        "I-42m",
        "I-42d",
        "P4/mmm",
        "P4/mcc",
        "P4/nbm",
        "P4/nnc",
        "P4/mbm",
        "P4/mnc",
        "P4/nmm",
        "P4/ncc",
        "P42/mmc",
        "P4_2/mcm",
        "P4_2/nbc",
        "P4_2/nnm",
        "P4_2/mbc",
        "P4_2/mnm",
        "P4_2/nmc",
        "P4_2/ncm",
        "I4/mmm",
        "I4/mcm",
        "I4_1/amd",
        "I4_1/acd",
    ],
    "Trigonal": [
        "P3",
        "P3_1",
        "P3_2",
        "R3",
        "P-3",
        "R-3",
        "P3_12",
        "P321",
        "P3_112",
        "P3_121",
        "P3_212",
        "P3_221",
        "R32",
        "P3m1",
        "P31m",
        "P3c1",
        "P31c",
        "R3m",
        "R3c",
        "P-31m",
        "P-31c",
        "P-3m1",
        "P-3c1",
        "R-3m",
        "R-3c",
    ],
    "Hexagonal": [
        "P6",
        "P6_1",
        "P6_5",
        "P6_2",
        "P6_4",
        "P6_3",
        "P-6",
        "P6/m",
        "P6_3/m",
        "P622",
        "P6_122",
        "P6_522",
        "P6_222",
        "P6_422",
        "P6_322",
        "P6mm",
        "P6cc",
        "P6_3cm",
        "P6_3mc",
        "P-6m2",
        "P-6c2",
        "P-62m",
        "P-62c",
        "P6/mmm",
        "P6/mcc",
        "P6_3/mcm",
        "P6_3/mmc",
    ],
    "Cubic": [
        "P23",
        "F23",
        "I23",
        "P2_13",
        "I2_13",
        "Pm-3",
        "Pn-3",
        "Fm-3",
        "Fd-3",
        "Im-3",
        "Pa-3",
        "Ia-3",
        "P432",
        "P4_232",
        "F432",
        "F4_132",
        "I432",
        "P4_332",
        "P4_132",
        "I4_132",
        "P-43m",
        "F-43m",
        "I-43m",
        "P-43n",
        "F-43c",
        "I-43d",
        "Pm-3m",
        "Pn-3n",
        "Pm-3n",
        "Pn-3m",
        "Fm-3m",
        "Fm-3c",
        "Fd-3m",
        "Fd-3c",
        "Im-3m",
        "Ia-3d",
    ],
}
