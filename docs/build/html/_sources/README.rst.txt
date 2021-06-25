ChemLite is a library that defines compounds, reactions, pathways

Install
^^^^^^^

From Conda
----------

.. code-block:: sh

   [sudo] conda install -c brsynth -c chemlite

Use
^^^

Compound
--------

.. code-block:: python

   from chemlite import Compound

   c = Compound(id='test_cmpd')

The code above creates an empty compound. The following fields can be filled and accessed either at build time or later on:

* smiles
* inchi
* inchikey
* formula
* name
* infos

Reaction
--------

.. code-block:: python

   from chemlite import Reaction

   r = Reaction(id='test_rxn')

The code above creates an empty reaction. The following fields can be filled and accessed either at build time or later on:

* ec_numbers
* reactants
* products
* infos

The following methods are also available:

* ``get_smiles()``
* ``add_reactant()``
* ``add_product()``

Pathway
-------

.. code-block:: python

   from chemlite import Pathway

   p = Pathway(id='test_path')

The code above creates an empty reaction. The following fields can be filled and accessed either at build time or later on:

* id
* species
* reactions

The following methods are also available:

* ``add_compound()``
* ``add_reaction()``
* ``del_reaction()``
* ``Pathway.net_reaction()``

Tests
^^^^^

Please follow instructions below ti run tests:

.. code-block::

   cd tests
   pytest -v

For further tests and development tools, a CI toolkit is provided in ``ci`` folder (see `ci/README.md <ci/README.md>`_\ ).

Acknowledgments
^^^^^^^^^^^^^^^

* Thomas Duigou

Licence
^^^^^^^

chemlite is released under the MIT licence. See the LICENCE file for details.
