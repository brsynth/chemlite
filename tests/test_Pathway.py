"""
Created on May 28 2021

@author: Joan Hérisson
"""

from unittest import TestCase
from chemlite import (
    Pathway,
    Reaction,
    Compound,
)
from copy import deepcopy


class Test_Pathway(TestCase):

    def setUp(self):
        self.species = {
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
            id=self.id,
            # species=species.values(),
            # reactions=reactions,
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
        self.pathway.replace_reaction(
            self.rxn.get_id(),
            rxn
        )
        self.assertNotEqual(
            self.pathway.get_reaction(self.rxn.get_id()),
            _rxn
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
        self.assertEqual(
            self.pathway.get_nb_species(),
            len(self.species)
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
        from brs_utils import Cache
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

    def test_to_dict(self):
        list_of_list_of_species = [rxn.get_species_ids() for rxn in self.reactions.values()]
        list_of_species = list(set([spe for species in list_of_list_of_species for spe in species]))
        self.assertDictEqual(
            self.pathway._to_dict(),
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
        pathway = Pathway(id=self.id)
        for rxn in self.reactions.values():
            pathway.add_reaction(rxn)
        # for spe in species:
        #     pathway.add_species(spe)
        self.assertEqual(
            self.pathway,
            pathway
        )

    def test_del_reaction(self):
        self.pathway.del_reaction(self.rxn.get_id())
        self.assertListEqual(
            self.pathway.get_reactions_ids(),
            [rxn.get_id() for rxn in list(self.reactions.values())[1:]]
        )

    def test_del_reaction_wrong_id(self):
        self.pathway.del_reaction('WRONG')
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
