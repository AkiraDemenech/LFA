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
	d = e = False 
	
	for n in g:
	
		for m in g[n]:
		
			if len(n) > 1: # sensível ao contexto 
				
				t //= t + (not t) # vira 1 se for não nulo e continua 0 se assim já for 
				
				if len(n) > len(m): # irrestrita quando alguma regra reduzir a forma sequencial 
				
					t = 0
					
			elif t == 3: # se ainda for possível que seja linear/regular		
			
				if len(m) > 0:
			
					e = e or m[0].isupper()
					
					 
			
					if len(m) > 1:
						
						d = d or m[-1].isupper()
						
						if d and e: # não é linear/regular se não for exclusivamente à direita ou esquerda
							
							t = 2
						
					elif e:	# se uma não-terminal levar a outro não-terminal 
					
						t = 2
				
				
				
			
			
	return t		
	
	
	

g = {'T': ['aIF'], 'I': ['E', 'aIbc'], 'cF': ['Fc'], 'cb': ['bc'], 'Eb': ['bE'], 'EF': ['bc'], 'A': ['a'], 'B': ['b'], 'C': ['c']}

s = 'aIF'
while 'I' in s:
	s = derivar(s, 'I', g['I'][int(input(s))])
	
while not s.islower():				
	for f in g:
		
	#	print(f, g[f])
		for h in range(len(s)):		
			s = derivar(s, f, g, h)
	
	print(s)	
	

g = {'I': ['EC'], 'C': ['D', 'aAC', 'bBC'], 'Aa': ['aA'], 'Ab': ['bA'], 'Bb': ['bB'], 'Ba': ['aB'], 'Ea': ['aE'], 'Eb': ['bE'], 'ED': [''], 'AD': ['Da'], 'BD': ['Db']}



s = 'EC'
while 'C' in s:
	s = derivar(s, 'C', g['C'][int(input(s))])

while not s.islower():	
	
	
	
	for f in g:
		for h in range(len(s)):		
			s = derivar(s, f, g, h)	
	print(s)	
	
	