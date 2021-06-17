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
from brs_utils import Cache
from chemlite.Compound import Compound
from chemlite.Object import Object


class Reaction(Object):

    def __init__(
        self,
        id: str,
        ec_numbers: Union[List[str], str] = [],
        reactants: Dict[str, int] = {},
        products: Dict[str, int] = {},
        logger: Logger = getLogger(__name__)
    ):
        super().__init__(
            id=id,
            logger=logger
        )
        if isinstance(ec_numbers, list):
            self.set_ec_numbers(ec_numbers)
        else:
            self.set_ec_numbers([])
            self.add_ec_number(ec_numbers)
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
                    [f'{spe_sto} {spe_id}' for spe_id, spe_sto in self.get_reactants().items()]
                ),
                products=' + '.join(
                    [f'{spe_sto} {spe_id}' for spe_id, spe_sto in self.get_products().items()]
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

        def get_smi(spe_id: str, spe_sto: int) -> str:
            check_smiles = (
                Cache.get(spe_id) is not None
                and Cache.get(spe_id).get_smiles() is not None
                and Cache.get(spe_id).get_smiles() != ''
            )
            if check_smiles:
                return [Cache.get(spe_id).get_smiles()]*spe_sto
            else:
                self.get_logger().warning(f'Compound {spe_id} has no smiles')
                return []

        ## LEFT
        smi = []
        # build list of compounds with stoichiometry
        for spe_id, spe_sto in self.get_reactants().items():
            smi += get_smi(spe_id, spe_sto)
        # build smiles string
        left_smi = '.'.join(smi)

        ## RIGHT
        smi = []
        # build list of compounds with stoichiometry
        for spe_id, spe_sto in self.get_products().items():
            smi += get_smi(spe_id, spe_sto)
        # build smiles string
        right_smi = '.'.join(smi)

        return left_smi + '>>' + right_smi

    def get_reactants(self) -> Dict[str, int]:
        try:
            return self.__reactants
        except AttributeError:
            return None

    def get_reactant(self, cmpd_id: str) -> int:
        try:
            return self.__reactants[cmpd_id]
        except (KeyError, TypeError):
            return 0

    def get_nb_reactants(self) -> int:
        try:
            return len(self.get_reactants())
        except TypeError:
            return 0

    def get_reactants_ids(self) -> List[str]:
        return list(self.get_reactants().keys())

    def get_reactants_compounds(self) -> List[Compound]:
        return [Cache.get(compound_id) for compound_id in self.get_reactants_ids()]

    def get_products(self) -> Dict[str, int]:
        try:
            return self.__products
        except AttributeError:
            return None

    def get_product(self, cmpd_id: str) -> int:
        try:
            return self.__products[cmpd_id]
        except (KeyError, TypeError):
            return 0

    def get_nb_products(self) -> int:
        try:
            return len(self.get_products())
        except TypeError:
            return 0

    def get_products_ids(self) -> List[str]:
        return list(self.get_products().keys())

    def get_products_compounds(self) -> List[Compound]:
        return [Cache.get(compound_id) for compound_id in self.get_products_ids()]

    def get_left(self) -> Dict[str, int]:
        return self.get_reactants()

    def get_right(self) -> Dict[str, int]:
        return self.get_products()

    def get_species(self) -> Dict:
        return {
            **dict(sorted({spe_id: -spe_sto for spe_id, spe_sto in self.get_reactants().items()}.items(), key=lambda item: item[0])),
            **dict(sorted(self.get_products().items(), key=lambda item: item[0])),
        }

    def get_species_ids(self) -> List[str]:
        return list(set(list(self.get_reactants().keys()) + list(self.get_products().keys())))

    def get_species_compounds(self) -> List[Compound]:
        return [Cache.get(spe_id) for spe_id in self.get_species_ids()]

    def get_nb_species(self) -> int:
        return len(self.get_species())

    ## WRITE METHODS
    def set_ec_numbers(self, numbers: List[str]) -> None:
        self.__ec_numbers = deepcopy(numbers)

    def add_ec_number(self, number: str) -> None:
        if number is not None and number != '':
            self.__ec_numbers += [number]

    def set_reactants(self, compounds: Dict) -> None:
        self.__reactants = {}
        if compounds is not None:
            for spe_id, spe_sto in compounds.items():
                self.set_reactant(spe_id, spe_sto)

    def set_reactant(self, cmpd_id: str, stoichio: int) -> None:
        if cmpd_id is None or cmpd_id == '':
            return None
            self.logger.warning(f'Compound ID passed is equal to {cmpd_id}')
        if self.get_reactants() is None:
            self.__reactants = {}
        self.__reactants[cmpd_id] = abs(stoichio)
        if cmpd_id not in Cache.get_list_of_objects():
            # add to Cache
            Compound(id=cmpd_id)

    def set_products(self, compounds: Dict) -> None:
        self.__products = {}
        if compounds is not None:
            for spe_id, spe_sto in compounds.items():
                self.set_product(spe_id, spe_sto)

    def set_product(self, cmpd_id: str, stoichio: int) -> None:
        if cmpd_id is None or cmpd_id == '':
            return None
            self.logger.warning(f'Compound ID passed is equal to {cmpd_id}')
        if self.get_products() is None:
            self.__products = {}
        self.__products[cmpd_id] = abs(stoichio)
        if cmpd_id not in Cache.get_list_of_objects():
            # add to Cache
            Compound(id=cmpd_id)

    def rename_compound(
        self,
        id: str,
        new_id: str
    ) -> None:

        # Reactants
        species = {}
        for spe_id, spe_sto in self.get_reactants().items():
            if spe_id == id:
                species[new_id] = spe_sto
            else:
                species[spe_id] = spe_sto
        self.set_reactants(species)

        # Products
        species = {}
        for spe_id, spe_sto in self.get_products().items():
            if spe_id == id:
                species[new_id] = spe_sto
            else:
                species[spe_id] = spe_sto
        self.set_products(species)

    def add_reactant(
        self,
        compound_id: str,
        stoichio: int,
    ) -> None:
        self.set_reactant(
            cmpd_id=compound_id,
            stoichio=self.get_reactant(compound_id)+abs(stoichio)
        )

    def add_product(
        self,
        compound_id: str,
        stoichio: int,
    ) -> None:
        self.set_product(
            cmpd_id=compound_id,
            stoichio=self.get_product(compound_id)+abs(stoichio)
        )

    def mult_stoichio_coeff(self, mult: int) -> None:
        for spe_id in self.get_reactants().keys():
            self.set_reactant(
                spe_id,
                self.get_reactant(spe_id)*mult
            )
        for spe_id in self.get_products().keys():
            self.set_product(
                spe_id,
                self.get_product(spe_id)*mult
            )

    @staticmethod
    def sum_stoichio(
        reactions: List['Reaction']
    ) -> Dict:
        '''
        '''

        l_reactants = [rxn.get_reactants() for rxn in reactions]
        l_products = [rxn.get_products() for rxn in reactions]

        # SUM ALL SPECIES
        species = {}

        # Reactants
        for reactants in l_reactants:
            for spe_id, spe_sto in reactants.items():
                print(spe_id, spe_sto)
                if spe_id in species:
                    species[spe_id] -= spe_sto
                else:
                    species[spe_id] = -spe_sto

        # Products
        for products in l_products:
            for spe_id, spe_sto in products.items():
                if spe_id in species:
                    species[spe_id] += spe_sto
                else:
                    species[spe_id] = spe_sto

        return {spe_id: spe_sto for (spe_id, spe_sto) in species.items() if spe_sto != 0}
