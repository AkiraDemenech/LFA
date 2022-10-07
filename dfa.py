





import sys 


e = l = '' # epsilon = lambda = empty string 
accepted = {set, dict} 

digits = [d for d in range(10)]
digits_char = [str(d) for d in digits]
lowercase = [chr(c) for c in range(ord('a'), ord('z') + 1)]
uppercase = [c.upper() for c in lowercase]
bothcases = uppercase + lowercase
bothcases.sort()
alpha = lambda a,b,chars=bothcases: [c for c in chars if c >= a and c <= b]
hexadec = digits_char + alpha('a','f', lowercase) + alpha('A', 'F', uppercase)
newline_char = '\n\r\036\025'
newline_ascii = {ord(n) for n in newline_char}

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



def rename (initial_state, automaton_transitions, final_states = {}, initial_value = 1):

	  
	k = initial_value
	i = -1

	states = list(expand_state(automaton_transitions, expand_state(final_states, set())))
	names = {}
	dep = {}
	q = initial_state
	
	while i < len(states):

		if not q in names:
			   
			names[q] = k
			k += 1

						

			if q in automaton_transitions:
				d = q in final_states 
				for s in set(automaton_transitions[q]):
					p = {}					 
					for t in expand_state(automaton_transitions[q][s]):
						
						if not t in final_states:	
							if (not t in automaton_transitions) or not len(automaton_transitions[t]): 								
								continue
							
							if not t in dep:
								dep[t] = set()
							dep[t].add((q,s))
						p[t] = len(p)	
						d = d or (t != q)
					if len(p):	
						automaton_transitions[q][s] = p
					else:	
						automaton_transitions[q].pop(s)
				if not (d and len(automaton_transitions[q])): 		
					automaton_transitions.pop(q)
					callback_uselessness(q, dep, automaton_transitions, final_states)


					


		
		q = states[i]	
		i += 1

	print(automaton_transitions)
	transitions = {}

	for q in automaton_transitions:		
		for s in set(automaton_transitions[q]):			
			v = set()
			for t in automaton_transitions[q][s]:
			#	print(q, s, t)
				v.add(names[t])
			if len(v) == 1:	
				automaton_transitions[q][s] = v.pop()
			else:	
				automaton_transitions[q][s] = v
		
		transitions[names[q]] = automaton_transitions[q]

	final_names = {}

	for f in final_states:
		try:
			final_names[names[f]] = final_states[f]
		except TypeError:	
			final_names[names[f]] = True

	return names[initial_state], transitions, final_names	
		





	





	

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
	
def callback_uselessness (q, dependencies, transitions, finals = {}):
	print(q,'isn\'t useful anymore.')	
	if not q in dependencies:
		return
	print(dependencies[q])	

	for t,s in dependencies.pop(q):
		if not t in transitions:
			continue
		transitions[t][s].pop(q)
		if not len(transitions[t][s]):
			transitions[t].pop(s)
			if not len(transitions[t]):
				transitions.pop(t)
				callback_uselessness(t,dependencies,transitions,finals)
				continue
			
		if not t in finals:	
			for s in transitions[t]:
				if len(transitions[t][s]) > 1:
					break # go to more states 
				for r in transitions[t][s]:
					if t != r: 
						break
			else: # if it only goes to itself (didn't find any other states)		
				transitions.pop(t)
				callback_uselessness(t,dependencies,transitions,finals)
					

				


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
	
def fsm (initial_state, automaton_transitions, final_states = {}):
	
	states = set(automaton_transitions)
	states.update(final_states)
	symbols = set()
	transitions = set()

	

	for q in automaton_transitions:
		symbols.update(automaton_transitions[q])
		for s in automaton_transitions[q]:
			for t in expand_state(automaton_transitions[q][s]):
				states.add(t)
				transitions.add((q,s,t))

	print('#states')			
	for q in states:
		print(q)

	print('#initial')	
	print(initial_state)

	print('#accepting')
	for qf in final_states:
		print(qf)

	print('#alphabet')	
	for s in symbols:
		print(s)

	print('#transitions')	
	for q,s,t in transitions:
		print(f'{q}:{s}>{t}')

			
def matrix (initial_state, automaton_transitions, final_states, token_priority = [], file=sys.stdout):			

	initial_state, automaton_transitions, final_states = rename(*minimize(initial_state, automaton_transitions, final_states, token_priority))


	print('q_0 = ',initial_state,file=file)
	alphabet = set()
	for q in automaton_transitions:
		for s in automaton_transitions[q]:
			alphabet.add(s)

	alphabet = list(alphabet)			
	print(alphabet)
	alphabet.sort()
	
	m = [None]*(1 + max(max(automaton_transitions), max(final_states)))

	for q in automaton_transitions:
		l = m[q] = [0] * len(alphabet)
		for s in automaton_transitions[q]:
			l[alphabet.index(s)] = automaton_transitions[q][s]

	print('S=' + str(alphabet).replace('[','{').replace(']','}'),file=file)

	print(f'M[{len(m)}][{len(alphabet)}] = ','{', file=file)
	m[0] = [0] * len(alphabet)
	c = 0
	for l in m:		
		if l == None:
			l = m[0]
		l.extend([0] * (len(alphabet) - len(l)))
		print('\t', str(l).replace('[','{').replace(']','}') + ',', '\t/*', c, '\t// */ ', file=file)
		c += 1 
	print('}', file=file)	

	print('q_f = ', final_states, file=file)

	return initial_state, m, final_states, alphabet

def add_symbol (s,q0,q1,t):
	if not q0 in t:
		t[q0] = {}

	if s in t[q0]:	
		try:
			hash(t[q0][s])
			t[q0][s] = {t[q0][s]}
		except TypeError:	
			t[q0][s] = set(t[q0][s])
	else:		
		t[q0][s] = set()
	t[q0][s].add(q1)






	







	





def add_token (token_text, token_name, state, automaton_transitions, final_states = None, case_sensitive = False):

	if final_states == None:
		final_states = {}

	#next_state = state

	for s in token_text:	
		
		n = 0#-len(automaton_transitions)
		next_state = token_name 
		while next_state == state or next_state in automaton_transitions:
			next_state = f'{token_name}{n}'
			n -= 1
		#	next_state += 1j	

		for s in ((2*s).title() if (type(s) == str and case_sensitive) else [s]):
			add_symbol(s,state,next_state,automaton_transitions)						
		
		state = next_state	

	final_states[state]	= token_name
	return state, automaton_transitions, final_states

def add_transitions (symbols, next_state, state, automaton_transitions):

	for s in symbols:	
		add_symbol(s, state, next_state, automaton_transitions)

	
	






portugol_id = 'ID'	#2
portugol_int = 'INT'	#3
portugol_point = '.'	#4
portugol_float = 'FLOAT'	#5		
portugol_string = 'STRING'
portugol_string_final = 'string'
portugol_contrabarra = '\\'
portugol_contrabarra_hex = '\\x'
portugol_contrabarra_hex1 = '\\x0'
portugol_nova_linha = '\\n'

portugol_inicial = 1
portugol_finais = {}
portugol_trans = {portugol_inicial: {'_': portugol_id, '"': portugol_string}, portugol_id: {'_': portugol_id}}
add_transitions(bothcases, portugol_id, portugol_inicial, portugol_trans) 
add_transitions(bothcases, portugol_id, portugol_id, portugol_trans)
add_transitions(digits_char, portugol_id, portugol_id, portugol_trans)
add_transitions(digits_char, portugol_int, portugol_inicial, portugol_trans)
add_transitions(digits_char, portugol_int, portugol_int, portugol_trans)
add_transitions(digits_char, portugol_float, portugol_float, portugol_trans)
portugol_trans[portugol_int]['.'] = portugol_float

add_transitions([chr(c) for c in range(1,ord(' ')) if not c in newline_ascii] + [chr(c) for c in range(ord(' '), ord('~') + 1) if c != ord('"') and c != ord('\\')] + [chr(c) for c in range(127, 128)], portugol_string, portugol_string, portugol_trans)
add_transitions('\\', portugol_contrabarra, portugol_string, portugol_trans)
add_transitions('\\\'"?$%{}0abfnrtvABFNRTV', portugol_string, portugol_contrabarra, portugol_trans)
#add_transitions('Xx', portugol_contrabarra_hex, portugol_contrabarra, portugol_trans)
#add_transitions(hexadec, portugol_contrabarra_hex1, portugol_contrabarra_hex, portugol_trans)
#add_transitions(hexadec, portugol_string, portugol_contrabarra_hex1, portugol_trans)
add_transitions('"', portugol_string_final, portugol_string, portugol_trans)

add_transitions(newline_char, portugol_nova_linha, portugol_inicial, portugol_trans)

# char '' 

portugol_char = 'char'
portugol_char1 = 'char1'
portugol_char2 = 'char2'
add_transitions("'", portugol_char, portugol_inicial, portugol_trans)
add_transitions([chr(c) for c in range(1,128) if c != ord("'") and c != ord('\\') and not c in newline_ascii], portugol_char1, portugol_char, portugol_trans)
add_transitions('\\', portugol_char2, portugol_char, portugol_trans)
add_transitions('\\\'"?$%{}0abfnrtvABFNRTV', portugol_char1, portugol_char2, portugol_trans)
add_token("'", 'char', portugol_char1, portugol_trans, portugol_finais)


# { comentário de bloco }

portugol_comentario_bloco = 'comentário bloco'
add_transitions('{', portugol_comentario_bloco, portugol_inicial, portugol_trans)
#add_transitions([chr(c) for c in range(1, 128) if c != ord('}')], portugol_comentario_bloco, portugol_comentario_bloco, portugol_trans) #erro: adicionar a autorreferência manualmente no estado que referencia o estado final do comentário de bloco
portugol_comentario_fecha = add_token('}', 'comentário de bloco', portugol_comentario_bloco, portugol_trans, portugol_finais)[0]


# // comentário de linha  

portugol_comentario_linha = add_token('//', 'comentário de linha', portugol_inicial, portugol_trans, portugol_finais)[0]
add_transitions([chr(c) for c in range(1, 128) if not c in newline_ascii], portugol_comentario_linha, portugol_comentario_linha, portugol_trans)



portugol_tokens = []
#print(portugol_trans)

for palavra in '''algoritmo vetor enquanto imprima
inicio matriz faca verdadeiro
fim tipo para falso
variaveis funcao de e
inteiro procedimento ate ou
real se passo nao
caractere entao repita div
logico senao leia'''.strip().split():
	add_token(palavra, palavra, portugol_inicial, portugol_trans, portugol_finais, True)
	portugol_tokens.append(palavra)


delnome = [(ln.strip().split()[0], ln.strip()[ln.strip().index(' '):].strip()) for ln in '''; ponto e vírgula
, vírgula
: dois pontos
. ponto
[ abre colchetes
] fecha colchetes
( abre parênteses
) fecha parênteses
= igual
<> diferente
> maior
>= maior igual
< menor
<= menor igual
+ mais
- menos
* vezes
/ divisão
<- atribuição'''.splitlines()]
#print(delnome)

for delimitador, nome in delnome:	
	add_token(delimitador, nome, portugol_inicial, portugol_trans, portugol_finais)
	portugol_tokens.append(nome)

portugol = portugol_inicial, portugol_trans, portugol_finais, portugol_tokens



portugol_finais[portugol_id] = 'identificador'
portugol_finais[portugol_int] = 'numero inteiro'
portugol_finais[portugol_float] = 'numero real'
portugol_finais[portugol_string_final] = 'string'
portugol_finais[portugol_nova_linha] = '\n'

for qf in portugol_finais:
	if not portugol_finais[qf] in portugol_tokens:
		portugol_tokens.append(portugol_finais[qf])


#print(portugol_trans, portugol_finais)

sys.stdout = open('dfa.log', 'w', encoding='utf-8')
print(portugol_trans)
print(matrix(*portugol, file=open('portugol.c','w', encoding='utf8')))
			
	






	