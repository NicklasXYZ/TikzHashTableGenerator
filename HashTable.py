#------------------------------------------------------------------------------#
#                     Author     : Nicklas Sindlev Andersen                    #
#------------------------------------------------------------------------------#
#
#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
from collections import OrderedDict


#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
class HashTable:
    """ A simple hashtable class, that is used to generate all the events that 
    are associated with searching or inserting keys into a hashtable with open 
    adressing using linear probing, quadratic probing or double hashing.
    
    All the generated events are then used to generate a set of illustrations,
    which can be imported into a LaTeX beamer presentation.
    """

    def __init__(self, size, hash_function):
        """
        """
        self.size = size
        self.hash_function = hash_function
        self.keys = [""] * self.size
        self.history = OrderedDict()
        self.collisions = OrderedDict()
        self.event_counter = 0

    def bulk_insert(self, keys):
        """ Insert the keys in the given list into the hash table
        """
        for k in keys:
            self.insert(k)

    def collision_resolution(self, k):
        """ Resolve possible collisions with keys that are
        already present in the hash table
        """
        i = 0
        index = self.hash_function(k, i)
        while self.keys[index] != "":
            if self.keys.count("") > 0:
                i += 1
                index = self.hash_function(k, i)
            else:
                index = ""
                break
        return index, k, i

    def insert(self, k):
        """
        """
        index, k, i = self.collision_resolution(k)
        if index != "":
            self.keys[index] = k
            # Register the attempt to insert the key k
            self.register_insertion_event(index, k, i)
        else:
            raise ValueError(
            "The key k = " + str(k) + " could not be inserted into the hash table!"
        )

    def register_insertion_event(self, index, k, i):
        """
        """
        indices = []; increments = []; status = []
        # Recalculate indices where collisions occurred
        if i >= 1:
            for j in range(0, i):
                new_index = self.hash_function(k, j)
                indices.append(new_index)
                increments.append(j)
                status.append("collision")
        # Finally, as the last thing we manage to find a free spot and insert the key
        # This is the case, as we only allow attempts to insert keys into the hash table
        # as long as there is actually space.
        new_index = self.hash_function(k, i)
        indices.append(new_index)
        increments.append(i)
        status.append("insertion")
        # Recalculate all other values for each collision, such that we can generate a
        # separate illustration for each collision and insertion
        for t in range(1, i + 2):
            temp_keys = self.keys.copy()
            if i >= 1 and t != i + 1:
                temp_keys[indices[-1]] = ""
            # Save the details at a new index in the ordered dictionary
            self.event_counter += 1
            self.history[self.event_counter] = {
                # The key to be inserted
                "k": k,
                # Create a copy of the current state of the hash table
                "hashtable": temp_keys,
                # Collect occupied indices, i.e., the indices where there were collisions
                "indices": indices[0:t],
                "increments": increments[0:t],
                "status": status[0:t],
            }

#------------------------------------------------------------------------------#
if __name__ == "__main__":
    """
    Script entry point...
    Create a few examples...
    """
    # Choose: "linear_probing", "quadratic_probing" or "double_hashing"
    run = "linear_probing"
    if run == "linear_probing":
        ######################################
        #### Example 1: Linear probing    ####
        ######################################
        # Specify the size of the hash table
        size = 11
        # Define a list of keys to be inserted into the hash table
        values = [67, 20, 17, 33, 16, 2, 15, 18, 26]
        # Specify the complete hash function 
        hash_function = lambda k, i: (((7 * k  + 4) % size) + i) % size 
        # Create the hash table and supply the hash function as an argument
        hashtable = HashTable(size = size, hash_function = hash_function)
        # Insert all the keys
        hashtable.bulk_insert(values)
        # Print out the final hash table along with the history of collisions/insertions
        print("\nFinal hash table: ", hashtable.keys)
        print()
        for step in hashtable.history:
            print("Step: ", step, "Event history  : ", hashtable.history[step])
        print()
    elif run == "quadratic_probing":
        ######################################
        #### Example 2: Quadratic probing ####
        ######################################
        # Specify the size of the hash table
        size = 11
        # Define a list of keys to be inserted into the hash table
        values = [10, 22, 31, 4, 15, 28, 17, 88, 59]
        # Specify the complete hash function 
        hash_function = lambda k, i: ((k % size) + 1 * i + 3 * i ** 2) % size 
        # Create the hash table and supply the hash function as an argument
        hashtable = HashTable(size = size, hash_function = hash_function)
        # Insert all the keys
        hashtable.bulk_insert(values)
        # Print out the final hash table along with the history of collisions/insertions
        print("\nFinal hash table: ", hashtable.keys)
        print()
        for step in hashtable.history:
            print("Step: ", step, "Event history  : ", hashtable.history[step])
        print()
    elif run == "double_hashing":
        ######################################
        #### Example 3: Doubke hashing    ####
        ######################################
        # Specify the size of the hash table
        size = 11
        # Define a list of keys to be inserted into the hash table
        values = [10, 22, 31, 4, 15, 28, 17, 88, 59]
        # Specify the complete hash function 
        hash_function = lambda k, i: ((k % size) + i * (1 + (k % (size - 1)))) % size 
        # Create the hash table and supply the hash function as an argument
        hashtable = HashTable(size = size, hash_function = hash_function)
        # Insert all the keys
        hashtable.bulk_insert(values)
        # Print out the final hash table along with the history of collisions/insertions
        print("\nFinal hash table: ", hashtable.keys)
        print()
        for step in hashtable.history:
            print("Step: ", step, "Event history  : ", hashtable.history[step])
        print()
