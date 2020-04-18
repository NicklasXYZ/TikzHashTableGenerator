# Tikz Hashtable Generator

This repository contains a simple script for generating illustrations of different operations on [hash tables](https://en.wikipedia.org/wiki/Hash_table) that use [open addressing](https://en.wikipedia.org/wiki/Open_addressing) as a collision resolution strategy. At the moment it is only possible to generate illustrations that show:
- Insertion of keys into a hash table, where collisions are resolved through linear probing, quadratic probing or double hashing

Illustrations for searching and deleting keys might be added at a later time.

**Note**: The purpose of the script is to be able to automatically create illustrations of simple constructed examples. In other words, the size of the table is fixed, as it should have a reasonable size to be able to fit into e.g. a LaTeX beamer or A4 document.

## Preview
<center>

![](preview/main.gif)

</center>
# Dependencies

- Python 3
- [jinja2](https://jinja.palletsprojects.com): A templating language for Python
- LaTeX & TikZ: To subsequently be able to compile the illustrations into a .pdf document. For Linux LaTeX distributions, see e.g. [Ubuntu LaTeX packages](https://packages.ubuntu.com/search?keywords=texlive) or [Arch Linux LaTeX packages](https://wiki.archlinux.org/index.php/TeX_Live).

**Note**: The script has only been tested on a Linux system (Manjaro).

# Usage

- First of all clone the repository to some local directory:
```
git clone https://github.com/NicklasXYZ/TikzHashTableGenerator && cd TikzHashTableGenerator
```

- Create and save a Python script inside the `TikzHasTableGenerator`, which contains something along the lines of:

```python
# Contents of the "example.py" file
from HashTableRenderer import HashTableRenderer

######################################
#     Example 1: Linear probing      #
######################################
# Specify the size of the hashtable
size = 11

# Define the list of keys to be inserted into the table
values = [67, 20, 17, 33, 16, 2, 15, 18, 26]

# Specify the complete hash function and thus the probing strategy
hash_function = lambda k, i: (((7 * k  + 4) % size) + i) % size 

# Create the hashtable and supply the hash function as an argument
hashtable = HashTableRenderer(size = size, hash_function = hash_function)

# Insert all the keys
hashtable.bulk_insert(values)

#--- Render the illustrations and compile them into a main.tex document ---#
# 1. Compile all the illustrations into a beamer presentation
hashtable.render(beamer = True, scale = 0.9)    # document class: beamer

# or 2. compile all the illustrations into an article document
# hashtable.render(beamer = False, scale = 0.9)   # document class: article
```

- Lastly, run the script, which was just created above. This should create a directory `output` that contains all the generated TikZ and LaTeX code, which is needed for compiling a .pdf document that contains a sequence of illustrations

As a last note, the files in the `output` directory can be compiled into a .pdf document by running `pdflatex main.tex`.
