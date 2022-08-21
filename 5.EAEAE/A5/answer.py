from pyfinite import ffield

ep = [[-1]*128 for i in range(128)]

fid = ffield.FField(7)

tuples = {'0000': 'f',
    '0001': 'g',
    '0010': 'h',
    '0011': 'i',
    '0100': 'j',
    '0101': 'k',
    '0110': 'l',
    '0111': 'm',
    '1000': 'n',
    '1001': 'o',
    '1010': 'p',
    '1011': 'q',
    '1100': 'r',
    '1101': 's',
    '1110': 't',
    '1111': 'u'}

def conversion(c):
    value = ""
    for i in range(0, len(c), 2):
        tmp = (ord(c[i]) - ord('f'))*16 + ord(c[i+1]) - ord('f')
        value += chr(tmp)
    return value

def Add(n1, n2):
    return int(n1) ^ int(n2)

def Multiply(n1, n2):
    return fid.Multiply(n1, n2)

def power(n, p):
    if ep[n][p] != -1:
        return ep[n][p]

    if p == 0:
        ep[n][p] = 1
        return 1
    elif p == 1:
        ep[n][p] = n
        return n
    elif p%2 == 0:
        ans = 0
        sqrt = power(n, p>>1)
        ans = Multiply(sqrt, sqrt)
        ep[n][p] = ans
        return ans
    else:
        ans = 0
        sqrt = power(n, p>>1)
        ans = Multiply(sqrt, sqrt)
        ans = Multiply(n, ans)
        ep[n][p] = ans
        return ans

def sum(v1, v2):
    ans = [0]*8
    i = 0
    for (e1, e2) in zip(v1, v2):
        ans[i] = int(e1)^int(e2)
        i = i+1
    return ans

def mult(v, elem):
    ans = [0]*8
    i = 0
    for e in v:
        ans[i] = fid.Multiply(e, elem)
        i = i+1
    return ans

def L(A, E):
    ans = [0]*8
    for i,j in zip(A, E):
        ans = sum(mult(i, j), ans)
    return ans

def encipher(value, A, E):
    Output = [[0 for i in range (8)] for j in range(8)]
    value = [ord(c) for c in value]
    
    i = 0
    for x in value:
        Output[0][i] = power(x, E[i])
        i = i+1

    Output[1] = L(A, Output[0])

    i = 0
    for x in Output[1]:
        Output[2][i] = power(x, E[i])
        i = i+1

    Output[3] = L(A, Output[2])

    i = 0
    for x in Output[3]:
        Output[4][i] = power(x, E[i])
        i = i+1
    return Output[4]

def byte_str(b):
    binnum = '{:0>8}'.format(format(b,"b"))
    a = tuples[binnum[0:4]], tuples[binnum[4:8]]
    return a[0]+a[1]

def decipher(password,A,E):
    password = conversion(password)
    ans = ""
    for i in range(8):
        for j in range(128):
            inp = ans + byte_str(j)+(16-len(ans)-2)*'f'
            if ord(password[i]) == encipher(conversion(inp), A, E)[i]:
                ans += byte_str(j)
                break
    return ans

val_e = [[] for i in range(8)]
val_a = [[[] for i in range(8)] for j in range(8)]

inp = open("plain.txt")
out = open("cipher.txt")

for i in range(8):
	inp_l = inp.readline()
	out_l = out.readline()
	i_byt = []
	o_byt = []
	for (j,k) in zip(inp_l.split(" "), out_l.split(" ")):
		if(len(j) >= 16):
			i_byt.append((ord(j[2*i])-ord('f'))*16 + ord(j[2*i+1])-ord('f'))
		if(len(k) >= 16):
			o_byt.append((ord(k[2*i])-ord('f'))*16 + ord(k[2*i+1])-ord('f'))

	for e in range(1,127):
		for a in range(1,128):
			mark = 1
			for l in range(128):
				if (o_byt[l] != power(Multiply(power(Multiply(power(i_byt[l], e), a), e), a), e)):
					mark = 0
					break 			
			if (mark==1):
				val_e[i].append(e)
				val_a[i][i].append(a)		

inp.seek(0,0)
out.seek(0,0)

for i in range(7):
	inp_l = inp.readline()
	out_l = out.readline()
	i_byt = []
	o_byt = []
	for (j,k) in zip(inp_l.split(" "), out_l.split(" ")):
		if(len(j) >= 16):
			i_byt.append((ord(j[2*i])-ord('f'))*16 + ord(j[2*i+1])-ord('f'))
		if(len(k) >= 16):
			o_byt.append((ord(k[2*i+2])-ord('f'))*16 + ord(k[2*i+3])-ord('f'))
	
	for var in range(1, 128):
		for ee, aa in zip(val_e[i+1], val_a[i+1][i+1]):
			for e, a in zip(val_e[i], val_a[i][i]):
				mark = 1
				for l in range(128):
					if (o_byt[l] != power(Add(Multiply(power(Multiply(power(i_byt[l], e), a), e), var) ,Multiply(power(Multiply(power(i_byt[l], e), var), ee), aa)), ee)):
						mark = 0
						break 			
				if (mark==1):
					val_e[i] = [e]
					val_a[i][i] = [a]
					val_e[i+1] = [ee]
					val_a[i+1][i+1] = [aa]
					val_a[i][i+1] = [var]

for num in range(2,8):        
        E = [e[0] for e in val_e]        
        A = [[0 for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                if (len(val_a[i][j]) != 0):
                    A[i][j] = val_a[i][j][0]
        inp.seek(0,0)
        out.seek(0,0)
        for i in range(8):
            inp_l = inp.readline()
            out_l = out.readline()
            if (i+num >= 8):
                continue
            i_byt = [conversion(val) for val in inp_l.strip().split(" ")]
            o_byt = [conversion(val) for val in out_l.strip().split(" ")]
        	
            for var in range(1, 128):
                A[i][i+num] = var
                mark = 1
                for inps, outs in zip(i_byt, o_byt):
                    if encipher(inps, A, E)[i+num] != ord(outs[i+num]):
                        mark = 0
                        break
                if (mark==1):
                    val_a[i][i+num] = [var]
                            
A = [[0 for i in range(8)] for j in range(8)]
for i in range(8):
	for j in range(8):
		if (len(val_a[i][j]) != 0) :
			A[i][j] = val_a[i][j][0]

print(E)
print(A)
		


password_1 = "lhlikkgllmkqimlh"
password_2 = "mmhkmfffhpffjifr"


print(conversion(decipher(password_1,A,E) + decipher(password_2,A,E)))

