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
    Union
)
from logging import (
    Logger,
    getLogger
)
from copy import deepcopy
import operator
from brs_utils import Cache
from chemlite.Compound import Compound
from chemlite.Object import Object


def get_truth(inp, relate, cut):
    ops = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq
    }
    return ops[relate](inp, cut)


class Reaction(Object):

    def __init__(
        self,
        id: str,
        ec_numbers: Union[List[str], str] = [],
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
        if isinstance(ec_numbers, list):
            self.set_ec_numbers(ec_numbers)
        else:
            self.set_ec_numbers([])
            self.add_ec_number(ec_numbers)
        self.set_stoichio(
            reactants=reactants,
            products=products
        )

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
            **super()._to_dict(),
            **self.__to_dict()
        }

    def __to_dict(self) -> Dict:
        return {
            'ec_numbers': deepcopy(self.get_ec_numbers()),
            'reactants': deepcopy(self.get_reactants()),
            'products': deepcopy(self.get_products()),
        }

    def __eq__(self, other) -> bool:
        if isinstance(self, other.__class__):
            return self.__to_dict() == other.__to_dict()
        return False

    ## READ METHODS
    def get_ec_numbers(self) -> List[str]:
        return self.__ec_numbers

    def get_smiles(self) -> str:
        ## LEFT
        smi = []
        # build list of compounds with stoichiometry
        for spe_id, spe_sto in self.get_reactants_stoichio().items():
            smi += [Cache.get(spe_id).get_smiles()]*spe_sto
        # build smiles string
        left_smi = '.'.join(smi)

        ## RIGHT
        smi = []
        # build list of compounds with stoichiometry
        for spe_id, spe_sto in self.get_products_stoichio().items():
            smi += [Cache.get(spe_id).get_smiles()]*spe_sto
        # build smiles string
        right_smi = '.'.join(smi)

        return left_smi + '>>' + right_smi

    def __get_species_stoichio(self, op: str, coeff: int) -> Dict[str, int]:
        return {
            spe_id: coeff*spe_sto
            for spe_id, spe_sto
            in self.get_species_stoichio().items()
            if get_truth(spe_sto, op, 0)
        }

    def get_reactants_stoichio(self) -> Dict[str, int]:
        return self.__get_species_stoichio('<', -1)

    def get_nb_reactants(self) -> int:
        return len(self.get_reactants_stoichio())

    def get_reactants_ids(self) -> List[str]:
        return list(self.get_reactants_stoichio().keys())

    def get_reactants(self) -> List[Compound]:
        return [Cache.get(compound_id) for compound_id in self.get_reactants_ids()]

    def get_products_stoichio(self) -> Dict[str, int]:
        return self.__get_species_stoichio('>', 1)

    def get_nb_products(self) -> int:
        return len(self.get_products_stoichio())

    def get_products_ids(self) -> List[str]:
        return list(self.get_products_stoichio().keys())

    def get_products(self) -> List[Compound]:
        return [Cache.get(compound_id) for compound_id in self.get_products_ids()]

    def get_left(self) -> Dict[str, int]:
        return self.get_reactants_stoichio()

    def get_right(self) -> Dict[str, int]:
        return self.get_products_stoichio()

    def get_species_stoichio(self) -> Dict:
        return dict(sorted(self.__stoichio.items(), key=lambda item: item[0]))

    def get_species_ids(self) -> List[str]:
        return list(self.get_species_stoichio().keys())

    def get_species(self) -> List[Compound]:
        return [Cache.get(spe_id) for spe_id in self.get_species_ids()]

    def get_nb_species(self) -> int:
        return len(self.get_species_stoichio())

    ## WRITE METHODS
    def set_ec_numbers(self, numbers: List[str]) -> None:
        self.__ec_numbers = deepcopy(numbers)

    def add_ec_number(self, number: str) -> None:
        if number is not None and number != '':
            self.__ec_numbers += [number]

    def set_stoichio(
        self,
        reactants: Dict[str, int],
        products: Dict[str, int]
    ) -> None:
        self.__stoichio = {
            **{spe_id: -spe_sto for spe_id, spe_sto in reactants.items()},
            **products
        }

    def set_reactants(self, compounds: Dict) -> None:
        self.__stoichio = {
            **{spe_id: -spe_sto for spe_id, spe_sto in compounds.items()},
            **self.get_products_stoichio()
        }

    def set_products(self, compounds: Dict) -> None:
        self.__stoichio = {
            **{spe_id: -spe_sto for spe_id, spe_sto in self.get_reactants_stoichio().items()},
            **compounds
        }

    def __add_compound(
        self,
        compound: Compound,
        id: str,
        stoichio: int
    ) -> None:
        if id is None:
            if compound is None:
                self.get_logger().error('At least compound or id argument has to be provided')
                return
            else:
                id = compound.get_id()
        if id == '':
            self.get_logger().error('id argument has to be provided')
        else:
            self.__stoichio[id] = stoichio

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

    def mult_stoichio_coeff(self, mult: int) -> None:
        for spe_id in self.get_species_stoichio().keys():
            self.__stoichio[spe_id] *= mult

    @staticmethod
    def sum_stoichio(
        l_reactants_sto: List[Dict[str, int]],
        l_products_sto: List[Dict[str, int]]
    ) -> Dict:
        '''
        '''

        # SUM ALL SPECIES
        species = {}

        # Reactants
        for reactants in l_reactants_sto:
            for spe_id, spe_sto in reactants.items():
                if spe_id in species:
                    species[spe_id] -= spe_sto
                else:
                    species[spe_id] = -spe_sto

        # Products
        for products in l_products_sto:
            for spe_id, spe_sto in products.items():
                if spe_id in species:
                    species[spe_id] += spe_sto
                else:
                    species[spe_id] = spe_sto

        return {spe_id: spe_sto for (spe_id, spe_sto) in species.items() if spe_sto != 0}
