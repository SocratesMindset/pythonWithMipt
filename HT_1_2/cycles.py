def cyclesTaskOne():
    max_value = 0
    while (True):
        numberFirst = input("type first number ")
        numberSecond = input("type second number ")
        numberFirst=int(numberFirst)
        numberSecond=int(numberSecond)
        print(f"{numberFirst} + {numberSecond} = {numberFirst+numberSecond}")

def cyclesTaskTwo():
    cur=1
    for i in range(5):
        for j in range(5):
            print("*".rjust(3),end=' ') if ((i+j)%2==0) else print(str(cur).rjust(3),end=' ')
            cur += 0 if (i + j) % 2 == 0 else 1
        print()

def cyclesTaskThree():
    Left=int(input(""))
    Right=int(input(""))
    switch=False
    while (Left<=Right):
        guess=int(Left+(Right-Left)/2)
        if (Left==Right):
            print(f"answer is {guess}")
            switch=True
            break
        print(f"Is it {guess}?")
        answer=input("please type yes-y or b-bigger,s-smaller [y/b/s]")
        if (answer=="y"):
            print(f"answer is {guess}")
            switch=True
            break
        elif (answer=="s"):
            Right=guess-1
        elif (answer=="b"):
            Left=guess+1
        else:
            print("error:another input")
    print(" ") if switch==True else print("error")


def cyclesTaskFour ():
    max_value = 0
    while(True):
        number=input("type number which bigger then zero,if you want to stop, type zero")
        number=int(number)
        if (number>0):
            if (number>max_value):
                max_value = number
        elif (number<0):
            print("incorrect input")
        elif (number==0):
            print(f"biggest number is {max_value}")
            print("bye!")
            break

def cyclesTaskFive():
    for i in range(10):
        for j in range(10):
            print(f"{i} * {j} = {i*j}")


if __name__ == '__main__':
    """вызов функций"""

