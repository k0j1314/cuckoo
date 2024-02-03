# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
		# you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py). 
		# this function randomly chooses an index from a given bucket for a given table. this ensures that the random 
		# index chosen by your code and our test script match.
		# 
		# for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
		# you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
		# will displace the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx) + str(table_id)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[List[int]]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.
			

	def insert(self, key: int) -> bool:
		# TODO

		curr_table = 0

		index_bucket = self.hash_func(key, curr_table)

		num_evictions = 0

		while num_evictions <= self.CYCLE_THRESHOLD:
			if self.tables[curr_table][index_bucket] is None:
				self.tables[curr_table][index_bucket] = [key]
				return True
			
			elif len(self.tables[curr_table][index_bucket]) < self.bucket_size:
				self.tables[curr_table][index_bucket].append(key)
				return True
			
			else:
				slot = self.get_rand_idx_from_bucket(index_bucket, curr_table)
				evicted_key = self.tables[curr_table][index_bucket][slot]
				self.tables[curr_table][index_bucket].pop(slot)
				self.tables[curr_table][index_bucket].append(key)
				
				key = evicted_key
				curr_table = 1 - curr_table
				index_bucket = self.hash_func(key, curr_table)
			
				num_evictions += 1

		return False

		pass

	def lookup(self, key: int) -> bool:
		# TODO

		index_1 = self.hash_func(key, 0)
		index_2 = self.hash_func(key, 1)

		if self.tables[0][index_1] is not None:
			if self.tables[0][index_1] == key:
				return True
			for i in range(len(self.tables[0][index_1])):
				if self.tables[0][index_1] == key:
					return True
		
		if self.tables[1][index_2] is not None:
			if self.tables[1][index_2] == key:
				return True
			for i in range(len(self.tables[1][index_2])):
				if self.tables[1][index_2] == key:
					return True

		return False

		pass


		
		

	def delete(self, key: int) -> None:
		# TODO

		# Get the possible bucket that the key could be in for each table
		index_1 = self.hash_func(key, 0)
		index_2 = self.hash_func(key, 1)


		# If both buckets are empty, then don't do anything
		if (self.tables[0][index_1] is None) and (self.tables[1][index_2] is None):
			return

		# Check through the buckets that the key could be in
		for curr_table in range(2):
			index_bucket = self.hash_func(key, curr_table)
			if self.tables[curr_table][index_bucket] is not None:
				for i in range(len(self.tables[curr_table][index_bucket])):
					if self.tables[curr_table][index_bucket][i] == key:
						if len(self.tables[curr_table][index_bucket]) == 1:
							self.tables[curr_table][index_bucket] = None
						else:
							self.tables[curr_table][index_bucket].remove(key)
					return

		 

		pass

	def rehash(self, new_table_size: int) -> None:
		old_tables = self.tables
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO

		self.tables = [[None] * new_table_size for _ in range(2)]

		for table in old_tables:
			for key in table:
				if key is not None:
					self.insert(key)

		pass

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


