def convert_to_binary(x):
	bin = ''
	for i in range(8):
		if (x >= 2**(7-i)):
			bin += '1'
			x = x-2**(7-i)
		else:
			bin += '0'
	return bin

def encode(padding):
	enc_padding = ''
	for i in padding:
		str = convert_to_binary(ord(i))
		enc_padding += str
	return int(enc_padding, 2)

def decode(x):
	binary_x = bin(x).replace("0b", "")
	no_of_char = ceil(len(binary_x)/8)
	rem = no_of_char*8 - len(binary_x)
	password = ''
	for i in range(rem):
		password += '0'
	password += binary_x
	answer = '' 
	for i in range(no_of_char):
		c = password[i*8:(i+1)*8]
		answer += chr(int(c, 2))
	return answer

N = 84364443735725034864402554533826279174703893439763343343863260342756678609216895093779263028809246505955647572176682669445270008816481771701417554768871285020442403001649254405058303439906229201909599348669565697534331652019516409514800265887388539283381053937433496994442146419682027649079704982600857517093
C = 14273633006182869531348702746940453424568817097018649956391523706920736690290588678934853836543251107625579528983812922774806328893028197745555491521354672015169848469985403582519701733114122610273583346235973552088697274671253465047740215546766824242796125456943011564315008034789547638838331251627585075232
K = -1
e = 5

padding = "Noobs: This door has RSA encryption with exponent 5 and the password is "
a = encode(padding)

for len_x in range(0, 210, 8):
	
	R.<x> = PolynomialRing(ZZ)
	pol = ((a<<len_x) + x)^e - C
	if K == -1:
	    K = ceil(N**((1**2/pol.degree()) - (1/7)))
	lattice = []
	for i in range(5):
		lattice.append((K**i)*(x**i)*(N**2))
	lattice.append(N*pol(K*x))
	lattice.append(K*x*N*pol(K*x))
	
	mat = Matrix(ZZ, 7)
	
	for i in range(7):
		for j in range(7):
			mat[i, j] = lattice[i][j]
	
	mat = mat.LLL()
	
	new_pol = 0
	for i in range(7):
		new_pol += x**i * mat[0, i] / K**i
	
	roots = new_pol.roots()
	if roots:
	    print(roots[0][0], decode(roots[0][0]))
        
		