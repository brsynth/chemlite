"""
Created on May 28 2021

@author: Joan Hérisson
"""

from unittest import TestCase
from pytest import raises as pytest_raises
from chemlite import Object


class Test_Object(TestCase):

    def setUp(self):
        self.id = "MNXM23"
        self.object = Object(
            id=self.id
        )

    def test___init___empty_id(self):
        with pytest_raises(ValueError):
            Object('').get_id(),

    def test___init___none_id(self):
        with pytest_raises(ValueError):
            Object(None).get_id(),

    def test_to_string(self):
        id = 'obj_id'
        self.assertEqual(
            Object(id).to_string(),
            f'Object {id}'
        )

    def test___str__(self):
        id = 'obj_id'
        self.assertEqual(
            Object(id).__str__(),
            f'Object {id}'
        )

    def test_eq(self):
        id = 'obj_id'
        obj = Object(id)
        self.assertEqual(
            obj,
            Object(id=id)
        )

    def test_eq_diffid(self):
        id = 'obj_id'
        obj = Object(id)
        self.assertNotEqual(
            obj,
            Object(id=id+'diff')
        )

    def test_eq_diff_type(self):
        id = 'obj_id'
        obj = Object(id)
        self.assertNotEqual(
            obj,
            0
        )

    def test_get(self):
        self.assertEqual(
            self.object.get_id(),
            self.id
        )

    def test_set_id(self):
        new_id = 'new_id'
        self.object.set_id(new_id)
        self.assertEqual(
            self.object.get_id(),
            new_id
        )

    def test__to_dict(self):
        self.assertDictEqual(
            self.object._to_dict(),
            {
                'id': self.id
            }
        )
