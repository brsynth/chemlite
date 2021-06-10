"""A class to represent a chemical reaction."""
# The MIT License (MIT)
#
# Copyright (c) 2018 Institute for Molecular Systems Biology, ETH Zurich.
# Copyright (c) 2019 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from typing import (
    Dict,
    List,
    TypeVar,
    Union
)
from logging import (
    Logger,
    getLogger
)
from copy import deepcopy
from brs_utils import Cache
from chemlite.Compound import Compound
from chemlite.Object import Object


class Reaction(Object):

    def __init__(
        self,
        id: str,
        ec_number: str = None,
        ec_numbers: List[str] = [],
        reactants: Dict[str, int] = {},
        products: Dict[str, int] = {},
        infos: Dict = {},
        logger: Logger = getLogger(__name__)
    ):
        super().__init__(
            id=id,
            infos=infos,
            logger=logger
        )
        self.__logger = logger
        self.set_ec_numbers(ec_numbers)
        self.add_ec_number(ec_number)
        self.set_reactants(reactants)
        self.set_products(products)

    ## OUT METHODS
    # def __repr__(self):
    #     return f'Reaction {self.get_name()}'

    def to_string(self) -> str:
        if self.get_nb_reactants() == 0 or self.get_nb_products() == 0:
            return super().to_string()
        else:
            return '{class_name} {rxn_name}: {reactants} = {products}'.format(
                class_name=type(self).__name__,
                rxn_name=self.get_id(),
                reactants=' + '.join(
                    [f'{spe_sto} {spe_id}' for spe_id, spe_sto in self.get_reactants_stoichio().items()]
                ),
                products=' + '.join(
                    [f'{spe_sto} {spe_id}' for spe_id, spe_sto in self.get_products_stoichio().items()]
                ),
        )

    def _to_dict(self) -> Dict:
        return {
            **{
                'ec_numbers': deepcopy(self.get_ec_numbers()),
                'reactants': deepcopy(self.get_reactants()),
                'products': deepcopy(self.get_products()),
            },
            **super()._to_dict()
        }

    def __eq__(self, other) -> bool:
        if isinstance(self, other.__class__):
            return self._to_dict() == other._to_dict()
        return False

    ## READ METHODS
    def get_ec_numbers(self) -> List[str]:
        return self.__ec_numbers

    def get_smiles(self) -> str:
        ## LEFT
        left = []
        # build list of compounds with stoichiometry
        for spe_id, spe_sto in self.get_reactants_stoichio().items():
            left += [Cache.get(spe_id).get_smiles()]*spe_sto
        # build smiles string
        left_smi = '.'.join(left)

        ## RIGHT
        right = []
        # build list of compounds with stoichiometry
        for spe_id, spe_sto in self.get_products_stoichio().items():
            right += [Cache.get(spe_id).get_smiles()]*spe_sto
        # build smiles string
        right_smi = '.'.join(right)

        return left_smi + '>>' + right_smi

    def get_reactants_stoichio(self) -> Dict[str, int]:
        return self.__reactants

    def get_nb_reactants(self) -> int:
        return len(self.get_reactants())

    def get_reactants_ids(self) -> List[str]:
        return list(self.get_reactants_stoichio().keys())

    def get_reactants(self) -> List[Compound]:
        return [Cache.get(compound_id) for compound_id in self.get_reactants_ids()]

    def get_products_stoichio(self) -> Dict[str, int]:
        return self.__products

    def get_nb_products(self) -> int:
        return len(self.get_products())

    def get_products_ids(self) -> List[str]:
        return list(self.get_products_stoichio().keys())

    def get_products(self) -> List[Compound]:
        return [Cache.get(compound_id) for compound_id in self.get_products_ids()]

    def get_left(self) -> Dict[str, int]:
        return self.get_reactants_stoichio()

    def get_right(self) -> Dict[str, int]:
        return self.get_products_stoichio()

    def get_species_stoichio(self) -> Dict:
        reactants = {spe_id:-spe_sto for (spe_id,spe_sto) in self.get_reactants_stoichio().items()}
        products = {spe_id:spe_sto for (spe_id,spe_sto) in self.get_products_stoichio().items()}
        return {**reactants, **products}

    def get_species_ids(self) -> List[str]:
        return list(self.get_species_stoichio().keys())

    def get_species(self) -> List[Compound]:
        return [Cache.get(spe_id) for spe_id in self.get_species_ids()]

    ## WRITE METHODS
    def set_ec_numbers(self, numbers: List[str]) -> None:
        self.__ec_numbers = deepcopy(numbers)

    def add_ec_number(self, number: str) -> None:
        if number is not None and number != '':
            self.__ec_numbers += [number]

    def set_reactants(self, compounds: Dict) -> None:
        self.__reactants = {}
        for compound_id, compound_stoichio in compounds.items():
            self.add_reactant(
                compound_id=compound_id,
                stoichio=compound_stoichio
            )

    def set_products(self, compounds: Dict) -> None:
        self.__products = {}
        for compound_id, compound_stoichio in compounds.items():
            self.add_product(
                compound_id=compound_id,
                stoichio=compound_stoichio
            )

    def __add_compound_id(
        self,
        id: str,
        stoichio: int = 1
    ) -> None:
        if id == '':
            self.__logger.error(f'id argument has to be provided')
        else:
            # Select the side to add the compound
            side = self.get_reactants_stoichio() if stoichio < 1 else self.get_products_stoichio()
            if id not in side.keys():
                side[id] = 0
            side[id] += abs(stoichio)

    def __add_compound(
        self,
        compound: Compound,
        id: str,
        stoichio: int
    ) -> None:
        if id is None:
            if compound is None:
                self.__logger.error(f'At least compound or id argument has to be provided')
                return
            else:
                id = compound.get_id()
        self.__add_compound_id(id, stoichio)

    def rename_compound(
        self,
        id: str,
        new_id: str
    ) -> None:
        # Reactants
        species = {}
        for spe_id, spe_sto in self.get_reactants_stoichio().items():
            if spe_id == id:
                species[new_id] = spe_sto
            else:
                species[spe_id] = spe_sto
        self.set_reactants(species)
        # Products
        species = {}
        for spe_id, spe_sto in self.get_products_stoichio().items():
            if spe_id == id:
                species[new_id] = spe_sto
            else:
                species[spe_id] = spe_sto
        self.set_products(species)

    def add_reactant(
        self,
        stoichio: int,
        compound_id: str = None,
        compound: Compound = None,
    ) -> None:
        # Handle pos and neg stoichio
        self.__add_compound(
            compound=compound,
            id=compound_id,
            stoichio=-abs(stoichio)
        )

    def add_product(
        self,
        stoichio: int,
        compound_id: str = None,
        compound: Compound = None
    ) -> None:
        # Handle pos and neg stoichio
        self.__add_compound(
            compound=compound,
            id=compound_id,
            stoichio=abs(stoichio)
        )


