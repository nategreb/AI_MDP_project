import pytest
import numpy
from ..main import MDP


#@pytest
def assert_probabilites():
    x = MDP('./tests/test.csv')
    #column 1 for HighHighHigh since these are all the final states in test.csv
    print(x.E_green.sum(axis=0)[1] == 7)
    print(x.N_green.sum(axis=0)[1] == 0)
    print(x.W_green.sum(axis=0)[1] == 0)
    print(x.value_iteration()) #should all be E... no values for N or W


def all_probabilities_add_to_one():
    x = MDP('./Data.csv')
    for i in range(1,8):
        print(x.E_green.sum(axis=1)[i])
        print(x.N_green.sum(axis=1)[i])
        print(x.W_green.sum(axis=1)[i])

#assert_probabilites()
all_probabilities_add_to_one()