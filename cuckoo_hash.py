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
		#testtest
		# if hash(key, 0) is empty, simply add
		next = 1 # the other hash, when curr = 0, next is 1 and vice versa
		index_1 = self.hash_func(key,0)	
		if self.tables[0][index_1] is None:
			self.tables[0][index_1] = key
			return True

		#else we stat ping ponging
		for i in range(self.CYCLE_THRESHOLD):
			if self.tables[0][index_1]is not None: # if hash0 9key of x) is not empty, we replace it and then move the other value into h1
				temp = self.tables[0][index_1]
				self.tables[0][index_1] = key
				index_bump = self.hash_func(temp)
				
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
		
		

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO
		pass



	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


