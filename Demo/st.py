with open("statistics.txt", "r") as myfile:
   data = myfile.read().split(',')

Ns = 0
Ws = 0
Es = 0
Ss = 0

for string in data:
    Ns += string.count('N')
    Ws += string.count('W')
    Es += string.count('E')
    Ss += string.count('S')
    
print('Ns: {}\nWs: {}\nEs: {}\nSs: {}'.format(Ns, Ws, Es, Ss))