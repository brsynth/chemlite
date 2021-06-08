"""
Created on May 28 2021

@author: Joan Hérisson
"""

from unittest import TestCase
from chemlite import (
    Pathway,
    Reaction,
    Compound,
    Object
)
from copy import deepcopy

        # infos={
        #     'transfo_id': "TRS_0_0_0",
        #     'rule_id': "RR-02-a0cc0be463ff412f-16-F",
        #     'rule_score': 0.5982208769718989,
        #     'tmpl_rxn_id': "MNXR96458",
        # },
        # fba_fraction=1.3648925522849815,
        # thermo={
        #     "dG0_prime": {
        #         "value": -324.1942486194258,
        #         "error": 5.946918851751192,
        #         "units": "kilojoule / mole"
        #     },
        #     "dGm_prime": {
        #         "value": -307.0794110847048,
        #         "error": 5.946918851751192,
        #         "units": "kilojoule / mole"
        #     },
        #     "dG_prime": {
        #         "value": -324.1942486194258,
        #         "error": 5.946918851751192,
        #         "units": "kilojoule / mole"
        #     }
        # },
        # # smiles="[H]Oc1c([H])c([H])c([H])c([H])c1O[H].O=O>>[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H].[H+].[H+]",

        # infos={
        #     'transfo_id': "TRS_0_1_19",
        #     'rule_id': "RR-02-9bcd062586f04b0c-16-F",
        #     'rule_score': 0.7023718970192103,
        #     'tmpl_rxn_id': "MNXR106706",
        # },
        # fba_fraction=1.3648925522849815,
        # thermo={
        #     "dG0_prime": {
        #         "value": -7.741996690048865,
        #         "error": 3.31976861655151,
        #         "units": "kilojoule / mole"
        #     },
        #     "dGm_prime": {
        #         "value": -24.856834224769898,
        #         "error": 3.31976861655151,
        #         "units": "kilojoule / mole"
        #     },
        #     "dG_prime": {
        #         "value": -7.741996690048865,
        #         "error": 3.31976861655151,
        #         "units": "kilojoule / mole"
        #     }
        # },
        # # smiles="[H]OC(=O)c1c([H])c([H])c(O[H])c(O[H])c1[H].[H+]>>[H]Oc1c([H])c([H])c([H])c([H])c1O[H].O=C=O",

        # infos={
        #     'transfo_id': "TRS_0_2_5",
        #     'rule_id': "RR-02-4b759d9ffae4e8ab-16-F",
        #     'rule_score': 1.0,
        #     'tmpl_rxn_id': "MNXR107096",
        # },
        # fba_fraction=1.3648925522849815,
        # thermo={
        #     "dG0_prime": {
        #         "value": -439.72331555029746,
        #         "error": 3.7590254041440385,
        #         "units": "kilojoule / mole"
        #     },
        #     "dGm_prime": {
        #         "value": -422.60847801557645,
        #         "error": 3.7590254041440385,
        #         "units": "kilojoule / mole"
        #     },
        #     "dG_prime": {
        #         "value": -439.72331555029746,
        #         "error": 3.7590254041440385,
        #         "units": "kilojoule / mole"
        #     }
        # },
        # # smiles="[H]OC(=O)c1c([H])c([H])c([H])c(O[H])c1[H].O=O.[H]N=C(O[H])C1=C([H])N(C2([H])OC([H])(C([H])([H])OP(=O)(O[H])OP(=O)(O[H])OC([H])([H])C3([H])OC([H])(n4c([H])nc5c(N([H])[H])nc([H])nc54)C([H])(OP(=O)(O[H])O[H])C3([H])O[H])C([H])(O[H])C2([H])O[H])C([H])=C([H])C1([H])[H].[H+]>>[H]OC(=O)c1c([H])c([H])c(O[H])c(O[H])c1[H].O.N=C(O)c1ccc[n+](C2OC(COP(=O)(O)OP(=O)(O)OCC3OC(n4cnc5c(N)ncnc54)C(OP(=O)(O)O)C3O)C(O)C2O)c1",

infos={
    'transfo_id': "TRS_0_3_65",
    'rule_id': "RR-02-b64ad57dc9b584cb-16-F",
    'rule_score': 1.0,
    'tmpl_rxn_id': "MNXR113924",
}
        # fba_fraction=1.3648925522849815,
        # thermo={
        #     "dG0_prime": {
        #         "value": -112.97007627560498,
        #         "error": 7.376345269431926,
        #         "units": "kilojoule / mole"
        #     },
        #     "dGm_prime": {
        #         "value": -130.08491381032601,
        #         "error": 7.376345269431926,
        #         "units": "kilojoule / mole"
        #     },
        #     "dG_prime": {
        #         "value": -112.97007627560498,
        #         "error": 7.376345269431926,
        #         "units": "kilojoule / mole"
        #     }
        # },
        # # smiles="[H]OC(=O)C(OC1([H])C([H])=C(C(=O)O[H])C([H])=C([H])C1([H])O[H])=C([H])[H]>>[H]OC(=O)c1c([H])c([H])c([H])c(O[H])c1[H].CC(=O)C(=O)O",

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
reactants = {
    "CMPD_0000000003": 1,
    "MNXM4": 1
}
products = {
    "TARGET_0000000001": 1,
    "MNXM1": 2
}
rxn_4 = Reaction(
    id="rxn_4",
    ec_numbers=[
        "1.13.11.1"
    ],
    reactants=reactants,
    products=products
)
reactions = [
    rxn_4,
    Reaction(
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
    Reaction(
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
    Reaction(
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
]

class Test_Object(TestCase):

    def test_to_string(self):
        id = 'obj_id'
        self.assertEqual(
            Object(id).to_string(),
            f'Object({id})'
        )

    def test_eq(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, infos)
        self.assertEqual(
            obj,
            Object(
                id=id,
                infos={
                    info_id: infos
                }
            )
        )

    def test_eq_diff(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, infos)
        self.assertNotEqual(
            obj,
            Object(
                id=id,
                infos=infos
            )
        )

    def test_eq_diff_type(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, infos)
        self.assertNotEqual(
            obj,
            0
        )

    def test_get_infos(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, infos)
        self.assertDictEqual(
            obj.get_infos(),
            {info_id: infos}
        )

    def test_get_info(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, infos)
        self.assertDictEqual(
            obj.get_info(info_id),
            infos
        )

    def test_get_info_wrong_key(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, infos)
        self.assertEqual(
            obj.get_info('WRONG'),
            None
        )

    def test_set_id(self):
        id = 'obj_id'
        new_id = 'new_'+id
        obj = Object(id)
        obj.set_id(new_id)
        self.assertEqual(
            obj.get_id(),
            'new_'+id
        )



class Test_Compound(TestCase):

    def test_str(self):
        self.assertEqual(
            species['TARGET_0000000001'].__str__(),
            'Compound(TARGET_0000000001)'
        )

    def test_eq_wrong_type(self):
        self.assertNotEqual(
            species['TARGET_0000000001'],
            0
        )


class Test_Reaction(TestCase):

    def test_str(self):
        name = 'Test'
        rxn = Reaction(name)
        self.assertEqual(
            rxn.__str__(),
            f'Reaction {name}'
        )

    def test_eq_wrong_type(self):
        self.assertNotEqual(
            reactions[0],
            0
        )

    def test_get_reactants_ids(self):
        self.assertListEqual(
            reactions[0].get_reactants_ids(),
            ['CMPD_0000000003', 'MNXM4']
        )

    def test_get_products_ids(self):
        self.assertListEqual(
            reactions[0].get_products_ids(),
            ['TARGET_0000000001', 'MNXM1']
        )

    def test_get_reactants(self):
        self.assertListEqual(
            reactions[0].get_reactants(),
            [species[spe_id] for spe_id in reactants.keys()]
        )

    def test_get_smiles(self):
        self.assertEqual(
            reactions[0].get_smiles(),
            '[H]Oc1c([H])c([H])c([H])c([H])c1O[H].O=O>>[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H].[H+].[H+]'
        )

    # def test_get_reactants_ids_wo_cache(self):
    #     self.assertListEqual(
    #         reactions[0].get_reactants_ids(),
    #         [None, None]
    #     )

    def test_get_products(self):
        self.assertListEqual(
            reactions[0].get_products(),
            [species[spe_id] for spe_id in products.keys()]
        )

    def test_get_species(self):
        self.assertListEqual(
            sorted([spe.get_id() for spe in reactions[0].get_species()]),
            sorted(list(set(list(reactants.keys()) + list(products.keys()))))
        )

    # def test_get_products_ids_wo_cache(self):
    #     self.assertListEqual(
    #         reactions[0].get_products_ids(),
    #         [None, None]
    #     )
    
    def test_get_left(self):
        self.assertDictEqual(
            reactions[0].get_left(),
            {
                'CMPD_0000000003': 1,
                'MNXM4': 1
            }
        )

    def test_get_right(self):
        self.assertDictEqual(
            reactions[0].get_right(),
            {
                'TARGET_0000000001': 1,
                'MNXM1': 2
            }
        )

    def test_add_info(self):
        rxn = Reaction('rxn_test')
        rxn.add_info(
            key='test_key',
            value='test_value'
        )
        self.assertDictEqual(
            rxn.get_infos(),
            {'test_key': 'test_value'}
        )

    def test_add_ec_number(self):
        ec_numbers = ['1.1']
        rxn = Reaction(
            id='rxn_test',
            ec_numbers=ec_numbers
        )
        ec_number = '1.2'
        rxn.add_ec_number(ec_number)
        self.assertListEqual(
            rxn.get_ec_numbers(),
            ec_numbers + [ec_number]
        )
    
    def test_add_reactant(self):
        spe_id = 'CMPD_0000000010'
        _species = deepcopy(reactions[0].get_reactants_stoichio())
        spe_sto = 3
        for spe_sto in [3, -3]:
            with self.subTest(spe_sto=spe_sto):
                rxn = deepcopy(reactions[0])
                rxn.add_reactant(
                    compound_id=spe_id,
                    compound=species[spe_id],
                    stoichio=spe_sto
                )
                self.assertDictEqual(
                    rxn.get_reactants_stoichio(),
                    {**_species, **{spe_id: abs(spe_sto)}}
                )

    def test_add_reactant_wo_id(self):
        cmpd_sto = 4
        rxn = deepcopy(rxn_4)
        rxn.add_reactant(stoichio=cmpd_sto, compound_id='')
        self.assertListEqual(
            rxn.get_reactants(),
            rxn_4.get_reactants()
        )

    def test_add_reactant_with_id_none(self):
        cmpd_sto = 4
        rxn = deepcopy(rxn_4)
        rxn.add_reactant(stoichio=cmpd_sto, compound=species['TARGET_0000000001'])
        self.assertListEqual(
            rxn.get_reactants_ids(),
            rxn_4.get_reactants_ids() + ['TARGET_0000000001']
        )

    def test_add_reactant_withall_none(self):
        cmpd_sto = 4
        rxn = deepcopy(rxn_4)
        rxn.add_reactant(stoichio=cmpd_sto, compound_id=None, compound=None)
        self.assertListEqual(
            rxn.get_reactants(),
            rxn_4.get_reactants()
        )

    def test_add_product(self):
        spe_id = 'CMPD_0000000010'
        _species = deepcopy(reactions[0].get_products_stoichio())
        spe_sto = 3
        for spe_sto in [3, -3]:
            with self.subTest(spe_sto=spe_sto):
                rxn = deepcopy(reactions[0])
                rxn.add_product(
                    compound_id=spe_id,
                    compound=species[spe_id],
                    stoichio=spe_sto
                )
                self.assertDictEqual(
                    rxn.get_products_stoichio(),
                    {**_species, **{spe_id: abs(spe_sto)}}
                )


class Test_Pathway(TestCase):

    id = 'test_pathway'
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
    # sink = [
    #     "MNXM337",
    #     "MNXM2",
    #     "MNXM4",
    #     "MNXM1",
    #     "MNXM6"
    # ]
    # fba = {
    #     "value": 0.57290585662576,
    #     "units": ''
    # }
    # thermo = {
    #     "dG0_prime": {
    #         "value": -884.6296371353768,
    #         "error": 9.819227446307337,
    #         "units": "kilojoule / mole"
    #     },
    #     "dGm_prime": {
    #         "value": -884.6296371353768,
    #         "error": 9.819227446307337,
    #         "units": "kilojoule / mole"
    #     },
    #     "dG_prime": {
    #         "value": -884.6296371353768,
    #         "error": 9.819227446307337,
    #         "units": "kilojoule / mole"
    #     }
    # }
    compartments = {
        "MNXC3": {
            "name": "",
            "annot": ""
        }
    }
    parameters = {
        "upper_flux_bound": {
            "value": 999999.0,
            "units": "mmol_per_gDW_per_hr"
        },
        "lower_flux_bound": {
            "value": 0.0,
            "units": "mmol_per_gDW_per_hr"
        }
    }
    units_def = {
        "mmol_per_gDW_per_hr": [
            {
                "kind": 23,
                "exponent": 1,
                "scale": -3,
                "multiplier": 1.0
            },
            {
                "kind": 8,
                "exponent": 1,
                "scale": 0,
                "multiplier": 1.0
            },
            {
                "kind": 28,
                "exponent": 1,
                "scale": 0,
                "multiplier": 3600.0
            }
        ],
        "kj_per_mol": [
            {
                "kind": 13,
                "exponent": 1,
                "scale": 3,
                "multiplier": 1.0
            },
            {
                "kind": 23,
                "exponent": -1,
                "scale": 1,
                "multiplier": 1.0
            }
        ]
    }
    infos = {
        'rpSBML': {
            'compartments': compartments,
            'parameters': parameters,
            'units_def': units_def
        }
}


    def setUp(self):
        self.test_pathway = Pathway(
            id=self.id,
            # species=species.values(),
            # reactions=reactions,
        )
        # rpSBML = {
        #     'compartments': self.compartments,
        #     'parameters': self.parameters,
        #     'units_def': self.units_def,
        # }
        # self.test_pathway.add_info('rpSBML', rpSBML)
        # self.test_pathway.add_info('fba', self.fba)
        # self.test_pathway.add_info('thermo', self.thermo)
        # self.test_pathway.add_info('sink', self.sink)
        # rxn = reactions[0]
        # self.test_pathway.add_reaction(
        #     reaction=rxn,
        #     target=True,
        #     target_id='TARGET_0000000001'
        # )
        for rxn in reactions:
            self.test_pathway.add_reaction(rxn)
        self.test_pathway.set_infos(self.infos)

    ## READ METHODS
    def test_get_info(self):
        self.assertDictEqual(
            self.test_pathway.get_info('rpSBML'),
            self.infos['rpSBML']
        )

    def test_get_info_wrong_key(self):
        self.assertEqual(
            self.test_pathway.get_info('WRONG'),
            None
        )

    def test_rename_compound(self):
        old_id = reactions[0].get_reactants_ids()[0]
        new_id = 'NEW_CMPD_ID'
        self.test_pathway.rename_compound(reactions[0].get_reactants_ids()[0], new_id)
        self.assertEqual(
            self.test_pathway.get_reaction(reactions[0].get_id()).get_reactants_ids()[0],
            new_id
        )
        self.test_pathway.rename_compound(new_id, old_id)

    def test_get_id(self):
        self.assertEqual(
            self.test_pathway.get_id(),
            self.id
        )

    def test_get_nb_reactions(self):
        self.assertEqual(
            self.test_pathway.get_nb_reactions(),
            len(reactions)
        )

    def test_get_nb_species(self):
        self.assertEqual(
            self.test_pathway.get_nb_species(),
            len(species)
        )

    def test_get_species(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in reactions]
        l = list(set([spe for species in list_of_list_of_species for spe in species]))
        self.assertListEqual(
            self.test_pathway.get_species(),
            [self.test_pathway.get_specie(spe_id) for spe_id in l]
        )

    def test_get_species_ids(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in reactions]
        self.assertListEqual(
            self.test_pathway.get_species_ids(),
            list(set([spe for species in list_of_list_of_species for spe in species]))
        )

    def test_get_species_from_id(self):
        self.assertEqual(
            self.test_pathway.get_specie('MNXM23'),
            species['MNXM23']
        )

    def test_get_species_from_id_wrong_key(self):
        self.assertEqual(
            self.test_pathway.get_specie('WRONG_KEY'),
            None
        )

    def test_get_compounds_ids(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in reactions]
        self.assertListEqual(
            self.test_pathway.get_compounds_ids(),
            list(set([spe for species in list_of_list_of_species for spe in species]))
        )

    def test_get_compounds(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in reactions]
        l = list(set([spe for species in list_of_list_of_species for spe in species]))
        self.assertListEqual(
            self.test_pathway.get_compounds(),
            [self.test_pathway.get_specie(spe_id) for spe_id in l]
        )

    def test_get_compound(self):
        self.assertEqual(
            self.test_pathway.get_compound('MNXM23'),
            species['MNXM23']
        )

    def test_get_reactions(self):
        self.assertListEqual(
            self.test_pathway.get_reactions(),
            reactions
        )

    def test_get_reaction(self):
        self.assertEqual(
            self.test_pathway.get_reaction('rxn_4'),
            reactions[0]
        )

    def test_get_reaction_wrong_id(self):
        self.assertEqual(
            self.test_pathway.get_reaction('WRONG_ID'),
            None
        )

    def test_reaction_ids(self):
        self.assertEqual(
            self.test_pathway.get_reactions_ids(),
            [rxn.get_id() for rxn in reactions]
        )

    # def test_get_rxn_target_id(self):
    #     self.assertEqual(
    #         self.test_pathway.get_rxn_target_id(),
    #         reactions[0].get_id()
    #     )

    # def test_get_rxn_target(self):
    #     self.assertEqual(
    #         self.test_pathway.get_target(),
    #         species['TARGET_0000000001']
    #     )

    # def test_get_target(self):
    #     self.assertEqual(
    #         self.test_pathway.get_rxn_target(),
    #         reactions[0]
    #     )

    # def test_get_target_id(self):
    #     self.assertEqual(
    #         self.test_pathway.get_target_id(),
    #         'TARGET_0000000001'
    #     )

    # def test_get_reaction_scores(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_reaction_scores('rxn_4'),
    #         reactions['rxn_4']['scores']
    #     )

    # def test_get_reaction_rule_score(self):
    #     self.assertEqual(
    #         self.test_pathway.get_reaction_rule_score('rxn_4'),
    #         reactions['rxn_4']['scores']['rule']
    #     )

    # def test_get_reaction_fba_score(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_reaction_fba_score('rxn_4'),
    #         reactions['rxn_4']['scores']['fba']
    #     )

    # def test_get_reaction_thermo_scores(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_reaction_thermo_scores('rxn_4'),
    #         reactions['rxn_4']['scores']['thermo']
    #     )

    # def test_get_pathway(self):
    #     self.assertListEqual(
    #         self.test_pathway.get_pathway(),
    #         self.pathway
    #     )

    # def test_get_sink(self):
    #     self.assertListEqual(
    #         self.test_pathway.get_sink(),
    #         self.sink
    #     )

    # def test_get_fba(self):
    #     self.assertEqual(
    #         self.test_pathway.get_fba(),
    #         self.fba
    #     )

    # def test_get_thermo(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_thermo(),
    #         self.thermo
    #     )

    # def test_get_compartments(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_compartments(),
    #         self.compartments
    #     )

    # def test_get_compartment(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_compartment('MNXC3'),
    #         self.compartments['MNXC3']
    #     )

    # def test_get_compartment_wrong_id(self):
    #     self.assertEqual(
    #         self.test_pathway.get_compartment('WRONG_ID'),
    #         None
    #     )

    # def test_get_parameters(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_parameters(),
    #         self.parameters
    #     )

    # def test_get_parameter(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_parameter('upper_flux_bound'),
    #         self.parameters['upper_flux_bound']
    #     )

    # def test_get_parameter_wrong_ID(self):
    #     self.assertEqual(
    #         self.test_pathway.get_parameter('WRONG_ID'),
    #         None
    #     )

    # def test_get_units_def(self):
    #     self.assertDictEqual(
    #         self.test_pathway.get_units_def(),
    #         self.units_def
    #     )

    # def test_get_units_def_id(self):
    #     id = 'mmol_per_gDW_per_hr'
    #     self.assertListEqual(
    #         self.test_pathway.get_units_def(id),
    #         self.units_def[id]
    #     )

    # def test_get_units_def_wrong_id(self):
    #     id = 'WRONG_ID'
    #     self.assertEqual(
    #         self.test_pathway.get_units_def(id),
    #         None
    #     )

    # def test_set_id(self):
    #     name = 'test test_pathway'
    #     self.test_pathway.set_id(name)
    #     self.assertEqual(
    #         self.test_pathway.get_id(),
    #         name
    #     )

    # def test_set_species_ids_1(self):
    #     species = ['TEST_CMPD_1', 'TEST_CMPD_2']
    #     self.test_pathway.set_species(species)
    #     self.assertListEqual(
    #         self.test_pathway.get_list_of_species_ids(),
    #         species
    #     )

    # def test_set_compounds(self):
    #     species = ['TEST_CMPD_1', 'TEST_CMPD_2']
    #     self.test_pathway.set_compounds(species)
    #     self.assertListEqual(
    #         self.test_pathway.get_list_of_species_ids(),
    #         species
    #     )

    # def test_set_species_1(self):
    #     species = [Compound('TEST_CMPD_1'), Compound('TEST_CMPD_2')]
    #     self.test_pathway.set_species(species)
    #     self.assertListEqual(
    #         self.test_pathway.get_species(),
    #         species
    #     )

    # def test_set_species_ids_2(self):
    #     compound = Compound('TEST_CMPD_2')
    #     species = ['TEST_CMPD_1', compound]
    #     self.test_pathway.set_species(species)
    #     self.assertListEqual(
    #         self.test_pathway.get_list_of_species_ids(),
    #         [species[0]] + [compound.get_id()]
    #     )

    def test_add_reaction(self):
        rxn = Reaction(id='rxn')
        self.test_pathway.add_reaction(rxn)
        self.assertListEqual(
            self.test_pathway.get_reactions(),
            reactions + [rxn]
        )
    
    # def test_add_species_id(self):
    #     name = 'TEST_1'
    #     self.assertFalse(name in self.test_pathway.get_list_of_species_ids())
    #     self.test_pathway.add_species(name)
    #     self.assertTrue(name in self.test_pathway.get_list_of_species_ids())

    # def test_add_species(self):
    #     compound = Compound('TEST_1')
    #     self.assertFalse(compound.get_id() in self.test_pathway.get_list_of_species_ids())
    #     self.test_pathway.add_species(compound)
    #     self.assertTrue(compound.get_id() in self.test_pathway.get_list_of_species_ids())

    # def test_add_compound(self):
    #     name = 'TEST_1'
    #     self.assertFalse(name in self.test_pathway.get_list_of_species_ids())
    #     self.test_pathway.add_compound(name)
    #     self.assertTrue(name in self.test_pathway.get_list_of_species_ids())

    # def test_add_species_wo_replace(self):
    #     compound = Compound(id='TARGET_0000000001', smiles='TEST')
    #     self.assertEqual(
    #         self.test_pathway.get_compound('TARGET_0000000001').get_smiles(),
    #         '[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H]'
    #     )
    #     self.test_pathway.add_species(compound)
    #     self.assertEqual(
    #         self.test_pathway.get_compound('TARGET_0000000001').get_smiles(),
    #         '[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H]'
    #     )

    # def test_add_species_w_replace(self):
    #     # # Add a species
    #     # self.test_pathway.add_species(species=species['TARGET_0000000001'])
    #     # Add a different species with the same name
    #     # w/o replacing the one already present in the cache
    #     compound = Compound(id='TARGET_0000000001', smiles='TEST')
    #     # self.test_pathway.add_species(species=compound)
    #     self.assertEqual(
    #         self.test_pathway.get_compound('TARGET_0000000001').get_smiles(),
    #         '[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H]'
    #     )
    #     # Add it and replacing the one already present
    #     self.test_pathway.add_species(species=compound, replace=True)
    #     self.assertEqual(
    #         self.test_pathway.get_compound('TARGET_0000000001').get_smiles(),
    #         'TEST'
    #     )
    #     # Put back the original compound in the cache
    #     self.test_pathway.add_species(species=species['TARGET_0000000001'], replace=True)

    # def test_get_smiles(self):
    #     self.assertEqual(
    #         self.test_pathway.get_list_of_reactions()[0].get_smiles(),
    #         '[H]Oc1c([H])c([H])c([H])c([H])c1O[H].O=O>>[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H].[H+].[H+]'
    #     )

    # def test_add_compartment(self):
    #     name = 'MNXC4'
    #     compartment = {
    #         "name": name,
    #         "annot": name
    #     }
    #     self.test_pathway.add_compartment(name, compartment)
    #     self.assertDictEqual(
    #         self.test_pathway.get_compartment(name),
    #         compartment
    #     )

    # def test_add_parameter(self):
    #     name = 'new_param'
    #     param = {
    #         "value": 999999.0,
    #         "units": "mmol_per_gDW_per_hr"
    #     }
    #     self.test_pathway.add_parameter(name, param)
    #     # print(self.test_pathway.get_parameter(name))
    #     self.assertDictEqual(
    #         self.test_pathway.get_parameter(name),
    #         param
    #     )

    # def test_add_units_def(self):
    #     name = 'mmol_per_gDW_per_hr'
    #     units_def = {
    #         "kind": 23,
    #         "exponent": 1,
    #         "scale": -3,
    #         "multiplier": 1.0
    #     }
    #     self.test_pathway.add_units_def(name, units_def)
    #     self.assertDictEqual(
    #         self.test_pathway.get_units_def(name),
    #         units_def
    #     )

    def test_to_dict(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in reactions]
        l = list(set([spe for species in list_of_list_of_species for spe in species]))
        self.assertDictEqual(
            self.test_pathway.to_dict(),
            {
                'reactions': {rxn.get_id():rxn.to_dict() for rxn in reactions},
                'species': {spe.get_id():spe.to_dict() for spe in [species[spe_id] for spe_id in l]},
                'infos': self.infos
            }
        )
    
    def test_to_string(self):
        self.assertEqual(
            self.test_pathway.to_string(),
            '----------------\n' \
          + f'Pathway {self.test_pathway.get_id()}\n' \
          + '----------------\n' \
          + 'Reaction rxn_4: 1 CMPD_0000000003 + 1 MNXM4 = 1 TARGET_0000000001 + 2 MNXM1\nReaction rxn_3: 1 CMPD_0000000010 + 1 MNXM1 = 1 CMPD_0000000003 + 1 MNXM13\nReaction rxn_2: 1 CMPD_0000000025 + 1 MNXM4 + 1 MNXM6 + 1 MNXM1 = 1 CMPD_0000000010 + 1 MNXM2 + 1 MNXM5\nReaction rxn_1: 1 MNXM337 = 1 CMPD_0000000025 + 1 MNXM23'
        )

    def test_eq(self):
        pathway = Pathway(
            id=self.id,
            # species=species.values(),
            # reactions=reactions,
            # pathway=self.pathway,
            # sink=self.sink,
            # fba=self.fba,
            # thermo=self.thermo,
            # compartments=self.compartments,
            # parameters=self.parameters,
            # units_def=self.units_def
        )
        for rxn in reactions:
            pathway.add_reaction(rxn)
        pathway.set_infos(self.infos)
        # for spe in species:
        #     pathway.add_species(spe)
        self.assertEqual(
            self.test_pathway,
            pathway
        )

    def test_del_reaction(self):
        self.test_pathway.del_reaction(rxn_4.get_id())
        self.assertListEqual(
            self.test_pathway.get_reactions_ids(),
            [rxn.get_id() for rxn in reactions[1:]]
        )

    def test_del_reaction_wrong_id(self):
        self.test_pathway.del_reaction('WRONG')
        self.assertListEqual(
            self.test_pathway.get_reactions_ids(),
            [rxn.get_id() for rxn in reactions]
        )

    def test_add_info(self):
        info_id = 'test'
        info = {'a': 1}
        self.test_pathway.add_info(info_id, info)
        self.assertDictEqual(
            self.test_pathway.get_info(info_id),
            info
        )

    def test_eq_not_equal(self):
        self.assertNotEqual(
            self.test_pathway,
            Pathway(
                id=self.id,
                # species=[],
                # reactions=reactions,
                # pathway=self.pathway,
                # sink=self.sink,
                # fba=self.fba,
                # thermo=self.thermo,
                # compartments=self.compartments,
                # parameters=self.parameters,
                # units_def=self.units_def
            )
        )

    def test_eq_wrong_type(self):
        self.assertNotEqual(
            self.test_pathway,
            0
        )

    def test_net_reaction(self):
        self.assertEqual(
            Pathway.net_reaction(self.test_pathway.get_reactions()).get_species_stoichio(),
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


    # def test_add_rxn_in_pathway_2(self):
    #     rxn_id = 'rxn_test'
    #     self.assertListEqual(
    #         self.test_pathway.add_rxn_in_pathway(rxn_id, 0),
    #         [rxn_id] + self.pathway
    #     )

    # def test_add_rxn_in_pathway_3(self):
    #     rxn_id = 'rxn_test'
    #     self.assertListEqual(
    #         self.test_pathway.add_rxn_in_pathway(rxn_id, 10),
    #         self.pathway + [rxn_id]
    #     )

    # def test_add_rxn_in_pathway_4(self):
    #     rxn_id = 'rxn_test'
    #     self.assertListEqual(
    #         self.test_pathway.add_rxn_in_pathway(rxn_id, -1),
    #         self.pathway[:-1] + [rxn_id] + self.pathway[-1:]
    #     )