

def flippblipp(n):
    if n%5==0 and n%3==0:
        return "flipp blipp"
    elif n%5==0:
        return "blipp"
    elif n%3==0:
        return "flipp"
    else:
        return str(n)
            
            
def flippblippLoop(n):
    for x in range(1,n+1):
        svar = flippblipp(x)
        print(svar)