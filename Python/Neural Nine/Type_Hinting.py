def myfunction(myparameter: int) -> str:
    return f"{myparameter + 10}"

def otherfunction(otherparameter: str):
    print(otherparameter)

otherfunction(myfunction(20))

# added this from Docker Dev Container. added another from home computer


