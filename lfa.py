def derivar (n, a, b, i = 0):
	i = n.find(a, i)
	if i < 0 or b == None:
		return n 
	if type(b) == dict:
		if not a in b:
			return n
		b = b[a]
	print(n)	
	while type(b) != str:	
		j = 0
		if len(b) > 1:		
			j = int(input(b)) % len(b)
		b = b[j]
	
	return n[:i] + b + n[i + len(a):] 	
	
def tipo (g):	
	t = 3
	d = e = f = False 
	
	for n in g:
	
		for m in g[n]:
		
			if len(n) > 1: # sensível ao contexto 
				
				t = 1  
				
				if len(n) > len(m): # irrestrita quando alguma regra reduzir a forma sequencial 
				
					return 0
					
			elif t == 3: # se ainda for possível que seja linear/regular		
			
				if len(m) > 0:
			
					e = e or m[0].isupper()
					
					 
			
					if len(m) > 1:
						
						d = d or m[-1].isupper()
						
						if len(m) > 2:
							
							for c in m:
							
								f = f or c.isupper() # se houver algum não-terminal 
											
	if ((d and e) or (d == e and f)) and t == 3: # não é linear/regular se não for exclusivamente à direita ou esquerda, ou se houver algum não-terminal no meio
							
		return 2					
						
																							
	return t		
	
	
def gerar (inicial, gerador, gramatica):	

	print('Gramática tipo', tipo(gramatica))

	s = derivar(inicial, inicial, gramatica[inicial])
	
	while True:
	
		s = derivar(s, gerador, gramatica)
		
		if not gerador in s:
			break
			
	r = True
	while len(s) and r:		
		r = False
		for f in gramatica:
			for h in range(len(s)):
				t = derivar(s, f, gramatica, h)
				if t != s:
					s = t
					r = True
		print(s)		
	
	return s	

gerar('A', 'B', {'A': ['0B1'], 'B': ['', 'A']})

gerar('B', 'A', {'A': ['', 'Aa'], 'B': ['Ab']})

gerar('C', 'C', {'C': ['c', 'aCb']})

gerar('T', 'I', {'T': ['aIF'], 'I': ['E', 'aIbc'], 'cF': ['Fc'], 'cb': ['bc'], 'Eb': ['bE'], 'EF': ['bc'], 'A': ['a'], 'B': ['b'], 'C': ['c']})

print(repr(gerar('I', 'C', {'I': ['EC'], 'C': ['D', 'aAC', 'bBC'], 'Aa': ['aA'], 'Ab': ['bA'], 'Bb': ['bB'], 'Ba': ['aB'], 'Ea': ['aE'], 'Eb': ['bE'], 'ED': [''], 'AD': ['Da'], 'BD': ['Db']})))
	
gerar('C', 'C', {'C': ['', '0C0', '1C1']})	
gerar('C', 'C', {'C': ['', '0A', '1B'], 'A': ['C0'], 'B': ['C1']})

	
	
	