list1 = [1,2,3]
list2 = [3,2,1,4,5,6]

i = 0
newlist = []

for x in list1:
    try:
        newlist.append(list2[list2.index(x)])
    except:
        newlist = newlist

print(newlist)