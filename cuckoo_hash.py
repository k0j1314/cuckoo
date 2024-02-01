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
	
		for _ in range(self.CYCLE_THRESHOLD):
			index_1 = self.hash_func(key, 0)

			#print("index_1:", index_1)						for testing

			# if hash(key, 0) is empty, simply add
			if self.tables[0][index_1] == None:
				self.tables[0][index_1] = key
				return True
			else:
				evicted_key = self.tables[0][index_1]		#Hash(key, 0) is not empty, so it gets evicted
				self.tables[0][index_1] = key				#replace the slot at Hash(key, 0) with the new key we inserted
				key = evicted_key							#Set the new key to the evicted key
				index_2 = self.hash_func(key, 1)			#Set index_2 to the hash function of the key for the second table
				#print("index_2: ", index_2)				for testing

				#if hash(key, 1) is empty, simply add
				if self.tables[1][index_2] == None:			
					self.tables[1][index_2] = key
					return True
				else:
					#else pingpong back to the first table and go through loop again
					evicted_key = self.tables[1][index_2]	
					self.tables[1][index_2] = key
					key = evicted_key
		return False										#If exit loop, then we have pingponged over the cycle_threshold without finding an empty slot, thus we return false
			

		pass

	def lookup(self, key: int) -> bool:
		# TODO 
		index_1 = self.hash_func(key, 0)
		index_2 = self.hash_func(key, 1)
		if self.tables[0][index_1] == key:
			return True
		elif self.tables[1][index_2] == key:
			return True
		else:
			return False
		pass
		

	def delete(self, key: int) -> None:
		# TODO 
		index_1 = self.hash_func(key, 0)
		index_2 = self.hash_func(key, 1)

		if self.tables[0][index_1] == key:
			self.tables[0][index_1] = None
		elif self.tables[1][index_2] == key:
			self.tables[1][index_2] = None
		pass

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO 

		#create a new table for the cuckoo hash
		new_tables = [[None] * new_table_size for _ in range(2)]

		#rehash the existing elements from old table to the new table
		for table_id in range(2):
			for slot in self.tables[table_id]:
				if slot:
					for key in slot:
						hash_value = self.hash_func(key, table_id)
						new_table_id = 1 - table_id
						new_tables[new_table_id][hash_value % new_table_size].apend(key)
		
		#update self.tables with new table
		self.tables = new_tables

		pass

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


