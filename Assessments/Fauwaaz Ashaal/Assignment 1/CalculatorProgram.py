#Calculator program for python

def add(x, y):
    return x + y
def subtract(x, y):
    return x - y
def multiply(x, y):
    return x * y
def divide(x, y):
    return x / y
print ("Select the operation.")    
print ("a. Add")    
print ("b. Subtract")    
print ("c. Multiply")    
print ("d. Divide") 
choice = input("Enter choice (a/ b/ c/ d): ")    
    
num1 = int (input ("Enter the first number: "))    
num2 = int (input ("Enter the second number: "))  
if choice == 'a':    
   print (num1, " + ", num2, " = ", add(num1, num2))    
elif choice == 'b':    
   print (num1, " - ", num2, " = ", subtract(num1, num2))    
elif choice == 'c':    
   print (num1, " * ", num2, " = ", multiply(num1, num2))    
elif choice == 'd':    
   print (num1, " / ", num2, " = ", divide(num1, num2))    
else:    
   print ("This is an invalid input") 
