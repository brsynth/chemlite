"""
Created on May 28 2021

@author: Joan Hérisson
"""

from typing import (
    TypeVar
)
from unittest import TestCase
from pytest import raises as pytest_raises
from chemlite import Object


class Test_Object(TestCase):

    def setUp(self):
        self.infos = {
            'rp2_transfo_id': "TRS_0_3_65",
            'rule_id': "RR-02-b64ad57dc9b584cb-16-F",
            'rule_score': 1.0,
            'tmpl_rxn_id': "MNXR113924",
        }
        self.id = "MNXM23"
        self.object = Object(
            id=self.id,
            infos=self.infos
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
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, self.infos)
        self.assertEqual(
            obj,
            Object(
                id=id,
                infos={
                    info_id: self.infos
                }
            )
        )

    def test_eq_diff(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, self.infos)
        self.assertNotEqual(
            obj,
            Object(
                id=id,
                infos=self.infos
            )
        )

    def test_eq_diff_type(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, self.infos)
        self.assertNotEqual(
            obj,
            0
        )

    def test_get_infos(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, self.infos)
        self.assertDictEqual(
            obj.get_infos(),
            {info_id: self.infos}
        )

    def test_get(self):
        self.assertEqual(
            self.object.get_id(),
            self.id
        )
        self.assertDictEqual(
            self.object.get_infos(),
            self.infos
        )

    def test_get_info_wrong_key(self):
        id = 'obj_id'
        info_id = 'rpSBML'
        obj = Object(id)
        obj.add_info(info_id, self.infos)
        self.assertEqual(
            obj.get_info('WRONG'),
            None
        )

    def test_set_id(self):
        new_id = 'new_id'
        self.object.set_id(new_id)
        self.assertEqual(
            self.object.get_id(),
            new_id
        )

    def test_set_infos(self):
        new_infos = {'a': 1}
        self.object.set_infos(new_infos)
        self.assertDictEqual(
            self.object.get_infos(),
            new_infos
        )

    def __add_info(self, info_id: str, info: TypeVar):
        self.object.add_info(info_id, info)
        self.assertDictEqual(
            self.object.get_infos(),
            {
                **self.infos,
                **{info_id: info}
            }
        )

    def test_del_info(self):
        info_id = 'new'
        info = {'a': 1}
        self.__add_info(info_id, info)
        self.object.del_info(info_id)
        self.assertDictEqual(
            self.object.get_infos(),
            self.infos
        )

    def test_del_info_wrong_key(self):
        info_id = 'new'
        self.object.del_info(info_id)
        self.assertDictEqual(
            self.object.get_infos(),
            self.infos
        )
