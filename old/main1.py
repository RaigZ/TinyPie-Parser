'''
BNF for var def code with format:

myvar= 5+6+2.3;

BNF:

exp -> id = math;
math -> int+math | float

Note that this is just a shortened example code for demostration only. The final tree misses internal nodes like int or float, since we are not doing word level BNF here.
'''
'''
for this updats from task 2 to BNF2 

In this the program must work with keyword basically

before worked with ---> myvar=2*3*4*2.3 or myvar=2*3.3+4*5.5
but does not work with ---> float myvar=2.4+5*6.1+3.5   

the float part in the beginning was added so must modify to work (reusing lab code)
'''


# Mytokens=[("id","myvar"),("op","="),("int","5"),("op","+"),("int","6"),("op","+"),("float","2.3"),("sep",";")]
inToken = ("empty", "empty")

# myvar=2*3*4*2.3;
# Mytokens = [("id","myvar"),("op","="),("int","2"),("op","*"),("int","3"),("op","*"),("int","4"),("op","*"), ("float","2.3"), ("sep",";")]

# float myVar =5*4.3+2.1;    or     float mynum= 3.4+7*2.1;
# Mytokens=[("id","myvar"),("op","="),("int","5"),("op","*"),("float","4.3"),("op","+"),("float","2.1"),("sep",";")]
# Mytokens=[("id","mynum"),("op","="),("float","3.4"),("op","+"),("int","7"),("op","*"),("float","2.1"),("sep",";")]

# myvar=2*3.3+4*5.5
#Mytokens=[("id","myvar"),("op","="),("int","2"),("op","*"),("float","3.3"),("op","+"),("int","4"),("op","*"),("float","5.5"),("sep",";")]

# myvar=2.4+5*6.1+3.5
Mytokens = [("keyword", "float"), ("id", "myvar"), ("op", "="), ("float", "2.4"), ("op", "+"), ("int", "5"), ("op", "*"), ("float", "6.1"), ("op", "+"), ("float", "3.5"), ("sep", ";")]


def accept_token():
    global inToken
    print("     accept token from the list:" + inToken[1])
    inToken = Mytokens.pop(0)


def math():
    print("\n----parent node math, finding children nodes:")
    global inToken
    if (inToken[0] == "float"):
        print("child node (internal): float")
        print("   float has child node (token):" + inToken[1])
        accept_token()

        if (inToken[1] == "+"):
            print("child node (token):" + inToken[1])
            accept_token()

            print("child node (internal): math")
            math()
        elif (inToken[1] == "*"):
            print("child node (token):" + inToken[1])
            accept_token()

            print("child node (internal): math")
            math()
        else:
            print("error, you need + after the int in the math")
    elif (inToken[0] == "int"):
        print("child node (internal): int")
        print("   int has child node (token):" + inToken[1])
        accept_token()

        if (inToken[1] == "+"):
            print("child node (token):" + inToken[1])
            accept_token()

            print("child node (internal): math")
            math()
        elif (inToken[1] == "*"):
            print("child node (token):" + inToken[1])
            accept_token()

            print("child node (internal): math")
            math()
        else:
            print("error, you need + after the int in the math")

    else:
        print("error, math expects float or int")


def exp():
    #print("\n---keyword node:")  #must be after paerant
    #global inToken;
    #typeK, token = inToken;
    #if (typeK == "keyword"):
    #    print("keyword node (root): keyword")
    #    print("   keyword has root node (token):" + token)
    #    accept_token()
    print("\n----parent node exp, finding children nodes:")
    global inToken;
    typeK, token = inToken;
    if (typeK == "keyword"):
        print("keyword node (root): keyword")
        print("   keyword has root node (token):" + token)
        accept_token()
    else:
        print("expexted keyword as the first element of the expression!\n")
        return
    #global inToken;
    typeT, token = inToken;
    if (typeT == "id"):
        print("child node (internal): identifier")
        print("   identifier has child node (token):" + token)
        accept_token()
    else:
        print("expect identifier as the second element of the expression!\n")
        return

    if (inToken[1] == "="):
        print("child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect = as the second element of the expression!")
        return

    print("Child node (internal): math")
    math()


def main():
    global inToken
    inToken = Mytokens.pop(0)
    exp()
    if (inToken[1] == ";"):
        print("\nparse tree building success!")
    return


main()

