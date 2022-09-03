e = l = '' # epsilon = lambda = empty string 
accepted = {set, dict} 


def is_final (state, final_states):

	state = expand_state(state)
	for qf in expand_state(final_states):
		if qf in state:
			return True 
	return False		

def expand_state (states, state_set = None):

	if type(states) in accepted:
		return states

	if state_set == None:
		state_set = set()

	try:
		state_set.add(states)
	except TypeError: # if it is unhashable 
		try:
			for q in states:
				expand_state(q, state_set)
		except TypeError: # if it is not iterable
			print('Unhashable and not iterable:\tcouldn\'t add',states)		
	return state_set 

def complete_state (state, automata):	
	state = expand_state(state)
	full_state = set(state)
	while True:

		expand_state(trans(state, automata, e), full_state)

		if len(full_state) == len(state):			
			break

		state.update(full_state)	
	return full_state	

def trans (state, automata, symbol):

	next_state = set() 
	for q in expand_state(state): # set format is required
		if symbol in automata[q]: # if there is transition for this symbol 
			print('\ttrans',(q,symbol),'=', automata[q][symbol])
			expand_state(automata[q][symbol], next_state)
	return next_state#complete_state(next_state, automata) # including all epsilon transitions after this symbol		

def transition (state, automata, symbol):	

	return complete_state(trans(complete_state(state,automata),automata,symbol),automata)

def consumes (state, automata, string):

	

	for s in string:

		print(state, s)

		state = transition(state, automata, s)

		if not len(state):
			print('Aborted')
			break

	return state		

	
			




			
	






	