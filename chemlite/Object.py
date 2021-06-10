"""A class to represent a basic object."""
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
    TypeVar
)
from logging import (
    Logger,
    getLogger
)
from json import dumps
from copy import deepcopy
from brs_utils import Cache


class Object:

    def __init__(
        self,
        id: str,
        infos: Dict = {},
        logger: Logger = getLogger(__name__)
    ):
        self.__logger = logger
        self.set_id(id)
        self.set_infos(infos)
        Cache.add(self, self.get_id())

    def to_string(self):
        return f'{type(self).__name__}({self.get_id()})'

    def __str__(self):
        return self.to_string()

    def _to_dict(self) -> Dict:
        return {
            'id': self.get_id(),
            'infos': deepcopy(self.get_infos())
        }

    def __eq__(self, other) -> bool:
        if isinstance(self, other.__class__):
            return self._to_dict() == other._to_dict()
        return False

    ## READ METHODS
    def get_id(self) -> str:
        return self.__id

    def get_infos(self) -> Dict:
        return self.__infos

    def get_info(self, key: str) -> TypeVar:
        try:
            return self.get_infos()[key]
        except:
            self.__logger.debug(f'There is no key \'{key}\' in the compound infos')
            return None

    ## WRITE METHODS
    def set_id(self, id: str) -> None:
        try:
            old_id = self.__id
        except AttributeError:
            old_id = id
        self.__id = id
        if id in Cache.get_list_of_objects():
            Cache.rename(old_id, self.get_id())

    def set_infos(self, infos: Dict) -> None:
        self.__infos = deepcopy(infos)
        # Cache.add(self, self.get_id())

    def add_info(self, key: str, value: TypeVar) -> None:
        self.__infos[key] = deepcopy(value)

    def del_info(self, key: str) -> None:
        try:
            del self.__infos[key]
        except KeyError:
            Cache.__logger.warning(f'No such key {key} found in infos, nothing deleted.')

