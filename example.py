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
