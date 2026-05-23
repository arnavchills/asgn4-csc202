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
  return HashTable([None for i in range(size)], 0)

def hash_size(ht : HashTable) -> int:
  """Return the number of bins in ht. """
  return len(ht.bins)

def hash_count(ht : HashTable) -> int:
  """Return the number of elements (key-value pairs) in ht. """
  return ht.count

def has_key(ht : HashTable, word : str) -> bool:
  """Return True if ht contains a mapping for word. """
  index : int = hash_fn(word) % hash_size(ht)
  current : WordLinesList = ht.bins[index]

  while current != None:
    if current.line.key == word:
      return True

    current = current.rest

  return False

def lookup(ht : HashTable, word : str) -> List[int]:
  """Return the line numbers associated with the key word in ht. 
  The returned list should not contain duplicates but need not be sorted. """
  final_list : List[int] = []

  index : int = hash_fn(word) % hash_size(ht)
  current_word : WordLinesList = ht.bins[index]

  while current_word != None:
    if current_word.line.key == word:
      current_line : IntList = current_word.line.value

      while current_line != None:
        final_list.append(current_line.line_num)
        current_line = current_line.rest

      return final_list

    current_word = current_word.rest

  return final_list
    
def add(ht : HashTable, word : str, line_num : int) -> None:
  """Record in ht that word has an occurence on line line_num. """
  index : int = hash_fn(word) % hash_size(ht)

  current : WordLinesList = ht.bins[index]

  while current != None:
    if current.line.key == word:
      current_line : IntList = current.line.value

      while current_line != None:
        if current_line.line_num == line_num:
          return

        current_line = current_line.rest

      current.line.value = IntNode(line_num, current.line.value)
      return

    current = current.rest

  new_word_lines : WordLines = WordLines(word, IntNode(line_num, None))
  ht.bins[index] = WLNode(new_word_lines, ht.bins[index])
  ht.count += 1

def hash_keys(ht : HashTable) -> List[str]:
  """Return the words that have mappings in ht. The returned list should not contain duplicates
  but need not be sorted. """
  return_list: List[str] = []

  for item in ht.bins:
    current: WordLinesList = item

    while current != None:
      return_list.append(current.line.key)
      current = current.rest

  return return_list

def make_concordance(stop_words : HashTable, lines : List[str]) -> HashTable:
  """Given a hash table of stop_words, containing stop words as keys, plus
  a sequence of strings lines representing the lines of a document, 
  return a hash table representing a concordance of that document. """

  concordance : HashTable = make_hash(max(1, len(lines) * 2))

  for i in range(len(lines)):
    line_num : int = i + 1

    clean_line : str = lines[i].lower()

    for char in string.punctuation:
      if char == "'":
        clean_line = clean_line.replace(char, "")
      else:
        clean_line = clean_line.replace(char, " ")

    words : List[str] = clean_line.split()

    for clean_word in words:
      if clean_word.isalpha() and not has_key(stop_words, clean_word):
        add(concordance, clean_word, line_num)
        
  return concordance

def full_concordance(in_file : str, stop_words_file : str, out_file : str) -> None:
  # Given an input file path, a stop-words file path, and an output file path,
  # overwrite the indicated output file with a sorted concordance of the input
  # file.

  stop_words : HashTable = make_hash(100)

  with open(stop_words_file, "r", encoding="utf-8", errors="ignore") as stop_file:
    stop_lines : List[str] = stop_file.readlines()

  for line in stop_lines:
    words : List[str] = line.split()

    for i in words:
      clean_word : str = i.lower()

      for char in string.punctuation:
        clean_word = clean_word.replace(char, "")

      if clean_word != "":
        add(stop_words, clean_word, 0)

  with open(in_file, "r", encoding="utf-8", errors="ignore") as input_file:
    lines : List[str] = input_file.readlines()

  concordance : HashTable = make_concordance(stop_words, lines)

  keys : List[str] = hash_keys(concordance)
  keys.sort()

  with open(out_file, "w", encoding="utf-8", errors="ignore") as output_file:
    for key in keys:
      line_nums : List[int] = lookup(concordance, key)
      line_nums.sort()

      output_file.write(key + ":")

      for line_num in line_nums:
        output_file.write(" " + str(line_num))

      output_file.write("\n")

# testing variables go here 
ht_1 : HashTable = HashTable([None, None], 0)
ht_2 : HashTable = HashTable([None, None, None, None, None, None, None, None, None, None], 0)
#ht_3 : HashTable = HashTable([], 3)

class Tests(unittest.TestCase):
  def test_hash_fn(self):
    self.assertEqual(hash_fn("a"), 128)

  def test_make_hash(self):
    self.assertEqual(make_hash(3), HashTable([None, None, None], 0))
    self.assertEqual(make_hash(10), HashTable([None, None, None, None, None, None, None, None, None, None], 0))

  def test_hash_size(self):
    self.assertEqual(hash_size(ht_1), 2)
    self.assertEqual(hash_size(ht_2), 10)

  def test_hash_count(self):
    self.assertEqual(hash_count(ht_1), 0)
    self.assertEqual(hash_count(ht_2), 0)

  def test_has_key(self):
    ht: HashTable = make_hash(5)
    add(ht, "hello", 1)
    self.assertTrue(has_key(ht, "hello"))
    self.assertFalse(has_key(ht, "world"))

  def test_lookup(self):
    ht: HashTable = make_hash(5)
    add(ht, "hello", 1)
    add(ht, "hello", 2)
    add(ht, "hello", 2)
    self.assertEqual(sorted(lookup(ht, "hello")), [1, 2])
    self.assertEqual(lookup(ht, "missing"), [])

  def test_add(self):
    ht: HashTable = make_hash(5)
    add(ht, "hello", 1)
    add(ht, "hello", 1)
    add(ht, "world", 2)
    self.assertEqual(hash_count(ht), 2)
    self.assertEqual(sorted(hash_keys(ht)), ["hello", "world"])

  def test_hash_keys(self):
    ht : HashTable = make_hash(5)
    add(ht, "hello", 1)
    add(ht, "hello", 1)
    add(ht, "there", 2)
    self.assertEqual(hash_keys(ht), ["there", "hello"])
  
  def test_make_concordance(self):
    ht_stop : HashTable = make_hash(5)
    add(ht_stop, "hello", 1)
    add(ht_stop, "there", 2)
    l : List[str] = ["hello there", "test testing"]
    result : HashTable = make_hash(max(1, len(l) * 2))
    add(result, "test", 2)
    add(result, "testing", 2)
    self.assertEqual(make_concordance(ht_stop, l), result)

if (__name__ == '__main__'):

  #full_concordance("monte-cristo.txt", "montecristo_stop.txt", "monte-output.txt")
  unittest.main()
