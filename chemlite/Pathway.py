"""A class to represent a metabolic pathway."""
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
    Union,
    Callable
)
from logging import (
    Logger,
    getLogger,
    ERROR
)
from copy import deepcopy
from brs_utils import Cache
from chemlite.Compound import Compound
from chemlite.Reaction import Reaction
from chemlite.Object import Object


class Pathway(Object):

    def __init__(
        self,
        id: str,
        cache: Cache = None,
        infos: Dict = {},
        logger: Logger = getLogger(__name__)
    ):
        super().__init__(
            id=id,
            infos=infos,
            logger=logger
        )
        self.__reactions = []

    ## OUT METHODS
    # def __repr__(self):
    #     return dumps(self._to_dict(), indent=4)

    def to_string(self):
        return '----------------\n' \
             + f'Pathway {self.get_id()}\n' \
             + '----------------\n' \
             + '\n'.join([rxn.__str__() for rxn in self.get_reactions()])

    def _to_dict(self) -> Dict:
        return {
            'reactions': {rxn_id:self.get_reaction(rxn_id)._to_dict() for rxn_id in self.get_reactions_ids()},
            'species': {spe_id:self.get_specie(spe_id)._to_dict() for spe_id in self.get_species_ids()},
            'infos': deepcopy(self.get_infos()),
        }

    def __eq__(self, other) -> bool:
        if isinstance(self, other.__class__):
            return self._to_dict() == other._to_dict()
        return False

    ## READ METHODS
    def get_id(self) -> str:
        return self.__id

    def get_nb_reactions(self) -> int:
        return len(self.get_reactions_ids())

    def get_nb_species(self) -> int:
        return len(self.get_species_ids())

    def get_species_ids(self) -> List[str]:
        # Build the list of species over all reactions
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.get_reactions()]
        # Expand the list and remove duplicates (set)
        set_of_species = set([spe for species in list_of_list_of_species for spe in species])
        return list(set_of_species)

    def get_species(self) -> List[Compound]:
        '''Returns all species of the pathway.
        '''
        return [self.get_specie(spe_id) for spe_id in self.get_species_ids()]

    def get_compounds(self) -> List[Compound]:
        return self.get_species()

    def get_specie(self, spe_id: str) -> Compound:
        compound = Cache.get(spe_id)
        if compound is None:
            self.get_logger().debug(f'There is no specie \'{id}\' in the pathway')
        return compound

    def get_compounds_ids(self) -> List[str]:
        return self.get_species_ids()

    def get_compound(self, cmpd_id: str) -> Compound:
        return self.get_specie(cmpd_id)

    def get_reactions_ids(self) -> List[str]:
        return self.__reactions

    def get_reaction(self, rxn_id: str) -> Reaction:
        rxn = Cache.get(self.__get_cache_id(rxn_id))
        if rxn is None:
            self.get_logger().debug(f'There is no reaction \'{rxn_id}\' in the pathway')
        return rxn

    def get_reactions(self) -> List[Reaction]:
        return [self.get_reaction(rxn_id) for rxn_id in self.get_reactions_ids()]

    def __get_cache_id(self, id: str) -> str:
        return f'{self.get_id()}_{id}'

    ## WRITE METHODS
    def set_id(self, id: str) -> None:
        self.__id = id

    def rename_compound(self, id: str, new_id: str) -> None:
        for rxn in self.get_reactions():
            if id in rxn.get_species_ids():
                # rename compound in cache
                compound = Cache.get(id)
                # Check if id is in the cache (not already renamed)
                if compound is not None:
                    compound.set_id(new_id)
                    # Cache.remove_object_by_id(id)
                    Cache.add(compound)
                # rename in reaction
                rxn.rename_compound(id, new_id)
                self.replace_reaction(rxn.get_id(), rxn)

    def replace_reaction(self, rxn_id: str, rxn: Reaction) -> None:
        self.get_logger().debug(rxn_id+' '+rxn.to_string())
        self.del_reaction(rxn_id)
        self.add_reaction(rxn, rxn_id)

    def add_reaction(
        self,
        rxn: Reaction,
        rxn_id: str = None,
    ) -> None:

        self.get_logger().debug(rxn)

        # RXN ID
        if rxn_id is None:
            rxn_id = rxn.get_id()        
        Cache.rename(
            id=rxn.get_id(),
            new_id=self.__get_cache_id(rxn_id)
        )
        if rxn.get_id() not in self.get_reactions_ids():
            self.__reactions += [rxn_id]

    def del_reaction(self, rxn_id: str) -> None:
        try:
            del self.__reactions[self.__reactions.index(rxn_id)]
        except ValueError:
            self.get_logger().error(f'There is no reaction \'{rxn_id}\' in the pathway, nothing deleted.')


    ## MISC
    @staticmethod
    def net_reaction(reactions: List[Reaction]) -> Reaction:
        '''
        '''

        # SUM ALL SPECIES
        species = {}
        for rxn in reactions:
            # LEFT
            for spe_id, spe_sto in rxn.get_reactants_stoichio().items():
                if spe_id in species:
                    species[spe_id] -= spe_sto
                else:
                    species[spe_id] = -spe_sto
            # RIGHT
            for spe_id, spe_sto in rxn.get_products_stoichio().items():
                if spe_id in species:
                    species[spe_id] += spe_sto
                else:
                    species[spe_id] = spe_sto

        # WRITE INTO A NEW REACTION
        return Reaction(
            id='net_rxn',
            reactants={spe_id:-spe_sto for (spe_id,spe_sto) in species.items() if spe_sto < 0},
            products={spe_id:spe_sto for (spe_id,spe_sto) in species.items() if spe_sto > 0}
        )

