"""
Created on May 28 2021

@author: Joan Hérisson
"""

from unittest import TestCase
from copy import deepcopy
from os import path as os_path
from json import load as jsload

from chemlite import (
    Pathway,
    Reaction,
    Compound,
)

HERE = os_path.dirname(os_path.realpath(__file__))
DATA_PATH = os_path.join(HERE, 'data')

class Test_Pathway(TestCase):

    def setUp(self):
        self.species = {}
        with open(os_path.join(DATA_PATH, 'compounds.json'), 'r') as fp:
            species = jsload(fp)
        for spe_id in species:
            self.species[spe_id] = Compound(**species[spe_id])
        self.reactants = {
            "CMPD_0000000003": 1,
            "MNXM4": 1
        }
        self.products = {
            "TARGET_0000000001": 1,
            "MNXM1": 2
        }
        self.rxn = Reaction(
            id="rxn_4",
            ec_numbers=[
                "1.13.11.1"
            ],
            reactants=self.reactants,
            products=self.products
        )
        self.reactions = {
            self.rxn.get_id(): self.rxn,
            "rxn_3": Reaction(
                id="rxn_3",
                ec_numbers=[
                    "4.1.1.63"
                ],
                reactants={
                    "CMPD_0000000010": 1,
                    "MNXM1": 1
                },
                products={
                    "CMPD_0000000003": 1,
                    "MNXM13": 1
                }
            ),
            "rxn_2": Reaction(
                id="rxn_2",
                ec_numbers=[
                    "1.14.13.23"
                ],
                reactants={
                    "CMPD_0000000025": 1,
                    "MNXM4": 1,
                    "MNXM6": 1,
                    "MNXM1": 1
                },
                products={
                    "CMPD_0000000010": 1,
                    "MNXM2": 1,
                    "MNXM5": 1
                }
            ),
            "rxn_1": Reaction(
                id="rxn_1",
                ec_numbers=[
                    "4.1.3.45"
                ],
                reactants={
                    "MNXM337": 1
                },
                products={
                    "CMPD_0000000025": 1,
                    "MNXM23": 1
                }
            )
        }
        self.id = 'pathway'
        self.pathway = Pathway(
            id=self.id
        )
        for rxn in self.reactions.values():
            self.pathway.add_reaction(rxn)

    ## READ METHODS
    def test_rename_compound(self):
        old_id = self.rxn.get_reactants_ids()[0]
        new_id = 'NEW_CMPD_ID'
        self.pathway.rename_compound(old_id, new_id)
        self.assertTrue(
            new_id in self.pathway.get_reaction(self.rxn.get_id()).get_species_ids()
        )
        self.assertFalse(
            old_id in self.pathway.get_reaction(self.rxn.get_id()).get_species_ids()
        )

    def test_replace_reaction(self):
        _rxn = deepcopy(self.rxn)
        rxn = Reaction(_rxn.get_id())
        self.assertEqual(
            self.pathway.get_reaction(self.rxn.get_id()),
            _rxn
        )
        self.assertTrue(
            self.pathway.replace_reaction(
                self.rxn.get_id(),
                rxn
            )
        )
        self.assertNotEqual(
            self.pathway.get_reaction(self.rxn.get_id()),
            _rxn
        )

    def test_replace_reaction_wrong_rxnid(self):
        self.assertFalse(
            self.pathway.replace_reaction(
                'wrong_rxn_id',
                Reaction(id='test')
            )
        )

    def test_get_id(self):
        self.assertEqual(
            self.pathway.get_id(),
            self.id
        )

    def test_get_nb_reactions(self):
        self.assertEqual(
            self.pathway.get_nb_reactions(),
            len(self.reactions)
        )

    def test_get_nb_species(self):
        # build the list of all species from all reactions
        species = [rxn.get_products_compounds()+rxn.get_reactants_compounds() for rxn in self.pathway.get_list_of_reactions()]
        # build a set from flatten species list of lists
        species = set([y.get_id() for x in species for y in x])
        self.assertEqual(
            self.pathway.get_nb_species(),
            len(species)
        )

    def test_get_species(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.reactions.values()]
        list_of_species = list(set([spe for species in list_of_list_of_species for spe in species]))
        self.assertListEqual(
            self.pathway.get_species(),
            [self.pathway.get_specie(spe_id) for spe_id in list_of_species]
        )

    def test_get_species_ids(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.reactions.values()]
        self.assertListEqual(
            self.pathway.get_species_ids(),
            list(set([spe for species in list_of_list_of_species for spe in species]))
        )

    def test_get_species_from_id(self):
        self.assertEqual(
            self.pathway.get_specie('MNXM23'),
            self.species['MNXM23']
        )

    def test_get_species_from_id_wrong_key(self):
        self.assertEqual(
            self.pathway.get_specie('WRONG_KEY'),
            None
        )

    def test_get_compounds_ids(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.reactions.values()]
        self.assertListEqual(
            self.pathway.get_compounds_ids(),
            list(set([spe for species in list_of_list_of_species for spe in species]))
        )

    def test_get_compounds(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.reactions.values()]
        list_of_species = list(set([spe for species in list_of_list_of_species for spe in species]))
        self.assertListEqual(
            self.pathway.get_compounds(),
            [self.pathway.get_specie(spe_id) for spe_id in list_of_species]
        )

    def test_get_compound(self):
        self.assertEqual(
            self.pathway.get_compound('MNXM23'),
            self.species['MNXM23']
        )

    def test_get_reactions(self):
        self.assertDictEqual(
            self.pathway.get_reactions(),
            self.reactions
        )

    def test_get_list_of_reactions(self):
        self.assertListEqual(
            self.pathway.get_list_of_reactions(),
            list(self.reactions.values())
        )

    def test_get_reaction(self):
        self.assertEqual(
            self.pathway.get_reaction('rxn_4'),
            self.rxn
        )

    def test_get_reaction_wrong_id(self):
        self.assertEqual(
            self.pathway.get_reaction('WRONG_ID'),
            None
        )

    def test_reaction_ids(self):
        self.assertEqual(
            self.pathway.get_reactions_ids(),
            [rxn.get_id() for rxn in self.reactions.values()]
        )

    def test_add_reaction(self):
        rxn = Reaction(id='rxn')
        self.pathway.add_reaction(rxn)
        self.assertListEqual(
            list(self.pathway.get_reactions().values()),
            list(self.reactions.values()) + [rxn]
        )
        self.assertListEqual(
            self.pathway.get_reactions_ids(),
            [rxn.get_id() for rxn in self.reactions.values()] + [rxn.get_id()]
        )

    def test_add_reaction_with_id(self):
        rxn = Reaction(id='rxn')
        other_id = 'other_' + rxn.get_id()
        self.pathway.add_reaction(rxn, other_id)
        self.assertListEqual(
            list(self.pathway.get_reactions().values()),
            list(self.reactions.values()) + [rxn]
        )
        self.assertListEqual(
            self.pathway.get_reactions_ids(),
            [rxn.get_id() for rxn in self.reactions.values()] + [other_id]
        )

    def test__to_dict(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.reactions.values()]
        list_of_species = list(set([spe for species in list_of_list_of_species for spe in species]))
        self.assertDictEqual(
            self.pathway._to_dict(full=False),
            {
                'reactions': {rxn.get_id(): rxn._to_dict() for rxn in self.reactions.values()},
                'species': {spe.get_id(): spe._to_dict() for spe in [self.species[spe_id] for spe_id in list_of_species]},
            }
        )

    def test__to_dict_full(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.reactions.values()]
        list_of_species = list(set([spe for species in list_of_list_of_species for spe in species]))
        self.assertDictEqual(
            self.pathway._to_dict(full=True),
            {
                'reactions': {rxn.get_id(): rxn._to_dict() for rxn in self.reactions.values()},
                'species': {spe.get_id(): spe._to_dict() for spe in [self.species[spe_id] for spe_id in list_of_species]},
                'id': self.id
            }
        )

    def test_to_string(self):
        # for rxn in self.reactions:
        #     print(rxn)
        self.assertEqual(
            self.pathway.to_string(),
            '----------------\n' +
            f'Pathway {self.pathway.get_id()}\n' +
            '----------------\n' +
            '\n'.join([rxn.to_string() for rxn in self.reactions.values()])
        )

    def test_eq(self):
        reactions = []
        for rxn in self.reactions.values():
            reactions.append(deepcopy(rxn))
        pathway = Pathway(id='pathway_test')
        for i in range(len(reactions)):
            index = len(reactions)-i-1
            # change id
            reactions[index].set_id(i)
            # add reaction in the reverse order
            pathway.add_reaction(rxn=reactions[index])
        self.assertEqual(
            self.pathway,
            pathway
        )

    def test_not_equal_reactions(self):
        pathway = deepcopy(Pathway(id=self.id))
        pathway.add_reaction(Reaction(id='test_1'))
        self.assertNotEqual(
            self.pathway,
            pathway
        )

    def test_del_reaction(self):
        self.assertTrue(
            self.pathway.del_reaction(
                self.rxn.get_id()
            )
        )
        self.assertListEqual(
            self.pathway.get_reactions_ids(),
            [
                rxn.get_id()
                for rxn
                in list(self.reactions.values())[1:]]
        )

    def test_del_reaction_wrong_id(self):
        self.assertFalse(
            self.pathway.del_reaction('WRONG')
        )
        self.assertListEqual(
            self.pathway.get_reactions_ids(),
            [rxn.get_id() for rxn in self.reactions.values()]
        )

    def test_eq_not_equal(self):
        self.assertNotEqual(
            self.pathway,
            Pathway(id=self.id)
        )

    def test_eq_wrong_type(self):
        self.assertNotEqual(
            self.pathway,
            0
        )

    def test_net_reaction(self):
        self.assertEqual(
            self.pathway.net_reaction(),
            {
                'MNXM4': -2,
                'TARGET_0000000001': 1,
                'MNXM13': 1,
                'MNXM6': -1,
                'MNXM2': 1,
                'MNXM5': 1,
                'MNXM337': -1,
                'MNXM23': 1
            }
        )

    def test_pseudo_reaction(self):
        self.assertEqual(
            self.pathway.pseudo_reaction(),
            {
                'MNXM4': -2,
                'TARGET_0000000001': 1,
                'MNXM13': 1,
                'MNXM6': -1,
                'MNXM2': 1,
                'MNXM5': 1,
                'MNXM337': -1,
                'MNXM23': 1
            }
        )

    def test_get_reactants(self):
        species = []
        for rxn in self.reactions.values():
            species += rxn.get_reactants_ids()
        self.assertListEqual(
            self.pathway.get_reactants_ids(),
            sorted(set(species))
        )

    def test_get_products(self):
        species = []
        for rxn in self.reactions.values():
            species += rxn.get_products_ids()
        self.assertListEqual(
            self.pathway.get_products_ids(),
            sorted(set(species))
        )
