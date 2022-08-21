dictionary = {
 '0000': 'f',
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

file = open("plain.txt","w+")

for i in range(8):
    for j in range(128):
        binary = bin(j)[2:].zfill(8)
        plain = 'ff'*i + dictionary[binary[:4]] + dictionary[binary[4:]] + 'ff'*(8-i-1)
        file.write(plain + " ")
    file.write("\n")
file.close()