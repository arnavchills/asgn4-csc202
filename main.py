from typing import *
from dataclasses import dataclass
import unittest
import sys
import string

sys.setrecursionlimit(10**6)

IntList : TypeAlias = Optional['LLNode'] 
@dataclass(frozen=True)
class LLNode:
  value : int
  rest : IntList

class WordLines:
  key : str
  lines : IntList

WordLinesList : TypeAlias = Optional['WLNode']
@dataclass(frozen=True)
class WLNode:
  value : WordLines
  rest : WordLinesList

class HashTable:
  bins : List[WordLinesList]
  count : int

class Tests(unittest.TestCase):
  pass

if (__name__ == '__main__'):
unittest.main()
