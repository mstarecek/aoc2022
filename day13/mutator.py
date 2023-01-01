import itertools
from pprint import pprint

my_set = ["[1,1,3,1,1]", "[1,1,5,1,1]", "[[1],[2,3,4]]"]

pprint(list(itertools.permutations(my_set)))
