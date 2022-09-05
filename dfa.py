





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

def determine_tokens (finals, priority):
	for qf in finals:
		if type(finals[qf]) != list:
			print('final state', qf,'token',finals[qf],'already determined.')
			continue
		dt = len(priority)
		for t in finals[qf]:
			dt = min(dt, (priority.index(t) if t in priority else dt))
		if dt < len(priority):	
			finals[qf] = priority[dt]
		else:	
			print('tokens:\tcoudn\'t find priority token for final state', qf, 'in list',finals[qf])
				
def callback_dependencies (x, y, dependencies):		
	print(x,y,'\t',dependencies[x][y])	
	if type(dependencies[x][y]) == set:
		for a,b in dependencies[x][y]:
			callback_dependencies(a,b,dependencies)
		dependencies[x][y] = dependencies[y][x] = False	
	


def minimize (initial_state, automaton_transitions, final_states = {}, token_priority = []):
	initial_state, automaton_transitions, final_states = dfa(initial_state, automaton_transitions, final_states)
	determine_tokens(final_states, token_priority)
	print(initial_state, automaton_transitions, final_states)

	equivalence = {}
	all_states = []
	states = list(final_states) + list(automaton_transitions)
	#print('states:\t',states)
	#states.insert(0, initial_state)
	i = -1
	q = initial_state 
	while i < len(states):
		if not q in equivalence: 
			equivalence[q] = {}
			all_states.append(q)
		#	print(q)

			

		
		q = states[i]		
		i += 1

	for q in equivalence:
		for t in equivalence:	
			if not q in equivalence[t]:									  
				r = True
				if q != t:
					if ((q in final_states) != (t in final_states)) or (q in final_states and final_states[q] != final_states[t]):
						r = False
					else: 	
						r = set()

				equivalence[q][t] = equivalence[t][q] = r
				print(q,t,end='\t')
		print()						 
	print(equivalence)

	for q in all_states:		
		for t in equivalence[q]:
			if type(equivalence[q][t]) == set:
				equals = True

				for s in set(automaton_transitions[q]).union(automaton_transitions[t]):

					qa = tb = None

					if s in automaton_transitions[q] and automaton_transitions[q][s] in equivalence: 
						qa = automaton_transitions[q][s]

					if s in automaton_transitions[t] and automaton_transitions[t][s] in equivalence: 
						tb = automaton_transitions[t][s]	

					if qa == tb:	
						continue

					if qa == None or tb == None or equivalence[qa][tb] == False:
						callback_dependencies(q, t, equivalence) # False and callback all 												
						break

					if type(equivalence[qa][tb]) == set: 		
						equivalence[qa][tb].add((q,t)) # please call me if this fails later 
						equals = False
				else: 		
					if equals:
						equivalence[q][t] = equivalence[t][q] = True




	replacing = {}
	for q in all_states:
		r = replacing[q] if q in replacing else q
		for t in equivalence[q]:
			if r != t and equivalence[q][t] != False and not t in replacing:
				replacing[t] = r
				print(t,'is',r)
	print(equivalence)			
	print(replacing)

	for q in replacing:
		automaton_transitions.pop(q)
		if q in final_states:
			final_states.pop(q)
	
	for q in automaton_transitions:
		for s in set(automaton_transitions[q]):
			if automaton_transitions[q][s] in replacing:
				automaton_transitions[q][s] = replacing[automaton_transitions[q][s]]
			elif not automaton_transitions[q][s] in equivalence:   	
				automaton_transitions[q].pop(s)


					

	return initial_state, automaton_transitions, final_states				

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

				tokens = []
				for q in t:
					if q in final_states:
						try:
							tokens.append(final_states[q])
						except TypeError:	
							print('final state',q,'token unidentified')
							tokens.append(True)
							break
				if len(tokens):		
					if len(tokens) == 1:
						tokens = tokens[0]
					deterministic_final_states[t] = tokens
			state_transitions[s] = t	

		print(states_tuples[i], state_transitions)

		if len(state_transitions):
			deterministic_finite_automaton[states_tuples[i]] = state_transitions # len(deterministic_finite_automaton) <= i		

		i += 1

	return states_tuples[0], deterministic_finite_automaton, deterministic_final_states		
	




'''
print(consumes(1,{1:{0:2,1:6},2:{0:7,1:3},3:{0:8,1:4},4:{1:10},6:{0:7,1:7},7:{0:8,1:8},8:{0:10,1:10},10:{}},[0,1,1]))
print(accepts(0, {0:{'a':1},1:{'a':2},2:{'a':3},3:{'a':4},4:{'a':0}}, 1, 'aaaaaaaaaaa'))

print(consumes(0,{0:{'a':{0,1},'b':0},1:{'b':2},2:{'b':3},3:{}},'ababb'))


print(consumes(0, {0: {'a': {1,3}, 'b': {}}, 1: {'a': {}, 'b': {0,2}}, 2: {'a': {1}, 'b': {3}}, 3: {'a': {0,2}, 'b': {}}}, 'abbaa'))


print(consumes(0,{0: {'a': {1,3}}, 1: {'a': {2}}, 2: {'a': {1}}, 3: {'a': {4}}, 4: {'a': {5}}, 5: {'a': {3}}}, 'aaaaaa'))
	

print(consumes(0, {0: {0: {0}, 1: {0,1}}, 1: {0: {2}, 1: {2}}, 2: {0: {3}, 1: {3}}}, [0,0,0,1,0,0,0]))	
'''

#print(consumes(1, {1: {'': {2}, 'x': {5}}, 2: {'': {3}, 'y': {6}}, 3: {'': 4}, 4: {'': 1}, 5: {'z': {2}, '': {6}}, 6: {'': 7}}, 'xzy'))
#print(dfa(1, {1: {'': {2}, 'x': {5}}, 2: {'': {3}, 'y': {6}}, 3: {'': 4}, 4: {'': 1}, 5: {'z': {2}, '': {6}}, 6: {'': 7}}, {7}))

#print(minimize(1, {1: {'a': 2, 'b': 4}, 2: {'a': 3}, 3: {'a': 2}, 4: {'a': 5}, 5: {'a': 4}}, {2, 4}))

print(minimize(1, {
	1: {'': {2,8}}, 
	2: {'': {3,4}}, 
	3: {'1': {5}}, 
	4: {'0': {6}}, 
	5: {'': {7}}, 
	6: {'': {7}}, 
	7: {'': {2, 8}}, 
	8: {'.': {9}}, 
	9: {'': {10, 16}}, 
	10: {'': {11, 12}}, 
	11: {'1': {13}}, 
	12: {'0': {14}}, 
	13: {'': {15}}, 
	14: {'': {15}}, 
	15: {'': {10, 16}} 
}, {16}))




			
	






	