e = l = '' # epsilon = lambda = empty string 
accepted = {set, dict} 


def is_final (state, final_states):

	state = expand_state(state)
	for qf in expand_state(final_states):
		if qf in state:
			return True 
	return False		

def expand_state (states, state_set = None):

	

	if state_set == None:
		if type(states) in accepted:
			return states
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

def complete_state (state, automaton):	
	state = expand_state(state)
	full_state = set(state)
	while True:

		expand_state(trans(state, automaton, e), full_state)

		if len(full_state) == len(state):			
			break

		state.update(full_state)	
	return full_state	

def trans (state, automaton, symbol):

	next_state = set() 
	for q in expand_state(state): # set format is required
		if not q in automaton:
			continue
		if symbol in automaton[q]: # if there is transition for this symbol 
			print('\ttrans',(q,symbol),'=', automaton[q][symbol])
			expand_state(automaton[q][symbol], next_state)
		#	print(next_state)
	return next_state#complete_state(next_state, automaton) # including all epsilon transitions after this symbol		

def transition (state, automaton, symbol):	

	return complete_state(trans(complete_state(state,automaton),automaton,symbol),automaton)

def consumes (state, automaton, string):

	

	for s in string:

		print(state, s)

		state = transition(state, automaton, s)

		if not len(state):
			print('Aborted')
			break

	return state		

	
			
def accepts (initial_state, automaton_transitions, final_states, input_string):			 
	return is_final(consumes(initial_state, automaton_transitions, input_string), final_states)

def dfa (initial_state, automaton_transitions, final_states = {}):

	states = [complete_state(initial_state, automaton_transitions)]
	states_tuples = [tuple(states[0])]
	deterministic_finite_automaton = {}
	deterministic_final_states = {}
	i = False 

	while i < len(states):

		state_transitions = {}
		print(states[i])

		for q in states[i]: 
			if not q in automaton_transitions:
				continue
			for s in automaton_transitions[q]: 
				if s == e: # remove epsilon transitions
					continue 
				if not s in state_transitions:
					state_transitions[s] = set()
				expand_state(transition(q, automaton_transitions, s), state_transitions[s]) 		

		for s in state_transitions:		
			if state_transitions[s] in states:
				t = states_tuples[states.index(state_transitions[s])]
			else: # add the new state to the list  	
				t = tuple(state_transitions[s])
				states_tuples.append(t)
				states.append(state_transitions[s])	
				
				print(state_transitions[s], 'created')

				tokens = set()
				for q in t:
					if q in final_states:
						try:
							tokens.add(final_states[q])
						except TypeError:	
							tokens = True
				if tokens:		
					deterministic_final_states[t] = tokens
			state_transitions[s] = t	

		print(states_tuples[i], state_transitions)

		if len(state_transitions):
			deterministic_finite_automaton[states_tuples[i]] = state_transitions # len(deterministic_finite_automaton) <= i		

		i += 1

	return states_tuples[0], deterministic_finite_automaton, deterministic_final_states		
	









	






			
	






	