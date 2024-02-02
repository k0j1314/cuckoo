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

		index_1 = self.hash_func(key, 0)

		# Check to see if the bucket is empty, if so, then add a list with the key in it
		if self.tables[curr_table][index_1] is None:
			self.tables[curr_table][index_1] = [key]
			return True
		
		# Check to see if the bucket is full, if not then append the key onto the list
		if len(self.tables[curr_table][index_1]) < self.bucket_size:
			#print(len(self.tables[curr_table][index_1]))
			print( self.tables)
			self.tables[curr_table][index_1].append(key)
			return True
		
		# else we start ping ponging
		for _ in range(self.CYCLE_THRESHOLD):

			# Check to see if bucket is empty, if so, then add a list with the key in it (second table)
			if self.tables[curr_table][index_1] is None:
				self.tables[curr_table][index_1] = [key]
				return True
			
			# Check to see if the bucket is full, if not then append the key onto the list (second table)
			if len(self.tables[curr_table][index_1]) < self.bucket_size:
				self.tables[curr_table][index_1].append(key)
				return True

			# Goes through the bucket and increments counter if slot in bucket is occupied
			if len(self.tables[curr_table][index_1]) >= self.bucket_size:
				slot = self.get_rand_idx_from_bucket(index_1, curr_table) # Get random slot in bucket to evict
				evicted_key = self.tables[curr_table][index_1][slot] # Set evicted key to the element in the slot
				self.tables[curr_table][index_1].remove(evicted_key) # Remove the evicted key from the bucket
				self.tables[curr_table][index_1].append(key) # Append the key to the bucket
				index_1 = self.hash_func(evicted_key, 1 - curr_table) # Update index for the other table

				curr_table = 1 - curr_table #flip between 0 and 1 on the hash
				key = evicted_key #Update the key

			# if the bucket isn't full, then append the key onto the bucket
			else:
				self.tables[curr_table][index_1].append(key)
				return True
		
		#after CYCLE-1 loops we do one more insert and then return false 
		slot = self.get_rand_idx_from_bucket(index_1, curr_table)
		evicted_key = self.tables[curr_table][index_1][slot]
		self.tables[curr_table][index_1].remove(evicted_key)
		self.tables[curr_table][index_1].append(key)
		index_1 = self.hash_func(evicted_key, 1 - curr_table)

		return False

	def lookup(self, key: int) -> bool:
		# TODO

		index_1 = self.hash_func(key, 0)
		index_2 = self.hash_func(key, 1)

		if self.tables[0][index_1] == None:
			return False
		if self.tables[1][index_2] == None:
			return False
		
		if self.tables[0][index_1] == key:
			return True
		if self.tables[1][index_2] == key:
			return True

		for i in range(self.bucket_size):
			if self.tables[0][index_1][i] == key:
				return True
			if self.tables[1][index_2][i] == key:
				return True
			
		return False

		


		
		

	def delete(self, key: int) -> None:
		# TODO

		index_1 = self.hash_func(key, 0)
		index_2 = self.hash_func(key, 1)

		if self.tables[0][index_1] == key:
			self.tables[0][index_1] = None
		if self.tables[1][index_1] == key:
			self.tables[1][index_2] = None

		for i in range(self.bucket_size):
			if self.tables[0][index_1][i] == key:
				if len(self.tables[0][index_1]) == 1:
					self.tables[0][index_1] = None
				else:
					self.tables[0][index_1].remove(key)
				return True
			if self.tables[1][index_2][i] == key:
				if len(self.tables[1][index_2]) == 1:
					self.tables[1][index_2] = None
				else:
					self.tables[1][index_2].remove(key)
				return True
		
		return False

		pass

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO

		

		pass

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define