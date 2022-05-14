import csv
import numpy as np
from itertools import count


class MDP:
    def __init__(self, file):
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
        self.actions_index = {'N': 0, 'W': 1, 'E':2}
        self.cost = 1
        #keep track of actions that state has
        self.states_actions = np.zeros((8,3))
        self.file = file
        self.goal = self.states['LowLowLow']
        self.N_green = np.zeros((8, 8))
        self.W_green = np.zeros((8, 8))
        self.E_green = np.zeros((8, 8))
        self.actions = {
            'N': self.N_green,
            'W': self.W_green,
            'E': self.E_green
        }
        self.get_transition_probabilities()
    
    #value iteration     
    def value_iteration(self):
        #initialize states Value to 0 at beginning
        old_V = np.zeros(8)
        optimal_policies = [None for _ in range(8)]
        
        #gets expected value of action
        def value_action(state, action, cost):
            return cost + sum(\
                self.actions[action][state][transition_state]*old_V[transition_state] for transition_state in range(8))

        #C(A) + sum(P(S'|S,a)*V(S))
        while True:
        #for _ in range(500):
            new_V = np.zeros(8)
            optimal_policies = [None for _ in range(8)]
            #skip value iteration of goal state 0
            for state in range(0,8):
                if state == self.goal:
                    old_V[state] = 0
                else:  
                    #Bellmans equation
                    min_value = None 
                    min_action = None
                    
                    #iterate over possible actions state has. Marked as 1 in 8x3 array
                    #for action in range(self.states_actions[state]):  
                    for action in self.actions.keys():
                        #get action index value [0,1,2] 
                        index_val_of_action = self.actions_index[action]                        
                        if self.states_actions[state][index_val_of_action] == 1:
                            value = value_action(state, action, self.cost)
                            
                            #store min action value of state
                            if min_value is None or value < min_value:
                                min_value = value
                                min_action = action
                                                    
                    #get optimal policy
                    new_V[state] = min_value
                    optimal_policies[state] = min_action                     
                    
            #check threshold to stop iterating for value
            if max(abs(old_V[state]-new_V[state]) for state in range(1,7)) < 1e-3:
                break   
            
            old_V = new_V
        
        return [new_V, optimal_policies]
                
    
    #get_counts reads the lines of the file and gets the counts of initital_states, lights, final_states
    def get_transition_probabilities(self):        
        #actions = {'N': 0, 'W':1, 'E':2}    
        with open(self.file, 'r') as f:
            linereader = csv.reader(f,delimiter=';', quotechar='|')
            
            #skip first line if not data point
            #next(linereader)
            
            for line in linereader:            
                #get indice values of state
                initial_state = self.states[''.join(line[0:3])]
                action = line[3]
                transition_state = self.states[''.join(line[4:])]
                
                
                if action == 'N':
                    self.N_green[initial_state][transition_state] += 1
                    #set to 1 to indicate state has this action
                    self.states_actions[initial_state][self.actions_index[action]] = 1
                elif action == 'W':
                    self.W_green[initial_state][transition_state] += 1
                    self.states_actions[initial_state][self.actions_index[action]] = 1
                else:
                    self.E_green[initial_state][transition_state] += 1
                    self.states_actions[initial_state][self.actions_index[action]] = 1
           
            #convert action counts to probabilities -> P(S'|S,a)
            def convert_array_counts_to_prob(arr):
                for r in range(len(arr)):
                    count = sum(arr[r])
                    if count>0:
                        for j in range(len(arr[0])):
                            arr[r][j] = arr[r][j]/count
            
            convert_array_counts_to_prob(self.N_green)
            convert_array_counts_to_prob(self.W_green)
            convert_array_counts_to_prob(self.E_green)


            


x = MDP('Data.csv')
print(x.value_iteration())
# print(x.states)
# print(x.value_iteration(x.W_green))
# print(x.value_iteration(x.N_green))