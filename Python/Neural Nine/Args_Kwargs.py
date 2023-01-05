def myfunc(*args, **kwargs):
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print("%s = %s" % (key, value))

myfunc("Trey", 1, "hello", keyword1 = "hiyah", keyword2 = "sup")

# ---------------------------------------------------------------------------- #

def myFunc2(arg1, arg2, arg3):
    print("arg1:", arg1)
    print("arg2:", arg2)
    print("arg3:", arg3)
 
 
# Now we can use *args or **kwargs to
# pass arguments to this function :
blargs = ("Geeks", "for", "Geeks")
myFunc2(*blargs)
 
kwargs = {"arg1": "Geeks", "arg2": "for", "arg3": "Geekeys"}
myFunc2(**kwargs)


# ------------------------------------------------------------------------------ #

class car(): #defining car class
    def __init__(self,*args): #args receives unlimited no. of arguments as an array
        self.speed = args[0] #access args index like array does
        self.color=args[1]
                 
#creating objects of car class
         
audi=car(200,'red')
bmw=car(250,'black')
mb=car(190,'white')
    
print(audi.color)
print(bmw.speed)