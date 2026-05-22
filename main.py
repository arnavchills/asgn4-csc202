from typing import *
from dataclasses import dataclass
import unittest
import sys
import string

sys.setrecursionlimit(10**6)

IntList : TypeAlias = Optional["IntNode"]
@dataclass(frozen = True)
class IntNode:
  line_num : int
  rest : IntList

@dataclass()
class WordLines:
  key : str
  value : IntList

WordLinesList : TypeAlias = Optional["WLNode"]
@dataclass(frozen = True)
class WLNode:
  line : WordLines
  rest : WordLinesList

@dataclass()
class HashTable:
  bins : List[WordLinesList]
  count : int

def hash_fn(s : str) -> int:
  """Return the hash code of s. """
  final_result : int = 1
  for i in range(len(s)):
    x : int = ord(s[i])
    final_result = final_result * 31 + x
  
  return final_result

def make_hash(size : int) -> HashTable:
  """Make a fresh hash table with size bins containing no elements. """
  return HashTable([None for i in range(size)], size)

def hash_size(ht : HashTable) -> int:
  """Return the number of bins in ht. """
  return len(ht.bins)

def hash_count(ht : HashTable) -> int:
  """Return the number of elements (key-value pairs) in ht. """
  return ht.count

def has_key(ht : HashTable, word : str) -> bool:
  """Return True if ht contains a mapping for word. """

  for item in ht.bins:
    current: WordLinesList = item

    while current != None:
      if current.line.key == word:
        return True

      current = current.rest
  
  return False

def lookup(ht : HashTable, word : str) -> List[int]:
  """Return the line numbers associated with the key word in ht. 
  The returned list should not contain duplicates but need not be sorted. """
  final_list : List[int] = []

  for bin in ht.bins:
    current_word: WordLinesList = bin

    while current_word != None:
      if current_word.line.key == word:
        current_line: IntList = current_word.line.value

        while current_line != None:
          if current_line.line_num not in final_list:
            final_list.append(current_line.line_num)

          current_line = current_line.rest

      current_word = current_word.rest

  return final_list
    
def add(ht : HashTable, word : str, line_num : int) -> None:
  """Record in ht that word has an occurence on line line_num. """
  index : int = hash_fn(word)
  
  if ht.bins[index] == None:
    ht.count += 1
  else:
    for item in ht.bins[index]:
      if item != None:
        if item.line.key == word:
          item.line.value += 1
        else:
          pass

def hash_keys(ht : HashTable) -> List[str]:
  """Return the words that have mappings in ht. The returned list should not contain duplicates
  but need not be sorted. """
  return_list: List[str] = []

  for item in ht.bins:
    current: WordLinesList = item

    while current != None:
      if current.line.key not in return_list:
        return_list.append(current.line.key)

      current = current.rest

  return return_list

def make_concordance(stop_words : HashTable, lines : List[str]) -> HashTable:
  """Given a hash table of stop_words, containing stop words as keys, plus
  a sequence of strings lines representing the lines of a document, 
  return a hash table representing a concordance of that document. """

  concordance : HashTable = make_hash(len(lines)*2)

  for i in range(len(lines)):
    line_num : int = i + 1
    words : List[str] = lines[i].split()

    for j in words:
      clean_word : str = j.lower()

      for char in string.punctuation:
        clean_word = clean_word.replace(char, "")

      if clean_word != "" and not has_key(stop_words, clean_word):
        if not has_key(concordance, clean_word):
          add(concordance, clean_word, line_num)
        elif line_num not in lookup(concordance, clean_word):
          add(concordance, clean_word, line_num)
        
  return concordance

def full_concordance(in_file : str, stop_words_file : str, out_file : str) -> None:
  # Given an input file path, a stop-words file path, and an output file path,
  # overwrite the indicated output file with a sorted concordance of the input
  #file.
  pass

# testing variables go here 
ht_1 : HashTable = HashTable([None, None], 0)
ht_2 : HashTable = HashTable([None, None, None, None, None, None, None, None, None, None], 0)
#ht_3 : HashTable = HashTable([], 3)

class Tests(unittest.TestCase):
  def test_hash_fn(self):
    self.assertEqual(hash_fn("a"), 128)

  def test_make_hash(self):
    self.assertEqual(make_hash(3), HashTable([None, None, None], 3))
    self.assertEqual(make_hash(10), HashTable([None, None, None, None, None, None, None, None, None, None], 10))
  
  def test_hash_size(self):
    self.assertEqual(hash_size(ht_1), 2)
    self.assertEqual(hash_size(ht_2), 10)
  
  def test_hash_count(self):
    self.assertEqual(hash_count(ht_1), 0)
    self.assertEqual(hash_count(ht_2), 0)
  
  def test_has_key(self):
    pass

  def test_lookup(self):
    pass

  def test_add(self):
    pass

if (__name__ == '__main__'):
  unittest.main()
