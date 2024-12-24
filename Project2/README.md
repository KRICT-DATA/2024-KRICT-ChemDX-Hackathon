# Environment settings
```bash
conda create -n krict python=3.10
conda activate krict
```
## Install pytorch mace
[pytorch](https://pytorch.org/)
[mace](https://github.com/ACEsuit/mace)

## Usage
- preprocessing data: `get_inputs.ipynb` after running the script below.
```
python data_reform.py
```

- Training: `experiments.ipynb`