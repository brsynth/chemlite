# Release history

## 2.5.0
#### Jun 25 2021
- chore(Object): remove 'id' attribute for objects comparison
- doc: add documentation material (produced by sphinx)

## 2.4.1
#### Jun 24 2021
- chore(Pathway): get_reactants/products_ids() returns a sorted list

## 2.4.0
#### Jun 24 2021
- feat(Pathway): add get_reactants_ids()
- feat(Pathway): add get_products_ids()
- chore: rename to_dict() methods
- doc: add methods documentation

## 2.2.0
#### Jun 17 2021
- feat(Pathway): add get_list_of_reactions()

## 2.2.0
#### Jun 17 2021
- chore(Pathway): change __reactions from List to Dict
- chore(Reaction): check get_nb_X()

## 2.1.1
#### Jun 17 2021
- chore(Reaction): do not touch()

## 2.1.0
#### Jun 17 2021
- chore(Reaction): fix smiles checking
- BREAK! chore(Pathway): change net_reaction() return

## 2.0.0
#### Jun 17 2021
- chore(Reaction): split __stoichio into __reactants and __products
- BREAK! chore(Reaction): rename get_reactants_stoichio() into get_reactants()
- BREAK! chore(Reaction): rename get_products_stoichio() into get_products()
- BREAK! chore(Reaction): rename get_species_stoichio() into get_species()
- BREAK! chore(Reaction): rename get_reactants() into get_reactants_compounds()
- BREAK! chore(Reaction): rename get_products() into get_products_compounds()
- BREAK! chore(Reaction): rename get_species() into get_speciess_compounds()

## 1.3.1
#### Jun 15 2021
- chore(Reaction): check harder compound smiles

## 1.3.0
#### Jun 15 2021
- chore: remove infos attribute
- fix(Reaction): check compound smiles before return it

## 1.2.1
#### Jun 15 2021
- chore(Reaction): __to_dict() returns stoichio for both reactants and products

## 1.2.0
#### Jun 14 2021
- feat(Reaction): add mult_stoichio_coeff() method

## 1.1.3
#### Jun 14 2021
- chore(Reaction): replace __reactants and __products by __species (transparent for the user)
- chore(Reaction): returns sorted dictionary for get_ methods

## 1.1.2
#### Jun 11 2021
- chore(Object): check id in set_id() so that get_id() always returns a value

## 1.1.1
#### Jun 10 2021
- chore(Pathway): change __eq__ method

## 1.1.0
#### Jun 10 2021
- chore(Pathway): net_reaction not static
- chore(Pathway): (rename_compound) do not rm compound from Cache when renamed
- chore(Pathway): inherit Pathway from Object
- chore(Reaction): sort (lexicography) compounds in get_smiles()
- chore: rename to_dict() into _to_dict()

## 1.0.1
#### Jun 9 2021
- chore(Reaction): add infos to __init__

## 1.0.0
#### Jun 8 2021
- first commit
