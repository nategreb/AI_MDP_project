from main import MDP

x = MDP('./test.csv')
x.get_transition_probabilities()
print(x.E_green.sum(axis=0)[1] == 7)
print(x.N_green.sum(axis=0)[1] == 7)
print(x.W_green.sum(axis=0)[1] == 0)