Orfic Codebase Documentation
---
### Introduction
This document aims to outline the Orfic backend codebase, it's customs, 
modules and other general information useful for any further development on this 
codebase. 
___
### Typing and Naming Customs
All modules and functions should follow snake_case naming customs inline with 
PEP008 python style guides

All variable names within the scope of a function that are local should be lowercase
and spaces between words should be denoted via a `_` 

_i.e_

`new_variable_in function = value`

_is correct_

Name mangling rules should be followed in that private variables should be
denoted with a `_` before the variable name. This should be a single `_`
if the variable is local to a method/function/procedure. If the variable which
you intend to be private needs to be a class attribute then it should be
denoted with a double underscore ( `__` )

_i.e_

    self.__private_class_attribute = value
    _local_attribute = anothervalue

_is correct_

### Modules
____

**The modules and their functions are listed below:**

_**orfic**_ - This module contains all of the venue focused code. It takes
the input from the commandline, checks the intensity of the venues, returns
relevant venues to the main program. It makes most calls to the venue database 
to return venue vectors, venue information and, importantly, it figures out the 
ideal package to return to the user.

_**K2K**_ - This module primarily works with the vectors. It can convert words
into vectors, add vectors, create keyword trees and find vectors similar to a 
given vector. All vectors must be of size 300 to be compatible with this module.
If orfic is the administrator, K2K is the computer that the administrator uses.

### Databases
___
_**ClubDataDB.db**_ - This contains all the venue information. It contains 6 tables
which are linked via the relational model. It is relatively simple and is in 3rd Normal
Form. It contains venue descriptions, age restrictions, entry prices, whether the club 
is considered to be a gay club dress codes, dress ratings, addresses 
(which are coordinates currently for `GeoPy`), venue vectors, which types of venue each 
venue is and the standard music genres played at the venues.

### Modules used
___
`spaCy` - This is our trusty NLP library for loading word vectors and establishing similarity
between them. We can also use it when loading raw data into our database to remove stop words 
from descriptions and generally carry out text parsing and natural language tasks. It also helps
us find similar words to an origin word.

`sqlite3` - Currently our DBMS for our database however, as the project evolves we will certainly 
have to move to a much more heavyweight DBMS for information retrieval, especially as the database
size increases and the relations increase in complexity. 

`numpy` - Used for vector management and adjustment

`pandas` - Used to hold venues which are valid during a session in an easy to manage fashion

`sklearn` - Used for normalising vectors

`scipy` - Used to get euclidean distance between two vectors to find similarity

`pickle` - Used to unpickle `lexemes.pkl`

`argparse` - Used to get commandline arguments given by user

`geopy` - Used to calculate physical distance between coordinates of venues

### Output
___
Currently, the output of the program is to output 3 different packages containing the number of venues 
the user wants to visit. This comes in the format of of 3 pandas dataframes. This can then be formatted 
and processed.

### Other Files
___
`LICENSE.md` - Contains the license information for the codebase

`lexemes.pkl` - Currently holding all the lexemes with the correct .prob values to speed up
the loading of spacy upon startup. We load all vectors from lexemes into a list which acts as 
our vocabulary of words.

`ClubData (dir)` - This contains the raw data that is in the database for backups sake as it was
a massive pain to get in the first place.

###Magic Words in Descriptions
___
Each description may contain a number of magic words, or words which are treated differently by the
algorithm. This is done so that certain features of a venue can be better reflected in the 
description. 

The following contains the words and their usage cases:

`food` - For any venues which serve any form of food

`theme` - For any venues which are themed by culture, style or dress code

`DJ` - For any venues which have a DJ on at least one night

`beer` - For any venues which specialise in beer and craft beer

`brunch` - For any venues which offer a 'boozy brunch' service

`traditional` - For any pubs/bars which are set out in a stereotypical english way

`cocktails` - For any venues which specialise in cocktails

`terrace` - For any venues which contain an outdoor seating area

`live` - For any venues which host live music/theatre events

`wine` - For any venues which keep specialise in fine wines

`sport` - For any venues which promote or show live sport 