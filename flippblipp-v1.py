n=40

def flippblipp(n):
    for x in range(1,n+1):
        if x%5==0 and x%3==0:
            print("flipp blipp")
        elif x%5==0:
            print("blipp")
        elif x%3==0:
            print("flipp")
        else:
            print(x)
            
            
flippblipp(n)