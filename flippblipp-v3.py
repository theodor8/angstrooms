ärSpeletFörlorat = False
x=1
print(x)
def flippblipp(n):
    if n%5==0 and n%3==0:
        return "flipp blipp"
    elif n%5==0:
        return "blipp"
    elif n%3==0:
        return "flipp"
    else:
        return str(n)
            
while not ärSpeletFörlorat:
    x+=1
    svar = input("Nästa: ")
    if svar != flippblipp(x):
        ärSpeletFörlorat = True
        print("Fel - " + flippblipp(x))
        print()
        print("Game Over")