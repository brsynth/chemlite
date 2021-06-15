"""
Created on May 28 2021

@author: Joan Hérisson
"""

from unittest import TestCase
from copy import deepcopy
from chemlite import (
    Reaction,
    Compound
)


species = {
    "TARGET_0000000001": Compound(
        id="TARGET_0000000001",
        smiles="[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H]",
        inchi="InChI=1S/C6H6O4/c7-5(8)3-1-2-4-6(9)10/h1-4H,(H,7,8)(H,9,10)",
        inchikey="TXXHDPDFNKHHGW-UHFFFAOYSA-N"
    ),
    "CMPD_0000000010": Compound(
        id="CMPD_0000000010",
        smiles="[H]OC(=O)c1c([H])c([H])c(O[H])c(O[H])c1[H]",
        inchi="InChI=1S/C7H6O4/c8-5-2-1-4(7(10)11)3-6(5)9/h1-3,8-9H,(H,10,11)",
        inchikey="YQUVCSBJEUQKSH-UHFFFAOYSA-N"
    ),
    "MNXM23": Compound(
        id="MNXM23",
        formula="C3H3O3",
        smiles="CC(=O)C(=O)O]",
        inchi="InChI=1S/C3H4O3/c1-2(4)3(5)6/h1H3,(H,5,6)",
        inchikey="LCTONWCANYUPML-UHFFFAOYSA-N",
        name="pyruvate"
    ),
    "CMPD_0000000025": Compound(
        id="CMPD_0000000025",
        smiles="[H]OC(=O)c1c([H])c([H])c([H])c(O[H])c1[H]",
        inchi="InChI=1S/C7H6O3/c8-6-3-1-2-5(4-6)7(9)10/h1-4,8H,(H,9,10)",
        inchikey="IJFXRHURBJZNAO-UHFFFAOYSA-N"
    ),
    "CMPD_0000000003": Compound(
        id="CMPD_0000000003",
        smiles="[H]Oc1c([H])c([H])c([H])c([H])c1O[H]",
        inchi="InChI=1S/C6H6O2/c7-5-3-1-2-4-6(5)8/h1-4,7-8H",
        inchikey="YCIMNLLNPGFGHC-UHFFFAOYSA-N"
    ),
    "CMPD_0000000003_wo_smiles": Compound(
        id="CMPD_0000000003_wo_smiles",
        inchi="InChI=1S/C6H6O2/c7-5-3-1-2-4-6(5)8/h1-4,7-8H",
        inchikey="YCIMNLLNPGFGHC-UHFFFAOYSA-N"
    ),
    "MNXM337": Compound(
        id="MNXM337",
        smiles="[H]OC(=O)C(OC1([H])C([H])=C(C(=O)O[H])C([H])=C([H])C1([H])O[H])=C([H])[H]",
        inchi="InChI=1S/C10H10O6/c1-5(9(12)13)16-8-4-6(10(14)15)2-3-7(8)11/h2-4,7-8,11H,1H2,(H,12,13)(H,14,15)",
        inchikey="WTFXTQVDAKGDEY-UHFFFAOYSA-N"
    ),
    "MNXM2": Compound(
        id="MNXM2",
        smiles="[H]O[H]",
        inchi="InChI=1S/H2O/h1H2",
        inchikey="XLYOFNOQVPJJNP-UHFFFAOYSA-N"
    ),
    "MNXM13": Compound(
        id="MNXM13",
        smiles="O=C=O",
        inchi="InChI=1S/CO2/c2-1-3",
        inchikey="CURLTUGMZLYLDI-UHFFFAOYSA-N",
        formula="CO2",
        name="CO2"
    ),
    "MNXM5": Compound(
        id="MNXM5",
        smiles="N=C(O)c1ccc[n+](C2OC(COP(=O)(O)OP(=O)(O)OCC3OC(n4cnc5c(N)ncnc54)C(OP(=O)(O)O)C3O)C(O)C2O)c1",
        inchi="InChI=1S/C21H28N7O17P3/c22-17-12-19(25-7-24-17)28(8-26-12)21-16(44-46(33,34)35)14(30)11(43-21)6-41-48(38,39)45-47(36,37)40-5-10-13(29)15(31)20(42-10)27-3-1-2-9(4-27)18(23)32/h1-4,7-8,10-11,13-16,20-21,29-31H,5-6H2,(H7-,22,23,24,25,32,33,34,35,36,37,38,39)/p+1",
        inchikey="XJLXINKUBYWONI-UHFFFAOYSA-O",
        formula="C21H25N7O17P3",
        name="NADP(+)"
    ),
    "MNXM4": Compound(
        id="MNXM4",
        smiles="O=O",
        inchi="InChI=1S/O2/c1-2",
        inchikey="MYMOFIZGZYHOMD-UHFFFAOYSA-N"
    ),
    "MNXM1": Compound(
        id="MNXM1",
        smiles="[H+]",
        inchi="InChI=1S/p+1",
        inchikey="GPRLSGONYQIRFK-UHFFFAOYSA-N"
    ),
    "MNXM6": Compound(
        id="MNXM6",
        smiles="[H]N=C(O[H])C1=C([H])N(C2([H])OC([H])(C([H])([H])OP(=O)(O[H])OP(=O)(O[H])OC([H])([H])C3([H])OC([H])(n4c([H])nc5c(N([H])[H])nc([H])nc54)C([H])(OP(=O)(O[H])O[H])C3([H])O[H])C([H])(O[H])C2([H])O[H])C([H])=C([H])C1([H])[H]",
        inchi="InChI=1S/C21H30N7O17P3/c22-17-12-19(25-7-24-17)28(8-26-12)21-16(44-46(33,34)35)14(30)11(43-21)6-41-48(38,39)45-47(36,37)40-5-10-13(29)15(31)20(42-10)27-3-1-2-9(4-27)18(23)32/h1,3-4,7-8,10-11,13-16,20-21,29-31H,2,5-6H2,(H2,23,32)(H,36,37)(H,38,39)(H2,22,24,25)(H2,33,34,35)",
        inchikey="ACFIXJIJDZMPPO-UHFFFAOYSA-N"
    )
}

class Test_Reaction(TestCase):

    def setUp(self):
        self.mnxm13 = Compound(
            id="MNXM13",
            smiles="O=C=O",
            inchi="InChI=1S/CO2/c2-1-3",
            inchikey="CURLTUGMZLYLDI-UHFFFAOYSA-N",
            formula="CO2",
            name="CO2"
        )
        self.mnxm1 = Compound(
            id="MNXM1",
            smiles="[H+]",
            inchi="InChI=1S/p+1",
            inchikey="GPRLSGONYQIRFK-UHFFFAOYSA-N"
        )
        self.new_cmpd = Compound(
            id="MNXM337",
            smiles="[H]OC(=O)C(OC1([H])C([H])=C(C(=O)O[H])C([H])=C([H])C1([H])O[H])=C([H])[H]",
            inchi="InChI=1S/C10H10O6/c1-5(9(12)13)16-8-4-6(10(14)15)2-3-7(8)11/h2-4,7-8,11H,1H2,(H,12,13)(H,14,15)",
            inchikey="WTFXTQVDAKGDEY-UHFFFAOYSA-N"
        )
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
        self.assertEqual(
            self.rxn.to_string(),
            f'Reaction {self.rxn.get_id()}'
        )

    def test_to_dict(self):
        self.assertEqual(
            self.rxn._to_dict(),
            {
                'ec_numbers': self.ec_numbers,
                'reactants': self.reactants,
                'products': self.products,
                'id': self.id
            }
        )

    def test_eq(self):
        rxn = deepcopy(self.rxn)
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

    def test_get_reactants(self):
        self.assertListEqual(
            self.rxn.get_reactants(),
            [species[spe_id] for spe_id in self.reactants.keys()]
        )

    def test_get_smiles(self):
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )

    def test_get_smiles_cmpd_wo_smiles(self):
        self.rxn.add_reactant(
            compound_id='CMPD_0000000003_wo_smiles',
            stoichio=1
        )
        self.assertEqual(
            self.rxn.get_smiles(),
            self.smiles
        )

    def test_get_products(self):
        self.assertListEqual(
            self.rxn.get_products(),
            [species[spe_id] for spe_id in self.products.keys()]
        )

    def test_get_species(self):
        self.assertListEqual(
            sorted([spe.get_id() for spe in self.rxn.get_species()]),
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
                    compound_id=self.new_cmpd.get_id(),
                    compound=self.new_cmpd,
                    stoichio=spe_sto
                )
                self.assertDictEqual(
                    rxn.get_reactants_stoichio(),
                    {
                        **self.rxn.get_reactants_stoichio(),
                        **{self.new_cmpd.get_id(): abs(spe_sto)}
                    }
                )

    def test_add_reactant_wo_id(self):
        cmpd_sto = 4
        rxn = deepcopy(self.rxn)
        rxn.add_reactant(stoichio=cmpd_sto, compound_id='')
        self.assertListEqual(
            rxn.get_reactants(),
            self.rxn.get_reactants()
        )

    def test_add_reactant_with_id_none(self):
        cmpd_sto = 4
        rxn = deepcopy(self.rxn)
        rxn.add_reactant(stoichio=cmpd_sto, compound=self.new_cmpd)
        self.assertListEqual(
            rxn.get_reactants_ids(),
            self.rxn.get_reactants_ids() + [self.new_cmpd.get_id()]
        )

    def test_add_reactant_withall_none(self):
        cmpd_sto = 4
        rxn = deepcopy(self.rxn)
        rxn.add_reactant(stoichio=cmpd_sto, compound_id=None, compound=None)
        self.assertListEqual(
            rxn.get_reactants(),
            self.rxn.get_reactants()
        )

    def test_add_product(self):
        for spe_sto in [3, -3]:
            with self.subTest(spe_sto=spe_sto):
                rxn = deepcopy(self.rxn)
                rxn.add_product(
                    compound_id=self.new_cmpd.get_id(),
                    compound=self.new_cmpd,
                    stoichio=spe_sto
                )
                self.assertDictEqual(
                    rxn.get_products_stoichio(),
                    {
                        **self.rxn.get_products_stoichio(),
                        **{self.new_cmpd.get_id(): abs(spe_sto)}
                    }
                )

    def test_rename_compound_reactant(self):
        old_id = self.mnxm1.get_id()
        new_id = 'new_cmpd_id'
        self.rxn.rename_compound(old_id, new_id)
        reactants_ids = list(self.reactants.keys())
        reactants_ids[reactants_ids.index(old_id)] = new_id
        self.assertEqual(
            self.rxn.get_reactants_ids(),
            reactants_ids
        )

    def test_rename_compound_product(self):
        old_id = self.mnxm13.get_id()
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
            self.rxn.get_species_stoichio(),
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
        self.assertDictEqual(
            Reaction.sum_stoichio(
                [reactants_1, reactants_2, reactants_3],
                [products_1, products_2, products_3],
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
