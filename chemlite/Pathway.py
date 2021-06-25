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
)
from logging import (
    Logger,
    getLogger,
)
from brs_utils import Cache
from chemlite.Compound import Compound
from chemlite.Reaction import Reaction
from chemlite.Object import Object


class Pathway(Object):

    def __init__(
        self,
        id: str,
        cache: Cache = None,
        logger: Logger = getLogger(__name__)
    ):
        super().__init__(
            id=id,
            logger=logger
        )
        self.__reactions = {}

    ## OUT METHODS
    # def __repr__(self):
    #     return dumps(self._to_dict(), indent=4)

    def to_string(self):
        '''Returns the string representation of the pathway

        Returns
        -------
        string: str
            String representation of the pathway
        '''
        return '----------------\n' \
            + f'Pathway {self.get_id()}\n' \
            + '----------------\n' \
            + '\n'.join([rxn.__str__() for rxn in self.get_reactions().values()])

    def _to_dict(self) -> Dict:
        '''Returns a dictionary with all (with legacy) attributes of the pathway:
            - id (legacy)
            - reactions
            - species

        Returns
        -------
        dict: Dict
            Dictionary with all (with legacy) attributes of the pathway
        '''
        return {
            **super()._to_dict(),
            **self.__to_dict()
        }

    def __to_dict(self) -> Dict:
        '''Returns a dictionary with only specific attributes of the pathway:
            - reactions
            - species

        Returns
        -------
        dict: Dict
            Dictionary with only specific attributes of the pathway
        '''
        return {
            'reactions': {rxn_id: self.get_reaction(rxn_id)._to_dict() for rxn_id in self.get_reactions_ids()},
            'species': {spe_id: self.get_specie(spe_id)._to_dict() for spe_id in self.get_species_ids()},
        }

    ## READ METHODS
    def get_nb_reactions(self) -> int:
        '''Returns the number of reactions of the pathway

        Returns
        -------
        nb: int
            Integer equal to the number of reactions in the pathway
        '''
        return len(self.get_reactions())

    def get_nb_species(self) -> int:
        '''Returns the number of species involved in all the reactions of the pathway

        Returns
        -------
        nb: int
            Integer equal to the number of species invloved in the pathway
        '''
        return len(self.get_species_ids())

    def get_species_ids(self) -> List[str]:
        '''Returns IDs of the species involved in all the reactions of the pathway

        Returns
        -------
        ids: List[str]
            IDs of the species involved in the pathway
        '''
        # Build the list of species over all reactions
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.get_reactions().values()]
        # Expand the list and remove duplicates (set)
        set_of_species = set([spe for species in list_of_list_of_species for spe in species])
        return list(set_of_species)

    def get_species(self) -> List[Compound]:
        '''Returns the species involved in all the reactions of the pathway

        Returns
        -------
        species: List[Compound]
            Species involved in the pathway
        '''
        return [self.get_specie(spe_id) for spe_id in self.get_species_ids()]

    def get_compounds(self) -> List[Compound]:
        '''Same as get_species()'''
        return self.get_species()

    def get_specie(self, spe_id: str) -> Compound:
        '''Returns a specific specie involved in the pathway if exists,
        None otherwise.

        Parameters
        ----------
        spe_id: str
            ID of the specie to get

        Returns
        -------
        specie: Compound
            The specie with id 'spe_id'
        '''
        compound = Cache.get(spe_id)
        return compound

    def get_compounds_ids(self) -> List[str]:
        '''Same as get_species_ids()'''
        return self.get_species_ids()

    def get_compound(self, cmpd_id: str) -> Compound:
        '''Same as get_specie(cmpd_id)'''
        return self.get_specie(cmpd_id)

    def get_reactions_ids(self) -> List[str]:
        '''Returns IDs of reactions of the pathway

        Returns
        -------
        ids: List[str]
            IDs of reactions of the pathway
        '''
        return list(self.__reactions.keys())

    def get_reaction(self, rxn_id: str) -> Reaction:
        '''Returns a specific reaction of the pathway if exists,
        None otherwise.

        Parameters
        ----------
        rxn_id: str
            ID of the reaction to get

        Returns
        -------
        reaction: Reaction
            The reaction with id 'rxn_id'
        '''
        return self.get_reactions().get(rxn_id, None)

    def get_reactions(self) -> Dict[str, Reaction]:
        '''Returns a dictionary where keys are reaction ids
        and values the reactions themselves

        Returns
        -------
        reactions: Dict[str, Reaction]
            Reactions of the pathway
        '''
        return self.__reactions

    def get_list_of_reactions(self) -> List[Reaction]:
        '''Returns a list of the reactions in the pathway

        Returns
        -------
        reactions: Dict[str, Reaction]
            Reactions of the pathway
        '''
        return list(self.__reactions.values())

    def get_reactants_ids(self) -> List[str]:
        '''Returns all reactants involved in the pathway,
        alphabetically sorted

        Returns
        -------
        reactants: List[str]
            Reactants of the pathway
        '''
        return sorted(
            set(
                [
                    spe_id
                    for rxn in self.get_list_of_reactions()
                    for spe_id in rxn.get_reactants_ids()
                ]
            )
        )

    def get_products_ids(self) -> List[str]:
        '''Returns all products involved in the pathway,
        alphabetically sorted

        Returns
        -------
        products: List[str]
            Products of the pathway
        '''
        return sorted(
            set(
                [
                    spe_id
                    for rxn in self.get_list_of_reactions()
                    for spe_id in rxn.get_products_ids()
                ]
            )
        )

    ## WRITE METHODS
    def rename_compound(self, id: str, new_id: str) -> None:
        '''Rename a compound within the pathway. Actually, the
        compound is renamed over all reactions

        Parameters
        ----------
        id: str
            ID of the compound to rename
        new_id: str
            ID that the compound has to be renamed to
        '''
        for rxn in self.get_reactions().values():
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

    def replace_reaction(self, rxn_id: str, rxn: Reaction) -> bool:
        '''Replace a reaction in the pathway. Returns True if the
        replacement has been done, False otherwise

        Parameters
        ----------
        rxn_id: str
            ID of the reaction to replace
        rxn: Reaction
            Reaction to add in the pathway
        
        Returns
        -------
        b: bool
            True if replacement has been done, False otherwise
        '''
        self.get_logger().debug(rxn_id+' '+rxn.to_string())
        if rxn_id in self.get_reactions_ids():
            self.add_reaction(rxn, rxn_id)
            return True
        else:
            self.get_logger().warning(f'Reaction {rxn_id} not found in the pathway, nothing done.')
            return False

    def add_reaction(
        self,
        rxn: Reaction,
        rxn_id: str = None,
    ) -> None:
        '''Add a reaction in the pathway

        Parameters
        ----------
        rxn: Reaction
            Reaction to add in the pathway
        new_id: str
            ID that the compound has to be renamed to
        '''
        self.get_logger().debug(rxn)

        # RXN ID
        if rxn_id is None:
            rxn_id = rxn.get_id()
        self.__reactions[rxn_id] = rxn

    def del_reaction(self, rxn_id: str) -> bool:
        '''Remove a reaction from the pathway. Returns True if the
        replacement has been done, False otherwise

        Parameters
        ----------
        rxn_id: str
            ID of the reaction to removed

        Returns
        -------
        b: bool
            True if deletion has been done, False otherwise
        '''
        try:
            del self.__reactions[rxn_id]
            return True
        except KeyError:
            self.get_logger().error(f'Reaction \'{rxn_id}\' not found in the pathway, nothing deleted.')
            return False

    ## MISC
    def net_reaction(self) -> Dict[str, float]:
        '''Returns the net reaction (or pseudo-reaction) of the pathway,
        i.e. the stoichiometric sum of all reactions of the pathway.
        See Reaction::sum_stoichio for more details.
        '''
        return Reaction.sum_stoichio(self.get_reactions().values())

    def pseudo_reaction(self) -> Reaction:
        '''Same as net_reaction()'''
        return self.net_reaction()
