
# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO 
		#testtest

		curr = 0

		index_1 = self.hash_func(key, 0)

		if self.tables[curr][index_1] is None:
			self.tables[curr][index_1] = key
			return True
		
		#else we start ping ponging
		for _ in range(self.CYCLE_THRESHOLD):
			
			if self.tables[curr][index_1] is not None:
				#print(f'{key}and  {curr} hash{ index_1}')
				temp = self.tables[curr][index_1] # copy whever is in it atm
				self.tables[curr][index_1] = key # shove x into new position
				index_1= self.hash_func(temp, 1- curr) # new index is x-1's position in the other hash

				curr = 1- curr # flip between 0 and 1 on the hash
				key = temp

			else: # if we end up in a empty slot,, put it in
				self.tables[curr][index_1] = key
				return True
			# after CYCLE-1  loops  we just do one more insert and then return false
			
		temp = self.tables[curr][index_1] # copy whever is in it atm
		self.tables[curr][index_1] = key # shove x into new position
		index_1= self.hash_func(temp, 1- curr) # new index is x-1's position in the other hash	

		return False


	def lookup(self, key: int) -> bool:
		index_1 = self.hash_func(key,0)
		index_2 = self.hash_func(key, 1)
		if self.tables[0][index_1] == key:
			return True
		elif self.tables[1][index_2] == key:
			return True
		else:
			return False
		


	def delete(self, key: int) -> None:
		index_1 = self.hash_func(key,0)
		index_2 = self.hash_func(key, 1)

		if self.tables[0][index_1] == key:
			self.tables[0][index_1] = None
		elif self.tables[1][index_2] == key:
			self.tables[1][index_2] = None
		else:
			{}
		

	def rehash(self, new_table_size: int) -> None:
		old_tables = self.tables # Store original table so we have a basis to rehash
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
        # TODO 

        #Create new table
		self.tables = [[None] * new_table_size for _ in range(2)]

        #Rehash existing elements from old to new table
		for table in old_tables:
			for key in table:
				if key is not None:
					self.insert(key)
					

		


	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define

