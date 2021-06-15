"""
Created on May 28 2021

@author: Joan Hérisson
"""

from unittest import TestCase
from chemlite import Compound


class Test_Compound(TestCase):

    def setUp(self):
        self.id = "MNXM23"
        self.smiles = "CC(=O)C(=O)O]"
        self.inchi = "InChI=1S/C3H4O3/c1-2(4)3(5)6/h1H3,(H,5,6)"
        self.inchikey = "LCTONWCANYUPML-UHFFFAOYSA-N"
        self.name = "target"
        self.formula = "C3H3O3"
        self.compound = Compound(
            id=self.id,
            smiles=self.smiles,
            inchi=self.inchi,
            inchikey=self.inchikey,
            name=self.name,
            formula=self.formula
        )

    def test_to_string(self):
        self.assertEqual(
            self.compound.to_string(),
            f'Compound {self.id}'
        )

    def test_to_dict(self):
        self.assertDictEqual(
            self.compound._to_dict(),
            {
                'name': self.name,
                'smiles': self.smiles,
                'inchi': self.inchi,
                'inchikey': self.inchikey,
                'formula': self.formula,
                'id': self.id
            }
        )

    def test_eq(self):
        self.assertEqual(
            self.compound,
            Compound(
                smiles=self.smiles,
                inchi=self.inchi,
                inchikey=self.inchikey,
                id=self.id,
                formula=self.formula,
                name=self.name
            )
        )

    # def test_not_eq_toomuch(self):
    #     self.assertNotEqual(
    #         self.compound,
    #         Compound(
    #             smiles=self.smiles,
    #             inchi=self.inchi,
    #             inchikey=self.inchikey,
    #             id=self.id
    #         )
    #     )

    def test_not_eq_notenough(self):
        self.assertNotEqual(
            self.compound,
            Compound(
                inchi=self.inchi,
                inchikey=self.inchikey,
                id=self.id
            )
        )

    def test_eq_wrong_type(self):
        self.assertNotEqual(
            self.compound,
            0
        )

    def test_get(self):
        for attr in ['smiles', 'inchi', 'inchikey', 'name', 'formula']:
            with self.subTest(f'test_get_{attr}', attr=attr):
                self.assertEqual(
                    getattr(self.compound, f'get_{attr}')(),
                    getattr(self, f'{attr}')
                )

    def test_set(self):
        new_str = 'new_str'
        for attr in ['smiles', 'inchi', 'inchikey', 'name', 'formula']:
            with self.subTest(f'test_set_{attr}', attr=attr):
                setattr(self.compound, attr, new_str),
                self.assertEqual(
                    getattr(self.compound, attr),
                    new_str
                )
