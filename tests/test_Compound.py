"""
Created on May 28 2021

@author: Joan Hérisson
"""

from unittest import TestCase
from os import path as os_path
from json import load as jsload

from chemlite import Compound

HERE = os_path.dirname(os_path.realpath(__file__))
DATA_PATH = os_path.join(HERE, 'data')

class Test_Compound(TestCase):

    def setUp(self):
        with open(os_path.join(DATA_PATH, 'compounds.json'), 'r') as fp:
            compounds = jsload(fp)
        self.compound_dict = compounds['MNXM23']
        self.compound = Compound(**self.compound_dict)

    def test_from_dict(self):
        self.assertEqual(
            self.compound,
            Compound.from_dict(self.compound_dict)
        )

    def test_to_string(self):
        self.assertEqual(
            self.compound.to_string(),
            f'Compound {self.compound_dict["id"]}'
        )

    def test__to_dict(self):
        self.assertDictEqual(
            self.compound._to_dict(),
            self.compound_dict
        )

    def test_eq(self):
        self.assertEqual(
            self.compound,
            Compound(
                smiles=self.compound_dict['smiles'],
                inchi=self.compound_dict['inchi'],
                inchikey=self.compound_dict['inchikey'],
                id=self.compound_dict['id'],
                formula=self.compound_dict['formula'],
                name=self.compound_dict['name']
            )
        )

    # def test_not_eq_toomuch(self):
    #     self.assertNotEqual(
    #         self.compound,
    #         Compound(
    #             smiles=self.compound_dict['smiles'],
    #             inchi=self.compound_dict['inchi'],
    #             inchikey=self.compound_dict['inchikey'],
    #             id=self.compound_dict['id']
    #         )
    #     )

    def test_not_eq_notenough(self):
        self.assertNotEqual(
            self.compound,
            Compound(
                inchi=self.compound_dict['inchi'],
                inchikey=self.compound_dict['inchikey'],
                id=self.compound_dict['id']
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
                    self.compound_dict[attr]
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
