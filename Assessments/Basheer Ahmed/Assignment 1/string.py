def reverse(s):
	str = ""
	for i in s:
		str = i + str
	return str

def split(s):
    a = s.split()
    return a

def conc(b):
    s=""
    for i in b:
        s=s+i
    return s

    
s = str(input("Enter your string: "))

print("The original string is : ", s)
print("The reversed string is : ", reverse(s))
print("The splited string is : ", split(s))
b=split(s)
print("The concatenate string is : ", conc(b))
