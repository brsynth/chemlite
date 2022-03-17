"""
Created on May 28 2021

@author: Joan Hérisson
"""

from unittest import TestCase
from copy import deepcopy
from os import path as os_path
from json import load as jsload
from brs_utils import Cache

from chemlite import (
    Reaction,
    Compound
)

HERE = os_path.dirname(os_path.realpath(__file__))
DATA_PATH = os_path.join(HERE, 'data')


class Test_Reaction(TestCase):

    def setUp(self):
        self.species = {}
        with open(os_path.join(DATA_PATH, 'compounds.json'), 'r') as fp:
            species = jsload(fp)
        for spe_id in species:
            self.species[spe_id] = Compound(**species[spe_id])
        self.reactants = {
            "CMPD_0000000010": 1,
            "MNXM1": 1
        }
        self.products = {
            "CMPD_0000000003": 1,
            "MNXM13": 1
        }
        self.smiles = '[H]OC(=O)c1c([H])c([H])c(O[H])c(O[H])c1[H].[H+]>>[H]Oc1c([H])c([H])c([H])c([H])c1O[H].O=C=O'
        self.string = '1 CMPD_0000000010 + 1 MNXM1 = 1 CMPD_0000000003 + 1 MNXM13'
        self.rxn_string_w_floating_coeff = '1.0 CMPD_0000000005 + 1.0 MNXM1462 + 1.7 MNXM27 = 1.0 CMPD_0000000028 + 1.0 CMPD_0000000022 + 1.7 MNXM27'
        self.ec_numbers = [
            "4.1.1.63"
        ]
        self.id = "rxn"
        self.rxn = Reaction(
            id=self.id,
            ec_numbers=self.ec_numbers,
            reactants=self.reactants,
            products=self.products
        )

    def test___init__ec_number(self):
        ec_number = '1.1.2'
        rxn = Reaction(
            id='rxn_test',
            ec_numbers=ec_number
        )
        self.assertListEqual(
            rxn.get_ec_numbers(),
            [ec_number]
        )

    def test_to_string(self):
        self.assertEqual(
            self.rxn.to_string(),
            f'Reaction {self.rxn.get_id()}: {self.string}'
        )

    def test_to_string_0(self):
        self.rxn.set_products({})
        self.rxn.set_reactants({})
        self.assertEqual(
            self.rxn.to_string(),
            f'Reaction {self.rxn.get_id()}:  = '
        )

    def test__to_dict(self):
        self.assertEqual(
            self.rxn._to_dict(full=False),
            {
                'reactants': self.reactants,
                'products': self.products,
            }
        )

    def test__to_dict_full(self):
        self.assertEqual(
            self.rxn._to_dict(full=True),
            {
                'ec_numbers': self.ec_numbers,
                'reactants': self.reactants,
                'products': self.products,
                'id': self.id
            }
        )

    def test_eq1(self):
        rxn = deepcopy(self.rxn)
        self.assertEqual(
            rxn,
            self.rxn
        )

    def test_eq2(self):
        rxn = Reaction(
            id='rxn_test_eq2',
            reactants=self.rxn.get_reactants(),
            products=self.rxn.get_products()
        )
        self.assertEqual(
            rxn,
            self.rxn
        )

    def test_not_eq(self):
        rxn = deepcopy(self.rxn)
        rxn.add_reactant(compound_id='c', stoichio=1)
        self.assertNotEqual(
            rxn,
            self.rxn
        )

    def test_eq_wrong_type(self):
        self.assertNotEqual(
            self.rxn,
            0
        )

    # def test_get_reactants_None(self):
    #     self.rxn.set_reactants(None)
    #     self.assertEqual(
    #         self.rxn.get_reactants(),
    #         None
    #     )

    def test_get_reactants_ids(self):
        self.assertListEqual(
            self.rxn.get_reactants_ids(),
            list(self.reactants.keys())
        )

    def test_get_products_ids(self):
        self.assertListEqual(
            self.rxn.get_products_ids(),
            list(self.products.keys())
        )

    def test_get_reactants_compounds(self):
        self.assertListEqual(
            self.rxn.get_reactants_compounds(),
            [self.species[spe_id] for spe_id in self.reactants.keys()]
        )

    def test_get_smiles(self):
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )

    def test_get_smiles_cmpd_wo_smiles_L(self):
        self.rxn.add_reactant(
            compound_id='CMPD_0000000003_wo_smiles',
            stoichio=1
        )
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )

    def test_get_smiles_cmpd_wo_smiles_R(self):
        self.rxn.add_product(
            compound_id='CMPD_0000000003_wo_smiles',
            stoichio=1
        )
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )

    def test_get_smiles_w_cmpd_not_in_cache(self):
        self.rxn.add_reactant(
            compound_id='CMPD_NOT_IN_CACHE',
            stoichio=1
        )
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )

    def test_get_smiles_w_smile_None_L(self):
        self.rxn.add_reactant(
            compound_id='CMPD_0000000003_w_smiles_None',
            stoichio=1
        )
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )

    def test_get_smiles_w_smile_None_R(self):
        self.rxn.add_product(
            compound_id='CMPD_0000000003_w_smiles_None',
            stoichio=1
        )
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )

    def test_get_smiles_w_all_cmpds_wo_smiles(self):
        self.rxn.add_reactant(
            compound_id='CMPD_0000000003_wo_smiles',
            stoichio=1
        )
        self.rxn.add_product(
            compound_id='CMPD_0000000004_wo_smiles',
            stoichio=1
        )
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )
    
    def test_get_smiles_w_floating_coeff(self):
        rxn = Reaction.from_string(
            id='test',
            rxn=self.rxn_string_w_floating_coeff
        )
        print(rxn._to_dict())
        print(rxn.get_smiles())
        self.assertEqual(
            rxn.get_smiles(),
            ''
        )


    def test_from_string(self):
        rxn = Reaction.from_string(
            id='test',
            rxn=self.rxn_string_w_floating_coeff
        )
        self.assertEqual(
            sum(rxn.get_specie('MNXM27').values()),
            3.4
        )

    def test_from_string_smiles(self):
        rxn = Reaction.from_string(
            id='test',
            rxn='[H][O][C](=[O])[C](=[O])[C]([H])([O][H])[C]([H])([O][H])[C]([H])([O][H])[C]([H])([H])[O][H]>>[H]OC(=O)C(=O)C([H])(O[H])C([H])(O[H])C([H])([H])C([H])=O.[H]O[H].[H]O[H]'
        )
        self.assertEqual(
            sum(rxn.get_specie('[H]O[H]').values()),
            2
        )

    def test_get_products_compounds(self):
        self.assertListEqual(
            self.rxn.get_products_compounds(),
            [self.species[spe_id] for spe_id in self.products.keys()]
        )

    def test_get_species_compounds(self):
        self.assertListEqual(
            sorted([spe.get_id() for spe in self.rxn.get_species_compounds()]),
            sorted(list(set(list(self.reactants.keys()) + list(self.products.keys()))))
        )

    def test_get_left(self):
        self.assertDictEqual(
            self.rxn.get_left(),
            self.reactants
        )

    def test_get_right(self):
        self.assertDictEqual(
            self.rxn.get_right(),
            self.products
        )

    def test_get_nb_species(self):
        self.assertEqual(
            self.rxn.get_nb_species(),
            len(self.reactants) + len(self.products)
        )

    def test_add_ec_number(self):
        ec_number = '1.2'
        self.rxn.add_ec_number(ec_number)
        self.assertListEqual(
            self.rxn.get_ec_numbers(),
            self.ec_numbers + [ec_number]
        )

    def test_add_reactant(self):
        for spe_sto in [3, -3]:
            with self.subTest(spe_sto=spe_sto):
                rxn = deepcopy(self.rxn)
                rxn.add_reactant(
                    compound_id=self.species['MNXM337'].get_id(),
                    stoichio=spe_sto
                )
                self.assertDictEqual(
                    rxn.get_reactants(),
                    {
                        **self.rxn.get_reactants(),
                        **{self.species['MNXM337'].get_id(): abs(spe_sto)}
                    }
                )

    def test_set_reactant(self):
        self.rxn.set_reactants(None)
        self.rxn.add_reactant('cmpd', 1)

    def test_set_product(self):
        self.rxn.set_products(None)
        self.rxn.add_product('cmpd', 1)

    def test_set_product_already_exist(self):
        self.rxn.add_product('MNXM13', 1)
        self.assertEqual(
            Cache.get('MNXM13').get_smiles(),
            self.species['MNXM13'].get_smiles()
        )

    def test_add_reactant_wo_id(self):
        cmpd_sto = 4
        rxn = deepcopy(self.rxn)
        rxn.add_reactant(stoichio=cmpd_sto, compound_id='')
        self.assertDictEqual(
            rxn.get_reactants(),
            self.rxn.get_reactants()
        )

    def test_add_reactant_with_id_none(self):
        cmpd_sto = 4
        rxn = deepcopy(self.rxn)
        rxn.add_reactant(stoichio=cmpd_sto, compound_id=None)
        self.assertListEqual(
            rxn.get_reactants_ids(),
            self.rxn.get_reactants_ids()
        )

    def test_add_product_with_id_none(self):
        cmpd_sto = 4
        rxn = deepcopy(self.rxn)
        rxn.add_product(stoichio=cmpd_sto, compound_id=None)
        self.assertListEqual(
            rxn.get_products_ids(),
            self.rxn.get_products_ids()
        )

    def test_add_reactant_withall_none(self):
        cmpd_sto = 4
        rxn = deepcopy(self.rxn)
        rxn.add_reactant(stoichio=cmpd_sto, compound_id=None)
        self.assertDictEqual(
            rxn.get_reactants(),
            self.rxn.get_reactants()
        )

    def test_add_product(self):
        for spe_sto in [3, -3]:
            with self.subTest(spe_sto=spe_sto):
                rxn = deepcopy(self.rxn)
                rxn.add_product(
                    compound_id=self.species['MNXM337'].get_id(),
                    stoichio=spe_sto
                )
                self.assertDictEqual(
                    rxn.get_products(),
                    {
                        **self.rxn.get_products(),
                        **{self.species['MNXM337'].get_id(): abs(spe_sto)}
                    }
                )

    def test_rename_compound_reactant(self):
        old_id = self.species['MNXM1'].get_id()
        new_id = 'new_cmpd_id'
        self.rxn.rename_compound(old_id, new_id)
        reactants_ids = list(self.reactants.keys())
        reactants_ids[reactants_ids.index(old_id)] = new_id
        self.assertEqual(
            self.rxn.get_reactants_ids(),
            reactants_ids
        )

    def test_rename_compound_product(self):
        old_id = self.species['MNXM13'].get_id()
        new_id = 'new_cmpd_id'
        self.rxn.rename_compound(old_id, new_id)
        products_ids = list(self.products.keys())
        products_ids[products_ids.index(old_id)] = new_id
        self.assertEqual(
            self.rxn.get_products_ids(),
            products_ids
        )

    def test_mult_stoichio_coeff(self):
        mult = 2
        self.rxn.mult_stoichio_coeff(mult)
        self.assertDictEqual(
            self.rxn.get_species(),
            {
                **{spe_id: -mult * self.reactants[spe_id] for spe_id in self.reactants.keys()},
                **{spe_id: mult * self.products[spe_id] for spe_id in self.products.keys()}
            }
        )

    def test_sum_stoichio(self):
        reactants_1 = {
            'MNXM4': 1,
            'MNXM337': 1,
            'MNXM3': 2
        }
        reactants_2 = {
            'MNXM4': 1,
            'MNXM337': 1,
        }
        reactants_3 = {
            'MNXM4': 2,
            'MNXM6': 1,
            'MNXM5': 1,
        }
        products_1 = {
            'MNXM2': 1,
            'MNXM5': 1,
            'MNXM23': 1
        }
        products_2 = {
            'MNXM13': 1,
            'MNXM6': 3,
            'MNXM5': 1,
            'MNXM3': 1
        }
        products_3 = {
            'TARGET_0000000001': 1,
            'MNXM2': 1,
            'MNXM5': 1,
            'MNXM3': 1
        }
        rxn_1 = Reaction(
            id='rxn_1',
            reactants=reactants_1,
            products=products_1,
        )
        rxn_2 = Reaction(
            id='rxn_2',
            reactants=reactants_2,
            products=products_2,
        )
        rxn_3 = Reaction(
            id='rxn_3',
            reactants=reactants_3,
            products=products_3,
        )
        self.assertDictEqual(
            Reaction.sum_stoichio(
                [rxn_1, rxn_2, rxn_3]
            ),
            {
                'MNXM4': -4,
                'MNXM337': -2,
                'MNXM6': 2,
                'MNXM2': 2,
                'MNXM5': 2,
                'TARGET_0000000001': 1,
                'MNXM13': 1,
                'MNXM23': 1
            }
        )
