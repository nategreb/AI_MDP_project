import csv
"""
    Initial traffic level N;Initial traffic level E;Initial traffic level W;Green traffic light;Final traffic level N;Final traffic level E;Final traffic level W
"""
def main():
    with open('./Data.csv', 'r') as f:
        #keep track of counts 
        initial_states = {}
        green_given_initial = {}
        final_state_given_initialState_green = {}        
        total_states = 0
        
        linereader = csv.reader(f,delimiter=';', quotechar='|')
        for line in linereader:
            #increment occurences initial states
            initial_state = ';'.join(line[0:3]) + ';'
            initial_states[initial_state] = 1 + initial_states.get(initial_state,0)
            
            #increment occurences green light given initial
            green_and_initial = ';'.join(line[0:4]) + ';'
            green_given_initial[green_and_initial] = 1 + green_given_initial.get(green_and_initial,0)
            
            #increment occurences of final state given final
            final_state_given_initial_and_green = ';'.join(line[:]) 
            final_state_given_initialState_green[final_state_given_initial_and_green] = 1+final_state_given_initialState_green.get(final_state_given_initial_and_green,0)
            
            #keep track of sample size
            total_states += 1
            
        
            
main()