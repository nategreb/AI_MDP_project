import csv
from itertools import count
"""
    Initial traffic level N;Initial traffic level E;Initial traffic level W;Green traffic light;Final traffic level N;Final traffic level E;Final traffic level W
"""
#get_counts reads the lines of the file and gets the counts of initital_states, lights, final_states
def get_counts(file):
          #keep track of counts 
        """
            {
                #each initial state
                initialState: {
                    count: INT,
                    
                    #each green direction given initial state
                    green_light_direction: {
                        count: INT,
                        #each final state occurrences given green direction
                        finalState: INT 
                    }  
                },
                
                total_count_states: int 
            }
    
        """
        occurrences = {}
        
        linereader = csv.reader(file,delimiter=';', quotechar='|')
        for line in linereader:
            #increment occurrences initial states
            initial_state = ';'.join(line[0:3]) + ';'
            occurrences[initial_state] = occurrences.get(initial_state, {})
            occurrences[initial_state]['count'] = 1 + occurrences[initial_state].get('count', 0)
            
            #increment occurences green light given initial and keep track of different green directions there are
            green_light = line[3]
            occurrences[initial_state][green_light] = occurrences[initial_state].get(green_light, {})
            green_light_given_initial = occurrences[initial_state][green_light]
            green_light_given_initial['count'] = 1 + green_light_given_initial.get('count',0)
            
            #increment occurences of final state given final
            final_state = ';'.join(line[4:]) 
            green_light_given_initial[final_state] = 1 + green_light_given_initial.get(final_state, 0)
            
            #keep track of total number of states
            occurrences['count'] = 1 + occurrences.get('count', 0) 
        return occurrences

def main():
    with open('./Data.csv', 'r') as f:
        print(get_counts(f))
  
            
main()