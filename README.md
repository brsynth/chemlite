# chemlite
Defines chemical compounds, reactions, pathways
| Name | Downloads | Version | Platforms |
| --- | --- | --- | --- |
| [![Conda Recipe](https://img.shields.io/badge/recipe-chemlite-green.svg)](https://anaconda.org/conda-forge/chemlite) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/chemlite.svg)](https://anaconda.org/conda-forge/chemlite) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/chemlite.svg)](https://anaconda.org/conda-forge/chemlite) | [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/chemlite.svg)](https://anaconda.org/conda-forge/chemlite) |

## Description
*chemlite* provides classes to deal with chemical compounds, reactions and metabolic pathways.

## Install
### From Conda
```sh
[sudo] conda install -c conda-forge -c chemlite
```

## Use
### Compound
```python
from chemlite import Compound

c = Compound(id='test_cmpd')
```
The code above creates an empty compound. The following fields can be filled and accessed either at build time or later on:
- smiles
- inchi
- inchikey
- formula
- name
- infos

### Reaction
```python
from chemlite import Reaction

r = Reaction(id='test_rxn')
```
The code above creates an empty reaction. The following fields can be filled and accessed either at build time or later on:
- ec_numbers
- reactants
- products
- infos

The following methods are also available:
- `get_smiles()`
- `add_reactant()`
- `add_product()`


### Pathway
```python
from chemlite import Pathway

p = Pathway(id='test_path')
```
The code above creates an empty reaction. The following fields can be filled and accessed either at build time or later on:
- id
- species
- reactions

The following methods are also available:
- `add_compound()`
- `add_reaction()`
- `del_reaction()`
- `Pathway.net_reaction()`


## Tests
Please follow instructions below ti run tests:
```
cd tests
pytest -v
```
For further tests and development tools, a CI toolkit is provided in `ci` folder (see [ci/README.md](ci/README.md)).


## Authors

* **Joan Hérisson**

## Acknowledgments

* Thomas Duigou


## Licence
chemlite is released under the MIT licence. See the LICENCE file for details.
