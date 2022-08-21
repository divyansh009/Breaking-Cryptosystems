import pexpect

obj = pexpect.spawn('/usr/bin/ssh students@172.27.26.188')


obj.expect('students@172.27.26.188\'s password: ', timeout=50)
obj.sendline("cs641a")
obj.expect('Enter your group name: ', timeout=50) 
obj.sendline("Noobs")
obj.expect('Enter password: ', timeout=50)
obj.sendline("Rishabh@12")

obj.expect('\r\n\r\n\r\nYou have solved 5 levels so far.\r\nLevel you want to start at: ', timeout=50)
obj.sendline("5")
#Commands used to reach to the cipher text
obj.expect('.*')
obj.sendline("go")
obj.expect('.*')
obj.sendline("wave")
obj.expect('.*')
obj.sendline("dive")
obj.expect('.*')
obj.sendline("go")
obj.expect('.*')
obj.sendline("read")
obj.expect('.*')
f = open("plain.txt", 'r')

out=[]
for line in f.readlines():
    li = line.split()
    st=""
    for l in li:
        obj.sendline(l)
        s = str(obj.before)[48:64]
        st+=(s+" ")
        obj.expect("Slowly, a new text starts*")
        obj.sendline("c")
        obj.expect('The text in the screen vanishes!')
    out.append(st)

obj.sendline("ffffffffffffffmu")
s = str(obj.before)[48:64]
obj.close()


for i in range(8):
    if i == 0:
        out[i] = out[i].lstrip()+out[i+1][:16]
        continue
    out[i] = out[i][17:]
    if i == 7:
        out[i] = out[i].lstrip() + s
    else:
        out[i] = out[i].lstrip()+out[i+1][:16]

f1= open("cipher.txt",'w')
j=1
for i in out:
    f1.write(i)
    if j!=8:
        f1.write("\n")
    j+=1
f1.close()
print("Ciphertext Corresponding to Plaintext Generated")
