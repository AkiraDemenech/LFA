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
	

g = {'I': ['E', 'AIBC'], 'CF': ['Fc'], 'CB': ['BC'], 'EB': ['bE'], 'EF': ['bc'], 'A': ['a']}

s = 'aIF'
while 'I' in s:
	s = derivar(s, 'I', g['I'][int(input(s))])
	
while not s.islower():				
	for f in g:
		
	#	print(f, g[f])
		for h in range(len(s)):		
			s = derivar(s, f, g, h)
	
	print(s)	
	

g = {'C': ['D', 'aAC', 'bBC'], 'Aa': ['aA'], 'Ab': ['bA'], 'Bb': ['bB'], 'Ba': ['aB'], 'Ea': ['aE'], 'Eb': ['bE'], 'ED': [''], 'AD': ['Da'], 'BD': ['Db']}

s = 'EC'
while 'C' in s:
	s = derivar(s, 'C', g['C'][int(input(s))])

while not s.islower():	
	
	
	
	for f in g:
		for h in range(len(s)):		
			s = derivar(s, f, g, h)	
	print(s)	
	