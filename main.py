import csv
import numpy as np
from itertools import count
"""
    Initial traffic level N;Initial traffic level E;Initial traffic level W;Green traffic light;Final traffic level N;Final traffic level E;Final traffic level W
"""
class MDP:
    def __init__(self) -> None:
        #use states as matrix indices
        self.states = {
            'LowLowLow': 0,
            'HighHighHigh': 1,
            'HighHighLow': 2,
            'HighLowLow': 3,
            'LowHighHigh': 4,
            'HighLowHigh': 5,
            'LowLowHigh': 6,
            'LowHighLow': 7
        }
        self.goal = self.states['LowLowLow']
        self.N_green = np.zeros((8, 8))
        self.W_green = np.zeros((8, 8))
        self.E_green = np.zeros((8, 8))
        self.actions = {
            'N': self.N_green,
            'W': self.W_green,
            'E': self.E_green
        }
        self.get_transition_probabilities(self.N_green, self.W_green, self.E_green)
    
    #value iteration     
    def value_iteration(self):
        #initialize states Value to 0 at beginning
        old_V = np.zeros(8)
        optimal_policies = [None for _ in range(8)]
        def value_action(state, action, cost):
            return cost + sum(\
                self.actions[action][state][transition_state]*old_V[transition_state] for transition_state in range(8))

        #C(A) + sum(P(S'|S,a)*V(S))
        while True:
            new_V = [0 for _ in range(8)]
            optimal_policies = [None for _ in range(8)]
            #skip value iteration of goal state 0
            for state in range(0,8):
                if state == self.goal:
                    old_V[state] = 0
                else:                    
                    N_value = value_action(state, 'N', 20)
                    W_value = value_action(state, 'W', 20)
                    E_value = value_action(state, 'E', 20)
                    
                    #get optimal policy
                    new_V[state] = min(N_value, W_value, E_value)
                    if N_value == new_V[state]:
                        optimal_policies[state] = 'N'
                    elif W_value == new_V[state]:
                        optimal_policies[state] = 'W'
                    else:
                        optimal_policies[state] = 'E'     
                    
            #check threshold to stop iterating for value
            if max(abs(old_V[state]-new_V[state]) for state in range(1,7)) < 1e-10:
                break   
            
            old_V = new_V
        
        return [new_V, optimal_policies]
                
    
    #get_counts reads the lines of the file and gets the counts of initital_states, lights, final_states
    def get_transition_probabilities(self, N_green, W_green, E_green):        
        #actions = {'N': 0, 'W':1, 'E':2}    
        with open('./Data.csv', 'r') as f:
            linereader = csv.reader(f,delimiter=';', quotechar='|')
            for line in linereader:            
                #get indice values of state
                initial_state = self.states[''.join(line[0:3])]
                action = line[3]
                transition_state = self.states[''.join(line[4:])]
                
                #transition_counts[initial_state][transition_state] += 1
                #action[action][initial_state][transition_state] += 1
                if action == 'N':
                    N_green[initial_state][transition_state] += 1
                elif action == 'W':
                    W_green[initial_state][transition_state] += 1
                else:
                    E_green[initial_state][transition_state] += 1
            #convert action counts to probabilities -> P(S'|S,a)
            def convert_array_counts_to_prob(arr):
                for r in range(len(arr)):
                    count = sum(arr[r])
                    if count>0:
                        for j in range(len(arr[0])):
                            arr[r][j] = arr[r][j]/count
            
            convert_array_counts_to_prob(N_green)
            convert_array_counts_to_prob(W_green)
            convert_array_counts_to_prob(E_green)


            


x = MDP()
print(x.value_iteration())
# print(x.value_iteration(x.W_green))
# print(x.value_iteration(x.N_green))