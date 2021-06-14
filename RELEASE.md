# Release history

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
