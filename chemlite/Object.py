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
    Union,
    TypeVar
)
from logging import (
    Logger,
    getLogger
)


class Object:

    def __init__(
        self,
        id: str,
        logger: Logger = getLogger(__name__)
    ):
        self.__logger = logger
        self.set_id(id)

    def to_string(self) -> str:
        '''
        Returns a string representation of the object

        Returns
        -------
        string: str
            The string representation of the object
        '''
        return f'{type(self).__name__} {self.get_id()}'

    def __str__(self) -> str:
        '''
        Prints a string representation of the object (called by print())

        Returns
        -------
        string: str
            The string representation of the object
        '''
        return self.to_string()

    def _to_dict(self) -> Dict[str, TypeVar]:
        '''
        Return a dictionary with the attributes of the object

        Returns
        -------
        obj_dict: Dict[str, TypeVar]
            A dictionary with the attributes of the object
        '''
        return self.__to_dict()

    def __to_dict(self) -> Dict:
        '''
        For compatibility with __eq__ method in child classes.
        Same as _to_dict().
        '''
        return {
            'id': self.get_id()
        }

    def __eq__(self, other) -> bool:
        '''
        Return the equality status of two Object objects

        Parameters
        ----------
        other: Object
            Object to compare with

        Returns
        -------
        equal: bool
            Return true if the two objects are equal, False otherwise
        '''
        if isinstance(self, other.__class__):
            return self._to_dict() == other._to_dict()
        return False

    ## READ METHODS
    def get_id(self) -> str:
        '''
        Return the ID of the object

        Returns
        -------
        id: str
            ID of the object
        '''
        return self.__id

    def get_logger(self) -> Logger:
        '''
        Return the object's logger

        Returns
        -------
        logger: Logger
            The object's logger
        '''
        return self.__logger

    ## WRITE METHODS
    def set_id(self, id: str) -> Union[str, None]:
        '''
        Set the object's id

        Parameters
        ----------
        id: str
            The object's id to set
        '''
        if id is None:
            raise ValueError('id argument must be different to None for an Object')
        elif id == '':
            raise ValueError('id argument must not be empty for an Object')
        else:
            self.__id = id
