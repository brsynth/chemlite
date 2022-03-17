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
from json import dumps as json_dumps
from copy import deepcopy
from brs_utils import Cache
from chemlite.Compound import Compound
from chemlite.Object import Object


class Reaction(Object):

    def get_SIDES() -> List: return ['left', 'right']

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

    @staticmethod
    def from_string(
        rxn: str,
        id: str,
        logger: Logger = getLogger(__file__)
    ) -> 'Reaction':
        """
        Build transformation to complete.

        Parameters
        ----------
        trans_smi: str
            Transformation in SMILES format or with CID.
            Stoichiometric coefficients must be separated by spaces.
        logger : Logger
            The logger object.

        Returns
        -------
        transfo: Dict
            Dictionary of the transformation.
        """
        logger.debug(f'transfo: {rxn}')

        transfo = Reaction.parse(rxn, logger)

        return Reaction(
            id=id,
            reactants=transfo['left'],
            products=transfo['right'],
            logger=logger
        )

    @staticmethod
    def parse(
        rxn: str,
        logger: Logger = getLogger(__file__)
    ):
        transfo = {
            'left': {},
            'right': {},
            'format': '',
            'sep_side': '',
            'sep_cmpd': ''
        }
        # Detect input format
        if '>>' in rxn:  # SMILES
            transfo['format'] = 'smiles'
            transfo['sep_side'] = '>>'
            transfo['sep_cmpd'] = '.'
        elif '=' in rxn:  # CMPD IDs
            transfo['format'] = 'cid'
            transfo['sep_side'] = '='
            transfo['sep_cmpd'] = '+'
        trans = {}
        trans['left'], trans['right'] = rxn.split(transfo['sep_side'])
        for side in Reaction.get_SIDES():
            for cmpd in trans[side].split(transfo['sep_cmpd']):
                # Separate compounds, remove leading and trailing spaces
                _list = cmpd.strip().split(' ')
                # Detect stoichio coeff
                if len(_list) > 1:
                    _coeff = float(_list[0])
                    _cmpd = _list[1]
                else:
                    _coeff = 1.0
                    _cmpd = _list[0]
                if not _cmpd in transfo[side]:
                    transfo[side][_cmpd] = 0
                transfo[side][_cmpd] += _coeff
        logger.debug('INPUT TRANSFORMATION: '+str(json_dumps(transfo, indent=4)))
        return transfo

    def to_string(self) -> str:
        '''Returns the string representation of the reaction

        Returns
        -------
        string: str
            String representation of the reaction
        '''
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

    def _to_dict(self, full=False) -> Dict:
        '''Returns a dictionary with all (with legacy) attributes of the reaction:
            - id (legacy)
            - ec_numbers
            - reactants
            - products

        Returns
        -------
        dict: Dict
            Dictionary with all (with legacy) attributes of the reaction
        '''
        d = {
            'reactants': deepcopy(self.get_reactants()),
            'products': deepcopy(self.get_products()),
        }
        if full:
            d.update(
                {
                    **super()._to_dict(),
                    'ec_numbers': deepcopy(self.get_ec_numbers()),
                }
            )
        return d

    ## READ METHODS
    def get_ec_numbers(self) -> List[str]:
        '''Returns the list of EC numbers of the reaction.

        Returns
        -------
        ec_numbers: List[str]
            List of EC numbers of the reaction
        '''
        return self.__ec_numbers

    def get_smiles(self) -> str:
        '''Builds and returns the SMILES string of the reaction

        Returns
        -------
        smiles: str
            SMILES string of the reaction
        '''
        def get_smi(spe_id: str, spe_sto: float) -> str:
            check_smiles = (
                Cache.get(spe_id) is not None
                and Cache.get(spe_id).get_smiles() is not None
                and Cache.get(spe_id).get_smiles() != ''
            )
            if check_smiles:
                _spe_sto = round(spe_sto)
                _spe_sto = _spe_sto if _spe_sto > 0 else 1
                if _spe_sto != spe_sto:
                    self.get_logger().warning(
                        f'Stoichiometric coefficient of compound {spe_id} ({spe_sto}) has been rounded to {_spe_sto}.'
                        )
                return [Cache.get(spe_id).get_smiles()]*_spe_sto
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
        '''Returns a dictionary (alphabetically sorted) where
        keys are IDs of products and
        values are the stoichiometric coefficient in the reaction

        Returns
        -------
        products: Dict[str, int]
            Stoichiometric dictionary of products
        '''
        try:
            return dict(sorted(self.__reactants.items(), key=lambda item: item[0]))
        except AttributeError:
            return None

    def get_reactant(self, cmpd_id: str) -> int:
        '''Returns the stoichiometric coefficient (> 0) of the
        reactant compound with ID = 'cmpd_id'

        Parameters
        ----------
        cmpd_id: str
            ID of the compound to return the stoichiometric coefficient

        Returns
        -------
        sto_coeff: Dict[str, int]
            Stoichiometric coefficient of the reactant compound of ID 'cmpd_id'
        '''
        try:
            return self.__reactants[cmpd_id]
        except (KeyError, TypeError):
            return 0

    def get_nb_reactants(self) -> int:
        '''Returns the number of reactants of the reaction

        Returns
        -------
        nb: int
            Number of reactants of the reaction
        '''
        try:
            return len(self.get_reactants())
        except TypeError:
            return 0

    def get_reactants_ids(self) -> List[str]:
        '''Returns the list of reactants IDs

        Returns
        -------
        reactants_ids: List[str]
            List of reactants IDs
        '''
        return list(self.get_reactants().keys())

    def get_reactants_compounds(self) -> List[Compound]:
        '''Returns the list of compounds that are reactants of the reaction

        Returns
        -------
        reactants: List[Compound]
            List of compounds that are reactants of the reaction
        '''
        return [Cache.get(compound_id) for compound_id in self.get_reactants_ids()]

    def get_products(self) -> Dict[str, int]:
        '''Returns a dictionary (alphabetically sorted) where
        keys are IDs of products and
        values are the stoichiometric coefficient in the reaction

        Returns
        -------
        products: Dict[str, int]
            Stoichiometric dictionary of products
        '''
        try:
            return dict(sorted(self.__products.items(), key=lambda item: item[0]))
        except AttributeError:
            return None

    def get_product(self, cmpd_id: str) -> int:
        '''Returns the stoichiometric coefficient (> 0) of the
        product compound with ID = 'cmpd_id'

        Parameters
        ----------
        cmpd_id: str
            ID of the compound to return the stoichiometric coefficient

        Returns
        -------
        sto_coeff: Dict[str, int]
            Stoichiometric coefficient of the product compound of ID 'cmpd_id'
        '''
        try:
            return self.__products[cmpd_id]
        except (KeyError, TypeError):
            return 0

    def get_nb_products(self) -> int:
        '''Returns the number of products of the reaction

        Returns
        -------
        nb: int
            Number of products of the reaction
        '''
        try:
            return len(self.get_products())
        except TypeError:
            return 0

    def get_products_ids(self) -> List[str]:
        '''Returns the list of products IDs

        Returns
        -------
        products_ids: List[str]
            List of products IDs
        '''
        return list(self.get_products().keys())

    def get_products_compounds(self) -> List[Compound]:
        '''Returns the list of compounds that are products of the reaction

        Returns
        -------
        products: List[Compound]
            List of compounds that are products of the reaction
        '''
        return [Cache.get(compound_id) for compound_id in self.get_products_ids()]

    def get_left(self) -> Dict[str, int]:
        '''Same as get_reactants()'''
        return self.get_reactants()

    def get_right(self) -> Dict[str, int]:
        '''Same as get_products()'''
        return self.get_products()

    def get_species(self) -> Dict:
        '''Combines the result of both get_reactants() and get_products() but
        stoichiometric coefficients for reactants are negative (< 0).

        Returns
        -------
        species: Dict[str, int]
            Stoichiometric (alphabetically sorted) dictionary of
            species in the reaction.
        '''
        return {
            **{spe_id: -spe_sto for spe_id, spe_sto in self.get_reactants().items()},
            **self.get_products(),
        }

    def get_species_ids(self) -> List[str]:
        '''Returns the list of species IDs

        Returns
        -------
        species_ids: List[str]
            List of species IDs
        '''
        return list(
            set(
                list(self.get_reactants().keys())
                + list(self.get_products().keys())
            )
        )

    def get_specie(self, cmpd_id: str) -> Dict:
        '''Return informations about a specie within the current reaction

        Parameters
        ----------
        cmpd_id: str
            ID of the compound to return the informations

        Returns
        -------
        infos: Dict
            Informations
        '''
        return {
            'reactant': self.get_reactant(cmpd_id),
            'product': self.get_product(cmpd_id)
        }

    def get_species_compounds(self) -> List[Compound]:
        '''Returns the list of compounds in the reaction

        Returns
        -------
        compounds: List[Compound]
            List of compounds in the reaction
        '''
        return [Cache.get(spe_id) for spe_id in self.get_species_ids()]

    def get_nb_species(self) -> int:
        '''Returns the number of species of the reaction

        Returns
        -------
        nb: int
            Number of species of the reaction
        '''
        return len(self.get_species_ids())

    ## WRITE METHODS
    def set_ec_numbers(self, numbers: List[str]) -> None:
        '''Set the EC numbers of the reaction

        Parameters
        ----------
        numbers: List[str]
            List of string to set the reaction's EC numbers to
        '''
        self.__ec_numbers = deepcopy(numbers)

    def add_ec_number(self, number: str) -> None:
        '''Add an EC number to the reaction

        Parameters
        ----------
        number: str
            String to add in the reaction's EC numbers
        '''
        if number is not None and number != '':
            self.__ec_numbers += [number]

    def set_reactants(self, compounds: Dict[str, int]) -> None:
        '''Set the reactants of the reaction

        Parameters
        ----------
        compounds: Dict[str, int]
            Stoichiometric dictionary to set the reactions's reactants to
        '''
        self.__reactants = {}
        if compounds is not None:
            for spe_id, spe_sto in compounds.items():
                self.set_reactant(spe_id, spe_sto)

    def set_reactant(self, cmpd_id: str, stoichio: int) -> None:
        '''Set the stoichiometric coefficient of the reactant compound
        with ID 'cmpd_id'. Do nothing if 'cmpd_id' is None or empty string

        Parameters
        ----------
        cmpd_id: str
            ID of the reactant compound
        stoichio: int
            Stoichiometric coefficient to set the reactant compound to
        '''
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
        '''Set the products of the reaction

        Parameters
        ----------
        compounds: Dict[str, int]
            Stoichiometric dictionary to set the reactions's products to
        '''
        self.__products = {}
        if compounds is not None:
            for spe_id, spe_sto in compounds.items():
                self.set_product(spe_id, spe_sto)

    def set_product(self, cmpd_id: str, stoichio: int) -> None:
        '''Set the stoichiometric coefficient of the product compound
        with ID 'cmpd_id'. Do nothing if 'cmpd_id' is None or empty string

        Parameters
        ----------
        cmpd_id: str
            ID of the product compound
        stoichio: int
            Stoichiometric coefficient to set the product compound to
        '''
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
        '''Rename a compound in the reaction.

        Parameters
        ----------
        id: str
            ID of the compound to rename
        new_id: str
            String to set the compound's ID to
        '''

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
        '''Add the compound with ID 'compound_id' and
        stoichiometric coefficient 'stoichio' to
        the reaction's list of reactants

        Parameters
        ----------
        compound_id: str
            ID of the reactant compound to add
        stoichio: int
            Stoichiometric coefficient of the reactant compound to add
        '''
        self.set_reactant(
            cmpd_id=compound_id,
            stoichio=self.get_reactant(compound_id)+abs(stoichio)
        )

    def add_product(
        self,
        compound_id: str,
        stoichio: int,
    ) -> None:
        '''Add the compound with ID 'compound_id' and
        stoichiometric coefficient 'stoichio' to
        the reaction's list of products

        Parameters
        ----------
        compound_id: str
            ID of the product compound to add
        stoichio: int
            Stoichiometric coefficient of the product compound to add
        '''
        self.set_product(
            cmpd_id=compound_id,
            stoichio=self.get_product(compound_id)+abs(stoichio)
        )

    def mult_stoichio_coeff(self, mult: float) -> None:
        '''Multiply stoichiometric coefficients of all species of the reaction by 'mult'

        Parameters
        ----------
        mult: float
            Integer to multiply all stoichiometric coefficients with
        '''
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
    ) -> Dict[str, int]:
        '''Make the sum of stoichiometric coefficients
        of all species in all reactions in the passed list and
        returns a stoichiometric dictionary of the pseudo-reaction.
        If a compound is both a reactant of a reaction of the list (coeff < 0)
        and a product of another reaction of the list (coeff > 0),
        the sum could be 0 and the compound is naturally deleted from the
        result (pseudo-reaction).

        Parameters
        ----------
        reactions: List['Reaction']
            List of reactions to make the stoichiometric sum of

        Returns
        -------
        stoichio: Dict[str, int]
            Stoichiometric dictionary of summed stoichiometric coefficients (pseudo-reaction)
        '''

        l_reactants = [rxn.get_reactants() for rxn in reactions]
        l_products = [rxn.get_products() for rxn in reactions]

        # SUM ALL SPECIES
        species = {}

        # Reactants
        for reactants in l_reactants:
            for spe_id, spe_sto in reactants.items():
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
